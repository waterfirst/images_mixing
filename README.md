# 🎨 픽셀 믹서 (Pixel Mixer)

**두 이미지를 픽셀 단위로 믹싱하는 Streamlit 웹 애플리케이션**

두 개의 이미지를 체스판, 줄무늬, 대각선 패턴으로 픽셀 단위로 조합하여 창의적인 이미지를 만드는 도구입니다.

---

# 🎨 Pixel Mixer

**Streamlit web application for pixel-by-pixel image mixing**

A creative tool that combines two images using checkerboard, stripe, and diagonal patterns at the pixel level.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url-here.streamlit.app)

---

## ✨ 주요 기능 / Features

- 🎭 **4가지 믹싱 패턴** / **4 Mixing Patterns**: 체스판, 세로/가로 줄무늬, 대각선 패턴
- 📏 **유연한 블록 크기** / **Flexible Block Size**: 1픽셀(정밀) ~ 20픽셀(큰 패턴)
- 📐 **자동 크기 조정** / **Auto Resize**: 두 이미지를 같은 크기로 자동 조정
- 🔍 **실시간 미리보기** / **Real-time Preview**: 패턴을 사이드바에서 실시간 확인
- 📊 **상세 분석** / **Detailed Analysis**: 픽셀 분포, 해상도 손실률 표시
- 💾 **간편한 다운로드** / **Easy Download**: 원클릭 PNG 다운로드

## 🎯 믹싱 패턴 / Mixing Patterns

| 패턴 / Pattern | 설명 / Description | 효과 / Effect |
|--------|-------|---------|
| **체스판 (Checkerboard)** | (1,1)→이미지1, (1,2)→이미지2 교대 배치 | 가장 균등한 50:50 믹싱 |
| **세로 줄무늬 (Vertical)** | 세로 방향으로 번갈아가며 배치 | 수직 방향성 효과 |
| **가로 줄무늬 (Horizontal)** | 가로 방향으로 번갈아가며 배치 | 수평 방향성 효과 |
| **대각선 (Diagonal)** | 대각선 패턴으로 배치 | 다이나믹한 대각선 효과 |

## 🚀 빠른 시작 / Quick Start

### 1. 저장소 복제 / Clone Repository
```bash
git clone https://github.com/waterfirst/images_mixing.git
cd images_mixing
```

### 2. 의존성 설치 / Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행 / Run Application
```bash
streamlit run app.py
```

### 4. 브라우저에서 열기 / Open in Browser
웹 브라우저에서 `http://localhost:8501`로 이동하세요.

Navigate to `http://localhost:8501` in your web browser.

## 📖 사용법 / How to Use

### 기본 사용법 / Basic Usage
1. **이미지 업로드** / **Upload Images**: 두 개의 이미지 파일 선택
2. **패턴 선택** / **Select Pattern**: 사이드바에서 원하는 믹싱 패턴 선택
3. **블록 크기 조정** / **Adjust Block Size**: 1-20픽셀 범위에서 조정
4. **크기 맞춤** / **Size Adjustment**: 자동 또는 사용자 지정 크기 설정
5. **믹싱 실행** / **Start Mixing**: "이미지 믹싱 시작" 버튼 클릭
6. **결과 다운로드** / **Download Result**: PNG 형태로 다운로드

### 패턴 예시 / Pattern Examples

```
원본 이미지 (4×4) / Original Images (4×4):
🔴🔴🔴🔴   🔵🔵🔵🔵
🔴🔴🔴🔴   🔵🔵🔵🔵
🔴🔴🔴🔴   🔵🔵🔵🔵
🔴🔴🔴🔴   🔵🔵🔵🔵

체스판 패턴 결과 / Checkerboard Result:
🔴🔵🔴🔵
🔵🔴🔵🔴
🔴🔵🔴🔵
🔵🔴🔵🔴

세로 줄무늬 결과 / Vertical Stripes Result:
🔴🔵🔴🔵
🔴🔵🔴🔵
🔴🔵🔴🔵
🔴🔵🔴🔵
```

## 💡 활용 팁 / Usage Tips

### 블록 크기별 효과 / Block Size Effects
- **1픽셀**: 최고 정밀도의 픽셀 단위 믹싱 / Maximum precision pixel mixing
- **2-5픽셀**: 부드러운 패턴 효과 / Smooth pattern effects
- **10+픽셀**: 타일 형태의 큰 패턴 / Large tile-like patterns

