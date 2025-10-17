"""
Qubit 논문 데이터에서 저자 국가 정보를 추출하는 스크립트

이 스크립트는 qubit_country.csv 파일을 읽어서 각 논문의 저자들이 속한 국가들을 추출하고,
중복을 제거하여 qubit_country_result.csv 파일로 저장합니다.
국가명과 ISO 3166 Alpha-2 국가 코드를 모두 추출합니다.

입력: qubit_country.csv (DOI, Addresses 컬럼)
출력: qubit_country_result.csv (DOI, Addresses, Country, Country_Code 컬럼)

작성자: AI Assistant
날짜: 2024
"""

import pandas as pd
import re

def extract_countries_from_address(address):
    """
    주소 문자열에서 국가들과 ISO 3166 Alpha-2 코드를 추출하는 함수
    
    Args:
        address (str): Web of Science에서 export한 저자 주소 정보
        
    Returns:
        tuple: (추출된 국가들을 comma로 구분한 문자열, 국가 코드들을 comma로 구분한 문자열)
    """
    if pd.isna(address) or address == '' or str(address).lower() == 'nan':
        return '', ''
    
    # 국가명과 코드를 함께 관리하는 딕셔너리 {국가명: 국가코드}
    country_data = {}
    
    # 세미콜론으로 구분된 각 기관 주소를 처리
    institutions = str(address).split(';')
    
    for institution in institutions:
        # 대괄호 부분 제거 (저자 이름들)
        institution = re.sub(r'\[.*?\]', '', institution).strip()
        
        # 쉼표로 분리하여 각 부분을 확인
        parts = [part.strip() for part in institution.split(',')]
        
        if not parts:
            continue
            
        # 마지막 부분이 국가일 가능성이 높음
        last_part = parts[-1]
        
        # 국가명과 ISO 3166 Alpha-2 코드 매핑 테이블
        country_mapping = {
            # 주요 국가들
            'USA': ('USA', 'US'),
            'United States': ('USA', 'US'),
            'Peoples R China': ('China', 'CN'),
            'China': ('China', 'CN'),
            'South Korea': ('South Korea', 'KR'),
            'Korea': ('South Korea', 'KR'),
            'Japan': ('Japan', 'JP'),
            'Germany': ('Germany', 'DE'),
            'France': ('France', 'FR'),
            'United Kingdom': ('United Kingdom', 'GB'),
            'UK': ('United Kingdom', 'GB'),
            'England': ('United Kingdom', 'GB'),
            'Scotland': ('United Kingdom', 'GB'),
            'Wales': ('United Kingdom', 'GB'),
            'North Ireland': ('United Kingdom', 'GB'),
            'Ireland': ('Ireland', 'IE'),
            'Canada': ('Canada', 'CA'),
            'Australia': ('Australia', 'AU'),
            'Austria': ('Austria', 'AT'),
            'Switzerland': ('Switzerland', 'CH'),
            'Netherlands': ('Netherlands', 'NL'),
            'Denmark': ('Denmark', 'DK'),
            'Sweden': ('Sweden', 'SE'),
            'Finland': ('Finland', 'FI'),
            'Norway': ('Norway', 'NO'),
            'Italy': ('Italy', 'IT'),
            'Spain': ('Spain', 'ES'),
            'Portugal': ('Portugal', 'PT'),
            'Belgium': ('Belgium', 'BE'),
            'Poland': ('Poland', 'PL'),
            'Czech Republic': ('Czech Republic', 'CZ'),
            'Hungary': ('Hungary', 'HU'),
            'Romania': ('Romania', 'RO'),
            'Bulgaria': ('Bulgaria', 'BG'),
            'Greece': ('Greece', 'GR'),
            'Turkey': ('Turkey', 'TR'),
            'Turkiye': ('Turkey', 'TR'),  # 터키의 새로운 공식 명칭
            'Russia': ('Russia', 'RU'),
            'Ukraine': ('Ukraine', 'UA'),
            'Brazil': ('Brazil', 'BR'),
            'Argentina': ('Argentina', 'AR'),
            'Chile': ('Chile', 'CL'),
            'Mexico': ('Mexico', 'MX'),
            'India': ('India', 'IN'),
            'Singapore': ('Singapore', 'SG'),
            'Taiwan': ('Taiwan', 'TW'),
            'Thailand': ('Thailand', 'TH'),
            'Malaysia': ('Malaysia', 'MY'),
            'Indonesia': ('Indonesia', 'ID'),
            'Philippines': ('Philippines', 'PH'),
            'Vietnam': ('Vietnam', 'VN'),
            'Israel': ('Israel', 'IL'),
            'Saudi Arabia': ('Saudi Arabia', 'SA'),
            'United Arab Emirates': ('United Arab Emirates', 'AE'),
            'Egypt': ('Egypt', 'EG'),
            'South Africa': ('South Africa', 'ZA'),
            'New Zealand': ('New Zealand', 'NZ'),
            'Panama': ('Panama', 'PA'),
            'Algeria': ('Algeria', 'DZ'),
            
            # 중동/아시아 국가들
            'Iran': ('Iran', 'IR'),
            'Pakistan': ('Pakistan', 'PK'),
            'Bangladesh': ('Bangladesh', 'BD'),
            'Sri Lanka': ('Sri Lanka', 'LK'),
            'Nepal': ('Nepal', 'NP'),
            'Bhutan': ('Bhutan', 'BT'),
            'Maldives': ('Maldives', 'MV'),
            'Afghanistan': ('Afghanistan', 'AF'),
            'Kazakhstan': ('Kazakhstan', 'KZ'),
            'Uzbekistan': ('Uzbekistan', 'UZ'),
            'Kyrgyzstan': ('Kyrgyzstan', 'KG'),
            'Tajikistan': ('Tajikistan', 'TJ'),
            'Turkmenistan': ('Turkmenistan', 'TM'),
            'Mongolia': ('Mongolia', 'MN'),
            'North Korea': ('North Korea', 'KP'),
            'Myanmar': ('Myanmar', 'MM'),
            'Laos': ('Laos', 'LA'),
            'Cambodia': ('Cambodia', 'KH'),
            'Brunei': ('Brunei', 'BN'),
            'East Timor': ('East Timor', 'TL'),
            
            # 유럽 국가들
            'Serbia': ('Serbia', 'RS'),
            'Slovakia': ('Slovakia', 'SK'),
            'Slovenia': ('Slovenia', 'SI'),
            'Croatia': ('Croatia', 'HR'),
            'Bosnia and Herzegovina': ('Bosnia and Herzegovina', 'BA'),
            'Montenegro': ('Montenegro', 'ME'),
            'North Macedonia': ('North Macedonia', 'MK'),
            'Albania': ('Albania', 'AL'),
            'Kosovo': ('Kosovo', 'XK'),
            'Moldova': ('Moldova', 'MD'),
            'Belarus': ('Belarus', 'BY'),
            'Lithuania': ('Lithuania', 'LT'),
            'Latvia': ('Latvia', 'LV'),
            'Estonia': ('Estonia', 'EE'),
            'Luxembourg': ('Luxembourg', 'LU'),
            'Malta': ('Malta', 'MT'),
            'Cyprus': ('Cyprus', 'CY'),
            'Iceland': ('Iceland', 'IS'),
            'Liechtenstein': ('Liechtenstein', 'LI'),
            'Monaco': ('Monaco', 'MC'),
            'San Marino': ('San Marino', 'SM'),
            'Vatican': ('Vatican', 'VA'),
            'Andorra': ('Andorra', 'AD'),
            
            # 아프리카 국가들
            'Kenya': ('Kenya', 'KE'),
            'Tanzania': ('Tanzania', 'TZ'),
            'Uganda': ('Uganda', 'UG'),
            'Rwanda': ('Rwanda', 'RW'),
            'Burundi': ('Burundi', 'BI'),
            'Ethiopia': ('Ethiopia', 'ET'),
            'Eritrea': ('Eritrea', 'ER'),
            'Djibouti': ('Djibouti', 'DJ'),
            'Somalia': ('Somalia', 'SO'),
            'Sudan': ('Sudan', 'SD'),
            'South Sudan': ('South Sudan', 'SS'),
            'Central African Republic': ('Central African Republic', 'CF'),
            'Chad': ('Chad', 'TD'),
            'Niger': ('Niger', 'NE'),
            'Mali': ('Mali', 'ML'),
            'Burkina Faso': ('Burkina Faso', 'BF'),
            'Senegal': ('Senegal', 'SN'),
            'Gambia': ('Gambia', 'GM'),
            'Guinea-Bissau': ('Guinea-Bissau', 'GW'),
            'Guinea': ('Guinea', 'GN'),
            'Sierra Leone': ('Sierra Leone', 'SL'),
            'Liberia': ('Liberia', 'LR'),
            'Ivory Coast': ('Ivory Coast', 'CI'),
            'Ghana': ('Ghana', 'GH'),
            'Togo': ('Togo', 'TG'),
            'Benin': ('Benin', 'BJ'),
            'Nigeria': ('Nigeria', 'NG'),
            'Cameroon': ('Cameroon', 'CM'),
            'Equatorial Guinea': ('Equatorial Guinea', 'GQ'),
            'Gabon': ('Gabon', 'GA'),
            'Republic of the Congo': ('Republic of the Congo', 'CG'),
            'Democratic Republic of the Congo': ('Democratic Republic of the Congo', 'CD'),
            'Angola': ('Angola', 'AO'),
            'Zambia': ('Zambia', 'ZM'),
            'Zimbabwe': ('Zimbabwe', 'ZW'),
            'Botswana': ('Botswana', 'BW'),
            'Namibia': ('Namibia', 'NA'),
            'Lesotho': ('Lesotho', 'LS'),
            'Swaziland': ('Swaziland', 'SZ'),
            'Madagascar': ('Madagascar', 'MG'),
            'Mauritius': ('Mauritius', 'MU'),
            'Seychelles': ('Seychelles', 'SC'),
            'Comoros': ('Comoros', 'KM'),
            'Cape Verde': ('Cape Verde', 'CV'),
            'Sao Tome and Principe': ('Sao Tome and Principe', 'ST'),
            'Morocco': ('Morocco', 'MA'),
            'Tunisia': ('Tunisia', 'TN'),
            'Libya': ('Libya', 'LY'),
            'Malawi': ('Malawi', 'MW'),
            'Mozambique': ('Mozambique', 'MZ'),
            
            # 오세아니아 국가들
            'Papua New Guinea': ('Papua New Guinea', 'PG'),
            'Fiji': ('Fiji', 'FJ'),
            'Samoa': ('Samoa', 'WS'),
            'Tonga': ('Tonga', 'TO'),
            'Vanuatu': ('Vanuatu', 'VU'),
            'Solomon Islands': ('Solomon Islands', 'SB'),
            'Palau': ('Palau', 'PW'),
            'Marshall Islands': ('Marshall Islands', 'MH'),
            'Micronesia': ('Micronesia', 'FM'),
            'Kiribati': ('Kiribati', 'KI'),
            'Nauru': ('Nauru', 'NR'),
            'Tuvalu': ('Tuvalu', 'TV'),
            
            # 기타 국가들
            'Armenia': ('Armenia', 'AM'),
            'Azerbaijan': ('Azerbaijan', 'AZ'),
            'Qatar': ('Qatar', 'QA')
        }
        
        # 정확한 매칭 시도
        if last_part in country_mapping:
            country_name, country_code = country_mapping[last_part]
            country_data[country_name] = country_code
        else:
            # 부분 매칭 시도
            found = False
            for country_key, (country_name, country_code) in country_mapping.items():
                if country_key.lower() in last_part.lower():
                    country_data[country_name] = country_code
                    found = True
                    break
            
            if not found:
                # 특별한 케이스들 처리
                if 'Peoples R China' in institution:
                    country_data['China'] = 'CN'
                elif 'South Korea' in institution:
                    country_data['South Korea'] = 'KR'
                elif 'USA' in institution or 'United States' in institution:
                    country_data['USA'] = 'US'
                elif any(uk_term in institution for uk_term in ['England', 'Scotland', 'Wales', 'North Ireland']):
                    country_data['United Kingdom'] = 'GB'
                elif 'CH-' in institution or 'Switzerland' in institution:
                    country_data['Switzerland'] = 'CH'
                elif 'D-' in institution or 'Germany' in institution:
                    country_data['Germany'] = 'DE'
                elif 'F-' in institution or 'France' in institution:
                    country_data['France'] = 'FR'
                elif 'NL-' in institution or 'Netherlands' in institution:
                    country_data['Netherlands'] = 'NL'
                elif 'DK-' in institution or 'Denmark' in institution:
                    country_data['Denmark'] = 'DK'
                elif 'SE-' in institution or 'Sweden' in institution:
                    country_data['Sweden'] = 'SE'
                elif 'FI-' in institution or 'Finland' in institution:
                    country_data['Finland'] = 'FI'
                elif 'A-' in institution or 'Austria' in institution:
                    country_data['Austria'] = 'AT'
                elif 'TR' in last_part or 'Turkey' in institution or 'Turkiye' in institution:
                    country_data['Turkey'] = 'TR'
                elif 'IR' in last_part or 'Iran' in institution:
                    country_data['Iran'] = 'IR'
                elif 'PK' in last_part or 'Pakistan' in institution:
                    country_data['Pakistan'] = 'PK'
                elif 'RS' in last_part or 'Serbia' in institution:
                    country_data['Serbia'] = 'RS'
                elif 'SK' in last_part or 'Slovakia' in institution:
                    country_data['Slovakia'] = 'SK'
                elif 'SI' in last_part or 'Slovenia' in institution:
                    country_data['Slovenia'] = 'SI'
                elif 'AM' in last_part or 'Armenia' in institution:
                    country_data['Armenia'] = 'AM'
                elif 'AZ' in last_part or 'Azerbaijan' in institution:
                    country_data['Azerbaijan'] = 'AZ'
                elif 'QA' in last_part or 'Qatar' in institution:
                    country_data['Qatar'] = 'QA'
                # 기타 국가 코드들
                elif 'CA' in last_part and 'Canada' in institution:
                    country_data['Canada'] = 'CA'
                elif 'AU' in last_part and 'Australia' in institution:
                    country_data['Australia'] = 'AU'
                elif 'JP' in last_part or 'Japan' in institution:
                    country_data['Japan'] = 'JP'
                elif 'KR' in last_part or 'Korea' in institution:
                    country_data['South Korea'] = 'KR'
                elif 'CN' in last_part or 'China' in institution:
                    country_data['China'] = 'CN'
                elif 'IN' in last_part or 'India' in institution:
                    country_data['India'] = 'IN'
                elif 'SG' in last_part or 'Singapore' in institution:
                    country_data['Singapore'] = 'SG'
                elif 'TW' in last_part or 'Taiwan' in institution:
                    country_data['Taiwan'] = 'TW'
                elif 'IL' in last_part or 'Israel' in institution:
                    country_data['Israel'] = 'IL'
                elif 'BR' in last_part or 'Brazil' in institution:
                    country_data['Brazil'] = 'BR'
                elif 'RU' in last_part or 'Russia' in institution:
                    country_data['Russia'] = 'RU'
                elif 'IT' in last_part or 'Italy' in institution:
                    country_data['Italy'] = 'IT'
                elif 'ES' in last_part or 'Spain' in institution:
                    country_data['Spain'] = 'ES'
                elif 'PT' in last_part or 'Portugal' in institution:
                    country_data['Portugal'] = 'PT'
                elif 'BE' in last_part or 'Belgium' in institution:
                    country_data['Belgium'] = 'BE'
                elif 'PL' in last_part or 'Poland' in institution:
                    country_data['Poland'] = 'PL'
                elif 'CZ' in last_part or 'Czech Republic' in institution:
                    country_data['Czech Republic'] = 'CZ'
                elif 'HU' in last_part or 'Hungary' in institution:
                    country_data['Hungary'] = 'HU'
                elif 'RO' in last_part or 'Romania' in institution:
                    country_data['Romania'] = 'RO'
                elif 'BG' in last_part or 'Bulgaria' in institution:
                    country_data['Bulgaria'] = 'BG'
                elif 'GR' in last_part or 'Greece' in institution:
                    country_data['Greece'] = 'GR'
                elif 'UA' in last_part or 'Ukraine' in institution:
                    country_data['Ukraine'] = 'UA'
                elif 'AR' in last_part or 'Argentina' in institution:
                    country_data['Argentina'] = 'AR'
                elif 'CL' in last_part or 'Chile' in institution:
                    country_data['Chile'] = 'CL'
                elif 'MX' in last_part or 'Mexico' in institution:
                    country_data['Mexico'] = 'MX'
                elif 'TH' in last_part or 'Thailand' in institution:
                    country_data['Thailand'] = 'TH'
                elif 'MY' in last_part or 'Malaysia' in institution:
                    country_data['Malaysia'] = 'MY'
                elif 'ID' in last_part or 'Indonesia' in institution:
                    country_data['Indonesia'] = 'ID'
                elif 'PH' in last_part or 'Philippines' in institution:
                    country_data['Philippines'] = 'PH'
                elif 'VN' in last_part or 'Vietnam' in institution:
                    country_data['Vietnam'] = 'VN'
                elif 'SA' in last_part or 'Saudi Arabia' in institution:
                    country_data['Saudi Arabia'] = 'SA'
                elif 'AE' in last_part or 'United Arab Emirates' in institution:
                    country_data['United Arab Emirates'] = 'AE'
                elif 'EG' in last_part or 'Egypt' in institution:
                    country_data['Egypt'] = 'EG'
                elif 'ZA' in last_part or 'South Africa' in institution:
                    country_data['South Africa'] = 'ZA'
                elif 'NZ' in last_part or 'New Zealand' in institution:
                    country_data['New Zealand'] = 'NZ'
                elif 'PA' in last_part or 'Panama' in institution:
                    country_data['Panama'] = 'PA'
                elif 'DZ' in last_part or 'Algeria' in institution:
                    country_data['Algeria'] = 'DZ'
    
    # 국가명으로 정렬하여 comma로 구분된 문자열로 반환
    sorted_countries = sorted(country_data.keys())
    countries_str = ','.join(sorted_countries)
    country_codes_str = ','.join([country_data[country] for country in sorted_countries])
    
    return countries_str, country_codes_str

