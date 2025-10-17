import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정 (macOS)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

def analyze_word_tfidf_mean_distribution(input_file):
    """
    qubit_TF_IDF_DTM.csv 파일을 읽어서 단어별 TF-IDF 평균 분포를 분석하고 시각화합니다.
    
    Args:
        input_file: 입력 CSV 파일 경로 (qubit_TF_IDF_DTM.csv)
    """
    
    print("TF-IDF DTM 데이터 읽는 중...")
    # CSV 파일 읽기
    df = pd.read_csv(input_file)
    
    print(f"총 {len(df)} 개의 문서를 읽었습니다.")
    print(f"총 {df.shape[1] - 1} 개의 단어가 있습니다.")  # DOI 컬럼 제외
    
    # DOI 컬럼과 단어 컬럼 분리
    doi_column = df['DOI']
    tfidf_matrix = df.iloc[:, 1:]  # DOI 컬럼 제외한 모든 단어 컬럼
    
    print("단어별 TF-IDF 평균 계산 중...")
    
    # 단어별 TF-IDF 평균 계산 (0이 아닌 값들만 고려)
    word_tfidf_means = []
    word_tfidf_stats = []
    
    for word in tfidf_matrix.columns:
        word_values = tfidf_matrix[word].values
        nonzero_values = word_values[word_values > 0]  # 0이 아닌 값들만
        
        if len(nonzero_values) > 0:
            mean_tfidf = nonzero_values.mean()
            max_tfidf = nonzero_values.max()
            min_tfidf = nonzero_values.min()
            std_tfidf = nonzero_values.std()
            nonzero_count = len(nonzero_values)
            total_count = len(word_values)
            nonzero_ratio = nonzero_count / total_count
            
            word_tfidf_means.append(mean_tfidf)
            word_tfidf_stats.append({
                'word': word,
                'mean_tfidf': mean_tfidf,
                'max_tfidf': max_tfidf,
                'min_tfidf': min_tfidf,
                'std_tfidf': std_tfidf,
                'nonzero_count': nonzero_count,
                'total_count': total_count,
                'nonzero_ratio': nonzero_ratio
            })
        else:
            word_tfidf_means.append(0)
            word_tfidf_stats.append({
                'word': word,
                'mean_tfidf': 0,
                'max_tfidf': 0,
                'min_tfidf': 0,
                'std_tfidf': 0,
                'nonzero_count': 0,
                'total_count': len(word_values),
                'nonzero_ratio': 0
            })
    
    # DataFrame 생성
    word_stats_df = pd.DataFrame(word_tfidf_stats)
    word_tfidf_means = np.array(word_tfidf_means)
    
    # 0이 아닌 평균값들만 추출
    nonzero_means = word_tfidf_means[word_tfidf_means > 0]
    
    print("단어별 TF-IDF 평균 분포 분석 완료")
    
    # 통계량 계산
    print("\n" + "="*70)
    print("단어별 TF-IDF 평균 분포 주요 통계량")
    print("="*70)
    
    print(f"총 단어 수: {len(word_tfidf_means)}")
    print(f"0이 아닌 평균값을 가진 단어 수: {len(nonzero_means)}")
    print(f"0인 평균값을 가진 단어 수: {len(word_tfidf_means) - len(nonzero_means)}")
    
    print(f"\n단어별 TF-IDF 평균값 통계:")
    print(f"최소 평균 TF-IDF: {word_tfidf_means.min():.6f}")
    print(f"최대 평균 TF-IDF: {word_tfidf_means.max():.6f}")
    print(f"전체 평균 TF-IDF: {word_tfidf_means.mean():.6f}")
    print(f"전체 중간값 TF-IDF: {np.median(word_tfidf_means):.6f}")
    print(f"전체 표준편차: {word_tfidf_means.std():.6f}")
    
    print(f"\n0이 아닌 평균값 통계:")
    print(f"최소 평균 TF-IDF: {nonzero_means.min():.6f}")
    print(f"최대 평균 TF-IDF: {nonzero_means.max():.6f}")
    print(f"평균 TF-IDF: {nonzero_means.mean():.6f}")
    print(f"중간값 TF-IDF: {np.median(nonzero_means):.6f}")
    print(f"표준편차: {nonzero_means.std():.6f}")
    
    # 사분위수
    q25, q50, q75 = np.percentile(word_tfidf_means, [25, 50, 75])
    print(f"\n전체 단어 TF-IDF 평균 사분위수:")
    print(f"25% 분위수: {q25:.6f}")
    print(f"50% 분위수 (중간값): {q50:.6f}")
    print(f"75% 분위수: {q75:.6f}")
    print(f"IQR (75% - 25%): {q75 - q25:.6f}")
    
    # 백분위수
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    print(f"\n백분위수별 TF-IDF 평균값:")
    for p in percentiles:
        value = np.percentile(word_tfidf_means, p)
        print(f"{p:2d}% 분위수: {value:.6f}")
    
    # TF-IDF 평균값 구간별 분포
    print(f"\n단어별 TF-IDF 평균값 구간별 분포:")
    mean_ranges = [
        (0, 0.1, "매우 낮음 (0-0.1)"),
        (0.1, 0.2, "낮음 (0.1-0.2)"),
        (0.2, 0.5, "보통 (0.2-0.5)"),
        (0.5, 1.0, "높음 (0.5-1.0)"),
        (1.0, 2.0, "매우 높음 (1.0-2.0)"),
        (2.0, float('inf'), "극도로 높음 (2.0+)")
    ]
    
    for min_val, max_val, label in mean_ranges:
        if max_val == float('inf'):
            count = np.sum((word_tfidf_means >= min_val))
        else:
            count = np.sum((word_tfidf_means >= min_val) & (word_tfidf_means < max_val))
        percentage = (count / len(word_tfidf_means)) * 100
        print(f"{label}: {count}개 단어 ({percentage:.1f}%)")
    
    # 상위/하위 단어들
    word_stats_df_sorted = word_stats_df.sort_values('mean_tfidf', ascending=False)
    
    print(f"\n상위 25개 TF-IDF 평균값을 가진 단어들:")
    for i, row in word_stats_df_sorted.head(25).iterrows():
        print(f"{i+1:2d}. {row['word']:<25} 평균={row['mean_tfidf']:6.4f}, 최대={row['max_tfidf']:6.2f}, 문서수={row['nonzero_count']:4d}, 비율={row['nonzero_ratio']:5.1%}")
    
    print(f"\n하위 25개 TF-IDF 평균값을 가진 단어들:")
    for i, row in word_stats_df_sorted.tail(25).iterrows():
        print(f"{i+1:2d}. {row['word']:<25} 평균={row['mean_tfidf']:6.4f}, 최대={row['max_tfidf']:6.2f}, 문서수={row['nonzero_count']:4d}, 비율={row['nonzero_ratio']:5.1%}")
    
    # 시각화
    print(f"\n시각화 생성 중...")
    
    plt.figure(figsize=(20, 16))
    
    # 1. 단어별 TF-IDF 평균 히스토그램
    plt.subplot(3, 4, 1)
    plt.hist(word_tfidf_means, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    plt.title('단어별 TF-IDF 평균 분포 히스토그램', fontsize=12, fontweight='bold')
    plt.xlabel('TF-IDF 평균값')
    plt.ylabel('단어 수')
    plt.grid(True, alpha=0.3)
    
    # 2. 0이 아닌 평균값만 히스토그램
    plt.subplot(3, 4, 2)
    plt.hist(nonzero_means, bins=50, alpha=0.7, color='lightcoral', edgecolor='black')
    plt.title('0이 아닌 TF-IDF 평균값 분포', fontsize=12, fontweight='bold')
    plt.xlabel('TF-IDF 평균값')
    plt.ylabel('단어 수')
    plt.grid(True, alpha=0.3)
    
    # 3. 로그 스케일 히스토그램
    plt.subplot(3, 4, 3)
    plt.hist(np.log10(nonzero_means + 1e-10), bins=50, alpha=0.7, color='lightgreen', edgecolor='black')
    plt.title('TF-IDF 평균값 분포 (로그 스케일)', fontsize=12, fontweight='bold')
    plt.xlabel('log10(TF-IDF 평균값)')
    plt.ylabel('단어 수')
    plt.grid(True, alpha=0.3)
    
    # 4. 박스플롯
    plt.subplot(3, 4, 4)
    plt.boxplot([word_tfidf_means, nonzero_means], labels=['전체', '0이 아닌 값'], 
                patch_artist=True, boxprops=dict(facecolor='lightblue'))
    plt.title('TF-IDF 평균값 박스플롯', fontsize=12, fontweight='bold')
    plt.ylabel('TF-IDF 평균값')
    plt.grid(True, alpha=0.3)
    
    # 5. 구간별 분포 막대그래프
    plt.subplot(3, 4, 5)
    ranges = ['0-0.1', '0.1-0.2', '0.2-0.5', '0.5-1.0', '1.0-2.0', '2.0+']
    counts = []
    for min_val, max_val, _ in mean_ranges:
        if max_val == float('inf'):
            count = np.sum((word_tfidf_means >= min_val))
        else:
            count = np.sum((word_tfidf_means >= min_val) & (word_tfidf_means < max_val))
        counts.append(count)
    
    bars = plt.bar(ranges, counts, color='orange', alpha=0.7, edgecolor='black')
    plt.title('TF-IDF 평균값 구간별 단어 수', fontsize=12, fontweight='bold')
    plt.xlabel('TF-IDF 평균값 구간')
    plt.ylabel('단어 수')
    plt.xticks(rotation=45)
    
    # 막대 위에 값 표시
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(counts)*0.01, 
                str(count), ha='center', va='bottom', fontsize=8)
    
    # 6. 누적 분포 함수 (CDF)
    plt.subplot(3, 4, 6)
    sorted_means = np.sort(word_tfidf_means)
    y = np.arange(1, len(sorted_means) + 1) / len(sorted_means)
    plt.plot(sorted_means, y, linewidth=2, color='purple')
    plt.title('TF-IDF 평균값 누적 분포 함수', fontsize=12, fontweight='bold')
    plt.xlabel('TF-IDF 평균값')
    plt.ylabel('누적 확률')
    plt.grid(True, alpha=0.3)
    
    # 7. 상위 단어들의 TF-IDF 평균 막대그래프
    plt.subplot(3, 4, 7)
    top_words = word_stats_df_sorted.head(20)
    bars = plt.bar(range(len(top_words)), top_words['mean_tfidf'], 
                   color='lightblue', alpha=0.7, edgecolor='black')
    plt.title('상위 20개 단어의 TF-IDF 평균값', fontsize=12, fontweight='bold')
    plt.xlabel('단어 순위')
    plt.ylabel('TF-IDF 평균값')
    plt.xticks(range(len(top_words)), [word[:8] + '...' if len(word) > 8 else word 
                                      for word in top_words['word']], rotation=45)
    
    # 8. TF-IDF 평균 vs 최대값 산점도
    plt.subplot(3, 4, 8)
    plt.scatter(word_stats_df['mean_tfidf'], word_stats_df['max_tfidf'], 
                alpha=0.6, s=20, color='green')
    plt.title('TF-IDF 평균 vs 최대값', fontsize=12, fontweight='bold')
    plt.xlabel('TF-IDF 평균값')
    plt.ylabel('TF-IDF 최대값')
    plt.grid(True, alpha=0.3)
    
    # 9. TF-IDF 평균 vs 문서 빈도 산점도
    plt.subplot(3, 4, 9)
    plt.scatter(word_stats_df['mean_tfidf'], word_stats_df['nonzero_count'], 
                alpha=0.6, s=20, color='red')
    plt.title('TF-IDF 평균 vs 문서 빈도', fontsize=12, fontweight='bold')
    plt.xlabel('TF-IDF 평균값')
    plt.ylabel('문서 빈도 (0이 아닌 문서 수)')
    plt.grid(True, alpha=0.3)
    
    # 10. TF-IDF 평균 vs 표준편차 산점도
    plt.subplot(3, 4, 10)
    plt.scatter(word_stats_df['mean_tfidf'], word_stats_df['std_tfidf'], 
                alpha=0.6, s=20, color='orange')
    plt.title('TF-IDF 평균 vs 표준편차', fontsize=12, fontweight='bold')
    plt.xlabel('TF-IDF 평균값')
    plt.ylabel('TF-IDF 표준편차')
    plt.grid(True, alpha=0.3)
    
    # 11. 문서 빈도 비율 분포
    plt.subplot(3, 4, 11)
    plt.hist(word_stats_df['nonzero_ratio'], bins=50, alpha=0.7, color='cyan', edgecolor='black')
    plt.title('문서 빈도 비율 분포', fontsize=12, fontweight='bold')
    plt.xlabel('문서 빈도 비율 (0이 아닌 문서 비율)')
    plt.ylabel('단어 수')
    plt.grid(True, alpha=0.3)
    
    # 12. 백분위수별 TF-IDF 평균 임계값
    plt.subplot(3, 4, 12)
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    threshold_values = [np.percentile(word_tfidf_means, p) for p in percentiles]
    plt.plot(percentiles, threshold_values, marker='o', linewidth=2, markersize=6, color='darkblue')
    plt.title('백분위수별 TF-IDF 평균 임계값', fontsize=12, fontweight='bold')
    plt.xlabel('백분위수 (%)')
    plt.ylabel('TF-IDF 평균 임계값')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('word_tfidf_mean_distribution_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 필터링 권장사항
    print(f"\n" + "="*70)
    print("단어별 TF-IDF 평균 기반 필터링 권장사항")
    print("="*70)
    
    print(f"필터링 전략 제안:")
    print(f"1. 매우 낮은 평균 TF-IDF (0-0.1): 일반적인 단어들 - 제거 고려")
    print(f"2. 낮은 평균 TF-IDF (0.1-0.2): 자주 등장하는 단어들 - 신중히 검토")
    print(f"3. 보통 평균 TF-IDF (0.2-0.5): 적당한 가중치 단어들 - 유지 권장")
    print(f"4. 높은 평균 TF-IDF (0.5-1.0): 중요한 단어들 - 유지 권장")
    print(f"5. 매우 높은 평균 TF-IDF (1.0-2.0): 매우 중요한 단어들 - 유지 권장")
    print(f"6. 극도로 높은 평균 TF-IDF (2.0+): 핵심 단어들 - 유지 권장")
    
    print(f"\n구체적인 필터링 임계값 제안:")
    print(f"- 최소 평균 TF-IDF 임계값: {np.percentile(word_tfidf_means, 10):.4f} (하위 10% 제거)")
    print(f"- 권장 평균 TF-IDF 임계값: {np.percentile(word_tfidf_means, 25):.4f} (하위 25% 제거)")
    print(f"- 보수적 평균 TF-IDF 임계값: {np.percentile(word_tfidf_means, 50):.4f} (하위 50% 제거)")
    
    return word_stats_df

if __name__ == "__main__":
    input_file = "qubit_TF_IDF_DTM.csv"
    
    result_df = analyze_word_tfidf_mean_distribution(input_file)
    
    # 결과를 CSV로 저장
    result_df.to_csv('word_tfidf_mean_analysis_results.csv', index=False)
    print(f"\n단어별 TF-IDF 평균 분석 결과가 'word_tfidf_mean_analysis_results.csv'에 저장되었습니다.")