### 패턴별 추천 용도 / Recommended Use Cases
- **체스판**: 두 이미지의 균등한 조합 / Even combination of two images
- **줄무늬**: 방향성이 있는 디자인 효과 / Directional design effects
- **대각선**: 다이나믹하고 역동적인 효과 / Dynamic and energetic effects

### 최적 결과를 위한 팁 / Tips for Best Results
- 비슷한 색조의 이미지 사용 시 자연스러운 결과 / Use similar tone images for natural results
- 대비가 강한 이미지 사용 시 극적인 효과 / Use high contrast images for dramatic effects
- 정사각형 이미지 권장 (패턴이 더 균등하게 표현) / Square images recommended for even patterns

## 📊 지원 형식 / Supported Formats

- **입력 / Input**: PNG, JPG, JPEG, BMP
- **출력 / Output**: PNG (무손실 압축 / lossless compression)

## ⚠️ 중요한 특징 / Important Features

### 해상도 변화 / Resolution Changes
- **각 이미지의 실질 해상도**: 원본의 약 50% / Each image's effective resolution: ~50% of original
- **최종 이미지 크기**: 조정된 크기 유지 / Final image size: maintains adjusted size
- **픽셀 분포**: 각 이미지가 전체 픽셀의 50% 차지 / Pixel distribution: each image occupies 50% of total pixels

### 크기 조정 옵션 / Size Adjustment Options
- **더 작은 이미지에 맞춤**: 품질 손실 최소화 / Fit to smaller image: minimize quality loss
- **더 큰 이미지에 맞춤**: 최대 해상도 활용 / Fit to larger image: utilize maximum resolution
- **사용자 지정**: 원하는 크기로 조정 / Custom size: adjust to desired dimensions

## 🔧 기술 세부사항 / Technical Details

### 핵심 기술 / Core Technologies
- **Streamlit**: 웹 애플리케이션 프레임워크 / Web application framework
- **PIL/Pillow**: 이미지 처리 라이브러리 / Image processing library
- **NumPy**: 픽셀 단위 배열 연산 / Pixel-level array operations

### 알고리즘 / Algorithm
1. **이미지 로드 및 크기 조정** / Load and resize images
2. **패턴 마스크 생성** / Generate pattern mask
3. **픽셀별 조건부 선택** / Pixel-wise conditional selection
4. **결과 이미지 합성** / Composite result image

### 성능 특성 / Performance Characteristics
- **처리 시간**: 이미지 크기에 비례 / Processing time: proportional to image size
- **메모리 사용량**: 이미지 크기의 약 3배 / Memory usage: ~3x image size
- **최적 이미지 크기**: 1000×1000 픽셀 이하 권장 / Optimal image size: under 1000×1000 pixels

## 🎨 예시 결과 / Example Results

### 자연 이미지 + 건축물
- **체스판 패턴**: 자연과 인공의 조화
- **세로 줄무늬**: 건축적 리듬감 강조

### 추상 이미지 + 인물 사진
- **대각선 패턴**: 역동적인 예술 효과
- **가로 줄무늬**: 안정감 있는 구성

## 🛠️ 개발 정보 / Development Info

### 프로젝트 구조 / Project Structure
```
images_mixing/
├── app.py              # 메인 애플리케이션
├── requirements.txt    # 의존성 패키지
├── README.md          # 프로젝트 문서
└── .gitignore         # Git 제외 파일
```

### 환경 요구사항 / Environment Requirements
- **Python**: 3.8 이상 / 3.8+
- **메모리**: 최소 2GB RAM / Minimum 2GB RAM
- **저장공간**: 100MB / 100MB storage

## 📝 라이선스 / License

이 프로젝트는 MIT 라이선스 하에 배포됩니다. / This project is licensed under the MIT License.

## 🤝 기여하기 / Contributing

버그 리포트, 기능 제안, 풀 리퀘스트를 환영합니다! / Bug reports, feature suggestions, and pull requests are welcome!

## 📞 지원 / Support

문제가 발생하거나 질문이 있으시면 GitHub Issues를 통해 문의해주세요. / For issues or questions, please use GitHub Issues.

---

**만든이 / Created by**: waterfirst  
**저장소 / Repository**: https://github.com/waterfirst/images_mixing