def check_duplicate_countries_in_row(countries_str, country_codes_str):
    """
    각 row의 국가 문자열에서 중복이 있는지 확인하는 함수
    
    Args:
        countries_str (str): comma로 구분된 국가 문자열
        country_codes_str (str): comma로 구분된 국가 코드 문자열
        
    Returns:
        tuple: (중복 여부, 중복된 국가 리스트, 중복된 코드 리스트)
    """
    if pd.isna(countries_str) or countries_str == '':
        return False, [], []
    
    # comma로 분리하고 공백 제거
    countries = [country.strip() for country in countries_str.split(',')]
    country_codes = [code.strip() for code in country_codes_str.split(',')] if country_codes_str else []
    
    # 중복 확인
    unique_countries = set(countries)
    unique_codes = set(country_codes)
    
    country_duplicates = []
    code_duplicates = []
    
    if len(countries) != len(unique_countries):
        # 국가명 중복이 있는 경우
        seen = set()
        for country in countries:
            if country in seen:
                country_duplicates.append(country)
            else:
                seen.add(country)
    
    if len(country_codes) != len(unique_codes):
        # 국가 코드 중복이 있는 경우
        seen = set()
        for code in country_codes:
            if code in seen:
                code_duplicates.append(code)
            else:
                seen.add(code)
    
    has_duplicates = len(country_duplicates) > 0 or len(code_duplicates) > 0
    
    return has_duplicates, country_duplicates, code_duplicates

