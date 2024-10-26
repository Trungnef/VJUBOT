import streamlit as st
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import jwt
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get admin credentials from environment variables
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")  # Secret key for JWT

# API URL
API_URL = "http://rag-server:8002"  # Adjust as needed

# --- Custom CSS ---
custom_css = """
    <style>
        .stButton>button {
            background-color: #e32636;
            color: white;
        }
        .stButton>button:hover {
            background-color: #bf1e2e;
        }
        .section-header {
            font-size: 24px;
            color: #e32636;
            margin-top: 20px;
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Function to create a JWT Token ---
def create_jwt_token(username):
    """Create a JWT token with a set expiration time."""
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# --- Function to verify JWT Token ---
def verify_jwt_token(token):
    """Verify the token and return the decoded data."""
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        st.error("Token đã hết hạn, vui lòng đăng nhập lại.")
        return None
    except jwt.InvalidTokenError:
        st.error("Token không hợp lệ.")
        return None

# --- Login Function ---
def login():
    """Handle the login process and generate a token."""
    with st.sidebar:
        st.header("🔐 Đăng nhập")
        username = st.text_input("Tên đăng nhập", key="username")
        password = st.text_input("Mật khẩu", type="password", key="password")
        if st.button("Đăng nhập"):
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                # Tạo JWT token sau khi đăng nhập thành công
                token = create_jwt_token(username)
                st.session_state["token"] = token  # Lưu token vào session_state
                st.session_state["logged_in"] = True
                st.success("Đăng nhập thành công!")
            else:
                st.error("Sai tên đăng nhập hoặc mật khẩu.")

# --- Logout Function ---
def logout():
    """Clear the session state to log out the user."""
    st.session_state["logged_in"] = False
    st.session_state["token"] = None
    st.success("Đã đăng xuất thành công!")

# --- Function to upload a file ---
def upload_file(file):
    """Upload a file with JWT token authentication."""
    if "token" in st.session_state:
        token = st.session_state["token"]
        headers = {
            "Authorization": f"Bearer {token}"
        }
        m = MultipartEncoder(
            fields={"file": (file.name, file, "application/pdf")}
        )
        headers["Content-Type"] = m.content_type

        response = requests.post(f"{API_URL}/upload", data=m, headers=headers)
        if response.status_code == 200:
            st.success("Tải lên file thành công!")
        else:
            st.error(f"Tải lên thất bại: {response.text}")
    else:
        st.error("Bạn cần đăng nhập để tải lên file.")

# --- Function to get list of files ---
def get_files():
    """Retrieve the list of files with JWT token authentication."""
    if "token" in st.session_state:
        token = st.session_state["token"]
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(f"{API_URL}/files", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Không thể lấy danh sách file: {response.text}")
            return []
    else:
        st.error("Bạn cần đăng nhập để lấy danh sách file.")
        return []

# --- Function to delete a file ---
def delete_file(filename):
    """Delete a file with JWT token authentication."""
    if "token" in st.session_state:
        token = st.session_state["token"]
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.delete(f"{API_URL}/delete/{filename}", headers=headers)
        if response.status_code == 200:
            st.success("Xóa file thành công!")
        else:
            st.error(f"Xóa thất bại: {response.text}")
    else:
        st.error("Bạn cần đăng nhập để xóa file.")

# --- Main Function ---
def main():
    # Initialize session state for login
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    st.title("📂 Quản lý File")

    if not st.session_state.logged_in:
        login()
    else:
        # Verify the token on each request to ensure it's valid
        token = st.session_state.get("token", None)
        if token:
            decoded_token = verify_jwt_token(token)
            if not decoded_token:
                logout()

        # Sidebar for logout
        with st.sidebar:
            st.button("🚪 Đăng xuất", on_click=logout)

        # --- Upload Section ---
        st.markdown('<div class="section-header">Tải lên File</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Chọn file PDF để tải lên", type=["pdf"])
        if uploaded_file:
            upload_file(uploaded_file)

        # --- File List Section ---
        st.markdown('<div class="section-header">Danh sách File</div>', unsafe_allow_html=True)
        files = get_files()
        if files:
            for file in files:
                col1, col2 = st.columns([4, 1])
                col1.write(file)
                with col2:
                    st.button("🗑️ Xóa", key=file, on_click=delete_file, args=(file,))
        else:
            st.info("Không tìm thấy file nào.")

if __name__ == "__main__":
    main()
