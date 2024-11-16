# 필요한 라이브러리들을 가져옵니다
import streamlit as st  # 웹 인터페이스를 만들기 위한 라이브러리
from PIL import Image  # 이미지 처리를 위한 라이브러리 
import PyPDF2  # PDF 파일 처리를 위한 라이브러리
import io  # 입출력 처리를 위한 라이브러리

# 페이지 설정
st.set_page_config(page_title="파일 업로더", layout="wide")
st.title("📁 파일 업로더")

def load_file():
    # 사용자가 파일을 업로드할 수 있는 업로더를 생성합니다
    uploaded_file = st.file_uploader("파일을 업로드하세요", type=['pdf', 'png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:  # 파일이 업로드되면
        # 업로드된 파일의 확장자를 확인합니다
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        # PDF 파일인 경우의 처리
        if file_type == 'pdf':
            try:
                # PDF 파일을 읽어옵니다
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text_content = ""
                # PDF의 모든 페이지의 텍스트를 추출합니다
                for page in pdf_reader.pages:
                    text_content += page.extract_text()
                st.write("PDF 내용:")
                st.write(text_content)
                
                # PDF 내용을 저장하는 버튼을 만듭니다
                if st.button("PDF 내용 저장", key="save_pdf"):
                    st.session_state['saved_content'] = text_content
                    st.success("PDF 내용이 저장되었습니다!")
            except Exception as e:
                st.error(f"PDF 처리 중 오류가 발생했습니다: {str(e)}")
                    
        # 이미지 파일인 경우의 처리
        elif file_type in ['png', 'jpg', 'jpeg']:
            try:
                # 이미지를 열어서 화면에 표시합니다
                image = Image.open(uploaded_file)
                st.image(image, caption="업로드된 이미지")
                
                # 이미지를 저장하는 버튼을 만듭니다
                if st.button("이미지 저장", key="save_image"):
                    st.session_state['saved_image'] = image
                    st.success("이미지가 저장되었습니다!")
                    
            except Exception as e:
                st.error(f"이미지 처리 중 오류가 발생했습니다: {str(e)}")
                
    # 저장된 내용을 불러오는 버튼을 만듭니다
    if st.button("저장된 내용 불러오기", key="load_content"):
        # 저장된 PDF 내용이 있으면 보여줍니다
        if 'saved_content' in st.session_state:
            st.write("저장된 PDF 내용:")
            st.write(st.session_state['saved_content'])
        # 저장된 이미지가 있으면 보여줍니다
        if 'saved_image' in st.session_state:
            st.write("저장된 이미지:")
            st.image(st.session_state['saved_image'])
        # 저장된 내용이 없으면 경고 메시지를 표시합니다
        if 'saved_content' not in st.session_state and 'saved_image' not in st.session_state:
            st.warning("저장된 내용이 없습니다.")

# 위에서 정의한 함수를 실행합니다
if __name__ == "__main__":
    load_file()