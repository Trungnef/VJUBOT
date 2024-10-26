import streamlit as st
from views import about_me, Admin, chatbot, chatbot1, FAQ, Setting
import logging


# Display logo at the top of the sidebar
st.sidebar.image("assets/bot_logo.png", width=80)  # Adjust width as needed

# Hide main menu, footer, and header
hide_st_style = """
                <style>
                MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- Custom Sidebar Styles ---
sidebar_style = """
    <style>
        /* Sidebar background and text styling */
        .css-1544g2n { 
            background-color: #1a1a1a;  /* Black background */
            color: #f5f5f5;  /* Light gray text */
        }

        /* Sidebar Title styling */
        .css-1cpxqw2 h1 { 
            color: #e32636;  /* Dark red for the title */
            font-family: 'Arial', sans-serif;
            font-size: 22px;
            margin-bottom: 20px;
        }

        /* Sidebar text and selectbox styling */
        .css-vfqx5j, .css-1cpxqw2 { 
            color: #f5f5f5;  /* Light text */
            font-family: 'Roboto', sans-serif;
            font-size: 18px;
        }

        /* Navigation menu styling */
        .css-1cpxqw2 .stSelectbox [data-baseweb="select"] {
            background-color: #333;  /* Dark background */
            color: #e32636;  /* Red text */
            border: 1px solid #555;  /* Subtle border */
        }
        
        /* Hover effect for the selectbox */
        .css-1cpxqw2 .stSelectbox [data-baseweb="select"]:hover {
            border-color: #e32636;  /* Red border on hover */
        }

        /* Sidebar divider styling */
        .sidebar-divider {
            margin: 20px 0;
            border-top: 1px solid #444;
        }

        /* Footer text styling */
        .css-1cpxqw2 .stText {
            color: #e32636;  /* Red text */
            font-size: 12px;
            margin-top: 30px;
        }

        /* External link styling */
        .css-1cpxqw2 .stLink {
            color: #e32636;  /* Red text */
            font-size: 14px;
            text-decoration: none;
        }

        .css-1cpxqw2 .stLink:hover {
            text-decoration: underline;
        }
    </style>
"""
st.markdown(sidebar_style, unsafe_allow_html=True)

# Configure logging
logging.basicConfig(level=logging.INFO)

# --- Sidebar Content ---
st.sidebar.title("😶‍🌫️")

# Add a short bio to the sidebar with an icon
st.sidebar.markdown("👤 **About Me**")
st.sidebar.info("""
Hi, I'm Trune! I'm passionate about AI and chatbots. 
Navigate through the sections to explore more or chat with me.
""")

# Navigation with enhanced icons
page = st.sidebar.selectbox(
    "📋 **Menu**",
    [
     "🏠 About Me", "🔐 Admin", "🤖 Chat Bot", "🤖 Chat Bot v2", "📚 FAQ", "⚙️ Settings"]
)

# Add a section with contact icons or social media
st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
st.sidebar.markdown("🌐 **Find me on**")
st.sidebar.markdown("""
- [![GitHub](https://img.icons8.com/material-outlined/24/ffffff/github.png) GitHub](https://github.com/trungnef)  
- [![LinkedIn](https://img.icons8.com/material-outlined/24/ffffff/linkedin.png) LinkedIn](https://linkedin.com/in/yourprofile)  
- [![Twitter](https://img.icons8.com/material-outlined/24/ffffff/twitter.png) Twitter](https://twitter.com/yourprofile)
""", unsafe_allow_html=True)

# Add useful external resources or project links with icons
st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
st.sidebar.markdown("📂 **Resources**")
st.sidebar.markdown("""
- [![Docs](https://img.icons8.com/material-outlined/24/ffffff/document.png) Project Docs](https://github.com/trungnef/VJUBOT)  
- [![AI](https://img.icons8.com/material-outlined/24/ffffff/brain.png) AI Tools](https://aitools.com)  
- [![API](https://img.icons8.com/material-outlined/24/ffffff/api.png) API References](https://aistudio.google.com/app/apikey)
""", unsafe_allow_html=True)

# Footer message
st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
st.sidebar.text("Made with ❤️ by Trune")

# --- Page Loading Logic ---
try:
    if page == "🏠 About Me":
        about_me.main()
    elif page == "🔐 Admin":
        Admin.main()
    elif page == "🤖 Chat Bot":
        chatbot.main()
    elif page == "🤖 Chat Bot v2":
        chatbot1.main()
    elif page == "📚 FAQ":
        FAQ.main()
    elif page == "⚙️ Settings":
        Setting.main()
except Exception as e:
    logging.error(f"Error loading page: {page}. Error: {e}")
    st.error("An error occurred while trying to load the selected page.")
