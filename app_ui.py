import streamlit as st
import requests

# إعدادات الصفحة
st.set_page_config(page_title="Gobber AI", page_icon="🤖", layout="wide")

API_URL = "http://localhost:8000/api/v1"

st.title("🤖 Gobber - Multi-Agent AI System")
st.markdown("An intelligent AI that writes, executes, and fixes Python code automatically.")

# إدارة حالة الجلسة لتخزين الرسائل والتوكن
if "messages" not in st.session_state:
    st.session_state.messages = []
if "token" not in st.session_state:
    st.session_state.token = None

# الشريط الجانبي لتسجيل الدخول
with st.sidebar:
    st.header("Authentication")
    if st.session_state.token is None:
        username = st.text_input("Username", value="admin")
        password = st.text_input("Password", type="password", value="123")
        if st.button("Login"):
            response = requests.post(
                f"{API_URL}/auth/login",
                data={"username": username, "password": password}
            )
            if response.status_code == 200:
                st.session_state.token = response.json()["access_token"]
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    else:
        st.success("✅ Logged In")
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.messages = []
            st.rerun()

# عرض سجل الدردشة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # إظهار الكود فقط إذا كان موجوداً وليس فارغاً
        if message.get("code"): 
            with st.expander("View Generated Code"):
                st.code(message["code"], language="python")
        if message.get("retries") is not None:
            st.caption(f"Retries: {message['retries']} | Memory Used: {message['memory_used']}")

# إدخال رسالة جديدة
if prompt := st.chat_input("Ask Gobber to write some Python code..."):
    if not st.session_state.token:
        st.error("Please login first from the sidebar.")
    else:
        # إضافة رسالة المستخدم
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # إرسال الطلب إلى الـ API
        with st.chat_message("assistant"):
            with st.spinner("Gobber is thinking and executing code..."):
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                response = requests.post(
                    f"{API_URL}/agent/ask",
                    json={"query": prompt},
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    final_output = data.get("output", "No output")
                    route = data.get("detected_route", "qa")
                    
                    if route == "code":
                        # في حال كان طلب برمجة
                        st.markdown(f"**Output:**\n```text\n{final_output}\n```")
                        with st.expander("View Generated Code"):
                            st.code(data.get("code", ""), language="python")
                        st.caption(f"Retries: {data.get('retries')} | Memory Used: {data.get('memory_used')} | Valid: {data.get('is_valid')}")
                        
                        msg_content = f"**Output:**\n```text\n{final_output}\n```"
                    else:
                        # في حال كان سؤالاً عاماً
                        st.markdown(f"**Response:**\n{final_output}")
                        st.caption(f"Route: QA | Memory Used: {data.get('memory_used')}")
                        
                        msg_content = final_output

                    # حفظ رد المساعد في السجل
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": msg_content,
                        "code": data.get("code", "") if route == "code" else None,
                        "retries": data.get("retries") if route == "code" else None,
                        "memory_used": data.get("memory_used")
                    })
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")