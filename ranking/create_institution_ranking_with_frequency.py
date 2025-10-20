#!/usr/bin/env python3
"""
Script to calculate institution exposure frequency from qubit implementation CSV files
and create a top 20 institution ranking table with frequency counts.
"""

import pandas as pd
import os
from collections import Counter

def calculate_institution_frequency(file_path):
    """
    Calculate institution exposure frequency from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        Counter: Counter object with institutions and their frequencies
    """
    df = pd.read_csv(file_path)
    institution_counter = Counter()
    
    for institutions in df['Institutions']:
        # Handle both single institutions and comma-separated institutions
        if pd.isna(institutions):
            continue
            
        # Split by comma and strip whitespace
        institution_list = [institution.strip() for institution in str(institutions).split(',')]
        
        # Count each institution
        for institution in institution_list:
            if institution:  # Skip empty strings
                institution_counter[institution] += 1
    
    return institution_counter

def create_institution_ranking_with_frequency():
    """
    Create the top 20 institution ranking table with frequency counts for all qubit implementation methods.
    """
    # Define the qubit implementation methods and their corresponding files
    methods = {
        'superconducting': 'superconducting.csv',
        'trapped-ion': 'trapped-ion.csv', 
        'spin': 'spin.csv',
        'photonic': 'photonic.csv'
    }
    
    # Calculate institution frequencies for each method
    method_rankings = {}
    
    for method_name, filename in methods.items():
        file_path = os.path.join(os.path.dirname(__file__), filename)
        print(f"Processing {filename}...")
        
        institution_freq = calculate_institution_frequency(file_path)
        
        # Get top 20 institutions with frequency
        top_20 = institution_freq.most_common(20)
        method_rankings[method_name] = top_20
        
        print(f"Top 5 institutions in {method_name}: {top_20[:5]}")
    
    # Create the ranking DataFrame
    ranking_data = []
    
    for rank in range(1, 21):
        row = {'ranking': rank}
        for method_name in methods.keys():
            if rank <= len(method_rankings[method_name]):
                institution, freq = method_rankings[method_name][rank-1]
                row[method_name] = f"{institution}({freq})"
            else:
                row[method_name] = ''  # Empty if less than 20 institutions
        ranking_data.append(row)
    
    # Create DataFrame and save to CSV
    df_ranking = pd.DataFrame(ranking_data)
    
    # Save to CSV
    output_path = os.path.join(os.path.dirname(__file__), 'institution-ranking-top-20.csv')
    df_ranking.to_csv(output_path, index=False)
    
    print(f"\nInstitution ranking table with frequency saved to: {output_path}")
    print("\nTop 20 Institution Rankings with Frequency:")
    print(df_ranking.to_string(index=False))
    
    return df_ranking

if __name__ == "__main__":
    create_institution_ranking_with_frequency()
