
import os
import sys
import csv
from typing import List

import pandas as pd

# spaCy setup
import spacy
from spacy.lang.en import English
from spacy.cli.download import download as spacy_download

# NLTK fallback
import nltk
from nltk.corpus import stopwords as nltk_stopwords
from nltk import pos_tag
from nltk.tokenize import word_tokenize

INPUT_XLSX = os.path.join(os.path.dirname(__file__), 'superconducting-all.xlsx')
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), 'superconducting', 'step1.csv')

# Columns: A=DOI, M=rawText (Title + Abstract)
DOI_COL = 'A'
TEXT_COL = 'M'


def ensure_spacy_model(model_name: str = 'en_core_web_sm'):
    try:
        return spacy.load(model_name)
    except OSError:
        try:
            spacy_download(model_name)
            return spacy.load(model_name)
        except Exception:
            # fallback to blank English pipeline (reduced accuracy)
            nlp = English()
            nlp.add_pipe('sentencizer')
            return nlp


def ensure_nltk_data():
    for pkg in ['punkt', 'averaged_perceptron_tagger', 'stopwords']:
        try:
            nltk.data.find(f'tokenizers/{pkg}') if pkg == 'punkt' else nltk.data.find(f'taggers/{pkg}') if pkg == 'averaged_perceptron_tagger' else nltk.data.find(f'corpora/{pkg}')
        except LookupError:
            nltk.download(pkg, quiet=True)


def extract_compound_terms(text: str) -> List[str]:
    """Extract important compound terms from quantum computing literature"""
    if not text:
        return []
    
    # Important compound terms in quantum computing
    compound_terms = [
        'josephson junction', 'quantum computer', 'quantum computing', 'quantum dot', 'quantum bit',
        'nitrogen vacancy', 'superconducting qubit', 'quantum gate', 'quantum circuit', 'quantum algorithm',
        'quantum entanglement', 'quantum superposition', 'quantum coherence', 'quantum decoherence',
        'quantum teleportation', 'quantum communication', 'quantum network', 'quantum cryptography',
        'quantum error correction', 'quantum measurement', 'quantum state', 'quantum system',
        'quantum processor', 'quantum device', 'quantum sensor', 'quantum simulator',
        'trapped ion', 'neutral atom', 'photon pair', 'quantum memory', 'quantum repeater',
        'adiabatic quantum', 'topological quantum', 'quantum annealing', 'quantum walk',
        'quantum machine learning', 'quantum optimization', 'quantum simulation',
        'bell state', 'ghz state', 'w state', 'cluster state', 'graph state',
        'quantum phase transition', 'quantum critical point', 'quantum spin liquid',
        'majorana fermion', 'anyon', 'braiding', 'topological order'
    ]
    
    found_terms = []
    text_lower = text.lower()
    
    for term in compound_terms:
        if term in text_lower:
            # Count occurrences
            count = text_lower.count(term)
            for _ in range(count):
                found_terms.append(term)
    
    return found_terms

def spacy_noun_extraction(nlp, text: str) -> List[str]:
    if not text:
        return []
    
    # Extract compound terms first
    compound_terms = extract_compound_terms(text)
    
    # Remove compound terms from text to avoid double extraction
    # Use a more careful replacement to avoid partial matches
    text_for_individual = text.lower()
    for term in compound_terms:
        # Replace with a placeholder to avoid partial replacements
        text_for_individual = text_for_individual.replace(term, ' COMPOUND_TERM_PLACEHOLDER ')
    
    doc = nlp(text_for_individual)
    nouns: List[str] = []
    
    # Extract individual nouns from remaining text
    for token in doc:
        try:
            if token.pos_ in ('NOUN', 'PROPN') and token.is_alpha and token.text.lower() != 'compound_term_placeholder':
                nouns.append(token.lemma_.lower() if token.lemma_ != '-PRON-' else token.text.lower())
        except Exception:
            # If pos_ isn't available, skip spaCy path
            return compound_terms
    
    # Combine compound terms and individual nouns
    all_terms = compound_terms + nouns
    return all_terms


def nltk_noun_extraction(text: str) -> List[str]:
    if not text:
        return []
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    nouns = [w.lower() for (w, t) in tagged if t.startswith('NN') and w.isalpha()]
    return nouns


def dedup_preserve_order(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for it in items:
        if it not in seen:
            seen.add(it)
            out.append(it)
    return out


def main():
    # Load data
    try:
        df = pd.read_excel(INPUT_XLSX, engine='openpyxl', dtype=str)
    except Exception as e:
        print(f"Failed to read Excel: {e}", file=sys.stderr)
        sys.exit(1)

    # Identify columns by Excel letters if available; else try labels
    # Pandas reads headers from first row. Assume A and M headers are named 'DOI' and 'rawText'.
    # We'll be robust by trying common variants and falling back by position.
    possible_doi = ['DOI', 'doi', 'Doi']
    possible_text = ['rawText', 'RawText', 'raw_text', 'TITLE_ABSTRACT', 'TitleAbstract', 'title_abstract']

    doi_series = None
    text_series = None

    for name in possible_doi:
        if name in df.columns:
            doi_series = df[name]
            break
    for name in possible_text:
        if name in df.columns:
            text_series = df[name]
            break

    if doi_series is None or text_series is None:
        # fallback to alphabetical columns by position (A=0, M=12)
        try:
            doi_series = df.iloc[:, 0]
            text_series = df.iloc[:, 12]
        except Exception as e:
            print(f"Failed to access fallback columns A/M: {e}", file=sys.stderr)
            sys.exit(1)

    doi_values = doi_series.fillna('').astype(str).tolist()
    text_values = text_series.fillna('').astype(str).tolist()

    # Prepare NLP
    nlp = ensure_spacy_model('en_core_web_sm')
    ensure_nltk_data()

    # NLTK stopwords (used later phases; keep minimal filtering here)
    try:
        stop_en = set(nltk_stopwords.words('english'))
    except Exception:
        stop_en = set()

    # Process rows
    rows_out = []
    for doi, text in zip(doi_values, text_values):
        # Try spaCy first
        nouns = spacy_noun_extraction(nlp, text)
        if not nouns:
            nouns = nltk_noun_extraction(text)
        # Basic cleanup: remove stopwords (light touch for step1)
        nouns = [n for n in nouns if n not in stop_en]
        # Keep duplicates to preserve word frequency for DTM
        # Use | as delimiter to separate terms clearly
        rows_out.append((doi, '|'.join(nouns)))

    # Write CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['DOI', 'nouns'])
        writer.writerows(rows_out)

    print(f"Wrote {OUTPUT_CSV} with {len(rows_out)} rows")

if __name__ == '__main__':
    main()
