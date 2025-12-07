import os
import csv
import pandas as pd
from collections import Counter
import nltk
from nltk.corpus import stopwords

INPUT_CSV = os.path.join(os.path.dirname(__file__), 'photonic_phase_1_step1.csv')
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), 'photonic_phase_1_step2.csv')

def ensure_nltk_data():
    """Ensure NLTK stopwords are available"""
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)

def remove_stopwords_and_common_terms(nouns_text, stop_words, common_threshold=0.1):
    """Remove stopwords and very common terms while preserving compound terms"""
    if not nouns_text:
        return ""
    
    # Split into individual terms using | delimiter
    terms = nouns_text.split('|')
    
    filtered_terms = []
    
    for term in terms:
        # Check if it's a compound term (contains space)
        if ' ' in term:
            # For compound terms, check if any individual word is a stopword
            individual_words = term.split()
            # Only keep compound terms if none of their individual words are stopwords
            if not any(word.lower() in stop_words for word in individual_words):
                filtered_terms.append(term)
        else:
            # For individual words, apply normal stopword filtering
            if term.lower() not in stop_words:
                filtered_terms.append(term)
    
    # Remove very common generic terms (but preserve compound terms)
    generic_terms = {'use', 'result', 'method', 'approach', 'system', 'model', 'study', 
                     'analysis', 'work', 'paper', 'research', 'application', 'development',
                     'design', 'implementation', 'performance', 'effect', 'process', 'time',
                     'case', 'example', 'problem', 'solution', 'technique', 'strategy'}
    
    final_terms = []
    for term in filtered_terms:
        if ' ' in term:
            # Keep compound terms regardless of length
            final_terms.append(term)
        else:
            # For individual words, apply length and generic term filtering
            if len(term) > 2 and term.lower() not in generic_terms:
                final_terms.append(term)
    
    return '|'.join(final_terms)

def main():
    # Load NLTK stopwords
    ensure_nltk_data()
    stop_words = set(stopwords.words('english'))
    
    # Read input CSV
    try:
        df = pd.read_csv(INPUT_CSV)
    except Exception as e:
        print(f"Failed to read {INPUT_CSV}: {e}")
        return
    
    print(f"Processing {len(df)} rows from {INPUT_CSV}")
    
    # Process each row
    processed_rows = []
    for _, row in df.iterrows():
        doi = row['DOI']
        nouns = row['nouns']
        
        # Remove stopwords and common terms
        filtered_nouns = remove_stopwords_and_common_terms(nouns, stop_words)
        processed_rows.append((doi, filtered_nouns))
    
    # Write output CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['DOI', 'nouns'])
        writer.writerows(processed_rows)
    
    print(f"Wrote {OUTPUT_CSV} with {len(processed_rows)} rows")

if __name__ == '__main__':
    main()



