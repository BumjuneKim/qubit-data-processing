import pandas as pd
from collections import defaultdict
import itertools

def create_institution_edge_list(input_file, output_file):
    """
    기관 쌍을 추출하여 엣지리스트를 생성하는 함수
    
    Args:
        input_file: 입력 CSV 파일 경로
        output_file: 출력 CSV 파일 경로
    """
    # CSV 파일 읽기
    df = pd.read_csv(input_file)
    
    # 기관 쌍 빈도수를 저장할 딕셔너리
    institution_pairs = defaultdict(int)
    
    # 각 논문의 기관 정보 처리
    for _, row in df.iterrows():
        institution_names = row['Institutions']
        
        # 쉼표로 분리하고 공백 제거
        institutions = [code.strip() for code in institution_names.split(',')]
        
        # 2개 이상의 기관 있는 경우에만 처리
        if len(institutions) >= 2:
            # 모든 기관쌍 생성 (조합)
            for pair in itertools.combinations(institutions, 2):
                # 알파벳 순으로 정렬하여 중복 방지 (A-B와 B-A를 같은 것으로 취급)
                sorted_pair = tuple(sorted(pair))
                institution_pairs[sorted_pair] += 1
    
    # 결과를 DataFrame으로 변환
    edge_data = []
    for (source, target), weight in institution_pairs.items():
        edge_data.append({
            'Source': source,
            'Target': target,
            'Weight': weight
        })
    
    # DataFrame 생성 및 정렬
    edge_df = pd.DataFrame(edge_data)
    edge_df = edge_df.sort_values(['Weight', 'Source', 'Target'], ascending=[False, True, True])
    
    # CSV 파일로 저장
    edge_df.to_csv(output_file, index=False)
    
    print(f"엣지리스트가 {output_file}에 저장되었습니다.")
    print(f"총 {len(edge_df)}개의 국가 쌍이 생성되었습니다.")
    print("\n상위 10개 국가 쌍:")
    print(edge_df.head(10))
    
    return edge_df

if __name__ == "__main__":
    # 입력 및 출력 파일 경로
    input_file = "trapped-ion-mip.csv"
    output_file = "trapped-ion-institution-edge.csv"
    
    # 엣지리스트 생성
    edge_df = create_institution_edge_list(input_file, output_file)
