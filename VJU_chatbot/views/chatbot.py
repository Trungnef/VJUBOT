import streamlit as st
import google.generativeai as genai

def main():
    # Thiết lập API key cho Gemini
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

    # Khởi tạo mô hình Gemini
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # Căn giữa tiêu đề ứng dụng Streamlit
    st.markdown("<h1 style='text-align: center;'>Trò chuyện với VJU-Bot</h1>", unsafe_allow_html=True)

    # Hàm để tạo cuộc trò chuyện mới
    def new_chat():
        st.session_state.messages = []
        
    # Lưu trữ lịch sử trò chuyện
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Hiển thị lịch sử trò chuyện
    chat_container = st.container()  # Tạo một container cho lịch sử trò chuyện
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Tạo một cột cho input và button cố định
    input_container = st.container()  # Tạo một container cho input và button
    with input_container:
        col1, col2 = st.columns([1, 18])  # Tạo hai cột cho input và button
        with col1:
            st.button("▢", on_click=new_chat)
        with col2:
            prompt = st.chat_input("What is up?")

    # Nhận input từ người dùng
    if prompt:
        # Lưu tin nhắn của người dùng vào lịch sử
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Hiển thị tin nhắn của người dùng
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gửi yêu cầu đến Gemini API
        response = model.generate_content(prompt)

        # Hiển thị phản hồi từ Gemini
        with st.chat_message("assistant"):
            st.markdown(response.text)

        # Lưu tin nhắn của Gemini vào lịch sử
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
if __name__ == "__main__":
    main()