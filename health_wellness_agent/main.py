import os
import streamlit as st
from dotenv import load_dotenv
import tempfile
import re
from datetime import datetime
from fpdf import FPDF
import google.generativeai as genai

# Load environment variables first
load_dotenv()

# Set page config first (must be first Streamlit command)
st.set_page_config(
    page_title="🤖 AI Health Assistant", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check API key before importing other modules
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("❌ **GEMINI_API_KEY not found!**")
    st.info("📝 **How to fix this:**")
    st.code("""
1. Create a .env file in your project root directory
2. Add your Gemini API key like this:
   GEMINI_API_KEY=your_actual_api_key_here
3. Get your API key from: https://aistudio.google.com/app/apikey
    """)
    st.stop()

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Initialize session state
if "chat" not in st.session_state:
    st.session_state.chat = []
if "name" not in st.session_state:
    st.session_state.name = ""

# Strip emojis and non-latin1 characters for PDF
def _strip_nonlatin(text: str) -> str:
    """Remove non-latin1 characters for PDF compatibility"""
    return re.sub(r"[^\x20-\xFF]", "", text)

# Export PDF function
def export_chat_to_pdf() -> str:
    """Export chat history to PDF file"""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        
        # Add header
        pdf.cell(0, 10, f"Health Chat History - {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
        pdf.ln(10)

        for role, msg in st.session_state.chat:
            name = "User" if role == "user" else "AI Assistant"
            clean_line = _strip_nonlatin(f"{name}: {msg}")
            # Split long lines to avoid PDF issues
            lines = [clean_line[i:i+80] for i in range(0, len(clean_line), 80)]
            for line in lines:
                pdf.multi_cell(0, 10, line)
            pdf.ln(5)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            pdf.output(tmpfile.name, "F")
            return tmpfile.name
    except Exception as e:
        st.error(f"Error creating PDF: {e}")
        return None

# Advanced CSS styling for modern UI
st.markdown("""
<style>
    /* ... (your CSS unchanged) ... */
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🤖 AI Health Assistant</h1>
    <p class="header-subtitle">Your intelligent wellness companion powered by advanced AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 2rem 1rem; border-radius: 15px; margin-bottom: 1rem;">
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <h2 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem;">👤 User Profile</h2>
            <div style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 0.5rem; background: #28a745; animation: pulse 2s infinite;"></div>
            <span>Online</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    name_val = st.text_input("🏷️ Enter your name:", value=st.session_state.name, placeholder="What should I call you?")
    if name_val != st.session_state.name:
        st.session_state.name = name_val
    
    if st.session_state.chat:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-around; margin: 1rem 0; padding: 1rem; background: rgba(102, 126, 234, 0.1); border-radius: 15px;">
            <div style="text-align: center;">
                <span style="font-size: 2rem; font-weight: 700; display: block; color: #667eea;">{len(st.session_state.chat)}</span>
                <span style="font-size: 0.9rem; opacity: 0.8;">Messages</span>
            </div>
            <div style="text-align: center;">
                <span style="font-size: 2rem; font-weight: 700; display: block; color: #667eea;">1</span>
                <span style="font-size: 0.9rem; opacity: 0.8;">Session</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎯 Quick Actions")
    
    if st.button("🔄 Clear Chat"):
        st.session_state.chat = []
        st.rerun()
    
    if st.button("💡 Get Health Tips"):
        st.session_state.chat.append(("user", "Give me some quick health tips"))
        st.rerun()

# Main content area
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # Name required check
    if not st.session_state.name.strip():
        st.markdown("""
        <div class="info-box">
            <h3>👋 Welcome to your AI Health Assistant!</h3>
            <p>Please enter your name in the sidebar to start chatting with your personal wellness companion.</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # Welcome message for new users
    if not st.session_state.chat:
        st.markdown(f"""
        <div class="info-box">
            <h3>Hello {st.session_state.name}! 👋</h3>
            <p>I'm your AI Health Assistant, ready to help you with wellness advice, health tips, and personalized recommendations.</p>
            <p>How can I assist you today?</p>
        </div>
        """, unsafe_allow_html=True)

    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Render chat history
    def render_history():
        for role, msg in st.session_state.chat:
            if role == "user":
                st.markdown(f"""
                <div class="chat-bubble user-bubble">
                    <div class="role-badge">👤 You</div>
                    <div>{msg}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-bubble assistant-bubble">
                    <div class="role-badge">🤖 AI Assistant</div>
                    <div>{msg}</div>
                </div>
                """, unsafe_allow_html=True)

    render_history()
    st.markdown('</div>', unsafe_allow_html=True)

    # Input area
    input_col1, input_col2 = st.columns([8, 2])
    
    with input_col1:
        user_msg = st.text_input(
            "💬 Type your message here...", 
            key="user_input", 
            placeholder="Ask me anything about health and wellness...",
            label_visibility="collapsed"
        )
    
    with input_col2:
        send_button = st.button("🚀 Send", use_container_width=True)

    # Gemini API call function
    def get_gemini_response(prompt: str) -> str:
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Gemini API error: {e}"

   # ...existing code...
    # Handle message sending
    if (send_button and user_msg.strip()) or (user_msg.strip() and st.session_state.get("enter_pressed", False)):
        st.session_state.chat.append(("user", user_msg.strip()))
        
        # Show thinking indicator
        with st.spinner("🤔 AI is thinking..."):
            try:
                assistant_text = get_gemini_response(user_msg.strip())
                if assistant_text and not assistant_text.startswith("❌"):
                    st.session_state.chat.append(("assistant", assistant_text))
                else:
                    st.session_state.chat.append(("assistant", "Sorry, I encountered an error. Please try again."))
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state.chat.append(("assistant", "Sorry, I encountered an error. Please try again."))
        
        # Clear the input and rerun
        # st.session_state.user_input = ""   # <-- Remove this line!
        st.rerun()
# ...existing code...

    # PDF Download Option
    if st.session_state.chat:
        st.markdown("---")
        col_download1, col_download2, col_download3 = st.columns([2, 2, 2])
        
        with col_download2:
            try:
                pdf_path = export_chat_to_pdf()
                if pdf_path:
                    with open(pdf_path, "rb") as file:
                        st.download_button(
                            "📄 Download Chat History",
                            data=file,
                            file_name=f"health_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    # Clean up temporary file
                    try:
                        os.unlink(pdf_path)
                    except:
                        pass
            except Exception as e:
                st.error(f"Error creating PDF: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem;">
    <p>🤖 Powered by Advanced AI Technology | Built with ❤️ for Better Health</p>
</div>
""", unsafe_allow_html=True)