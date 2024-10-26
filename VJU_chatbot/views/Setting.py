# VJU_chatbot/views/Setting.py
import streamlit as st
import requests
import os
import json


def main():
        
    st.title("Cài đặt")

    # --- Hàm hỗ trợ ---
    def check_api_connection(api_url):
        try:
            requests.get(api_url)
            return True
        except requests.exceptions.RequestException:
            return False

    # --- Đường dẫn đến file settings.json ---
    SETTINGS_FILE = "settings.json"

    # --- Đọc cài đặt từ file ---
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {
            #Local test
            # "rasa_api_url": "http://127.0.0.1:5005/webhooks/rest/webhook",
            # "rag_api_url": "http://127.0.0.1:5000/generative_ai",
            "rasa_api_url": "http://rasa-server:5005/webhooks/rest/webhook",
            "rag_api_url": "http://rag-server:8002/generative_ai"
        }

    # --- 1. Cấu hình kết nối Rasa và RAG ---
    st.header("Kết nối API")

    rasa_api_url = st.text_input("RASA API URL", value=settings.get("rasa_api_url"))
    rag_api_url = st.text_input("RAG API URL", value=settings.get("rag_api_url"))

    if st.button("Kiểm tra kết nối"):
        if check_api_connection(rasa_api_url):
            st.success("Kết nối Rasa thành công!")
        else:
            st.error("Lỗi kết nối Rasa!")

        if check_api_connection(rag_api_url):
            st.success("Kết nối RAG thành công!")
        else:
            st.error("Lỗi kết nối RAG!")

# --- Chạy ứng dụng nếu file được chạy trực tiếp ---
if __name__ == "__main__":
    main()