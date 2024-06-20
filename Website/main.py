import streamlit as st
from time import sleep
import google.generativeai as genai
from streamlit_chat import message
from streamlit.components.v1 import html

# Configure the API key for Gemini

genai.configure(api_key='Your_API_Key')

# Define function to upload file to Gemini
def upload_to_gemini(path, mime_type=None):
    file = genai.upload_file(path, mime_type=mime_type)
    return file

# Define function to wait for files to be active
def wait_for_files_active(files):
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")

# Create the generative model
generation_config = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Define file paths
file_paths = [
    "interview_guide.txt",
]

# Upload files to Gemini
files = [
    upload_to_gemini(path, mime_type="text/plain" if path.endswith(".txt") else "application/octet-stream") 
    for path in file_paths
]

# Wait for files to be processed
wait_for_files_active(files)

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Start a chat session if not already started
if 'chat_session' not in st.session_state:
    # Start a chat session
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    files[0],
                    "I want you to act like an interviewer for Social Sciences. Keep your language simple and friendly. Pose one question at a time, allowing ample space for the interviewee to respond. Approach each question with a warm and inviting demeanor. Feel free to adapt your questions based on the interviewee's responses. You can find the topics and examples for the interview attached. Use Interview Guide file for more information.\nStart with Healthy Homes then Asthma Action Plan and finally Questions on Culturally Sensitive Education to Improve Self-management Skills. IF the interviewee is unaware about any of them make them aware about the program then followup. Stop at the time when we have all the survey information that we are looking for.",
                ],
            },
        ]
    )
    st.session_state.chat_session = chat_session

# Function to add user message to chat
def add_user_message(msg):
    st.session_state.chat_history.append({"role": "user", "parts": [msg]})
    response = st.session_state.chat_session.send_message(msg)
    st.session_state.chat_history.append({"role": "model", "parts": [response.text]})
    st.session_state.prompt = ''

# User input section
st.set_page_config(page_title="DC Healthy Homes Survey ChatBot", page_icon="🤖", layout="wide")

html(f"""
<script>
    function scroll(index){{
        setTimeout(() => {{
            const container = parent.document.querySelector('.block-container');
            if (!container) return false;
            container.scrollTop = container.scrollHeight;
            if (index > -1) {{
                scroll(-1);
            }}
        }}, "3000");
    }}
    scroll({st.session_state.get('message_count', 0)});
</script>
""")

intro_text = '''Thank you for participating in our survey. Your input is invaluable to our research at Howard University, School of Social Work, where we are investigating the impact and effectiveness of the DC Healthy Homes Program. This program aims to improve the health and well-being of residents by addressing housing-related health issues.

Please be assured that all information you provide will be kept strictly confidential. Your responses will be used solely for research purposes and will not be shared with anyone outside of our research team. We are committed to protecting your privacy and ensuring the anonymity of your responses.

To begin, we kindly ask you to provide your name and age.
'''

message(intro_text, key='-1')

if 'prompt' in st.session_state and st.session_state.prompt:
    add_user_message(st.session_state.prompt)

st.text_input(key='input', on_change=lambda: st.session_state.update(prompt=st.session_state.input), label='Type in your question here', label_visibility='hidden', placeholder='Type in your question here')

styl = f"""
<style>
    .stTextInput {{
        position: fixed;
        bottom: 10px;
        left: 0;
        right: 0;
        width: 96vw;
        margin: auto;
    }}    

    .block-container {{
        position: fixed !important;
        bottom: 5rem !important;
        padding: 0 !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        max-height: 90vh !important;
        width: 96vw !important;
    }}

    #MainMenu {{
        display: none;
    }}

    footer {{
        display: none;
    }}
    
    iframe[title="st.iframe"] {{
        height: 0px;
        overflow: hidden;
        display: block;
    }}

</style>
"""
st.markdown(styl, unsafe_allow_html=True)

num_messages_to_display = 5  # Adjust this number as needed

if len(st.session_state.chat_history) > num_messages_to_display:
    start_index = len(st.session_state.chat_history) - num_messages_to_display
else:
    start_index = 0

for chat_item in st.session_state.chat_history[start_index:]:
    if chat_item["role"] == "user":
        message(chat_item["parts"][0], is_user=True, avatar_style="adventurer", key=chat_item["parts"][0] + '_user')
    else:
        message(chat_item["parts"][0], key=chat_item["parts"][0])