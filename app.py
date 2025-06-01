import streamlit as st
import numpy as np
from PIL import Image
import io

def create_pattern_mask(width, height, pattern_type, block_size):
    """패턴에 따른 마스크 생성"""
    mask = np.zeros((height, width), dtype=bool)
    
    if pattern_type == "체스판 (Checkerboard)":
        # 체스판 패턴: (i//block_size + j//block_size) % 2
        for i in range(height):
            for j in range(width):
                if (i // block_size + j // block_size) % 2 == 0:
                    mask[i, j] = True
                    
    elif pattern_type == "세로 줄무늬 (Vertical)":
        # 세로 줄무늬: j//block_size % 2
        for i in range(height):
            for j in range(width):
                if (j // block_size) % 2 == 0:
                    mask[i, j] = True
                    
    elif pattern_type == "가로 줄무늬 (Horizontal)":
        # 가로 줄무늬: i//block_size % 2
        for i in range(height):
            for j in range(width):
                if (i // block_size) % 2 == 0:
                    mask[i, j] = True
                    
    elif pattern_type == "대각선 (Diagonal)":
        # 대각선 패턴: (i + j)//block_size % 2
        for i in range(height):
            for j in range(width):
                if ((i + j) // block_size) % 2 == 0:
                    mask[i, j] = True
    
    return mask

def resize_images(img1, img2, resize_option, custom_width=None, custom_height=None):
    """이미지 크기 조정"""
    if resize_option == "더 작은 이미지에 맞춤":
        target_width = min(img1.width, img2.width)
        target_height = min(img1.height, img2.height)
    elif resize_option == "더 큰 이미지에 맞춤":
        target_width = max(img1.width, img2.width)
        target_height = max(img1.height, img2.height)
    else:  # 사용자 지정
        target_width = custom_width or min(img1.width, img2.width)
        target_height = custom_height or min(img1.height, img2.height)
    
    img1_resized = img1.resize((target_width, target_height), Image.Resampling.LANCZOS)
    img2_resized = img2.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    return img1_resized, img2_resized, target_width, target_height

def mix_images(img1, img2, pattern_type, block_size):
    """두 이미지를 패턴에 따라 믹싱"""
    # NumPy 배열로 변환
    arr1 = np.array(img1)
    arr2 = np.array(img2)
    
    height, width = arr1.shape[:2]
    
    # 패턴 마스크 생성
    mask = create_pattern_mask(width, height, pattern_type, block_size)
    
    # 결과 배열 초기화
    result = np.zeros_like(arr1)
    
    # 마스크에 따라 픽셀 선택
    if len(arr1.shape) == 3:  # 컬러 이미지
        for c in range(arr1.shape[2]):
            result[:, :, c] = np.where(mask, arr1[:, :, c], arr2[:, :, c])
    else:  # 그레이스케일 이미지
        result = np.where(mask, arr1, arr2)
    
    return Image.fromarray(result.astype(np.uint8))

def create_pattern_preview(pattern_type, block_size, preview_size=100):
    """패턴 미리보기 생성"""
    mask = create_pattern_mask(preview_size, preview_size, pattern_type, block_size)
    
    # 빨간색과 파란색으로 패턴 표시
    preview = np.zeros((preview_size, preview_size, 3), dtype=np.uint8)
    preview[mask] = [255, 100, 100]  # 빨간색
    preview[~mask] = [100, 100, 255]  # 파란색
    
    return Image.fromarray(preview)

def calculate_stats(img1, img2, mixed_img):
    """이미지 통계 계산"""
    # 픽셀 분포 (각 이미지가 차지하는 비율)
    pixel_ratio = 0.5  # 모든 패턴에서 50:50
    
    # 해상도 손실률 계산
    original_pixels = img1.width * img1.height
    final_pixels = mixed_img.width * mixed_img.height
    resolution_retention = (final_pixels / original_pixels) * 100
    
    return {
        "pixel_ratio": pixel_ratio,
        "resolution_retention": resolution_retention,
        "original_size": (img1.width, img1.height),
        "final_size": (mixed_img.width, mixed_img.height)
    }

# Streamlit 앱 설정
st.set_page_config(
    page_title="🎨 픽셀 믹서 (Pixel Mixer)",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 메인 타이틀
st.title("🎨 픽셀 믹서 (Pixel Mixer)")
st.markdown("**두 이미지를 픽셀 단위로 믹싱하는 창의적 도구**")

# 사이드바 설정
st.sidebar.header("⚙️ 믹싱 설정")

# 패턴 선택
pattern_options = [
    "체스판 (Checkerboard)",
    "세로 줄무늬 (Vertical)", 
    "가로 줄무늬 (Horizontal)",
    "대각선 (Diagonal)"
]
selected_pattern = st.sidebar.selectbox(
    "🎭 믹싱 패턴 선택",
    pattern_options,
    help="각 패턴은 서로 다른 시각적 효과를 제공합니다."
)

# 블록 크기 설정
block_size = st.sidebar.slider(
    "📏 블록 크기 (픽셀)",
    min_value=1,
    max_value=20,
    value=2,
    help="작을수록 정밀하고, 클수록 큰 패턴이 생성됩니다."
)

# 패턴 미리보기
st.sidebar.subheader("🔍 패턴 미리보기")
preview_img = create_pattern_preview(selected_pattern, block_size)
st.sidebar.image(preview_img, caption=f"{selected_pattern} (블록 크기: {block_size})", width=150)

# 크기 조정 옵션
st.sidebar.subheader("📐 크기 조정 옵션")
resize_options = ["더 작은 이미지에 맞춤", "더 큰 이미지에 맞춤", "사용자 지정"]
resize_option = st.sidebar.selectbox("크기 조정 방식", resize_options)

custom_width, custom_height = None, None
if resize_option == "사용자 지정":
    col1, col2 = st.sidebar.columns(2)
    with col1:
        custom_width = st.number_input("폭", min_value=100, max_value=2000, value=500)
    with col2:
        custom_height = st.number_input("높이", min_value=100, max_value=2000, value=500)

# 메인 컨텐츠 영역
col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 첫 번째 이미지")
    uploaded_file1 = st.file_uploader(
        "이미지 1 업로드",
        type=['png', 'jpg', 'jpeg', 'bmp'],
        key="img1"
    )
    
    if uploaded_file1:
        img1 = Image.open(uploaded_file1)
        st.image(img1, caption=f"이미지 1 ({img1.width}×{img1.height})", use_container_width=True)

with col2:
    st.subheader("📸 두 번째 이미지")
    uploaded_file2 = st.file_uploader(
        "이미지 2 업로드",
        type=['png', 'jpg', 'jpeg', 'bmp'],
        key="img2"
    )
    
    if uploaded_file2:
        img2 = Image.open(uploaded_file2)
        st.image(img2, caption=f"이미지 2 ({img2.width}×{img2.height})", use_container_width=True)

# 믹싱 실행
if uploaded_file1 and uploaded_file2:
    if st.button("🎨 이미지 믹싱 시작", type="primary", use_container_width=True):
        with st.spinner("이미지를 믹싱하는 중..."):
            # 이미지 크기 조정
            img1_resized, img2_resized, final_width, final_height = resize_images(
                img1, img2, resize_option, custom_width, custom_height
            )
            
            # 이미지 믹싱
            mixed_image = mix_images(img1_resized, img2_resized, selected_pattern, block_size)
            
            # 통계 계산
            stats = calculate_stats(img1, img2, mixed_image)
        
        st.success("✅ 믹싱 완료!")
        
        # 결과 표시
        st.subheader("🎉 믹싱 결과")
        st.image(mixed_image, caption=f"믹싱된 이미지 ({final_width}×{final_height})", use_container_width=True)
        
        # 통계 정보
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("픽셀 분포", f"{stats['pixel_ratio']*100:.0f}% : {(1-stats['pixel_ratio'])*100:.0f}%")
        with col2:
            st.metric("최종 해상도", f"{stats['final_size'][0]}×{stats['final_size'][1]}")
        with col3:
            st.metric("해상도 유지율", f"{stats['resolution_retention']:.1f}%")
        
        # 다운로드 버튼
        buf = io.BytesIO()
        mixed_image.save(buf, format='PNG')
        buf.seek(0)
        
        st.download_button(
            label="💾 PNG로 다운로드",
            data=buf.getvalue(),
            file_name=f"mixed_image_{selected_pattern.split()[0]}_{block_size}px.png",
            mime="image/png",
            use_container_width=True
        )

else:
    st.info("👆 두 개의 이미지를 모두 업로드해주세요.")

# 하단 정보
st.markdown("---")
st.markdown("""
### 💡 사용 팁
- **블록 크기 1-2픽셀**: 정밀한 픽셀 믹싱
- **블록 크기 5-10픽셀**: 균형잡힌 패턴 효과  
- **블록 크기 10+픽셀**: 큰 타일 형태의 패턴

### 🎯 패턴별 특징
- **체스판**: 가장 균등한 50:50 믹싱
- **세로/가로 줄무늬**: 방향성 있는 디자인 효과
- **대각선**: 다이나믹하고 역동적인 효과
""")
