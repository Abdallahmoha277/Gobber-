import streamlit as st
import requests

st.set_page_config(page_title="Gobber AI", page_icon="🤖", layout="wide")
API_URL = "http://localhost:8000/api/v1"

st.title("🤖 Gobber - Multi-Agent AI System")
st.markdown("An intelligent AI that writes, executes, and fixes Python code automatically.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "token" not in st.session_state:
    st.session_state.token = None

def fetch_history():
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{API_URL}/history/", headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def save_message_to_db(role, content):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    requests.post(f"{API_URL}/history/", json={"role": role, "content": content}, headers=headers)

# الشريط الجانبي
with st.sidebar:
    st.header("Authentication")
    if st.session_state.token is None:
        username = st.text_input("Username", value="admin")
        password = st.text_input("Password", type="password", value="123")
        if st.button("Login"):
            response = requests.post(f"{API_URL}/auth/login", data={"username": username, "password": password})
            if response.status_code == 200:
                st.session_state.token = response.json()["access_token"]
                st.session_state.messages = [] # مسح الرسائل القديمة في الذاكرة
                history_data = fetch_history() # جلب الرسائل من قاعدة البيانات
                for msg in history_data:
                    st.session_state.messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
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
        if st.button("Clear Chat"):
            st.session_state.messages = []
            # (اختياري: يمكنك إضافة مسار API لحذف الرسائل من قاعدة البيانات هنا)
            st.rerun()

# عرض سجل الدردشة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال رسالة جديدة
if prompt := st.chat_input("Ask Gobber..."):
    if not st.session_state.token:
        st.error("Please login first.")
    else:
        # 1. حفظ وإظهار رسالة المستخدم
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        save_message_to_db("user", prompt) # حفظ في قاعدة البيانات

        # 2. إرسال الطلب للذكاء الاصطناعي
        with st.chat_message("assistant"):
            with st.spinner("Gobber is thinking..."):
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                response = requests.post(f"{API_URL}/agent/ask", json={"query": prompt}, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    final_output = data.get("output", "No output")
                    
                    # تنسيق الرد
                    if data.get("detected_route") == "code":
                        display_content = f"**Output:**\n```text\n{final_output}\n```\n**Code:**\n```python\n{data.get('code', '')}\n```"
                    else:
                        display_content = final_output
                        
                    st.markdown(display_content)
                    
                    # 3. حفظ رد الذكاء الاصطناعي
                    st.session_state.messages.append({"role": "assistant", "content": display_content})
                    save_message_to_db("assistant", display_content)
                else:
                    st.error(f"Error: {response.text}")