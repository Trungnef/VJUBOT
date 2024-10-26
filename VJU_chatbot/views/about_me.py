import streamlit as st
from forms.contact import contact_form

def main():
    @st.dialog("Liên Hệ")
    def show_contact_form():
        contact_form()

    # Inject custom CSS for the background and content layout
    st.markdown(
        """
        <style>
        .body {
            background: linear-gradient(136deg, black, black, red, black);
            color: white;
            min-height: 100vh; /* Ensure the page takes full height of the viewport */
            padding-bottom: 150px; /* Prevent the footer from overlapping the content */
        }

        .footer {
            padding: 20px;
            border-top: 1px solid white;
            background-color: rgba(0, 0, 0, 0.8); /* Slightly transparent background for better readability */
        }

        .footer-icon {
            margin: 0 10px;
            color: white;
            text-decoration: none;
        }

        .footer-section1 {
            flex: 1;
            text-align: left;
        }
        
        .footer-section2 {
            flex: 1;
            text-align: center;
        }

        .social-section {
            text-align: center;
            padding: 10px;
        }
        
        .footer-address {
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- HERO SECTION ---
    col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
    with col1:
        st.image("./assets/logo.png", width=300)

    with col2:
        st.title("VJU Bot - Trường Đại Học Việt Nhật", anchor=False)
        st.write("Chào mừng bạn đến với VJU Bot! 🌟")
        st.write("VJU Bot là trợ lý ảo thông minh, được thiết kế để hỗ trợ sinh viên và phụ huynh trong việc tìm kiếm thông tin về chương trình học, quy trình tuyển sinh và các dịch vụ tại trường.")
        if st.button("✉️ Liên Hệ"):
            show_contact_form()

    # --- GIỚI THIỆU VJU BOT ---
    st.write("\n")
    st.subheader("Giới thiệu về VJU Bot", anchor=False)
    st.write(""" 
        VJU Bot không chỉ là một công cụ tự động hóa mà còn là một giải pháp hỗ trợ toàn diện nhằm nâng cao trải nghiệm học tập tại Trường Đại Học Việt Nhật. Với công nghệ trí tuệ nhân tạo tiên tiến, bot có khả năng:
        - **Cung cấp thông tin chính xác và nhanh chóng**: Tìm kiếm thông tin về các khóa học, giảng viên, và lịch học một cách dễ dàng.
        - **Hướng dẫn quy trình tuyển sinh**: Đảm bảo bạn hiểu rõ các bước cần thiết để đăng ký nhập học.
        - **Giải đáp thắc mắc**: Cung cấp phản hồi ngay lập tức cho các câu hỏi thường gặp liên quan đến học phí, học bổng, và các dịch vụ hỗ trợ sinh viên.
        - **Tích hợp với hệ thống trường học**: Đảm bảo thông tin luôn được cập nhật và chính xác.
    """)

    # --- LỢI ÍCH CỦA VJU BOT ---
    st.write("\n")
    st.subheader("Lợi ích của VJU Bot", anchor=False)
    st.write(""" 
        VJU Bot mang lại nhiều lợi ích cho sinh viên và phụ huynh, bao gồm:
        - **Tiết kiệm thời gian**: Truy cập thông tin nhanh chóng mà không cần phải liên hệ trực tiếp với phòng ban.
        - **Tăng cường sự hài lòng**: Với khả năng cung cấp thông tin 24/7, bạn có thể nhận hỗ trợ bất cứ lúc nào.
        - **Cải thiện quy trình giao tiếp**: Giảm tải cho nhân viên trường, cho phép họ tập trung vào nhiệm vụ quan trọng hơn.
        - **Khuyến khích sự tham gia**: Cập nhật thông tin về các hoạt động ngoại khóa và sự kiện của trường.
    """)

    # --- TẦM NHÌN VÀ SỨ MỆNH ---
    st.write("\n")
    st.subheader("Tầm nhìn và Sứ mệnh", anchor=False)
    st.write(""" 
        VJU Bot được phát triển với tầm nhìn trở thành một trợ lý ảo hàng đầu trong lĩnh vực giáo dục, phục vụ sinh viên của Trường Đại Học Việt Nhật và cộng đồng học thuật toàn cầu. Sứ mệnh của chúng tôi là:
        - **Cung cấp thông tin và hỗ trợ kịp thời**: Giúp sinh viên đạt được thành công trong học tập và phát triển bản thân.
        - **Thúc đẩy trải nghiệm học tập**: Nâng cao sự tương tác giữa sinh viên và trường thông qua công nghệ hiện đại.
    """)


    # --- THÔNG TIN LIÊN HỆ ---
    st.write("\n")
    st.subheader("Support", anchor=False)
    st.write(
        """
        Nếu bạn có bất kỳ câu hỏi nào hoặc cần hỗ trợ thêm, đừng ngần ngại liên hệ với chúng tôi qua VJU Bot hoặc gửi email đến [cauchubebong184@gmail.com](mailto:cauchubebong184@gmail.com).
        """  
    )

    # --- KẾT LUẬN ---
    st.write("\n")
    st.markdown(
        """
        **Cảm ơn bạn đã ghé thăm VJU Bot! Chúng tôi rất vui khi được hỗ trợ bạn trong hành trình học tập tại Trường Đại Học Việt Nhật.** 🎓
        """
    )


    # --- FOOTER SECTION ---
    st.markdown(
        """
        <div class="footer">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div class="footer-section" style="flex: 1; margin-right: 20px;">
                    <h4>Liên hệ</h4>
                    <div>
                        <p><strong>TUYỂN SINH:</strong><br>(+84) 24 7306 6001</p>
                        <p><strong>THÔNG TIN CHUNG:</strong><br>(+84) 24 7306 6001</p>
                        <p><strong>HOTLINE:</strong><br>(+84) 966 954 736<br>(+84) 969 638 426</p>
                        <p><strong>EMAIL:</strong><br><a href="mailto:admission@vju.ac.vn">admission@vju.ac.vn</a><br><a href="mailto:info@vju.ac.vn">info@vju.ac.vn</a></p>
                    </div>
                </div>
                <div class="footer-section" style="flex: 1; margin-right: 20px;">
                    <div>
                        <br>
                        <br>
                        <p><strong>TECHNICAL:</strong><br><a href="mailto:cauchubebong184@gmail.com">cauchubebong184@gmail.com</a></p>
                        <p><strong>PHONE TECH:</strong><br>(+84) 373 104 304</p>
                        <p> Hãy connect với tui! 🫡 </p>
                    </div>
                </div>
                <div class="footer-section" style="flex: 1;">
                    <div class="footer-address">
                        <br>
                        <p><strong>Cơ sở Mỹ Đình:</strong><br>
                            Trường Đại Học Việt Nhật,<br>
                            đường Lưu Hữu Phước, Cầu Diễn,<br>
                            Nam Từ Liêm, Hà Nội.
                        </p>
                        <p><strong>Địa chỉ Hòa Lạc:</strong><br>
                            Trường Đại Học Việt Nhật,<br>
                            Khu công nghệ cao Hòa Lạc,<br>
                            Thạch Thất, Hà Nội, Việt Nam.
                        </p>
                    </div>
                </div>
            </div>
            <div class="social-section" style="margin-top: 20px;">
                <p><strong>Theo dõi chúng tôi</strong></p>
                <a href="https://www.facebook.com" target="_blank" class="footer-icon">Facebook</a>
                <a href="https://www.youtube.com" target="_blank" class="footer-icon">YouTube</a>
                <a href="https://www.linkedin.com" target="_blank" class="footer-icon">LinkedIn</a>
            </div>
            <div style="text-align: center; margin-top: 10px;">
                <p>
                    <a href="https://vju.ac.vn" target="_blank" style="color:white;">Website chính thức</a> |
                    <a href="/privacy-policy" target="_blank" style="color:white;">Chính sách bảo mật</a> |
                    <a href="/terms-of-service" target="_blank" style="color:white;">Điều khoản dịch vụ</a>
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- COPYRIGHT SECTION ---
    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
            <p>© 2024 VJU Bot | Trường Đại Học Việt Nhật</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()