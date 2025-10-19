# 필요한 라이브러리 로드
library(ggplot2)
library(dplyr)
library(tidyr)
library(scales)

# CSV 파일 읽기
data <- read.csv("publication_freq.csv", stringsAsFactors = FALSE)

# 데이터 확인
print("Data structure:")
str(data)
print("\nFirst few rows:")
head(data)

# 데이터를 long format으로 변환 (ggplot2에서 사용하기 위해)
data_long <- data %>%
  pivot_longer(cols = -year, 
               names_to = "qubit_type", 
               values_to = "publication_count")

# qubit_type을 factor로 변환하고 레벨 순서 설정
data_long$qubit_type <- factor(data_long$qubit_type, 
                               levels = c("superconducting", "trapped.ion", "spin", "photonic", "neutral.atom"),
                               labels = c("Superconducting", "Trapped Ion", "Spin", "Photonic", "Neutral Atom"))

# R² 값 계산 함수
calculate_r_squared <- function(x, y) {
  model <- lm(y ~ x)
  r_squared <- summary(model)$r.squared
  return(r_squared)
}

# 각 qubit_type별 R² 값 계산
r_squared_values <- data_long %>%
  group_by(qubit_type) %>%
  summarise(r_squared = calculate_r_squared(year, publication_count),
            max_count = max(publication_count),
            max_year = year[which.max(publication_count)],
            .groups = 'drop')

print("\nR-squared values:")
print(r_squared_values)

# 색상 팔레트 설정
colors <- c("#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd")
shapes <- c(16, 15, 17, 18, 19)  # 원, 사각형, 삼각형, 다이아몬드, 역삼각형

# ggplot2로 그래프 생성
p <- ggplot(data_long, aes(x = year, y = publication_count, color = qubit_type, shape = qubit_type)) +
  # 꺾은선 그래프
  geom_line(linewidth = 1.2) +
  geom_point(size = 3) +
  
  # 각 데이터 포인트에 출판회수 숫자 표시 (dot 하단)
  geom_text(aes(label = publication_count), 
            vjust = 2, hjust = 0.5, size = 2.5,
            show.legend = FALSE,
            color = "black") +
  
  # R² 값 텍스트 추가 - 위치를 조정하여 가려지지 않도록 함
  geom_text(data = r_squared_values, 
            aes(x = max_year, y = max_count, 
                label = paste("R² =", round(r_squared, 3))),
            hjust = -0.2, vjust = -0.5, size = 3.5,
            show.legend = FALSE,
            color = "black", fontface = "bold") +
  
  # 색상과 모양 설정
  scale_color_manual(values = colors) +
  scale_shape_manual(values = shapes) +
  
  # 축 설정
  scale_x_continuous(breaks = data$year, 
                     labels = data$year,
                     limits = c(min(data$year) - 0.5, max(data$year) + 0.5)) +
  scale_y_continuous(limits = c(0, max(data_long$publication_count) * 1.1)) +
  
  # 제목과 라벨 - 제목과 축 라벨 제거, 범례 제목도 제거
  labs(color = "",
       shape = "") +
  
  # 테마 설정
  theme_minimal() +
  theme(
    axis.title = element_blank(),  # X, Y축 제목 제거
    axis.text = element_text(size = 10),
    axis.text.x = element_text(angle = 0, hjust = 0.5),
    legend.title = element_blank(),  # 범례 제목 제거
    legend.text = element_text(size = 10),
    legend.position = "top",
    legend.justification = "left",
    panel.grid.major = element_line(color = "grey90", linewidth = 0.5),
    panel.grid.minor = element_line(color = "grey95", linewidth = 0.25),
    panel.background = element_rect(fill = "white", color = NA),
    plot.background = element_rect(fill = "white", color = NA)
  )

# 그래프 출력
print(p)

# 그래프 저장
ggsave("v_2.png", 
       plot = p, 
       width = 12, 
       height = 8, 
       dpi = 300, 
       bg = "white")

# 통계 요약 출력
cat("\n=== Publication Statistics by Qubit Implementation Method ===\n")
summary_stats <- data_long %>%
  group_by(qubit_type) %>%
  summarise(
    total_publications = sum(publication_count),
    avg_per_year = round(mean(publication_count), 1),
    peak_year = year[which.max(publication_count)],
    peak_count = max(publication_count),
    r_squared = calculate_r_squared(year, publication_count),
    .groups = 'drop'
  )

print(summary_stats)

cat("\nGraph saved as 'v_2.png'\n")
