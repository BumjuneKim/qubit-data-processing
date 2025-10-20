import pandas as pd
import re

def extract_institutions_from_address(address):
    """
    Address 문자열에서 소속기관을 추출하는 함수
    
    Args:
        address (str): Web of Science의 Addresses 필드
        
    Returns:
        str: 추출된 기관명들을 comma로 join한 문자열 (중복 제거됨)
    """
    if pd.isna(address) or address == '':
        return ''
    
    # 1. 먼저 [저자명들] 패턴을 모두 제거
    cleaned_address = re.sub(r'\[[^\]]*\]', '', address)
    
    # 2. 그 다음에 semicolon으로 split
    parts = cleaned_address.split(';')
    
    institutions = []
    
    # 3. 각 부분에 대해 반복
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        # 4. comma로 split하여 가장 첫번째 요소를 메인 기관으로 본다
        institution_parts = part.split(',')
        if institution_parts:
            main_institution = institution_parts[0].strip()
            if main_institution:
                institutions.append(main_institution)
    
    # 5. 중복을 제거하고 comma로 join (대소문자 구분 없이)
    unique_institutions = []
    seen = set()
    for inst in institutions:
        inst_lower = inst.lower()
        if inst_lower not in seen:
            unique_institutions.append(inst)  # 원본 형태 유지
            seen.add(inst_lower)
    
    return ','.join(unique_institutions)

def normalize_institution_name(inst_name):
    """
    기관명을 정규화하는 함수 (대소문자 통일)
    """
    return inst_name.strip()

def get_canonical_name(inst_name, canonical_map):
    """
    기관명의 표준 형태를 반환하는 함수
    """
    normalized = inst_name.lower()
    if normalized in canonical_map:
        return canonical_map[normalized]
    else:
        canonical_map[normalized] = inst_name
        return inst_name

def main():
    """
    qubit_country.csv 파일에서 소속기관을 추출하여 qubit_institution_result.csv로 저장
    """
    # CSV 파일 읽기
    print("qubit_country.csv 파일을 읽는 중...")
    df = pd.read_csv('qubit_country.csv')
    
    print(f"총 {len(df)}개의 행을 처리합니다.")
    
    # 결과를 저장할 리스트
    results = []
    extraction_stats = {
        'total_rows': len(df),
        'successful_extractions': 0,
        'failed_extractions': 0,
        'empty_addresses': 0
    }
    
    # 기관명 정규화를 위한 맵
    canonical_institution_map = {}
    
    # 각 행에 대해 기관 추출
    for idx, row in df.iterrows():
        doi = row['DOI']
        address = row['Addresses']
        
        institutions_str = extract_institutions_from_address(address)
        
        if not institutions_str:
            if pd.isna(address) or address == '':
                extraction_stats['empty_addresses'] += 1
            else:
                extraction_stats['failed_extractions'] += 1
                print(f"Row {idx+1}: 추출 실패 - {address[:100]}...")
        else:
            extraction_stats['successful_extractions'] += 1
            
            # 기관명 정규화 적용
            normalized_institutions = []
            for inst in institutions_str.split(','):
                inst = inst.strip()
                if inst:
                    canonical_name = get_canonical_name(inst, canonical_institution_map)
                    normalized_institutions.append(canonical_name)
            
            institutions_str = ','.join(normalized_institutions)
        
        results.append({
            'DOI': doi,
            'institution': institutions_str
        })
    
    # 결과를 DataFrame으로 변환
    result_df = pd.DataFrame(results)
    
    # 결과 저장
    output_file = 'qubit_institution_result.csv'
    result_df.to_csv(output_file, index=False)
    
    # 통계 출력
    print("\n=== 추출 결과 통계 ===")
    print(f"총 처리된 행: {extraction_stats['total_rows']}")
    print(f"성공적으로 추출된 행: {extraction_stats['successful_extractions']}")
    print(f"추출 실패한 행: {extraction_stats['failed_extractions']}")
    print(f"빈 주소 행: {extraction_stats['empty_addresses']}")
    
    # 기관 통계
    non_empty = result_df[result_df['institution'] != '']
    if len(non_empty) > 0:
        institution_counts = non_empty['institution'].apply(lambda x: len(x.split(',')) if x else 0)
        print(f"논문당 평균 기관 수: {institution_counts.mean():.2f}")
        print(f"논문당 최대 기관 수: {institution_counts.max()}")
        print(f"논문당 최소 기관 수: {institution_counts.min()}")
    
    print(f"\n결과가 {output_file}에 저장되었습니다.")
    
    # 상위 10개 기관 출력
    print("\n=== 상위 10개 기관 (빈도순) ===")
    all_institutions = []
    for institutions_str in non_empty['institution']:
        if institutions_str:
            all_institutions.extend([inst.strip() for inst in institutions_str.split(',')])
    
    if all_institutions:
        institution_counts = pd.Series(all_institutions).value_counts()
        print(institution_counts.head(10))

if __name__ == "__main__":
    main()
