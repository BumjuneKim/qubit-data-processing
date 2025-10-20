#!/usr/bin/env python3
"""
Script to calculate country exposure frequency from qubit implementation CSV files
and create a top 20 country ranking table with frequency counts.
"""

import pandas as pd
import os
from collections import Counter

def calculate_country_frequency(file_path):
    """
    Calculate country exposure frequency from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        Counter: Counter object with country codes and their frequencies
    """
    df = pd.read_csv(file_path)
    country_counter = Counter()
    
    for countries in df['Country Code']:
        # Handle both single countries and comma-separated countries
        if pd.isna(countries):
            continue
            
        # Split by comma and strip whitespace
        country_list = [country.strip() for country in str(countries).split(',')]
        
        # Count each country
        for country in country_list:
            if country:  # Skip empty strings
                country_counter[country] += 1
    
    return country_counter

def create_country_ranking_with_frequency():
    """
    Create the top 20 country ranking table with frequency counts for all qubit implementation methods.
    """
    # Define the qubit implementation methods and their corresponding files
    methods = {
        'superconducting': 'superconducting.csv',
        'trapped-ion': 'trapped-ion.csv', 
        'spin': 'spin.csv',
        'photonic': 'photonic.csv'
    }
    
    # Calculate country frequencies for each method
    method_rankings = {}
    
    for method_name, filename in methods.items():
        file_path = os.path.join(os.path.dirname(__file__), filename)
        print(f"Processing {filename}...")
        
        country_freq = calculate_country_frequency(file_path)
        
        # Get top 20 countries with frequency
        top_20 = country_freq.most_common(20)
        method_rankings[method_name] = top_20
        
        print(f"Top 5 countries in {method_name}: {top_20[:5]}")
    
    # Create the ranking DataFrame
    ranking_data = []
    
    for rank in range(1, 21):
        row = {'ranking': rank}
        for method_name in methods.keys():
            if rank <= len(method_rankings[method_name]):
                country, freq = method_rankings[method_name][rank-1]
                row[method_name] = f"{country}({freq})"
            else:
                row[method_name] = ''  # Empty if less than 20 countries
        ranking_data.append(row)
    
    # Create DataFrame and save to CSV
    df_ranking = pd.DataFrame(ranking_data)
    
    # Save to CSV
    output_path = os.path.join(os.path.dirname(__file__), 'country-ranking-top-20.csv')
    df_ranking.to_csv(output_path, index=False)
    
    print(f"\nCountry ranking table with frequency saved to: {output_path}")
    print("\nTop 20 Country Rankings with Frequency:")
    print(df_ranking.to_string(index=False))
    
    return df_ranking

if __name__ == "__main__":
    create_country_ranking_with_frequency()
