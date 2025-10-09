import pandas as pd
import numpy as np
from math import log

def calculate_tfidf_dtm(input_file, output_file):
    """
    qubit_filtered_DTM.csv 파일을 읽어서 TF-IDF 가중치를 적용한 Document Term Matrix를 생성합니다.
    
    Args:
        input_file: 입력 CSV 파일 경로 (qubit_filtered_DTM.csv)
        output_file: 출력 TF-IDF DTM CSV 파일 경로
    """
    
    print("필터링된 DTM 데이터 읽는 중...")
    # CSV 파일 읽기
    df = pd.read_csv(input_file)
    
    print(f"총 {len(df)} 개의 문서를 읽었습니다.")
    print(f"총 {df.shape[1] - 1} 개의 단어가 있습니다.")  # DOI 컬럼 제외
    
    # DOI 컬럼과 단어 컬럼 분리
    doi_column = df['DOI']
    term_matrix = df.iloc[:, 1:]  # DOI 컬럼 제외한 모든 단어 컬럼
    
    print("TF-IDF 계산 중...")
    
    # 1. TF (Term Frequency) 계산 - 이미 빈도수로 되어 있음
    tf_matrix = term_matrix.values.astype(float)
    
    # 2. IDF (Inverse Document Frequency) 계산
    # 각 단어가 등장하는 문서 수 계산
    doc_frequency = (tf_matrix > 0).sum(axis=0)  # 각 단어별로 0보다 큰 값을 가진 문서 수
    
    # 총 문서 수
    total_docs = len(df)
    
    # IDF 계산: log(총 문서 수 / 해당 단어가 등장하는 문서 수)
    # 0으로 나누는 것을 방지하기 위해 1을 더함
    idf_values = np.log(total_docs / (doc_frequency + 1))
    
    print(f"IDF 계산 완료. 최소 IDF: {idf_values.min():.4f}, 최대 IDF: {idf_values.max():.4f}")
    
    # 3. TF-IDF 계산: TF × IDF
    tfidf_matrix = tf_matrix * idf_values
    
    print("TF-IDF 계산 완료")
    
    # 4. 소수점 두자리로 반올림
    tfidf_matrix_rounded = np.round(tfidf_matrix, 2)
    
    # 5. DataFrame 재구성
    tfidf_df = pd.DataFrame(tfidf_matrix_rounded, columns=term_matrix.columns)
    tfidf_df.insert(0, 'DOI', doi_column)  # DOI 컬럼을 첫 번째에 삽입
    
    print("TF-IDF DTM 저장 중...")
    # CSV 파일로 저장
    tfidf_df.to_csv(output_file, index=False)
    
    print(f"TF-IDF Document Term Matrix가 {output_file}에 저장되었습니다.")
    print(f"행렬 크기: {tfidf_df.shape[0]} 문서 × {tfidf_df.shape[1]} 단어")
    
    # 통계 정보 출력
    print("\n=== TF-IDF 통계 정보 ===")
    print(f"총 문서 수: {tfidf_df.shape[0]}")
    print(f"총 단어 수: {tfidf_df.shape[1] - 1}")  # DOI 컬럼 제외
    
    # TF-IDF 값의 통계
    tfidf_values = tfidf_matrix_rounded[tfidf_matrix_rounded > 0]
    print(f"0이 아닌 TF-IDF 값의 개수: {len(tfidf_values)}")
    print(f"TF-IDF 값 범위: {tfidf_values.min():.4f} ~ {tfidf_values.max():.4f}")
    print(f"TF-IDF 평균값: {tfidf_values.mean():.4f}")
    print(f"TF-IDF 중간값: {np.median(tfidf_values):.4f}")
    
    # 상위 TF-IDF 값을 가진 단어들 (문서별 평균)
    word_tfidf_means = tfidf_df.iloc[:, 1:].mean(axis=0).sort_values(ascending=False)
    print(f"\n상위 10개 TF-IDF 평균값을 가진 단어:")
    for i, (word, tfidf_mean) in enumerate(word_tfidf_means.head(10).items()):
        print(f"{i+1:2d}. {word}: {tfidf_mean:.4f}")
    
    # IDF 값이 높은 단어들 (희귀한 단어들)
    word_idf_df = pd.DataFrame({
        'word': term_matrix.columns,
        'idf': idf_values,
        'doc_frequency': doc_frequency
    }).sort_values('idf', ascending=False)
    
    print(f"\n상위 10개 IDF 값을 가진 단어 (희귀한 단어들):")
    for i, row in word_idf_df.head(10).iterrows():
        print(f"{i+1:2d}. {row['word']}: IDF={row['idf']:.4f}, 문서빈도={row['doc_frequency']}")
    
    print(f"\n하위 10개 IDF 값을 가진 단어 (자주 등장하는 단어들):")
    for i, row in word_idf_df.tail(10).iterrows():
        print(f"{i+1:2d}. {row['word']}: IDF={row['idf']:.4f}, 문서빈도={row['doc_frequency']}")

if __name__ == "__main__":
    input_file = "qubit_filtered_DTM.csv"
    output_file = "qubit_TF_IDF_DTM.csv"
    
    calculate_tfidf_dtm(input_file, output_file)
