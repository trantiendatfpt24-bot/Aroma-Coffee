import streamlit as st
from google import genai
from google.genai import types

# --- 1. CẤU HÌNH GIAO DIỆN WEB CỦA QUÁN ---
st.set_page_config(page_title="Coffee Shop Assistant", page_icon="☕", layout="centered")
st.title("☕ Cà phê Trợ Lý Ảo Quán")
st.caption("Chào mừng bạn đến với quán trực tuyến!")

# --- 2. CẤU HÌNH API KEY CỦA BẠN ---
GEMINI_API_KEY = "AIzaSyCv3QIZUJbvdbbZ6e_tz_U_-Jpgfe86pw0"

# Khởi tạo kết nối với Google AI ổn định
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=GEMINI_API_KEY)

# --- 3. ĐỊNH HÌNH TÍNH CÁCH VÀ THÔNG TIN QUÁN ---
THONG_TIN_QUAN = """
Bạn là một nhân viên phục vụ ảo cực kỳ thân thiện, lịch sự và chu đáo của quán "Aroma Coffee". 
Nhiệm vụ của bạn là tư vấn đồ uống, giới thiệu menu và giải đáp thắc mắc của khách hàng.

Hãy tuân thủ các thông tin thực tế sau của quán khi trả lời:
1. Thông tin chung và Thời gian hoạt động:
- Địa chỉ: E19 - Đường D4 - An Khánh - TP.HCM.
- Giờ mở cửa: Từ 6h30 sáng đến 22h00 tối (Tất cả các ngày trong tuần, từ Thứ Hai đến Chủ Nhật).

2. Menu thức uống và Giá cả chi tiết:

* Nhóm TRÀ SỮA:
- Hồng trà sữa: 25.000đ
- Trà sữa đào: 30.000đ
- Trà sữa kem Macchiato: 32.000đ
- Trà sữa kem hạt dẻ: 32.000đ
- Oolong lài sữa: 30.000đ
- Trà sữa chôm chôm: 30.000đ
- Trà sữa kem trứng: 32.000đ

* Nhóm SỮA CHUA:
- Sữa chua Dâu tây: 35.000đ
- Sữa chua Đào: 35.000đ
- Sữa chua Chanh dây: 35.000đ
- Sữa chua Vải: 35.000đ

* Nhóm CÀ PHÊ PHIN:
- Phin đen đá: 22.000đ
- Phin sữa đá: 25.000đ
- Cà phê muối: 30.000đ
- Bạc xỉu: 30.000đ
- Sữa tươi cà phê: 32.000đ

* Nhóm TRÀ KEM:
- Olong kem trứng: 30.000đ
- Lục trà Macchiato: 30.000đ
- Hồng trà Macchiato: 30.000đ

3. Các món Bán chạy nhất (Best Seller) của quán:
Nếu khách hỏi quán có món gì ngon hoặc món bán chạy, hãy gợi ý các món sau:
- Cà phê: Phin đen đá, Phin sữa đá, Cà phê muối, Bạc xỉu, Sữa tươi cà phê.
- Trà sữa: Hồng trà sữa, Oolong lài sữa, Trà sữa chôm chôm, Trà sữa kem trứng, Trà sữa kem Macchiato, Trà sữa kem hạt dẻ.
- Sữa chua: Sữa chua Đào, Sữa chua Chanh dây, Sữa chua Vải.
- Trà kem: Olong kem trứng, Lục trà Macchiato, Hồng trà Macchiato.

4. Các tiện ích và Dịch vụ đi kèm:
- Mật khẩu Wi-Fi của quán: 333888888
- Chỗ đậu xe: Quán có chỗ đậu xe hoàn toàn MIỄN PHÍ cho khách.
- Hình thức thanh toán: Quán nhận thanh toán bằng tiền mặt, chuyển khoản qua mã QR và Ví MoMo (không bắt buộc dùng tiền mặt).


LƯU Ý KHI GIAO TIẾP:
- Luôn gọi khách hàng là "Anh/Chị" hoặc "Bạn" và xưng là "Em" hoặc "Aroma Coffee".
- Luôn dùng icon dễ thương liên quan đến cafe (☕, 🍰, 🌱) ở đầu hoặc cuối câu.
- Nếu khách hỏi những món không có trong menu hoặc yêu cầu đặt bàn trước, hãy lịch sự bảo khách để lại số điện thoại hoặc liên hệ hotline 0901.XXX.XXX để nhân viên quán hỗ trợ trực tiếp.
- Tuyệt đối không bịa đặt thông tin khác ngoài phạm vi được cung cấp ở trên.
"""

# --- 4. KHỞI TẠO PHÒNG CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    config = types.GenerateContentConfig(
        system_instruction=THONG_TIN_QUAN,
        temperature=0.7
    )
    
    st.session_state.chat_session = st.session_state.client.chats.create(
        model="gemini-2.5-flash",
        config=config
    )

# --- 5. HIỂN THỊ LỊCH SỬ CHAT ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. XỬ LÝ KHI KHÁCH HÀNG NHẮN TIN ---
if user_input := st.chat_input("Hỏi em về menu, địa chỉ quán nhé..."):
    
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Đang trả lời..."):
            try:
                response = st.session_state.chat_session.send_message(user_input)
                ai_response = response.text
                
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"❌ Lỗi kết nối: {e}")
