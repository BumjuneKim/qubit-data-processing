#!/usr/bin/env python3
"""
VOSViewer용 sparse format txt 파일 생성 스크립트

qubit_co_occurence.csv 파일을 읽어서 VOSViewer에서 사용할 수 있는 
sparse format의 txt 파일로 변환합니다.

조건:
1. 가중치가 0인 pair는 제외
2. 컬럼 구분은 tab으로 지정
3. 자기 자신의 pair는 무시 (예: qubit qubit 1)
4. 결과는 qubit_node_edge.txt로 저장
"""

import pandas as pd
import numpy as np
import os

def convert_cooccurrence_to_vosviewer(input_file, output_file):
    """
    Co-occurrence CSV 파일을 VOSViewer sparse format으로 변환
    
    Args:
        input_file (str): 입력 CSV 파일 경로
        output_file (str): 출력 TXT 파일 경로
    """
    
    print(f"Reading {input_file}...")
    
    # CSV 파일 읽기
    df = pd.read_csv(input_file, index_col=0)
    
    print(f"Data shape: {df.shape}")
    print(f"Number of words: {len(df.columns)}")
    
    # 결과를 저장할 리스트
    edge_list = []
    
    # 각 단어 쌍에 대해 처리
    for i, word1 in enumerate(df.columns):
        for j, word2 in enumerate(df.columns):
            # 자기 자신과의 pair는 건너뛰기
            if i == j:
                continue
            
            # 가중치 값 가져오기
            weight = df.iloc[i, j]
            
            # 가중치가 0이 아닌 경우만 추가
            if weight > 0:
                edge_list.append((word1, word2, weight))
    
    print(f"Found {len(edge_list)} non-zero edges")
    
    # 결과를 파일로 저장
    print(f"Writing to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for word1, word2, weight in edge_list:
            f.write(f"{word1}\t{word2}\t{weight}\n")
    
    print(f"Conversion completed! Output saved to {output_file}")
    
    # 통계 정보 출력
    print("\n=== Statistics ===")
    print(f"Total edges: {len(edge_list)}")
    print(f"Unique words: {len(df.columns)}")
    
    # 가중치 통계
    weights = [weight for _, _, weight in edge_list]
    print(f"Weight range: {min(weights):.6f} - {max(weights):.6f}")
    print(f"Average weight: {np.mean(weights):.6f}")
    print(f"Median weight: {np.median(weights):.6f}")
    
    # 상위 10개 edge 출력 (중복 제거 및 qubit, quantum 제외)
    print("\n=== Top 20 edges by weight ===")
    
    # 중복 제거: A-B와 B-A를 하나로 통합 (가중치가 더 큰 것을 선택)
    unique_edges = {}
    excluded_words = {'qubit', 'quantum'}
    
    for word1, word2, weight in edge_list:
        # qubit이나 quantum이 포함된 edge는 제외
        if word1 in excluded_words or word2 in excluded_words:
            continue
        
        # 정렬된 쌍을 키로 사용하여 중복 제거
        pair_key = tuple(sorted([word1, word2]))
        
        # 기존에 없거나 가중치가 더 큰 경우 업데이트
        if pair_key not in unique_edges or weight > unique_edges[pair_key][2]:
            unique_edges[pair_key] = (pair_key[0], pair_key[1], weight)
    
    # 가중치 기준으로 정렬
    sorted_edges = sorted(unique_edges.values(), key=lambda x: x[2], reverse=True)
    
    # 상위 10개 출력
    for i, (word1, word2, weight) in enumerate(sorted_edges[:20]):
        print(f"{word1} - {word2} ({weight:.6f})")

if __name__ == "__main__":
    # 입력 및 출력 파일 경로
    input_file = os.path.join(os.path.dirname(__file__), 'photonic', 'phase3_co-occurrence-matrix.csv')
    output_file = os.path.join(os.path.dirname(__file__), 'photonic', 'phase3_node_edge_pair.txt')
    
    # 변환 실행
    convert_cooccurrence_to_vosviewer(input_file, output_file)
