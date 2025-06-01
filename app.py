import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="Pixel Mixer",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #E74C3C;
        margin-bottom: 2rem;
    }
    .pattern-preview {
        border: 2px solid #3498DB;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f8f9fa;
    }
    .stButton > button {
        background-color: #E74C3C;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .info-box {
        background-color: #EBF3FD;
        border-left: 4px solid #3498DB;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

def resize_images_to_same_size(img1, img2, target_size=None):
    """두 이미지를 같은 크기로 조정"""
    if target_size is None:
        # 더 작은 이미지에 맞춤
        width = min(img1.width, img2.width)
        height = min(img1.height, img2.height)
        target_size = (width, height)
    
    img1_resized = img1.resize(target_size, Image.LANCZOS)
    img2_resized = img2.resize(target_size, Image.LANCZOS)
    
    return img1_resized, img2_resized, target_size

def create_checkerboard_pattern(width, height, start_with_first=True):
    """체스판 패턴 마스크 생성 (True = 첫 번째 이미지, False = 두 번째 이미지)"""
    pattern = np.zeros((height, width), dtype=bool)
    
    for y in range(height):
        for x in range(width):
            # 체스판 패턴: (x + y) % 2
            if start_with_first:
                pattern[y, x] = (x + y) % 2 == 0
            else:
                pattern[y, x] = (x + y) % 2 == 1
    
    return pattern

def create_custom_pattern(width, height, pattern_type, block_size=1):
    """다양한 패턴 생성"""
    pattern = np.zeros((height, width), dtype=bool)
    
    if pattern_type == "checkerboard":
        for y in range(height):
            for x in range(width):
                pattern[y, x] = ((x // block_size) + (y // block_size)) % 2 == 0
                
    elif pattern_type == "vertical_stripes":
        for y in range(height):
            for x in range(width):
                pattern[y, x] = (x // block_size) % 2 == 0
                
    elif pattern_type == "horizontal_stripes":
        for y in range(height):
            for x in range(width):
                pattern[y, x] = (y // block_size) % 2 == 0
                
    elif pattern_type == "diagonal":
        for y in range(height):
            for x in range(width):
                pattern[y, x] = ((x - y) // block_size) % 2 == 0
                
    return pattern

def mix_images_with_pattern(img1, img2, pattern):
    """패턴에 따라 두 이미지 믹싱"""
    # 이미지를 NumPy 배열로 변환
    arr1 = np.array(img1)
    arr2 = np.array(img2)
    
    # 결과 배열 초기화
    result = np.zeros_like(arr1)
    
    # 패턴에 따라 픽셀 선택
    if len(arr1.shape) == 3:  # 컬러 이미지
        for c in range(arr1.shape[2]):  # RGB 채널별로
            result[:, :, c] = np.where(pattern, arr1[:, :, c], arr2[:, :, c])
    else:  # 그레이스케일
        result = np.where(pattern, arr1, arr2)
    
    return Image.fromarray(result.astype(np.uint8))

def create_pattern_preview(pattern_type, block_size, preview_size=(100, 100)):
    """패턴 미리보기 생성"""
    pattern = create_custom_pattern(preview_size[0], preview_size[1], pattern_type, block_size)
    
    # 미리보기 이미지 생성 (빨강=이미지1, 파랑=이미지2)
    preview = np.zeros((preview_size[1], preview_size[0], 3), dtype=np.uint8)
    preview[pattern] = [255, 100, 100]  # 빨간색 (이미지1)
    preview[~pattern] = [100, 100, 255]  # 파란색 (이미지2)
    
    return Image.fromarray(preview)

def get_download_link(img, filename):
    """다운로드 링크 생성"""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_data = buffered.getvalue()
    b64 = base64.b64encode(img_data).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}" style="text-decoration: none; background-color: #E74C3C; color: white; padding: 8px 16px; border-radius: 5px; display: inline-block; margin: 5px;">📥 Download {filename}</a>'
    return href

def main():
    # 헤더
    st.markdown("<h1 class='main-header'>🎨 Pixel Mixer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em; color: #666;'>두 이미지를 픽셀 단위로 믹싱하는 도구</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic;'>Mix two images pixel by pixel with various patterns</p>", unsafe_allow_html=True)
    
    # 사이드바 설정
    st.sidebar.title("⚙️ 믹싱 설정")
    
    # 패턴 타입 선택
    pattern_options = {
        "체스판 (Checkerboard)": "checkerboard",
        "세로 줄무늬 (Vertical Stripes)": "vertical_stripes", 
        "가로 줄무늬 (Horizontal Stripes)": "horizontal_stripes",
        "대각선 (Diagonal)": "diagonal"
    }
    
    selected_pattern = st.sidebar.selectbox(
        "🎭 믹싱 패턴",
        options=list(pattern_options.keys()),
        index=0,
        help="두 이미지를 어떤 패턴으로 섞을지 선택하세요"
    )
    
    # 블록 크기 설정
    block_size = st.sidebar.slider(
        "📏 블록 크기",
        min_value=1,
        max_value=20,
        value=1,
        help="패턴의 블록 크기 (1 = 픽셀 단위)"
    )
    
    # 크기 조정 옵션
    st.sidebar.markdown("---")
    resize_option = st.sidebar.radio(
        "📐 크기 조정 방법",
        ["더 작은 이미지에 맞춤", "더 큰 이미지에 맞춤", "사용자 지정"],
        help="두 이미지 크기가 다를 때 처리 방법"
    )
    
    custom_size = None
    if resize_option == "사용자 지정":
        col1, col2 = st.sidebar.columns(2)
        with col1:
            custom_width = st.number_input("너비", min_value=50, max_value=2000, value=512)
        with col2:
            custom_height = st.number_input("높이", min_value=50, max_value=2000, value=512)
        custom_size = (custom_width, custom_height)
    
    # 패턴 미리보기
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 패턴 미리보기")
    pattern_type = pattern_options[selected_pattern]
    preview_img = create_pattern_preview(pattern_type, block_size)
    st.sidebar.image(preview_img, caption="🔴 이미지1 / 🔵 이미지2", use_column_width=True)
    
    # 메인 영역
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 이미지 업로드")
        
        uploaded_file1 = st.file_uploader(
            "첫 번째 이미지 (🔴)",
            type=['png', 'jpg', 'jpeg', 'bmp'],
            key="img1"
        )
        
        uploaded_file2 = st.file_uploader(
            "두 번째 이미지 (🔵)",
            type=['png', 'jpg', 'jpeg', 'bmp'],
            key="img2"
        )
    
    with col2:
        if uploaded_file1 and uploaded_file2:
            st.subheader("📋 이미지 정보")
            
            # 이미지 로드
            img1 = Image.open(uploaded_file1)
            img2 = Image.open(uploaded_file2)
            
            # RGB 변환
            if img1.mode != 'RGB':
                img1 = img1.convert('RGB')
            if img2.mode != 'RGB':
                img2 = img2.convert('RGB')
            
            # 원본 크기 표시
            st.write(f"**이미지1 크기**: {img1.size[0]} × {img1.size[1]}")
            st.write(f"**이미지2 크기**: {img2.size[0]} × {img2.size[1]}")
            
            # 크기 조정
            if resize_option == "더 작은 이미지에 맞춤":
                target_size = (min(img1.width, img2.width), min(img1.height, img2.height))
            elif resize_option == "더 큰 이미지에 맞춤":
                target_size = (max(img1.width, img2.width), max(img1.height, img2.height))
            else:
                target_size = custom_size
            
            img1_resized, img2_resized, final_size = resize_images_to_same_size(img1, img2, target_size)
            
            st.write(f"**최종 크기**: {final_size[0]} × {final_size[1]}")
            
            # 해상도 손실 정보
            resolution_loss1 = ((img1.width * img1.height) - (final_size[0] * final_size[1] / 2)) / (img1.width * img1.height) * 100
            resolution_loss2 = ((img2.width * img2.height) - (final_size[0] * final_size[1] / 2)) / (img2.width * img2.height) * 100
            
            if resolution_loss1 > 0:
                st.warning(f"⚠️ 이미지1 실질 해상도 손실: {resolution_loss1:.1f}%")
            if resolution_loss2 > 0:
                st.warning(f"⚠️ 이미지2 실질 해상도 손실: {resolution_loss2:.1f}%")
    
    # 원본 이미지 표시
    if uploaded_file1 and uploaded_file2:
        st.markdown("---")
        st.subheader("📷 원본 이미지")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🔴 첫 번째 이미지**")
            st.image(img1_resized, use_column_width=True)
        
        with col2:
            st.markdown("**🔵 두 번째 이미지**")
            st.image(img2_resized, use_column_width=True)
        
        # 믹싱 실행 버튼
        if st.button("🎨 이미지 믹싱 시작", type="primary"):
            with st.spinner("이미지를 믹싱하는 중..."):
                # 패턴 생성
                pattern = create_custom_pattern(
                    final_size[0], 
                    final_size[1], 
                    pattern_type, 
                    block_size
                )
                
                # 이미지 믹싱
                mixed_image = mix_images_with_pattern(img1_resized, img2_resized, pattern)
                
                # 결과 표시
                st.markdown("---")
                st.subheader("🎉 믹싱 결과")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.image(mixed_image, caption=f"믹싱된 이미지 ({final_size[0]}×{final_size[1]})", use_column_width=True)
                
                with col2:
                    st.markdown("### 📊 결과 정보")
                    st.write(f"**패턴**: {selected_pattern}")
                    st.write(f"**블록 크기**: {block_size}px")
                    st.write(f"**최종 크기**: {final_size[0]}×{final_size[1]}")
                    
                    # 픽셀 분포 계산
                    total_pixels = final_size[0] * final_size[1]
                    img1_pixels = np.sum(pattern)
                    img2_pixels = total_pixels - img1_pixels
                    
                    st.write(f"**이미지1 픽셀**: {img1_pixels:,}개 ({img1_pixels/total_pixels*100:.1f}%)")
                    st.write(f"**이미지2 픽셀**: {img2_pixels:,}개 ({img2_pixels/total_pixels*100:.1f}%)")
                
                # 다운로드 링크
                st.markdown("### 💾 다운로드")
                filename = f"mixed_image_{pattern_type}_block{block_size}.png"
                download_link = get_download_link(mixed_image, filename)
                st.markdown(download_link, unsafe_allow_html=True)
                
                # 추가 분석
                with st.expander("🔍 상세 분석"):
                    st.markdown("#### 패턴 분포")
                    
                    # 패턴 시각화 (작은 크기로)
                    if final_size[0] <= 50 and final_size[1] <= 50:
                        st.write("**픽셀별 패턴 맵** (🔴=이미지1, 🔵=이미지2)")
                        pattern_viz = np.zeros((final_size[1], final_size[0], 3), dtype=np.uint8)
                        pattern_viz[pattern] = [255, 100, 100]
                        pattern_viz[~pattern] = [100, 100, 255]
                        st.image(Image.fromarray(pattern_viz), use_column_width=False)
                    
                    st.markdown("#### 통계")
                    st.write(f"- 총 픽셀 수: {total_pixels:,}개")
                    st.write(f"- 각 이미지의 실질 해상도: 약 {total_pixels//2:,}픽셀")
                    st.write(f"- 블록당 픽셀 수: {block_size}×{block_size} = {block_size**2}개")
    
    # 사용법 및 팁
    with st.expander("ℹ️ 사용법 및 팁"):
        st.markdown("""
        ### 🎯 사용법
        1. **이미지 업로드**: 두 개의 이미지를 업로드하세요
        2. **패턴 선택**: 사이드바에서 믹싱 패턴 선택
        3. **블록 크기 조정**: 1픽셀부터 20픽셀까지 조정 가능
        4. **크기 맞춤**: 두 이미지 크기 조정 방법 선택
        5. **믹싱 실행**: "이미지 믹싱 시작" 버튼 클릭
        6. **결과 다운로드**: 완성된 이미지 다운로드
        
        ### 💡 활용 팁
        - **블록 크기 1**: 픽셀 단위로 정밀하게 섞기
        - **블록 크기 2-5**: 부드러운 패턴 효과
        - **블록 크기 10+**: 타일 형태의 큰 패턴
        - **체스판 패턴**: 가장 균등한 50:50 믹싱
        - **줄무늬 패턴**: 방향성 있는 믹싱
        
        ### ⚠️ 주의사항
        - 두 이미지는 같은 크기로 조정됩니다
        - 각 이미지의 실질 해상도는 약 50%로 감소합니다
        - 큰 이미지일수록 처리 시간이 오래 걸립니다
        - 블록 크기가 클수록 패턴이 명확해집니다
        """)
    
    # 푸터
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>🎨 Made with ❤️ for pixel art enthusiasts</p>
        <p>두 이미지를 창의적으로 조합해보세요!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
