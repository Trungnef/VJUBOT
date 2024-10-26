import streamlit as st
from transformers import pipeline

# Khởi tạo mô hình chatbot từ Hugging Face
@st.cache_resource  # Lưu trữ để không tải lại mô hình mỗi khi app chạy lại
def load_chatbot_model():
    return pipeline("text-generation", model="meta-llama/Llama-3.2-1B-Instruct")  # Chọn mô hình phù hợp trên Hugging Face

# Hàm xử lý nhập liệu và trả về phản hồi
def generate_response(chatbot, user_input):
    responses = chatbot(user_input, max_length=100, num_return_sequences=1)
    return responses[0]['generated_text']

# Hàm làm mới chat
def new_chat():
    st.session_state.messages = []  # Reset lại lịch sử trò chuyện

# Giao diện Streamlit
def main():
    st.title("Chatbot")
    st.write("Chatbot V2")

    # Khởi tạo mô hình chatbot
    chatbot = load_chatbot_model()

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
            st.button("▢", on_click=new_chat)  # Nút để làm mới cuộc trò chuyện
        with col2:
            prompt = st.chat_input("Nhập câu hỏi của bạn...")  # Input cho người dùng

    # Nhận input từ người dùng
    if prompt:
        # Lưu tin nhắn của người dùng vào lịch sử
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Hiển thị tin nhắn của người dùng
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gửi yêu cầu đến mô hình chatbot
        with st.spinner("Đang xử lý..."):
            response = generate_response(chatbot, prompt)

        # Hiển thị phản hồi từ mô hình
        with st.chat_message("assistant"):
            st.markdown(response)

        # Lưu phản hồi của chatbot vào lịch sử
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
