import pandas as pd
import os
from collections import Counter
import numpy as np

def build_document_term_matrix(input_file, output_file):
    """
    qubit_step4.csv 파일을 읽어서 Document Term Matrix를 생성합니다.
    각 문서(DOI)에 대해 단어의 빈도수를 계산하여 행렬을 만듭니다.
    
    Args:
        input_file: 입력 CSV 파일 경로
        output_file: 출력 DTM CSV 파일 경로
    """
    
    print("데이터 읽는 중...")
    # CSV 파일 읽기
    df = pd.read_csv(input_file)
    
    print(f"총 {len(df)} 개의 문서를 읽었습니다.")
    
    # 모든 단어를 수집하여 vocabulary 생성
    all_words = set()
    document_word_counts = {}
    
    print("단어 추출 및 빈도 계산 중...")
    for idx, row in df.iterrows():
        doi = row['DOI']
        nouns_text = row['nouns']
        
        # nouns 컬럼의 값을 |로 split하여 개별 단어 추출
        words = nouns_text.split('|')
        
        # 각 문서의 단어 빈도 계산
        word_counts = Counter(words)
        document_word_counts[doi] = word_counts
        
        # 전체 vocabulary에 단어 추가
        all_words.update(words)
        
        if (idx + 1) % 1000 == 0:
            print(f"처리 완료: {idx + 1}/{len(df)}")
    
    # vocabulary를 정렬된 리스트로 변환
    vocabulary = sorted(list(all_words))
    print(f"총 {len(vocabulary)} 개의 고유 단어를 찾았습니다.")
    
    # Document Term Matrix 생성
    print("Document Term Matrix 생성 중...")
    dtm_data = []
    
    for doi in df['DOI']:
        row = [doi]  # 첫 번째 컬럼은 DOI
        word_counts = document_word_counts[doi]
        
        # 각 단어에 대해 빈도수 추가 (없으면 0)
        for word in vocabulary:
            count = word_counts.get(word, 0)
            row.append(count)
        
        dtm_data.append(row)
    
    # 컬럼명 생성 (DOI + 모든 단어)
    columns = ['DOI'] + vocabulary
    
    # DataFrame 생성
    dtm_df = pd.DataFrame(dtm_data, columns=columns)
    
    print("DTM 저장 중...")
    # CSV 파일로 저장
    dtm_df.to_csv(output_file, index=False)
    
    print(f"Document Term Matrix가 {output_file}에 저장되었습니다.")
    print(f"행렬 크기: {dtm_df.shape[0]} 문서 × {dtm_df.shape[1]} 단어")
    
    # 통계 정보 출력
    print("\n=== 통계 정보 ===")
    print(f"총 문서 수: {dtm_df.shape[0]}")
    print(f"총 단어 수: {dtm_df.shape[1] - 1}")  # DOI 컬럼 제외
    print(f"평균 문서당 단어 수: {dtm_df.iloc[:, 1:].sum(axis=1).mean():.2f}")
    print(f"최대 문서당 단어 수: {dtm_df.iloc[:, 1:].sum(axis=1).max()}")
    print(f"최소 문서당 단어 수: {dtm_df.iloc[:, 1:].sum(axis=1).min()}")
    
    # 가장 빈번한 단어들 출력
    word_totals = dtm_df.iloc[:, 1:].sum(axis=0).sort_values(ascending=False)
    print(f"\n상위 10개 빈번한 단어:")
    for i, (word, count) in enumerate(word_totals.head(10).items()):
        print(f"{i+1:2d}. {word}: {count}회")

if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(__file__), 'superconducting', 'all_step4.csv')
    output_file = os.path.join(os.path.dirname(__file__), 'superconducting', 'all_DTM.csv')
    
    build_document_term_matrix(input_file, output_file)