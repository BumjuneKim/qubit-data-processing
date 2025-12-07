import os
import csv
import pandas as pd
import spacy
from collections import defaultdict

INPUT_CSV = os.path.join(os.path.dirname(__file__), 'superconducting', 'step2.csv')
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), 'superconducting', 'step3.csv')

def ensure_spacy_model():
    """Ensure spaCy model is available"""
    try:
        return spacy.load('en_core_web_sm')
    except OSError:
        print("spaCy model not found. Please run: python -m spacy download en_core_web_sm")
        return None

def create_quantum_synonym_dict():
    """Create a dictionary for quantum computing synonyms"""
    synonyms = {
        # Quantum states and properties
        'superposition': ['superposition', 'superposed', 'superposing'],
        'entanglement': ['entanglement', 'entangled', 'entangling', 'bell', 'bell_state'],
        'coherence': ['coherence', 'coherent', 'cohering'],
        'decoherence': ['decoherence', 'decoherent', 'decohering'],
        
        # Quantum gates and operations
        'gate': ['gate', 'gates', 'operation', 'operations'],
        'rotation': ['rotation', 'rotate', 'rotating', 'rotated'],
        'phase': ['phase', 'phasing', 'phased'],
        
        # Quantum systems
        'qubit': ['qubit', 'qubits', 'quantum_bit', 'quantum_bits'],
        'quantum': ['quantum', 'quantized'],
        'atom': ['atom', 'atoms', 'atomic'],
        'ion': ['ion', 'ions', 'ionic'],
        'photon': ['photon', 'photons', 'photonic'],
        'electron': ['electron', 'electrons', 'electronic'],
        
        # Quantum computing concepts
        'algorithm': ['algorithm', 'algorithms', 'algorithim'],
        'computation': ['computation', 'computing', 'computational'],
        'simulation': ['simulation', 'simulating', 'simulated'],
        'optimization': ['optimization', 'optimizing', 'optimized'],
        
        # Quantum technologies
        'circuit': ['circuit', 'circuits', 'circuitry'],
        'processor': ['processor', 'processors', 'processing'],
        'computer': ['computer', 'computers', 'computing'],
        'device': ['device', 'devices'],
        'system': ['system', 'systems'],
        
        # Quantum materials
        'superconductor': ['superconductor', 'superconducting', 'superconductivity'],
        'semiconductor': ['semiconductor', 'semiconducting'],
        'crystal': ['crystal', 'crystalline', 'crystallization'],
        'diamond': ['diamond', 'diamonds'],
        
        # Quantum measurements
        'measurement': ['measurement', 'measuring', 'measured'],
        'detection': ['detection', 'detecting', 'detected'],
        'readout': ['readout', 'read_out', 'reading'],
        
        # Quantum noise and errors
        'noise': ['noise', 'noisy', 'noiseless'],
        'error': ['error', 'errors', 'erroneous'],
        'correction': ['correction', 'correcting', 'corrected'],
        'fidelity': ['fidelity', 'fidelities'],
        
        # Quantum communication
        'teleportation': ['teleportation', 'teleporting', 'teleported'],
        'communication': ['communication', 'communicating', 'communicated'],
        'network': ['network', 'networks', 'networking'],
        
        # Quantum control
        'control': ['control', 'controlling', 'controlled'],
        'manipulation': ['manipulation', 'manipulating', 'manipulated'],
        'preparation': ['preparation', 'preparing', 'prepared'],
    }
    
    # Create reverse mapping for quick lookup
    synonym_map = {}
    for canonical, variants in synonyms.items():
        for variant in variants:
            synonym_map[variant.lower()] = canonical
    
    return synonym_map

def lemmatize_and_normalize(nouns_text, nlp, synonym_map):
    """Apply lemmatization and synonym normalization"""
    if not nouns_text:
        return ""
    
    # Split into individual terms using | delimiter
    terms = nouns_text.split('|')
    processed_terms = []
    
    for term in terms:
        # Check if it's a compound term (contains space)
        if ' ' in term:
            # For compound terms, apply synonym mapping to the whole term
            normalized = synonym_map.get(term.lower(), term.lower())
            processed_terms.append(normalized)
        else:
            # For individual words, use spaCy for lemmatization
            doc = nlp(term)
            if doc:
                lemma = doc[0].lemma_.lower()
                
                # Apply synonym mapping
                normalized = synonym_map.get(lemma, lemma)
                
                # Only keep meaningful terms (length > 2)
                if len(normalized) > 2:
                    processed_terms.append(normalized)
    
    # Keep duplicates to preserve word frequency for DTM
    return '|'.join(processed_terms)

def main():
    # Load spaCy model
    nlp = ensure_spacy_model()
    if nlp is None:
        return
    
    # Create synonym dictionary
    synonym_map = create_quantum_synonym_dict()
    
    # Read input CSV
    try:
        df = pd.read_csv(INPUT_CSV)
    except Exception as e:
        print(f"Failed to read {INPUT_CSV}: {e}")
        return
    
    print(f"Processing {len(df)} rows from {INPUT_CSV}")
    print(f"Using {len(synonym_map)} synonym mappings")
    
    # Process each row
    processed_rows = []
    for i, row in df.iterrows():
        if i % 1000 == 0:
            print(f"Processing row {i+1}/{len(df)}")
        
        doi = row['DOI']
        nouns = row['nouns']
        
        # Apply lemmatization and synonym normalization
        normalized_nouns = lemmatize_and_normalize(nouns, nlp, synonym_map)
        processed_rows.append((doi, normalized_nouns))
    
    # Write output CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['DOI', 'nouns'])
        writer.writerows(processed_rows)
    
    print(f"Wrote {OUTPUT_CSV} with {len(processed_rows)} rows")

if __name__ == '__main__':
    main()
