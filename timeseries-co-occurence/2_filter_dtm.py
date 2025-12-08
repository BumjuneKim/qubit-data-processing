#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
10개 이상 문서에서 검출되는 단어들로만 DTM을 필터링하여 차원을 축소하는 스크립트
"""

import pandas as pd
import numpy as np
import os

def compute_word_document_frequency(dtm_df, save_path=None):
    """
    DTM으로부터 단어별 문서 빈도(DF)를 계산합니다.
    
    Args:
        dtm_df (pd.DataFrame): DOI 컬럼과 단어 빈도 컬럼을 포함한 DTM
        save_path (str | None): 계산 결과를 CSV로 저장할 경로
    
    Returns:
        pd.DataFrame: ['단어', '문서개수'] 컬럼을 가진 DF
    """
    # DOI를 제외한 단어 컬럼
    term_df = dtm_df.iloc[:, 1:]
    # 각 단어가 등장한 문서 수 (빈도 > 0인 문서 수)
    doc_frequency = (term_df > 0).sum(axis=0)
    word_freq_df = pd.DataFrame({
        '단어': term_df.columns,
        '문서개수': doc_frequency.values
    })
    if save_path:
        word_freq_df.to_csv(save_path, index=False, encoding='utf-8-sig')
        print(f"문서 빈도 파일 저장 완료: {save_path}")
    return word_freq_df


def filter_dtm_by_document_frequency(dtm_df, word_freq_df, min_docs=10, output_file=None):
    """
    문서 빈도가 최소값 이상인 단어들로만 DTM을 필터링
    
    Args:
        dtm_df (pd.DataFrame): 원본 DTM
        word_freq_df (pd.DataFrame): 단어별 문서 빈도 DF
        min_docs (int): 최소 문서 개수 (기본값: 10)
        output_file (str): 출력 파일 경로
    
    Returns:
        pd.DataFrame: 필터링된 DTM
    """
    print(f"원본 DTM 크기: {dtm_df.shape}")
    print(f"원본 단어 수: {len(dtm_df.columns) - 1}")  # DOI 컬럼 제외
    
    # 최소 문서 개수 이상에서 검출되는 단어들 필터링
    filtered_words = word_freq_df[word_freq_df['문서개수'] >= min_docs]['단어'].tolist()
    
    print(f"{min_docs}개 이상 문서에서 검출되는 단어 수: {len(filtered_words)}")
    
    # DOI 컬럼과 필터링된 단어 컬럼들만 선택
    columns_to_keep = ['DOI'] + filtered_words
    filtered_dtm = dtm_df[columns_to_keep]
    
    print(f"필터링된 DTM 크기: {filtered_dtm.shape}")
    print(f"필터링된 단어 수: {len(filtered_dtm.columns) - 1}")
    
    # 차원 축소 비율 계산
    original_words = len(dtm_df.columns) - 1
    filtered_words_count = len(filtered_dtm.columns) - 1
    reduction_ratio = (1 - filtered_words_count / original_words) * 100
    
    print(f"차원 축소 비율: {reduction_ratio:.2f}%")
    print(f"축소된 단어 수: {original_words - filtered_words_count}개")
    
    # 결과 저장
    if output_file:
        filtered_dtm.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"필터링된 DTM이 저장되었습니다: {output_file}")
    
    return filtered_dtm

def analyze_filtered_dtm(filtered_dtm):
    """
    필터링된 DTM의 통계 분석
    
    Args:
        filtered_dtm (pd.DataFrame): 필터링된 DTM
    """
    print("\n" + "="*60)
    print("필터링된 DTM 통계 분석")
    print("="*60)
    
    # DOI 컬럼 제외한 단어 컬럼들
    word_columns = filtered_dtm.columns[1:]
    
    # 각 문서의 총 단어 수 (0이 아닌 값의 합)
    doc_word_counts = filtered_dtm[word_columns].sum(axis=1)
    
    print(f"문서별 평균 단어 수: {doc_word_counts.mean():.2f}")
    print(f"문서별 최대 단어 수: {doc_word_counts.max()}")
    print(f"문서별 최소 단어 수: {doc_word_counts.min()}")
    print(f"문서별 단어 수 표준편차: {doc_word_counts.std():.2f}")
    
    # 각 단어의 총 빈도
    word_total_freqs = filtered_dtm[word_columns].sum(axis=0)
    
    print(f"\n단어별 평균 빈도: {word_total_freqs.mean():.2f}")
    print(f"단어별 최대 빈도: {word_total_freqs.max()}")
    print(f"단어별 최소 빈도: {word_total_freqs.min()}")
    
    # 상위 빈도 단어들
    top_words = word_total_freqs.sort_values(ascending=False).head(10)
    print(f"\n상위 10개 단어 (총 빈도 기준):")
    for i, (word, freq) in enumerate(top_words.items(), 1):
        print(f"{i:2d}. {word}: {freq}")

def main():
    """메인 함수"""
    dtm_file = os.path.join(os.path.dirname(__file__), 'photonic', 'all_DTM.csv')
    output_file = os.path.join(os.path.dirname(__file__), 'photonic', 'all_filtered_DTM.csv')
    word_freq_file = os.path.join(os.path.dirname(__file__), 'photonic', 'word_document_frequency.csv')
    
    try:
        print(f"원본 DTM 파일 읽는 중: {dtm_file}")
        dtm_df = pd.read_csv(dtm_file)
        
        # DTM으로부터 DF 계산 및 저장
        word_freq_df = compute_word_document_frequency(dtm_df, save_path=word_freq_file)
        
        # DTM 필터링 (10개 이상 문서에서 검출되는 단어들만)
        filtered_dtm = filter_dtm_by_document_frequency(
            dtm_df=dtm_df,
            word_freq_df=word_freq_df,
            min_docs=10,
            output_file=output_file
        )
        
        # 필터링된 DTM 분석
        analyze_filtered_dtm(filtered_dtm)
        
        print(f"\n✅ 차원 축소 완료!")
        print(f"원본 파일: {dtm_file}")
        print(f"결과 파일: {output_file}")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

