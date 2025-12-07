import os
import csv
import pandas as pd
import re
from collections import Counter

INPUT_CSV = os.path.join(os.path.dirname(__file__), 'superconducting', 'step3.csv')
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), 'superconducting', 'all_step4.csv')
REMOVED_WORDS_CSV = os.path.join(os.path.dirname(__file__), 'remove_words.csv')

def is_meaningless_word(word):
    """Check if word is meaningless (short, repeated chars, etc.)"""
    if len(word) < 2:
        return True
    
    # Repeated characters (aaa, bbb, etc.) - only for 3+ chars
    if len(word) >= 3 and len(set(word)) <= 2:
        return True
    
    # Very short meaningless words
    meaningless_words = {
        'aah', 'abc', 'abd', 'abe', 'abf', 'abg', 'abh', 'abi', 'abj', 'abk', 'abl', 'abm', 'abn', 'abo', 'abp', 'abq', 'abr', 'abs', 'abt', 'abu', 'abv', 'abw', 'abx', 'aby', 'abz',
        'aaa', 'aab', 'aac', 'aad', 'aae', 'aaf', 'aag', 'aah', 'aai', 'aaj', 'aak', 'aal', 'aam', 'aan', 'aao', 'aap', 'aaq', 'aar', 'aas', 'aat', 'aau', 'aav', 'aaw', 'aax', 'aay', 'aaz',
        'baa', 'bab', 'bac', 'bad', 'bae', 'baf', 'bag', 'bah', 'bai', 'baj', 'bak', 'bal', 'bam', 'ban', 'bao', 'bap', 'baq', 'bar', 'bas', 'bat', 'bau', 'bav', 'baw', 'bax', 'bay', 'baz',
        'caa', 'cab', 'cac', 'cad', 'cae', 'caf', 'cag', 'cah', 'cai', 'caj', 'cak', 'cal', 'cam', 'can', 'cao', 'cap', 'caq', 'car', 'cas', 'cat', 'cau', 'cav', 'caw', 'cax', 'cay', 'caz',
        'etc', 'fig', 'ref', 'eq', 'eqs', 'eqn', 'eqns', 'figs', 'refs', 'tab', 'tabs',
        'id', 'ids', 'no', 'nos', 'num', 'nums', 'val', 'vals', 'var', 'vars',
        'x', 'y', 'z', 'xx', 'yy', 'zz', 'xxx', 'yyy', 'zzz'
    }
    
    return word.lower() in meaningless_words

def is_typo(word):
    """Check if word looks like a typo"""
    if len(word) < 4:
        return False
    
    # Common typo patterns
    typo_patterns = [
        r'^[a-z]*[0-9]+[a-z]*$',  # mixed letters and numbers
        r'^[a-z]+[0-9]+[a-z]+$',  # letters-number-letters
        r'^[0-9]+[a-z]+[0-9]+$',  # number-letters-number
        r'^[a-z]{1,2}[0-9]{1,2}[a-z]{1,2}$',  # short mixed patterns
    ]
    
    for pattern in typo_patterns:
        if re.match(pattern, word.lower()):
            return True
    
    # Repeated character patterns that look like typos
    if len(word) >= 4:
        # Check for 3+ consecutive same characters
        for i in range(len(word) - 2):
            if word[i] == word[i+1] == word[i+2]:
                return True
    
    return False

