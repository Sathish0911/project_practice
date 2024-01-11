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


###################################################################################################

from PIL import Image
import streamlit as st

# ... (your other imports and global variable declarations)

# ... (your other code)

# # to show chat history on ui
# Initialize chat history and session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?", "image_path": None, "image_caption": None}]

if "image_paths" not in st.session_state:
    st.session_state.image_paths = []

def main():
    # ... (your existing code)

    with st.chat_message("assistant"):
        user_question = format_user_question(user_input)
        answer, image_path = Copilot_assistant_agent.run(user_question)

        st.markdown(answer)

        if image_path:
            image = Image.open(image_path)
            st.image(image, caption="image", use_column_width=True)
            st.session_state.image_paths.append(image_path)

        st.session_state.messages.append({"role": "assistant", "content": full_response, 'image_path': image_path, "image_caption": "image"})

        # Display old images from previous queries
        for old_image_path in st.session_state.image_paths:
            old_image = Image.open(old_image_path)
            st.image(old_image, caption="image", use_column_width=True)

        INITIALIZED = True
####################################################################################################################

import pandas as pd
import faker  # You might need to install this library using: pip install faker

# Function to generate fake data
def generate_fake_data(num_rows=5):
    fake = faker.Faker()

    data = {
        'site_name': [fake.random_element(['3459302D 39394-S', '3430294D 29838-S']) for _ in range(num_rows)],
        'location_code': [fake.random_element(['84739484C', '8459602C']) for _ in range(num_rows)],
        'address': [fake.address() for _ in range(num_rows)],
        'latitude': [fake.latitude() for _ in range(num_rows)],
        'longitude': [fake.longitude() for _ in range(num_rows)],
        'provider': [fake.company() for _ in range(num_rows)],
        'state': [fake.state() for _ in range(num_rows)],
        'country': ['USA' for _ in range(num_rows)]  # All entries are in the USA
    }

    df = pd.DataFrame(data)
    return df

# Generate fake data
fake_data = generate_fake_data()

# Save the DataFrame to a CSV file

########################################################################################################

import pandas as pd
import faker  # You might need to install this library using: pip install faker

# Function to fake data for specific columns in an existing DataFrame
def fake_data_for_columns(df, columns):
    fake = faker.Faker()

    for column in columns:
        if column in df.columns:
            # Check the column type to generate appropriate fake data
            if df[column].dtype == 'object':
                df[column] = [fake.address() for _ in range(len(df))]
            elif df[column].dtype == 'float64':
                df[column] = [fake.latitude() for _ in range(len(df))]
            elif df[column].dtype == 'int64':
                df[column] = [fake.random_int() for _ in range(len(df))]

    return df

# Example: Assuming you have an existing DataFrame called 'existing_df'
existing_df = pd.DataFrame({
    'site_name': ['ExampleSite1', 'ExampleSite2', 'ExampleSite3'],
    'location_code': ['ABC123', 'DEF456', 'GHI789'],
    'address': ['123 Main St', '456 Oak St', '789 Pine St'],
    'latitude': [40.7128, 34.0522, 41.8781],
    'longitude': [-74.0060, -118.2437, -87.6298],
    'provider': ['Provider1', 'Provider2', 'Provider3'],
    'state': ['NY', 'CA', 'IL'],
    'country': ['USA', 'USA', 'USA']
})

# Specify the columns you want to fake
columns_to_fake = ['address', 'latitude', 'longitude']

# Call the function to fake data for specified columns
fake_data_df = fake_data_for_columns(existing_df.copy(), columns_to_fake)

# Display the original and modified DataFrames
print("Original DataFrame:")
print(existing_df)
print("\nDataFrame with Fake Data:")
print(fake_data_df)

##########################################################################################
fake_data.to_csv('fake_data.csv', index=False)

# Display the generated DataFrame
print(fake_data)

