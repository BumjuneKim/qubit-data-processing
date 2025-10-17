#!/usr/bin/env python3
"""
Create a circular wordcloud from qubit_DTM.csv showing the top 200 most frequent words,
excluding 'qubit' and 'quantum', with no text rotation and horizontal alignment.
"""

import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def create_circular_wordcloud_from_dtm():
    """
    Create a circular wordcloud from DTM data showing top 200 most frequent words,
    excluding common terminology, with no text rotation.
    """
    
    # Read the DTM data
    print("Reading DTM data...")
    df = pd.read_csv('/Users/bumjunekim/Desktop/qubit-data-processing/qubit_DTM.csv')
    
    print(f"Original data shape: {df.shape}")
    print(f"Number of documents: {len(df)}")
    print(f"Number of words: {len(df.columns) - 1}")  # -1 for DOI column
    
    # Separate DOI column and word columns
    doi_column = df['DOI']
    word_columns = df.drop('DOI', axis=1)
    
    # Calculate total frequency for each word across all documents
    print("Calculating word frequencies...")
    word_frequencies = word_columns.sum()
    
    # Sort by frequency (descending)
    word_frequencies_sorted = word_frequencies.sort_values(ascending=False)
    
    print(f"\nTop 10 most frequent words:")
    for i, (word, freq) in enumerate(word_frequencies_sorted.head(10).items()):
        print(f"{i+1:2d}. {word:15s} - {freq:6d}")
    
    # Exclude 'qubit' and 'quantum' from the data
    words_to_exclude = ['qubit', 'quantum']
    print(f"\nExcluding words: {words_to_exclude}")
    
    # Remove excluded words
    filtered_frequencies = word_frequencies_sorted.drop(words_to_exclude, errors='ignore')
    
    print(f"Words after exclusion: {len(filtered_frequencies)}")
    
    # Select top 200 words
    top_200_words = filtered_frequencies.head(200)
    
    print(f"\nSelected top 200 words (excluding qubit/quantum)")
    print(f"Frequency range: {top_200_words.iloc[-1]:,} - {top_200_words.iloc[0]:,}")
    
    # Convert to dictionary format for WordCloud
    word_freq_dict = top_200_words.to_dict()
    
    # Create circular mask
    print("\nCreating circular mask...")
    x, y = np.ogrid[:800, :800]
    mask = (x - 400) ** 2 + (y - 400) ** 2 > 400 ** 2
    mask = 255 * mask.astype(int)
    
    # Create wordcloud with circular shape and no rotation
    print("Creating circular wordcloud...")
    
    # Configure wordcloud parameters for circular shape and no rotation
    wordcloud = WordCloud(
        width=800,
        height=800,
        background_color='white',
        max_words=200,
        colormap='viridis',
        relative_scaling=0.5,
        min_font_size=10,
        max_font_size=80,
        font_path=None,  # Use default font
        prefer_horizontal=1.0,  # Force horizontal text (no rotation)
        margin=10,
        mask=mask,  # Apply circular mask
        contour_width=0,  # No contour
        contour_color='white'
    ).generate_from_frequencies(word_freq_dict)
    
    # Create the plot
    plt.figure(figsize=(12, 12))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Top 200 Words (Based on frequent)', 
              fontsize=18, fontweight='bold', pad=20)
    
    # Save the wordcloud
    output_file = '/Users/bumjunekim/Desktop/qubit-data-processing/qubit_wordcloud_circular_top200.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Circular wordcloud saved as: {output_file}")
    
    # Show some statistics
    print(f"\nCircular Wordcloud Statistics:")
    print(f"- Total words in dataset: {len(word_frequencies):,}")
    print(f"- Words after exclusions: {len(filtered_frequencies):,}")
    print(f"- Words in wordcloud: {len(top_200_words)}")
    print(f"- Most frequent word: '{top_200_words.index[0]}' ({top_200_words.iloc[0]:,} occurrences)")
    print(f"- Least frequent word in top 200: '{top_200_words.index[-1]}' ({top_200_words.iloc[-1]:,} occurrences)")
    print(f"- Shape: Circular (800x800 pixels)")
    print(f"- Text orientation: Horizontal only (no rotation)")
    
    # Show top 20 words for reference
    print(f"\nTop 20 words in circular wordcloud:")
    for i, (word, freq) in enumerate(top_200_words.head(20).items()):
        print(f"{i+1:2d}. {word:20s} - {freq:6,}")
    
    plt.show()

if __name__ == "__main__":
    create_circular_wordcloud_from_dtm()