def is_person_name(word):
    """Check if word looks like a person name - more conservative approach"""
    if len(word) < 5:
        return False
    
    # Only check for very obvious person names
    known_names = {
        'aaronson', 'abdumalikov', 'aharonov', 'albert', 'alexandrov', 'alice', 'aliferis',
        'anderson', 'arute', 'aspen', 'bacon', 'barnum', 'barrett', 'bennett', 'berthiaume', 'bob', 'bombin',
        'briegel', 'brun', 'bub', 'calderbank', 'campbell', 'chao', 'chau', 'chen', 'chow', 'cirac',
        'cleve', 'cory', 'datta', 'david', 'deutsch', 'devitt', 'dirac', 'divincenzo', 'dowling', 'doyle',
        'duan', 'dür', 'eberhard', 'einstein', 'ekert', 'elitzur', 'emmanuel', 'feynman', 'fowler', 'fujii',
        'gambetta', 'garcia', 'gisin', 'gottesman', 'grover', 'gu', 'harrow', 'haselgrove', 'hausladen', 'hayden',
        'heisenberg', 'hen', 'hirsch', 'horodecki', 'huang', 'hwang', 'james', 'jones', 'josza', 'kane',
        'kelly', 'kim', 'kitaev', 'knill', 'koch', 'kraus', 'kumar', 'kwiat', 'laflamme', 'landauer',
        'lanyon', 'leung', 'levine', 'li', 'liang', 'lindblad', 'lloyd', 'lukin', 'lupo', 'ma',
        'majumdar', 'marcus', 'martinis', 'mcmahon', 'mermin', 'meyer', 'michal', 'mike', 'miller', 'monroe',
        'montanaro', 'mukherjee', 'nielsen', 'nori', 'obrien', 'palma', 'pan', 'peng', 'peres', 'peter',
        'pittman', 'preskill', 'raussendorf', 'reed', 'renger', 'riess', 'ripperger', 'robert', 'roetteler',
        'rol', 'ross', 'russell', 'ryan', 'sanders', 'santos', 'sasaki', 'schmidt', 'schrödinger', 'schumacher',
        'scott', 'shor', 'simon', 'smith', 'sorensen', 'steane', 'stephen', 'stucki', 'suter', 'svore',
        'takahashi', 'tanaka', 'taylor', 'terhal', 'thomas', 'tian', 'tillich', 'tittel', 'tom', 'torres',
        'tseng', 'vandersypen', 'vedral', 'vidal', 'vrijen', 'wang', 'weinstein', 'werner', 'white', 'william',
        'wong', 'wu', 'xiao', 'yang', 'yoder', 'yu', 'zalka', 'zhang', 'zhao', 'zhou', 'zhu'
    }
    
    return word.lower() in known_names

def should_remove_word(word):
    """Determine if word should be removed"""
    return is_meaningless_word(word) or is_typo(word) or is_person_name(word)

def clean_nouns(nouns_text):
    """Clean nouns by removing unwanted words"""
    if not nouns_text:
        return "", []
    
    # Split into individual terms using | delimiter
    terms = nouns_text.split('|')
    cleaned_terms = []
    removed_words = []
    
    for term in terms:
        if should_remove_word(term):
            removed_words.append(term)
        else:
            cleaned_terms.append(term)
    
    return '|'.join(cleaned_terms), removed_words

def main():
    # Read input CSV
    try:
        df = pd.read_csv(INPUT_CSV)
    except Exception as e:
        print(f"Failed to read {INPUT_CSV}: {e}")
        return
    
    print(f"Processing {len(df)} rows from {INPUT_CSV}")
    
    # Process each row and collect removed words
    processed_rows = []
    all_removed_words = []
    
    for i, row in df.iterrows():
        if i % 1000 == 0:
            print(f"Processing row {i+1}/{len(df)}")
        
        doi = row['DOI']
        nouns = row['nouns']
        
        # Clean nouns
        cleaned_nouns, removed_words = clean_nouns(nouns)
        processed_rows.append((doi, cleaned_nouns))
        all_removed_words.extend(removed_words)
    
    # Write cleaned output CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['DOI', 'nouns'])
        writer.writerows(processed_rows)
    
    # Count and deduplicate removed words
    removed_word_counts = Counter(all_removed_words)
    unique_removed_words = sorted(removed_word_counts.keys())
    
    # Write removed words CSV
    with open(REMOVED_WORDS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['removed_word'])
        for word in unique_removed_words:
            writer.writerow([word])
    
    print(f"Wrote {OUTPUT_CSV} with {len(processed_rows)} rows")
    print(f"Wrote {REMOVED_WORDS_CSV} with {len(unique_removed_words)} unique removed words")
    print(f"Total word removals: {len(all_removed_words)}")

if __name__ == '__main__':
    main()
