import os
import streamlit as st
from dotenv import load_dotenv
import tempfile
import re
from datetime import datetime
from fpdf import FPDF
import google.generativeai as genai
import time

# Load environment variables first
load_dotenv()

# Set page config first (must be first Streamlit command)
st.set_page_config(
    page_title="Personal Health AI", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
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
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "typing" not in st.session_state:
    st.session_state.typing = False

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
        pdf.cell(0, 10, f"Personal Health AI Session - {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
        pdf.ln(10)

        for role, msg in st.session_state.chat:
            name = "User" if role == "user" else "Health AI"
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

# Ultra-sophisticated CSS for premium AI interface
def get_css():
    if st.session_state.dark_mode:
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        .stApp {
            background: #0a0a0a;
            background-image: 
                radial-gradient(circle at 20% 20%, rgba(120, 119, 198, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255, 119, 198, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 60%, rgba(76, 29, 149, 0.1) 0%, transparent 50%);
            font-family: 'Space Grotesk', monospace;
            color: #e8e8e8;
            overflow-x: hidden;
        }
        
        .nexus-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 0 20px;
            position: relative;
        }
        
        .nexus-header {
            text-align: center;
            padding: 40px 0 60px 0;
            position: relative;
        }
        
        .nexus-logo {
            position: relative;
            display: inline-block;
            margin-bottom: 30px;
        }
        
        .logo-core {
            width: 120px;
            height: 120px;
            background: linear-gradient(135deg, #ff006b, #8b00ff, #00d4ff);
            border-radius: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
            font-weight: 700;
            color: white;
            position: relative;
            overflow: hidden;
            margin: 0 auto;
            transform-style: preserve-3d;
            animation: float 6s ease-in-out infinite;
        }
        
        .logo-core::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #ff006b, #8b00ff, #00d4ff, #ff006b);
            border-radius: 32px;
            z-index: -1;
            animation: rotate 4s linear infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotateX(0deg); }
            50% { transform: translateY(-20px) rotateX(5deg); }
        }
        
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .nexus-title {
            font-size: 4rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            background: linear-gradient(135deg, #ff006b, #8b00ff, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
            letter-spacing: -2px;
            text-transform: uppercase;
        }
        
        .nexus-subtitle {
            font-size: 1.1rem;
            color: #888;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        
        .status-bar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 15px 30px;
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .status-left {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        .neural-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: #00ff88;
        }
        
        .neural-dot {
            width: 6px;
            height: 6px;
            background: #00ff88;
            border-radius: 50%;
            animation: pulse-neural 1.5s infinite;
        }
        
        @keyframes pulse-neural {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.3; transform: scale(1.5); }
        }
        
        .user-badge {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 8px 16px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .theme-switch {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 8px 16px;
            color: #e8e8e8;
            cursor: pointer;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }
        
        .theme-switch:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }
        
        .chat-interface {
            background: rgba(0, 0, 0, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            margin: 80px 0 30px 0;
            overflow: hidden;
            backdrop-filter: blur(20px);
            position: relative;
        }
        
        .chat-header {
            background: rgba(255, 255, 255, 0.05);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .session-info {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: #888;
        }
        
        .chat-stats {
            display: flex;
            gap: 20px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
        }
        
        .stat {
            color: #00ff88;
        }
        
        .chat-messages {
            min-height: 400px;
            max-height: 600px;
            overflow-y: auto;
            padding: 30px;
        }
        
        .message {
            margin-bottom: 30px;
            animation: slideIn 0.6s ease-out;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user-message {
            display: flex;
            justify-content: flex-end;
        }
        
        .user-bubble {
            background: linear-gradient(135deg, #ff006b, #8b00ff);
            color: white;
            padding: 18px 24px;
            border-radius: 20px 20px 4px 20px;
            max-width: 70%;
            font-size: 0.95rem;
            line-height: 1.6;
            box-shadow: 0 8px 32px rgba(255, 0, 107, 0.3);
            position: relative;
        }
        
        .ai-message {
            display: flex;
            align-items: flex-start;
            gap: 16px;
        }
        
        .ai-avatar {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #00d4ff, #8b00ff);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            color: white;
            flex-shrink: 0;
            position: relative;
        }
        
        .ai-avatar::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #00d4ff, #8b00ff, #ff006b);
            border-radius: 14px;
            z-index: -1;
            animation: rotate 8s linear infinite;
        }
        
        .ai-bubble {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #e8e8e8;
            padding: 18px 24px;
            border-radius: 20px 20px 20px 4px;
            max-width: 70%;
            font-size: 0.95rem;
            line-height: 1.7;
            backdrop-filter: blur(10px);
            position: relative;
        }
        
        .ai-bubble::before {
            content: '';
            position: absolute;
            left: -1px;
            top: 0;
            bottom: 0;
            width: 3px;
            background: linear-gradient(180deg, #00d4ff, #8b00ff);
            border-radius: 0 2px 2px 0;
        }
        
        .welcome-screen {
            text-align: center;
            padding: 80px 40px;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        .welcome-screen::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 30% 30%, rgba(255, 0, 107, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 70% 70%, rgba(0, 212, 255, 0.1) 0%, transparent 50%);
            pointer-events: none;
        }
        
        .welcome-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #e8e8e8;
            margin-bottom: 20px;
            position: relative;
            z-index: 1;
        }
        
        .welcome-subtitle {
            font-size: 1rem;
            color: #999;
            margin-bottom: 40px;
            line-height: 1.6;
            position: relative;
            z-index: 1;
        }
        
        .capabilities {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 40px;
            position: relative;
            z-index: 1;
        }
        
        .capability {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
        }
        
        .capability:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
        }
        
        .capability-title {
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 0.9rem;
        }
        
        .typing-indicator {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-left: 56px;
            color: #666;
            font-style: italic;
            font-size: 0.9rem;
        }
        
        .neural-waves {
            display: flex;
            gap: 3px;
        }
        
        .wave {
            width: 3px;
            height: 12px;
            background: linear-gradient(180deg, #00d4ff, #8b00ff);
            border-radius: 2px;
            animation: wave 1.2s ease-in-out infinite;
        }
        
        .wave:nth-child(2) { animation-delay: 0.1s; }
        .wave:nth-child(3) { animation-delay: 0.2s; }
        .wave:nth-child(4) { animation-delay: 0.3s; }
        .wave:nth-child(5) { animation-delay: 0.4s; }
        
        @keyframes wave {
            0%, 40%, 100% { transform: scaleY(0.4); opacity: 0.5; }
            20% { transform: scaleY(1); opacity: 1; }
        }
        
        .input-zone {
            background: rgba(0, 0, 0, 0.7);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding: 25px 30px;
        }
        
        .input-container {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        
        .neural-input {
            flex: 1;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 18px 24px;
            color: #e8e8e8;
            font-size: 0.95rem;
            font-family: 'Space Grotesk', sans-serif;
            outline: none;
            transition: all 0.3s ease;
        }
        
        .neural-input:focus {
            border-color: #00d4ff;
            box-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
            background: rgba(255, 255, 255, 0.15);
        }
        
        .neural-input::placeholder {
            color: #666;
            font-style: italic;
        }
        
        .send-btn {
            background: linear-gradient(135deg, #ff006b, #8b00ff);
            border: none;
            border-radius: 12px;
            width: 55px;
            height: 55px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 22px;
            color: white;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .send-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s;
        }
        
        .send-btn:hover::before {
            left: 100%;
        }
        
        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(255, 0, 107, 0.4);
        }
        
        .action-panel {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin: 25px 0;
        }
        
        .action-btn {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 12px 20px;
            color: #e8e8e8;
            cursor: pointer;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }
        
        .action-btn:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(255, 255, 255, 0.1);
        }
        
        .name-prompt {
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 50px;
            text-align: center;
            margin: 40px 0;
            backdrop-filter: blur(20px);
        }
        
        .name-title {
            font-size: 2rem;
            font-weight: 700;
            color: #e8e8e8;
            margin-bottom: 20px;
        }
        
        .name-subtitle {
            color: #999;
            margin-bottom: 30px;
            font-size: 1rem;
        }
        
        .name-input {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            padding: 18px 24px;
            color: #e8e8e8;
            font-size: 1.1rem;
            width: 100%;
            max-width: 400px;
            margin: 0 auto 25px auto;
            text-align: center;
            outline: none;
            transition: all 0.3s ease;
        }
        
        .name-input:focus {
            border-color: #00d4ff;
            box-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
        }
        
        .name-input::placeholder {
            color: #666;
        }
        
        .connect-btn {
            background: linear-gradient(135deg, #ff006b, #8b00ff);
            border: none;
            border-radius: 15px;
            padding: 15px 40px;
            color: white;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .connect-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(255, 0, 107, 0.4);
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #ff006b, #8b00ff);
            border-radius: 3px;
        }
        
        @media (max-width: 768px) {
            .nexus-title {
                font-size: 2.5rem;
            }
            
            .capabilities {
                grid-template-columns: 1fr;
            }
            
            .status-bar {
                padding: 10px 20px;
            }
            
            .chat-messages {
                padding: 20px;
            }
        }
        </style>
        """
    else:
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        .stApp {
            background: #f8f9fa;
            background-image: 
                radial-gradient(circle at 20% 20%, rgba(120, 119, 198, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255, 119, 198, 0.06) 0%, transparent 50%);
            font-family: 'Space Grotesk', sans-serif;
            color: #2d3748;
            overflow-x: hidden;
        }
        
        .nexus-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 0 20px;
            position: relative;
        }
        
        .nexus-header {
            text-align: center;
            padding: 40px 0 60px 0;
            position: relative;
        }
        
        .nexus-logo {
            position: relative;
            display: inline-block;
            margin-bottom: 30px;
        }
        
        .logo-core {
            width: 120px;
            height: 120px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
            font-weight: 700;
            color: white;
            position: relative;
            overflow: hidden;
            margin: 0 auto;
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .nexus-title {
            font-size: 4rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
            letter-spacing: -2px;
            text-transform: uppercase;
        }
        
        .nexus-subtitle {
            font-size: 1.1rem;
            color: #718096;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        
        .status-bar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            padding: 15px 30px;
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .status-left {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        .neural-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: #38a169;
        }
        
        .neural-dot {
            width: 6px;
            height: 6px;
            background: #38a169;
            border-radius: 50%;
            animation: pulse-neural 1.5s infinite;
        }
        
        @keyframes pulse-neural {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.3; transform: scale(1.5); }
        }
        
        .user-badge {
            background: rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 20px;
            padding: 8px 16px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #4a5568;
        }
        
        .theme-switch {
            background: rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 20px;
            padding: 8px 16px;
            color: #4a5568;
            cursor: pointer;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }
        
        .theme-switch:hover {
            background: rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }
        
        .chat-interface {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 20px;
            margin: 80px 0 30px 0;
            overflow: hidden;
            backdrop-filter: blur(20px);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
            position: relative;
        }
        
        .chat-header {
            background: rgba(0, 0, 0, 0.03);
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .session-info {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: #718096;
        }
        
        .chat-stats {
            display: flex;
            gap: 20px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
        }
        
        .stat {
            color: #667eea;
        }
        
        .chat-messages {
            min-height: 400px;
            max-height: 600px;
            overflow-y: auto;
            padding: 30px;
        }
        
        .message {
            margin-bottom: 30px;
            animation: slideIn 0.6s ease-out;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user-message {
            display: flex;
            justify-content: flex-end;
        }
        
        .user-bubble {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 18px 24px;
            border-radius: 20px 20px 4px 20px;
            max-width: 70%;
            font-size: 0.95rem;
            line-height: 1.6;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
            position: relative;
        }
        
        .ai-message {
            display: flex;
            align-items: flex-start;
            gap: 16px;
        }
        
        .ai-avatar {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            color: white;
            flex-shrink: 0;
            position: relative;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .ai-bubble {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(0, 0, 0, 0.1);
            color: #2d3748;
            padding: 18px 24px;
            border-radius: 20px 20px 20px 4px;
            max-width: 70%;
            font-size: 0.95rem;
            line-height: 1.7;
            backdrop-filter: blur(10px);
            position: relative;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }
        
        .ai-bubble::before {
            content: '';
            position: absolute;
            left: -1px;
            top: 0;
            bottom: 0;
            width: 3px;
            background: linear-gradient(180deg, #667eea, #764ba2);
            border-radius: 0 2px 2px 0;
        }
        
        .welcome-screen {
            text-align: center;
            padding: 80px 40px;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 20px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        .welcome-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 20px;
            position: relative;
            z-index: 1;
        }
        
        .welcome-subtitle {
            font-size: 1rem;
            color: #718096;
            margin-bottom: 40px;
            line-height: 1.6;
            position: relative;
            z-index: 1;
        }
        
        .capabilities {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 40px;
            position: relative;
            z-index: 1;
        }
        
        .capability {
            background: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        }
        
        .capability:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.9);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }
        
        .capability-title {
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 0.9rem;
            color: #2d3748;
        }
        
        .typing-indicator {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-left: 56px;
            color: #718096;
            font-style: italic;
            font-size: 0.9rem;
        }
        
        .neural-waves {
            display: flex;
            gap: 3px;
        }
        
        .wave {
            width: 3px;
            height: 12px;
            background: linear-gradient(180deg, #667eea, #764ba2);
            border-radius: 2px;
            animation: wave 1.2s ease-in-out infinite;
        }
        
        .wave:nth-child(2) { animation-delay: 0.1s; }
        .wave:nth-child(3) { animation-delay: 0.2s; }
        .wave:nth-child(4) { animation-delay: 0.3s; }
        .wave:nth-child(5) { animation-delay: 0.4s; }
        
        @keyframes wave {
            0%, 40%, 100% { transform: scaleY(0.4); opacity: 0.5; }
            20% { transform: scaleY(1); opacity: 1; }
        }
        
        .input-zone {
            background: rgba(255, 255, 255, 0.9);
            border-top: 1px solid rgba(0, 0, 0, 0.1);
            padding: 25px 30px;
        }
        
        .input-container {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        
        .neural-input {
            flex: 1;
            background: rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 15px;
            padding: 18px 24px;
            color: #2d3748;
            font-size: 0.95rem;
            font-family: 'Space Grotesk', sans-serif;
            outline: none;
            transition: all 0.3s ease;
        }
        
        .neural-input:focus {
            border-color: #667eea;
            box-shadow: 0 0 30px rgba(102, 126, 234, 0.2);
            background: rgba(255, 255, 255, 0.9);
        }
        
        .neural-input::placeholder {
            color: #a0aec0;
            font-style: italic;
        }
        
        .send-btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border: none;
            border-radius: 12px;
            width: 55px;
            height: 55px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 22px;
            color: white;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        .action-panel {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin: 25px 0;
        }
        
        .action-btn {
            background: rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 12px;
            padding: 12px 20px;
            color: #4a5568;
            cursor: pointer;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }
        
        .action-btn:hover {
            background: rgba(0, 0, 0, 0.1);
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        }
        
        .name-prompt {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 20px;
            padding: 50px;
            text-align: center;
            margin: 40px 0;
            backdrop-filter: blur(20px);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
        }
        
        .name-title {
            font-size: 2rem;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 20px;
        }
        
        .name-subtitle {
            color: #718096;
            margin-bottom: 30px;
            font-size: 1rem;
        }
        
        .name-input {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(0, 0, 0, 0.2);
            border-radius: 15px;
            padding: 18px 24px;
            color: #2d3748;
            font-size: 1.1rem;
            width: 100%;
            max-width: 400px;
            margin: 0 auto 25px auto;
            text-align: center;
            outline: none;
            transition: all 0.3s ease;
        }
        
        .name-input:focus {
            border-color: #667eea;
            box-shadow: 0 0 30px rgba(102, 126, 234, 0.2);
        }
        
        .name-input::placeholder {
            color: #a0aec0;
        }
        
        .connect-btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border: none;
            border-radius: 15px;
            padding: 15px 40px;
            color: white;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .connect-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.1);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #667eea, #764ba2);
            border-radius: 3px;
        }
        
        @media (max-width: 768px) {
            .nexus-title {
                font-size: 2.5rem;
            }
            
            .capabilities {
                grid-template-columns: 1fr;
            }
            
            .status-bar {
                padding: 10px 20px;
            }
            
            .chat-messages {
                padding: 20px;
            }
        }
        </style>
        """

# Apply CSS
st.markdown(get_css(), unsafe_allow_html=True)

# Gemini API call function
def get_gemini_response(prompt: str) -> str:
    try:
        health_context = f"""
        You are an advanced personal AI health intelligence system. You're assisting {st.session_state.name or 'User'}.
        
        Core Parameters:
        - Provide advanced, evidence-based health intelligence
        - Maintain professional, authoritative tone
        - Always recommend professional medical consultation for serious concerns
        - Deliver precise, actionable health protocols
        - Use sophisticated, clinical language when appropriate
        - Keep responses focused and impactful
        
        Query: {prompt}
        """
        
        response = model.generate_content(health_context)
        return response.text
    except Exception as e:
        return "AI SYSTEM ERROR: Connection to health intelligence network interrupted. Attempting reconnection..."

# Status bar
st.markdown(f"""
<div class="status-bar">
    <div class="status-left">
        <div class="neural-indicator">
            <div class="neural-dot"></div>
            AI ACTIVE
        </div>
        {f'<div class="user-badge">{st.session_state.name}</div>' if st.session_state.name else ''}
    </div>
    <div class="theme-switch" onclick="toggleTheme()">
        {'NIGHT MODE' if st.session_state.dark_mode else 'DAY MODE'}
    </div>
</div>
""", unsafe_allow_html=True)

# Main container
st.markdown('<div class="nexus-container">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="nexus-header">
    <div class="nexus-logo">
        <div class="logo-core">⚡</div>
    </div>
    <h1 class="nexus-title">Health AI</h1>
    <p class="nexus-subtitle">Personal Medical Intelligence Assistant</p>
</div>
""", unsafe_allow_html=True)

# Name input screen if not set
if not st.session_state.name.strip():
    st.markdown("""
    <div class="name-prompt">
        <h2 class="name-title">AI INITIALIZATION</h2>
        <p class="name-subtitle">Enter your name to establish secure connection</p>
    </div>
    """, unsafe_allow_html=True)
    
    name_input = st.text_input("", placeholder="Your name...", key="name_input", label_visibility="collapsed")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("⚡ CONNECT", use_container_width=True, key="connect_btn"):
            if name_input.strip():
                st.session_state.name = name_input.strip()
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# Theme toggle
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button(f"{'🌙 NIGHT' if not st.session_state.dark_mode else '☀️ DAY'}", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Chat interface
st.markdown('<div class="chat-interface">', unsafe_allow_html=True)

# Chat header
st.markdown(f"""
<div class="chat-header">
    <div class="session-info">SESSION: ACTIVE</div>
    <div class="chat-stats">
        <span>MSG: <span class="stat">{len(st.session_state.chat)}</span></span>
        <span>QRY: <span class="stat">{len([msg for role, msg in st.session_state.chat if role == 'user'])}</span></span>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat messages area
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

if not st.session_state.chat:
    # Welcome screen
    st.markdown(f"""
    <div class="welcome-screen">
        <h2 class="welcome-title">AI CONNECTION ESTABLISHED</h2>
        <p class="welcome-subtitle">
            Welcome, {st.session_state.name}. I am your advanced personal health intelligence system.
            I provide evidence-based health analysis, wellness optimization protocols, and medical insights.
        </p>
        <div class="capabilities">
            <div class="capability">
                <div class="capability-title">🧬 HEALTH ANALYSIS</div>
                Advanced symptom evaluation and health risk assessment
            </div>
            <div class="capability">
                <div class="capability-title">⚕️ MEDICAL INSIGHTS</div>
                Evidence-based medical information and treatment protocols
            </div>
            <div class="capability">
                <div class="capability-title">💪 OPTIMIZATION</div>
                Personalized fitness and nutrition optimization strategies
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Render chat messages
    for role, msg in st.session_state.chat:
        if role == "user":
            st.markdown(f"""
            <div class="message">
                <div class="user-message">
                    <div class="user-bubble">{msg}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message">
                <div class="ai-message">
                    <div class="ai-avatar">⚡</div>
                    <div class="ai-bubble">{msg}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Typing indicator
    if st.session_state.typing:
        st.markdown("""
        <div class="typing-indicator">
            AI processing...
            <div class="neural-waves">
                <div class="wave"></div>
                <div class="wave"></div>
                <div class="wave"></div>
                <div class="wave"></div>
                <div class="wave"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input zone
st.markdown('<div class="input-zone">', unsafe_allow_html=True)
st.markdown('<div class="input-container">', unsafe_allow_html=True)

user_input = st.text_input(
    "",
    placeholder="Input health query or medical concern...",
    key="neural_input",
    label_visibility="collapsed"
)

col_input, col_send = st.columns([6, 1])
with col_send:
    send_clicked = st.button("⚡", help="Transmit", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Handle message sending
if send_clicked and user_input.strip():
    st.session_state.chat.append(("user", user_input.strip()))
    st.session_state.typing = True
    st.rerun()

# Process AI response
if st.session_state.chat and st.session_state.chat[-1][0] == "user":
    with st.spinner("🧠 AI PROCESSING..."):
        try:
            user_message = st.session_state.chat[-1][1]
            ai_response = get_gemini_response(user_message)
            
            if ai_response:
                st.session_state.chat.append(("assistant", ai_response))
                st.session_state.typing = False
                time.sleep(0.1)
                st.rerun()
                
        except Exception as e:
            st.session_state.chat.append(("assistant", "AI DIAGNOSTIC: System temporarily unavailable. Retrying connection..."))
            st.session_state.typing = False
            st.rerun()

# Action panel
if st.session_state.chat:
    st.markdown('<div class="action-panel">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 RESET", use_container_width=True):
            st.session_state.chat = []
            st.session_state.typing = False
            st.rerun()
    
    with col2:
        try:
            pdf_path = export_chat_to_pdf()
            if pdf_path:
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        "📄 EXPORT",
                        data=file,
                        file_name=f"nexus_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                try:
                    os.unlink(pdf_path)
                except:
                    pass
        except Exception as e:
            st.error(f"Export error: {e}")
    
    with col3:
        if st.button("🧬 ANALYZE", use_container_width=True):
            st.session_state.chat.append(("user", "Provide comprehensive health analysis based on our discussion"))
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)