

# # Địa chỉ local API của Rasa và RAG
# RASA_API_URL = "http://127.0.0.1:5005/webhooks/rest/webhook"
# RAG_API_URL = "http://127.0.0.1:5000/generative_ai"

# # Địa chỉ API của Rasa và RAG
RASA_API_URL = "http://rasa-server:5005/webhooks/rest/webhook"
RAG_API_URL = "http://rag-server:8002/generative_ai"


import streamlit as st
import requests

# URLs cho API Rasa và RAG
# RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"  # Thay đổi port nếu cần
# RAG_API_URL = "http://localhost:5000/generative_ai"  # Thay đổi port nếu cần

# Câu hỏi nổi bật và câu hỏi khác
HIGHLIGHTED_QUESTIONS = [
    "Tôi muốn đăng ký khóa học",
    "Làm sao để liên lạc VJU?"
]

OTHER_FAQ_QUESTIONS = [
    "VJU?",
    "Tuyển sinh VJU?",
    "Văn phòng tuyển sinh mở cửa vào giờ nào?",
    "Trường Đại học Việt Nhật nằm ở đâu?",
    "Giờ mở cửa của thư viện là khi nào?",
    "Giờ mở cửa của văn phòng tuyển sinh là khi nào?",
]

# --- Hàm gửi yêu cầu đến API RAG ---
def get_rag_response(question):
    data = {"question": question}
    try:
        response = requests.post(RAG_API_URL, json=data)
        response.raise_for_status()
        return response.json()['answer']
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi khi kết nối đến RAG API: {e}")
        return None

# --- Hàm gửi yêu cầu đến API Rasa ---
def get_rasa_response(user_input):
    data = {"sender": "user", "message": user_input}
    try:
        response = requests.post(RASA_API_URL, json=data)
        response.raise_for_status()
        response_json = response.json()
        
        # Kiểm tra intent của phản hồi để xác định câu hỏi ngoài phạm vi
        if response_json and isinstance(response_json, list):
            # Chỉ kiểm tra intent nếu có
            intent = response_json[0].get('intent', {}).get('name', '')
            if intent == 'outofscope':
                return None
            # Trả về câu trả lời văn bản nếu intent không phải out_of_scope
            return response_json[0].get('text')
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi khi kết nối đến Rasa API: {e}")
        return None

# --- Hàm hiển thị lịch sử chat ---
def display_chat_history(messages):
    for message in messages:
        with st.chat_message(message["role"]):
            content = message["content"]
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and "text" in item:
                        # Chuyển đổi \n thành <br> trước khi hiển thị bằng st.markdown
                        text_with_breaks = item["text"].replace("\n", "<br>")
                        st.markdown(text_with_breaks, unsafe_allow_html=True)
                        # ... (code xử lý buttons vẫn giữ nguyên)
                    elif isinstance(item, str):
                        # Chuyển đổi \n thành <br> trước khi hiển thị bằng st.markdown
                        text_with_breaks = item.replace("\n", "<br>")
                        st.markdown(text_with_breaks, unsafe_allow_html=True)
            elif isinstance(content, str):
                 # Chuyển đổi \n thành <br> trước khi hiển thị bằng st.markdown
                text_with_breaks = content.replace("\n", "<br>")
                st.markdown(text_with_breaks, unsafe_allow_html=True)
                
                
# --- Hàm xử lý câu hỏi từ người dùng ---
def handle_user_input(user_input):
    # Gọi Rasa để nhận câu trả lời
    rasa_response = get_rasa_response(user_input)
    
    if rasa_response:
        st.session_state.messages.append({"role": "assistant", "content": rasa_response})
    else:
        # Nếu Rasa không trả lời được, gọi RAG
        rag_response = get_rag_response(user_input)
        if rag_response:
            st.session_state.messages.append({"role": "assistant", "content": rag_response})
        else:
            st.session_state.messages.append({"role": "assistant", "content": "Xin lỗi, tôi không thể trả lời câu hỏi này."})


# --- Hàm main ---
def main():
    """Hàm main của ứng dụng Streamlit."""
    st.markdown("<h1 style='text-align: center;'>Hỏi đáp FAQ</h1>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    with st.sidebar:
        if st.button("▢"):
            st.session_state.messages = []

    # Hiển thị hai câu hỏi nổi bật trong hai cột
    st.markdown("<h3 style='text-align: left;'>Câu hỏi nổi bật</h3>", unsafe_allow_html=True)
    highlighted_cols = st.columns(2)
    for i, question in enumerate(HIGHLIGHTED_QUESTIONS):
        with highlighted_cols[i % 2]:  # Hiển thị từng câu hỏi nổi bật vào cột
            if st.button(question):
                st.session_state.messages.append({"role": "user", "content": question})
                handle_user_input(question)  # Sử dụng question thay vì prompt
                
    # Hiển thị các câu hỏi khác trong 2 cột
    st.markdown("<h3 style='text-align: left;'>Các câu hỏi phổ biến khác</h3>", unsafe_allow_html=True)
    other_faq_cols = st.columns(2)  # Chia thành 2 cột để hiển thị cân đối
    for i, question in enumerate(OTHER_FAQ_QUESTIONS):
        with other_faq_cols[i % 2]:  # Để hiển thị lần lượt vào từng cột
            if st.button(question):
                st.session_state.messages.append({"role": "user", "content": question})
                handle_user_input(question)  # Sử dụng question thay vì prompt
                
    # Cho phép người dùng nhập câu hỏi tùy chỉnh
    if prompt := st.chat_input("Nhập câu hỏi của bạn"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Gửi câu hỏi tùy chỉnh đến Rasa
        with st.chat_message("assistant"):
            with st.spinner("Đang tìm nè! bạn đợi chút nhen..."):
                handle_user_input(prompt)

    display_chat_history(st.session_state.messages)

if __name__ == "__main__":
    main()