def main():
    """
    메인 실행 함수
    """
    print("=" * 70)
    print("Qubit 논문 저자 국가 정보 추출 프로그램 (ISO 3166 Alpha-2 코드 포함)")
    print("=" * 70)
    
    # CSV 파일 읽기
    print("\n1. CSV 파일을 읽는 중...")
    try:
        df = pd.read_csv('/Users/bumjunekim/Desktop/research_day/qubit-data-processing/co-country/qubit_country.csv')
        print(f"   ✓ qubit_country.csv 파일을 성공적으로 읽었습니다.")
        print(f"   ✓ 총 {len(df)} 개의 논문 데이터를 발견했습니다.")
    except FileNotFoundError:
        print("   ✗ qubit_country.csv 파일을 찾을 수 없습니다.")
        return
    except Exception as e:
        print(f"   ✗ 파일 읽기 중 오류가 발생했습니다: {e}")
        return
    
    # 국가 추출
    print("\n2. 국가 정보와 ISO 3166 Alpha-2 코드를 추출하는 중...")
    country_data = df['Addresses'].apply(extract_countries_from_address)
    df['Country'] = [data[0] for data in country_data]
    df['Country_Code'] = [data[1] for data in country_data]
    print("   ✓ 국가 정보와 국가 코드 추출이 완료되었습니다.")
    
    # 중복 체크
    print("\n3. 중복 국가를 확인하는 중...")
    duplicate_rows = []
    
    for idx, row in df.iterrows():
        has_duplicates, country_duplicates, code_duplicates = check_duplicate_countries_in_row(
            row['Country'], row['Country_Code']
        )
        if has_duplicates:
            duplicate_rows.append({
                'row_index': idx + 1,
                'doi': row['DOI'],
                'countries': row['Country'],
                'country_codes': row['Country_Code'],
                'country_duplicates': country_duplicates,
                'code_duplicates': code_duplicates
            })
    
    if duplicate_rows:
        print(f"   ⚠️  {len(duplicate_rows)} 개의 논문에서 중복이 발견되었습니다.")
        for item in duplicate_rows[:5]:  # 처음 5개만 표시
            print(f"      Row {item['row_index']}: {item['countries']} / {item['country_codes']}")
            if item['country_duplicates']:
                print(f"         국가명 중복: {', '.join(set(item['country_duplicates']))}")
            if item['code_duplicates']:
                print(f"         국가코드 중복: {', '.join(set(item['code_duplicates']))}")
        if len(duplicate_rows) > 5:
            print(f"      ... (총 {len(duplicate_rows)}개)")
    else:
        print("   ✓ 모든 논문에서 중복이 발견되지 않았습니다.")
    
    # 결과 저장
    print("\n4. 결과를 저장하는 중...")
    try:
        output_file = '/Users/bumjunekim/Desktop/research_day/qubit-data-processing/co-country/qubit_country_result.csv'
        df.to_csv(output_file, index=False)
        print(f"   ✓ 결과가 {output_file}에 저장되었습니다.")
    except Exception as e:
        print(f"   ✗ 파일 저장 중 오류가 발생했습니다: {e}")
        return
    
    # 통계 출력
    print("\n" + "=" * 70)
    print("처리 결과 통계")
    print("=" * 70)
    print(f"총 논문 수: {len(df):,}")
    print(f"국가 정보가 추출된 논문 수: {len(df[df['Country'] != '']):,}")
    print(f"국가 정보가 추출되지 않은 논문 수: {len(df[df['Country'] == '']):,}")
    print(f"성공률: {len(df[df['Country'] != '']) / len(df) * 100:.2f}%")
    
    # 국가별 논문 수 통계
    all_countries = []
    all_country_codes = []
    for countries_str in df['Country']:
        if countries_str:
            all_countries.extend(countries_str.split(','))
    for codes_str in df['Country_Code']:
        if codes_str:
            all_country_codes.extend(codes_str.split(','))
    
    country_counts = pd.Series(all_countries).value_counts()
    code_counts = pd.Series(all_country_codes).value_counts()
    
    print(f"\n상위 20개 국가별 논문 수:")
    print("-" * 50)
    for i, (country, count) in enumerate(country_counts.head(20).items(), 1):
        print(f"{i:2d}. {country:<20} {count:>6,}개")
    
    print(f"\n상위 20개 국가 코드별 논문 수:")
    print("-" * 50)
    for i, (code, count) in enumerate(code_counts.head(20).items(), 1):
        print(f"{i:2d}. {code:<5} {count:>6,}개")
    
    # 새로 추가된 주요 국가들 확인
    new_countries = ['Iran', 'Pakistan', 'Serbia', 'Slovakia', 'Slovenia', 'Turkey', 'Armenia', 'Azerbaijan', 'Qatar']
    print(f"\n새로 추가된 주요 국가들의 논문 수:")
    print("-" * 50)
    for country in new_countries:
        count = country_counts.get(country, 0)
        if count > 0:
            # 해당 국가의 코드 찾기
            code = None
            for idx, row in df.iterrows():
                if country in str(row['Country']):
                    codes = str(row['Country_Code']).split(',')
                    if codes and codes[0] != 'nan':
                        # 해당 국가의 위치 찾기
                        countries = str(row['Country']).split(',')
                        try:
                            country_idx = countries.index(country)
                            code = codes[country_idx]
                        except (ValueError, IndexError):
                            pass
                        break
            print(f"    {country:<20} ({code}) {count:>6,}개")
    
    # 남은 논문들 확인
    missing_countries = df[df['Country'].isna() | (df['Country'] == '')]
    if len(missing_countries) > 0:
        print(f"\n국가가 추출되지 않은 논문들:")
        print("-" * 50)
        for idx, row in missing_countries.iterrows():
            print(f"    Row {idx + 1}: DOI = {row['DOI']}")
            if str(row['Addresses']).lower() != 'nan':
                print(f"             Addresses = {str(row['Addresses'])[:100]}...")
            else:
                print(f"             Addresses = nan (빈 데이터)")
    
    print("\n" + "=" * 70)
    print("작업이 완료되었습니다!")
    print("=" * 70)

if __name__ == "__main__":
    main()
