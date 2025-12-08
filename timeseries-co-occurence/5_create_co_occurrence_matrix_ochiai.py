#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ochiai-Salton 알고리즘을 사용하여 TF-IDF DTM에서 co-occurrence matrix 생성
"""

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import os
warnings.filterwarnings('ignore')

def ochiai_salton_similarity(matrix):
    """
    Ochiai-Salton 유사도 계산
    
    Ochiai-Salton 계수는 두 용어 간의 공출현 강도를 측정하는 지표입니다.
    공식: |A ∩ B| / sqrt(|A| * |B|)
    
    Args:
        matrix (numpy.ndarray): TF-IDF 행렬 (문서 x 용어)
    
    Returns:
        numpy.ndarray: 용어 간 Ochiai-Salton 유사도 행렬
    """
    # 이진 행렬로 변환 (TF-IDF > 0이면 1, 아니면 0)
    binary_matrix = (matrix > 0).astype(int)
    
    # 각 용어의 문서 빈도 계산
    term_freq = np.sum(binary_matrix, axis=0)
    
    # 용어 간 공출현 빈도 계산
    co_occurrence = np.dot(binary_matrix.T, binary_matrix)
    
    # Ochiai-Salton 계수 계산
    # 분모: sqrt(|A| * |B|)
    denominator = np.sqrt(np.outer(term_freq, term_freq))
    
    # 분자: |A ∩ B|
    numerator = co_occurrence
    
    # Ochiai-Salton 계수 계산 (0으로 나누기 방지)
    similarity_matrix = np.divide(numerator, denominator, 
                                 out=np.zeros_like(numerator, dtype=float), 
                                 where=denominator!=0)
    
    # 대각선을 1로 설정 (자기 자신과의 유사도)
    np.fill_diagonal(similarity_matrix, 1.0)
    
    return similarity_matrix

def create_co_occurrence_matrix(input_file, output_file):
    """
    TF-IDF DTM에서 Ochiai-Salton 알고리즘을 사용하여 co-occurrence matrix 생성
    
    Args:
        input_file (str): 입력 TF-IDF DTM 파일 경로
        output_file (str): 출력 co-occurrence matrix 파일 경로
    """
    
    print("TF-IDF DTM 파일을 읽는 중...")
    # CSV 파일 읽기
    df = pd.read_csv(input_file, index_col=0)
    
    print(f"데이터 크기: {df.shape}")
    print(f"문서 수: {df.shape[0]}")
    print(f"용어 수: {df.shape[1]}")
    
    # 용어 목록 저장
    terms = df.columns.tolist()
    
    print("TF-IDF 행렬을 numpy 배열로 변환 중...")
    # TF-IDF 행렬을 numpy 배열로 변환
    tfidf_matrix = df.values
    
    print("Ochiai-Salton 유사도 계산 중...")
    # Ochiai-Salton 유사도 계산
    similarity_matrix = ochiai_salton_similarity(tfidf_matrix)
    
    print("Co-occurrence matrix 생성 중...")
    # 용어명을 인덱스와 컬럼으로 하는 DataFrame 생성
    co_occurrence_df = pd.DataFrame(
        similarity_matrix, 
        index=terms, 
        columns=terms
    )
    
    # 결과 저장
    print(f"Co-occurrence matrix를 {output_file}에 저장 중...")
    co_occurrence_df.to_csv(output_file)
    
    print("작업 완료!")
    
    # 통계 정보 출력
    print("\n=== Co-occurrence Matrix 통계 ===")
    print(f"행렬 크기: {co_occurrence_df.shape}")
    print(f"최대 유사도: {co_occurrence_df.values.max():.4f}")
    print(f"최소 유사도: {co_occurrence_df.values.min():.4f}")
    print(f"평균 유사도: {co_occurrence_df.values.mean():.4f}")
    
    # 상위 10개 용어 쌍 출력
    print("\n=== 상위 10개 용어 쌍 (Ochiai-Salton 유사도 기준) ===")
    
    # 대각선 제외한 상위 유사도 쌍 찾기
    similarity_values = []
    for i in range(len(terms)):
        for j in range(i+1, len(terms)):
            similarity_values.append((terms[i], terms[j], similarity_matrix[i, j]))
    
    # 유사도 기준으로 정렬
    similarity_values.sort(key=lambda x: x[2], reverse=True)
    
    for i, (term1, term2, sim) in enumerate(similarity_values[:10]):
        print(f"{i+1:2d}. {term1} - {term2}: {sim:.4f}")
    
    # 용어별 평균 유사도 계산
    print("\n=== 상위 10개 용어 (평균 유사도 기준) ===")
    avg_similarity = co_occurrence_df.mean(axis=1).sort_values(ascending=False)
    for i, (term, avg_sim) in enumerate(avg_similarity.head(10).items()):
        print(f"{i+1:2d}. {term}: {avg_sim:.4f}")

if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(__file__), 'superconducting', 'all_TFIDF_filtered_TOP20_DTM.csv')
    output_file = os.path.join(os.path.dirname(__file__), 'superconducting', 'co-occurrence-matrix.csv')
    
    create_co_occurrence_matrix(input_file, output_file)
