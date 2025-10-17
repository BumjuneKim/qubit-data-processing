#!/usr/bin/env python3
"""
Create a circular wordcloud from qubit_TF_IDF_DTM.csv showing the top 200 words
by average TF-IDF values, excluding 'qubit' and 'quantum', with no text rotation.
"""

import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def create_tfidf_circular_wordcloud():
    """
    Create a circular wordcloud from TF-IDF data showing top 200 words by average TF-IDF,
    excluding common terminology, with no text rotation.
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
    avg_tfidf = word_columns.mean()
    
    # Sort by average TF-IDF (descending)
    avg_tfidf_sorted = avg_tfidf.sort_values(ascending=False)
    
    print(f"\nTop 10 words by average TF-IDF:")
    for i, (word, tfidf) in enumerate(avg_tfidf_sorted.head(10).items()):
        print(f"{i+1:2d}. {word:20s} - {tfidf:.3f}")
    
    # Exclude 'qubit' and 'quantum' from the data
    words_to_exclude = ['qubit', 'quantum']
    print(f"\nExcluding words: {words_to_exclude}")
    
    # Remove excluded words
    filtered_tfidf = avg_tfidf_sorted.drop(words_to_exclude, errors='ignore')
    
    print(f"Words after exclusion: {len(filtered_tfidf)}")
    
    # Select top 200 words
    top_200_words = filtered_tfidf.head(200)
    
    print(f"\nSelected top 200 words (excluding qubit/quantum)")
    print(f"TF-IDF range: {top_200_words.iloc[-1]:.3f} - {top_200_words.iloc[0]:.3f}")
    
    # Convert to dictionary format for WordCloud
    word_tfidf_dict = top_200_words.to_dict()
    
    # Create circular mask
    print("\nCreating circular mask...")
    x, y = np.ogrid[:800, :800]
    mask = (x - 400) ** 2 + (y - 400) ** 2 > 400 ** 2
    mask = 255 * mask.astype(int)
    
    # Create wordcloud with circular shape and no rotation
    print("Creating circular TF-IDF wordcloud...")
    
    # Configure wordcloud parameters for circular shape and no rotation
    wordcloud = WordCloud(
        width=800,
        height=800,
        background_color='white',
        max_words=200,
        colormap='plasma',  # Different colormap for TF-IDF
        relative_scaling=0.5,
        min_font_size=10,
        max_font_size=80,
        font_path=None,  # Use default font
        prefer_horizontal=1.0,  # Force horizontal text (no rotation)
        margin=10,
        mask=mask,  # Apply circular mask
        contour_width=0,  # No contour
        contour_color='white'
    ).generate_from_frequencies(word_tfidf_dict)
    
    # Create the plot
    plt.figure(figsize=(12, 12))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Top 200 Words (Based on TF-IDF)', 
              fontsize=18, fontweight='bold', pad=20)
    
    # Save the wordcloud
    output_file = '/Users/bumjunekim/Desktop/qubit-data-processing/qubit_tfidf_wordcloud_circular_top200.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Circular TF-IDF wordcloud saved as: {output_file}")
    
    # Show some statistics
    print(f"\nCircular TF-IDF Wordcloud Statistics:")
    print(f"- Total words in dataset: {len(avg_tfidf):,}")
    print(f"- Words after exclusions: {len(filtered_tfidf):,}")
    print(f"- Words in wordcloud: {len(top_200_words)}")
    print(f"- Highest average TF-IDF: '{top_200_words.index[0]}' ({top_200_words.iloc[0]:.3f})")
    print(f"- Lowest average TF-IDF in top 200: '{top_200_words.index[-1]}' ({top_200_words.iloc[-1]:.3f})")
    print(f"- Shape: Circular (800x800 pixels)")
    print(f"- Text orientation: Horizontal only (no rotation)")
    print(f"- Colormap: Plasma")
    
    # Show top 20 words for reference
    print(f"\nTop 20 words in circular TF-IDF wordcloud:")
    for i, (word, tfidf) in enumerate(top_200_words.head(20).items()):
        print(f"{i+1:2d}. {word:20s} - {tfidf:.3f}")
    
    plt.show()

if __name__ == "__main__":
    create_tfidf_circular_wordcloud()
