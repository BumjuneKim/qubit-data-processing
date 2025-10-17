#!/usr/bin/env python3
"""
Filter TF-IDF data to keep only top 10% words by average TF-IDF value
and remove common terminology like 'quantum' and 'qubit'.
"""

import pandas as pd
import numpy as np

def filter_tfidf_data():
    """
    Filter TF-IDF data to keep only top 10% words by average TF-IDF value,
    excluding common terminology.
    """
    
    # Read the TF-IDF data
    print("Reading TF-IDF data...")
    df = pd.read_csv('/Users/bumjunekim/Desktop/qubit-data-processing/qubit_TF_IDF_DTM.csv')
    
    print(f"Original data shape: {df.shape}")
    print(f"Number of documents: {len(df)}")
    print(f"Number of words: {len(df.columns) - 1}")  # -1 for DOI column
    
    # Separate DOI column and word columns
    doi_column = df['DOI']
    word_columns = df.drop('DOI', axis=1)
    
    # Calculate average TF-IDF for each word across all documents
    print("Calculating average TF-IDF values...")
    word_averages = word_columns.mean()
    
    # Sort words by average TF-IDF in descending order
    sorted_words = word_averages.sort_values(ascending=False)
    
    # Calculate top 10% threshold
    top_10_percent_count = int(len(sorted_words) * 0.2)
    print(f"Top 10% words count: {top_10_percent_count}")
    
    # Get top 10% words
    top_10_percent_words = sorted_words.head(top_10_percent_count)
    
    # Remove common terminology (quantum, qubit)
    print("Removing common terminology...")
    words_to_remove = ['quantum', 'qubit']
    
    # Filter out common terminology from top 10% words
    filtered_words = top_10_percent_words[~top_10_percent_words.index.isin(words_to_remove)]
    
    print(f"Words after removing common terminology: {len(filtered_words)}")
    print(f"Removed words: {[word for word in words_to_remove if word in top_10_percent_words.index]}")
    
    # Create filtered dataset
    print("Creating filtered dataset...")
    filtered_columns = ['DOI'] + list(filtered_words.index)
    filtered_df = df[filtered_columns]
    
    print(f"Filtered data shape: {filtered_df.shape}")
    
    # Save the filtered data
    output_file = '/Users/bumjunekim/Desktop/qubit-data-processing/qubit_TF_IDF_filtered_V2.csv'
    filtered_df.to_csv(output_file, index=False)
    
    print(f"Filtered data saved to: {output_file}")
    
    # Display some statistics
    print("\nTop 20 words by average TF-IDF (after filtering):")
    print(filtered_words.head(20))
    
    print(f"\nSummary:")
    print(f"- Original words: {len(word_columns.columns)}")
    print(f"- Top 10% words: {len(top_10_percent_words)}")
    print(f"- After removing common terms: {len(filtered_words)}")
    print(f"- Final reduction: {len(word_columns.columns) - len(filtered_words)} words removed")
    print(f"- Reduction percentage: {((len(word_columns.columns) - len(filtered_words)) / len(word_columns.columns)) * 100:.1f}%")

if __name__ == "__main__":
    filter_tfidf_data()