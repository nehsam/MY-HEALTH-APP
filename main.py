import os, asyncio, streamlit as st
from dotenv import load_dotenv
import tempfile, re
from datetime import datetime
from fpdf import FPDF

# Load environment variables first
load_dotenv()

# Check API key before importing other modules
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.set_page_config(page_title="🤖 AI Health Assistant", page_icon="🤖")
    st.error("❌ **GROQ_API_KEY not found!**")
    st.info("📝 **How to fix this:**")
    st.code("""
1. Create a .env file in your project root directory
2. Add your GROQ API key like this:
   GROQ_API_KEY=your_actual_api_key_here
3. Get your API key from: https://console.groq.com/keys
    """)
    st.stop()

# Now import the streaming module
try:
    from utils.streaming import stream_agent_response
except ImportError as e:
    st.error(f"❌ Error importing streaming module: {e}")
    st.info("Make sure utils/streaming.py exists and is properly configured")
    st.stop()

# Strip emojis and non-latin1 characters for PDF
def _strip_nonlatin(text: str) -> str:
    return re.sub(r"[^\x20-\xFF]", "", text)

# Export PDF
def export_chat_to_pdf() -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=12)
    
    # Add header
    pdf.cell(0, 10, f"Health Chat History - {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.ln(10)

    for role, msg in st.session_state.chat:
        name = "User" if role == "user" else "AI Assistant"
        clean_line = _strip_nonlatin(f"{name}: {msg}")
        pdf.multi_cell(0, 10, clean_line)
        pdf.ln(5)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf.output(tmpfile.name, "F")
        return tmpfile.name

# Page setup
st.set_page_config(
    page_title="🤖 AI Health Assistant", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS styling for modern UI
st.markdown("""
<style>
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Main container */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    /* Chat container */
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 15px;
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
    }
    
    /* Chat bubbles */
    .chat-bubble {
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        border-radius: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        animation: slideIn 0.3s ease-out;
        position: relative;
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        margin-left: 20%;
        border-bottom-right-radius: 5px;
    }
    
    .assistant-bubble {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        margin-right: 20%;
        border-bottom-left-radius: 5px;
    }
    
    /* Role badges */
    .role-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 0.5rem;
        animation: pulse 2s infinite;
    }
    
    .status-online {
        background: #28a745;
    }
    
    /* Animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6);
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e9ecef;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Stats container */
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        backdrop-filter: blur(5px);
    }
    
    .stat-item {
        text-align: center;
        color: white;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        display: block;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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
    
    name_val = st.text_input("🏷️ Enter your name:", value=st.session_state.get("name", ""), placeholder="What should I call you?")
    st.session_state["name"] = name_val
    
    if st.session_state.get("chat"):
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
        if "chat" not in st.session_state:
            st.session_state.chat = []
        st.session_state.chat.append(("user", "Give me some quick health tips"))
        st.rerun()

# Main content area
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # Name required check
    if not st.session_state.name:
        st.markdown("""
        <div class="info-box">
            <h3>👋 Welcome to your AI Health Assistant!</h3>
            <p>Please enter your name in the sidebar to start chatting with your personal wellness companion.</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # Chat state setup
    if "chat" not in st.session_state:
        st.session_state.chat = []

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
    # Create input and send button in columns
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

    # On Send
    if send_button and user_msg:
        st.session_state.chat.append(("user", user_msg))
        
        # Show thinking indicator
        with st.spinner("🤔 AI is thinking..."):
            reply_ph = st.empty()
            
            try:
                async def get_reply():
                    return await stream_agent_response(user_msg, placeholder=reply_ph)
                
                assistant_text = asyncio.run(get_reply())
                st.session_state.chat.append(("assistant", assistant_text))
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state.chat.append(("assistant", "Sorry, I encountered an error. Please try again."))
        
        st.rerun()

    # PDF Download Option
    if st.session_state.chat:
        st.markdown("---")
        col_download1, col_download2, col_download3 = st.columns([2, 2, 2])
        
        with col_download2:
            try:
                pdf_path = export_chat_to_pdf()
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        "📄 Download Chat History",
                        data=file,
                        file_name=f"health_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Error creating PDF: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem;">
    <p>🤖 Powered by Advanced AI Technology | Built with ❤️ for Better Health</p>
</div>
""", unsafe_allow_html=True)