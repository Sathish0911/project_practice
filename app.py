import os
import json
import time
import random
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
from scripts.utils import format_user_question
from scripts.copilot_assistant import ConversationAgent
from scripts.tools import generated_image_path, reinitialize_image_path

# WHITE = "\033[37m"
# GREEN = "\033[32m"
# RESET_COLOR = "\033[0m"

#GLOBAL VARIABLE DECLARATION
IMAGE_IN_RESPONSE = False
INITIALIZED = False

load_dotenv()

st.set_page_config(page_title="Verizon Copilot", page_icon="💬")
st.header('Copilot Assistant with Streamlit')

# # to show chat history on ui
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?", "image": None}]
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.sidebar.title('Info')
st.sidebar.write("-Answer questions")
st.sidebar.write("Simple answer")

example_questions = [
    "How many critical tickets are open?",
    "How many total tickets are there as of today?"
]

def main():
    global INITIALIZED
    if not INITIALIZED:
        Copilot_assistant_agent = ConversationAgent()
        # st.title("Copilot Assistant with Streamlit")
        user_input = st.chat_input(placeholder="Ask me your query!")
        if user_input:
            # Display user message in chat message container
            with st.chat_message("user"):
                st.session_state.messages.append({"role": 'User', "content": user_input, 'image': None})
                st.markdown(user_input)

            with st.chat_message("assistant"):
                user_question = format_user_question(user_input)
                answer = Copilot_assistant_agent.run(user_question)
                # answer, image_path = Copilot_assistant_agent.run(user_question)

                message_placeholder = st.empty()
                full_response = ""

                # Simulate stream of response with milliseconds delay
                for chunk in answer.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

                image_path = generated_image_path()
                if image_path:
                    # image_path = "./temp_images/Pasted_image.png"
                    image = Image.open(image_path)
                    st.image(image, caption = "image", use_column_width = True)
                    reinitialize_image_path()
                st.session_state.messages.append({"role": "assistant", "content": full_response,'image': image_path})
                # st.markdown(assistant_response)

                INITIALIZED = True


if __name__ == "__main__":
    main()