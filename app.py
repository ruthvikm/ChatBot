import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings
import cohere
import time

# Load environment variables from .env file
load_dotenv()

# Load the PDF and prepare the content
loader = PyPDFLoader('Resume.pdf')
documents = loader.load()
YOUR_NAME = 'Ruthvik'

# Get API key from environment variable
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Initialize embeddings and vector store
embeddings = CohereEmbeddings(model="embed-multilingual-v3.0", cohere_api_key=COHERE_API_KEY)
vector_store = FAISS.from_documents(documents, embeddings)

# Initialize Cohere client directly
cohere_client = cohere.Client(api_key=COHERE_API_KEY)

# Function to generate a response using Cohere
def generate_response(prompt, max_tokens=200):
    try:
        response = cohere_client.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.4
        )
        return response.generations[0].text if response.generations else "I'm sorry, I couldn't find an answer to that."
    except Exception as e:
        return f"An error occurred: {e}"

# Function to ensure response ends properly
def ensure_proper_ending(response):
    response = response.strip()

    # Check if the response ends properly with a punctuation mark
    if not response.endswith(('.', '!', '?')) and len(response.split()) > 5 :
        st.session_state.incomplete_response = response
        response += " ...it seems I didn't finish. Would you like more details?"
    else:
        st.session_state.incomplete_response = None
        
    return response


# Function to retrieve relevant chunks using the vector store
def retrieve_relevant_chunks(question):
    query_embedding = embeddings.embed_query(question)
    docs = vector_store.similarity_search_by_vector(query_embedding, k=5)
    return " ".join([doc.page_content for doc in docs])

# Function to get a response from Jarvis
def get_chatbot_response(question):
    # Handle common greetings or simple questions
    if question.lower() in ["hello", "hi", "hey", "greetings", "who are you"]:
        return f"Hello! I am Jarvis, {YOUR_NAME}'s personal assistant. How can I assist you today?"
    elif question.lower() in ["who created you"]:
        return f"{YOUR_NAME} brought me to life on August 22nd, 2024."
    elif question.lower() == "yes" and st.session_state.get('incomplete_response'):
        # Continue from the incomplete response
        previous_response = st.session_state.incomplete_response
        return generate_response(f"Please continue the following response: {previous_response}")

    # Retrieve the most relevant chunks of text
    relevant_content = retrieve_relevant_chunks(question)

    # Simplified and focused prompt
    prompt = f"""
    Answer the following question directly and concisely: '{question}'.
    Only use relevant information from {YOUR_NAME}'s background and skills.

    Relevant information:
    {relevant_content}
    """

    response = generate_response(prompt)
    response = ensure_proper_ending(response)

    if "I'm sorry" in response or len(response.strip()) < 10:
        response = "I'm sorry, I couldn't find a relevant answer to your question."

    return response

# Streamlit UI
st.set_page_config(page_title="Jarvis - Ruthvik's Personal Assistant", layout="centered")

st.title("Jarvis - Your Personal Assistant")
st.write("Ask me anything about Ruthvik!")

# Initialize session state for conversation history and incomplete responses if it doesn't exist
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

if 'incomplete_response' not in st.session_state:
    st.session_state.incomplete_response = None

# CSS styling for chat bubbles, text input, and blinking animation
st.markdown("""
    <style>
    .jarvis-bubble {
        background-color: #e0f7fa;
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
        max-width: 70%;
        text-align: left;
        box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
        color: black;
        margin-left: 0;
    }
    .user-bubble {
        background-color: #c8e6c9;
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
        max-width: 70%;
        text-align: right;
        margin-left: auto;
        box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
        color: black;
    }
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding-right: 15px;
        padding-left: 15px;
        background-color: #f5f5f5;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        padding: 20px;
    }
    .textbox {
        padding: 10px;
        border-radius: 15px;
        border: 1px solid #ccc;
        width: 100%;
        color: black;
    }
    .button {
        background-color: #007bff;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        font-size: 16px;
    }
    .button:hover {
        background-color: #0056b3;
    }
    .blinking-bubble {
        background-color: #e0f7fa;
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
        max-width: 70%;
        height: 20px;
        text-align: left;
        box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
        margin-left: 0;
        animation: blink 1.5s infinite;
    }
    @keyframes blink {
        0% { opacity: 0.2; }
        50% { opacity: 1; }
        100% { opacity: 0.2; }
    }
    </style>
    """, unsafe_allow_html=True)

# Display the conversation history in a bubbled format
chat_container = st.container()  # Create a container for chat

# Create a form to handle the user input and response submission
with st.form(key='question_form', clear_on_submit=True):
    question = st.text_input("Your question:", "", key="input_box", placeholder="Type your question here...", label_visibility="collapsed")

    # Submit button inside the form
    submit_button = st.form_submit_button(label="Ask Jarvis")

    # Handle the form submission
    if submit_button and question:
        # Display the user's question immediately
        st.session_state.conversation_history.append({"role": "user", "content": question})
        
        # Render the chat immediately after the user's input
        with chat_container:
            for entry in st.session_state.conversation_history:
                if entry["role"] == "user":
                    st.markdown(f'<div class="user-bubble">{entry["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="jarvis-bubble">{entry["content"]}</div>', unsafe_allow_html=True)

        # Create the response placeholder inside the chat container
        with chat_container:
            response_placeholder = st.empty()
            response_placeholder.markdown(f'<div class="blinking-bubble"></div>', unsafe_allow_html=True)
        
        # Artificial delay to simulate thinking (optional)
        time.sleep(2)  # Simulate processing time

        # Generate Jarvis's response
        response = get_chatbot_response(question)
        st.session_state.conversation_history.append({"role": "jarvis", "content": response})

        # Replace the blinking bubble with the actual response
        response_placeholder.empty()  # Clear the previous "blinking" bubble
        with response_placeholder.container():
            st.markdown(f'<div class="jarvis-bubble">{response}</div>', unsafe_allow_html=True)

# Clear session history (for a fresh start)
if st.button("Clear Conversation", key="clear_button"):
    st.session_state.conversation_history = []  # Reset conversation history
    st.rerun()  # This will reload the app to reflect the cleared history
