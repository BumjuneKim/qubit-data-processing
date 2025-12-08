#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TF-IDF DTM에서 단어별 평균 TF-IDF 값을 기준으로 상위 50%의 단어만 남기는 스크립트
"""

import pandas as pd
import os
import numpy as np

def filter_tfidf_dtm(input_file, output_file):
    """
    TF-IDF DTM에서 단어별 평균 TF-IDF 값을 계산하고 상위 50%의 단어만 남기는 함수
    
    Args:
        input_file (str): 입력 TF-IDF DTM 파일 경로
        output_file (str): 출력 필터링된 DTM 파일 경로
    """
    
    print("TF-IDF DTM 파일을 읽는 중...")
    # CSV 파일 읽기
    df = pd.read_csv(input_file, index_col=0)
    
    print(f"원본 데이터 크기: {df.shape}")
    print(f"총 단어 수: {df.shape[1]}")
    
    # DOI 컬럼 제외하고 단어 컬럼만 추출
    word_columns = df.columns.tolist()
    
    print("단어별 평균 TF-IDF 값 계산 중...")
    # 각 단어(컬럼)별로 평균 TF-IDF 값 계산
    word_mean_tfidf = df.mean()
    
    print("50% 분위수 계산 중...")
    # 50% 분위수 계산
    median_tfidf = word_mean_tfidf.median()
    
    print(f"50% 분위수 값: {median_tfidf:.4f}")
    
    # 상위 50% 단어 선택 (중앙값 이상인 단어들)
    top_words = word_mean_tfidf[word_mean_tfidf >= median_tfidf].index.tolist()
    
    print(f"상위 50% 단어 수: {len(top_words)}")
    print(f"필터링 후 단어 수: {len(top_words)}")
    
    # 상위 50% 단어들로만 필터링된 데이터프레임 생성
    filtered_df = df[top_words]
    
    print(f"필터링된 데이터 크기: {filtered_df.shape}")
    
    # 결과 저장
    print(f"필터링된 결과를 {output_file}에 저장 중...")
    filtered_df.to_csv(output_file)
    
    print("작업 완료!")
    
    # 통계 정보 출력
    print("\n=== 필터링 결과 통계 ===")
    print(f"원본 단어 수: {df.shape[1]}")
    print(f"필터링된 단어 수: {filtered_df.shape[1]}")
    print(f"제거된 단어 수: {df.shape[1] - filtered_df.shape[1]}")
    print(f"단어 감소율: {((df.shape[1] - filtered_df.shape[1]) / df.shape[1] * 100):.1f}%")
    
    # 상위 10개 단어 출력
    print("\n=== 상위 10개 단어 (평균 TF-IDF 기준) ===")
    top_10_words = word_mean_tfidf.nlargest(10)
    for word, tfidf in top_10_words.items():
        print(f"{word}: {tfidf:.4f}")

if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(__file__), 'photonic', 'all_TFIDF_DTM.csv')
    output_file = os.path.join(os.path.dirname(__file__), 'photonic', 'all_TFIDF_filtered_TOP50_DTM.csv')
    
    filter_tfidf_dtm(input_file, output_file)
