# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.vectorstores import FAISS
# from langchain_cohere import CohereEmbeddings
# from langchain.prompts import PromptTemplate
# from langchain.chains import RetrievalQA
# import cohere

# # Load the PDF
# loader = PyPDFLoader('mypdf.pdf')
# documents = loader.load()

# # API key for Cohere
# COHERE_API_KEY = "VegoJTcGcEhVI5taUccJDtXuFmgRnjXqGsQjsXMQ"

# # Initialize embeddings and vector store
# embeddings = CohereEmbeddings(model="embed-english-light-v3.0", cohere_api_key=COHERE_API_KEY)
# vector_store = FAISS.from_documents(documents, embeddings)

# # Define the prompt template
# prompt_template = PromptTemplate.from_template("Use the following document to answer questions: {document}. Question: {question}")

# # Initialize Cohere client directly
# cohere_client = cohere.Client(api_key=COHERE_API_KEY)

# # Function to generate response using Cohere
# def generate_response(prompt):
#     response = cohere_client.generate(
#         model='command-xlarge-nightly',
#         prompt=prompt,
#         max_tokens=100
#     )
#     return response.generations[0].text

# # Function to get a response from the chatbot
# def get_chatbot_response(question):
#     prompt = prompt_template.format(document=documents[0].page_content, question=question)
#     response = generate_response(prompt)
#     return response

# # Example usage
# if __name__ == "__main__":
#     question = "Does this insurance cover explosion?"
#     response = get_chatbot_response(question)
#     print(response)


# from flask import Flask, render_template, request
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.vectorstores import FAISS
# from langchain_cohere import CohereEmbeddings
# import cohere

# app = Flask(__name__)

# # Load the PDF
# loader = PyPDFLoader('Resume.pdf')
# documents = loader.load()
# full_document_content = " ".join([doc.page_content for doc in documents])

# # API key for Cohere
# COHERE_API_KEY = "VegoJTcGcEhVI5taUccJDtXuFmgRnjXqGsQjsXMQ"

# # Initialize embeddings and vector store
# embeddings = CohereEmbeddings(model="embed-english-light-v3.0", cohere_api_key=COHERE_API_KEY)
# vector_store = FAISS.from_documents(documents, embeddings)

# # Initialize Cohere client directly
# cohere_client = cohere.Client(api_key=COHERE_API_KEY)

# # Function to generate response using Cohere
# def generate_response(prompt):
#     response = cohere_client.generate(
#         model='command-xlarge-nightly',
#         prompt=prompt,
#         max_tokens=100
#     )
#     return response.generations[0].text

# # Function to get a response from the chatbot
# def get_chatbot_response(question):
#     prompt = f"Use the following document to answer questions: {full_document_content}. Question: {question}"
#     response = generate_response(prompt)
#     return response

# @app.route("/", methods=["GET", "POST"])
# def index():
#     response = ""
#     if request.method == "POST":
#         question = request.form["question"]
#         response = get_chatbot_response(question)
#     return render_template("index.html", response=response)

# if __name__ == "__main__":
#     app.run(debug=True)





# from flask import Flask, render_template, request, session, redirect
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.vectorstores import FAISS
# from langchain_cohere import CohereEmbeddings
# import cohere
# import time

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# # Load the PDF and prepare the content
# loader = PyPDFLoader('Resume.pdf')
# documents = loader.load()
# full_document_content = " ".join([doc.page_content for doc in documents])
# YOUR_NAME = 'Ruthvik'

# # API key for Cohere
# COHERE_API_KEY = "VegoJTcGcEhVI5taUccJDtXuFmgRnjXqGsQjsXMQ"

# # Initialize embeddings and vector store
# embeddings = CohereEmbeddings(model="embed-multilingual-v3.0", cohere_api_key=COHERE_API_KEY)
# vector_store = FAISS.from_documents(documents, embeddings)

# # Initialize Cohere client directly
# cohere_client = cohere.Client(api_key=COHERE_API_KEY)

# # Function to generate a response using Cohere
# def generate_response(prompt):
#     try:
#         start_time = time.time()
#         response = cohere_client.generate(
#             model='command-r',
#             prompt=prompt,
#             max_tokens=200,
#             temperature=0.6
#         )
#         end_time = time.time()
#         print(f"Response time: {end_time - start_time} seconds")
#         return response.generations[0].text if response.generations else "I'm sorry, I couldn't find an answer to that."
#     except Exception as e:
#         return f"An error occurred: {e}"

# # Function to determine if a question is likely irrelevant
# def is_question_irrelevant(question):
#     # Consider a question irrelevant if it is very short or if it does not match any content in the document
#     question_words = question.lower().split()
    
#     # Check for very short questions
#     if len(question_words) < 3:
#         return True
    
#     # Check if the question contains any words from the document
#     document_words = set(full_document_content.lower().split())
#     common_words = set(question_words) & document_words
    
#     # If there are no common words between the question and the document, consider it irrelevant
#     if not common_words:
#         return True

#     return False

# # Function to get a response from Jarvis
# def get_chatbot_response(question):
#     if question.lower() in ["hello", "hi", "hey", "greetings", "who are you"]:
#         return f"Hello! I am Jarvis, {YOUR_NAME}'s personal assistant. How can I assist you today?"
#     elif question.lower() in ["who created you"]:
#         return f"{YOUR_NAME} brought me to life on August 22nd 2024"

#     # Check if the question is likely irrelevant
#     if is_question_irrelevant(question):
#         return "That doesn't seem related to my knowledge. Could you ask something else?"

#     # Only use context when necessary
#     context = " ".join(session["conversation_history"][-3:]) if "conversation_history" in session else ""
    
#     # Building a clear and concise prompt
#     prompt = f"""
#     As {YOUR_NAME}'s assistant, your task is to provide a precise and concise answer to the following question: '{question}'.
#     - Context: {context}.
#     - Use the relevant information from {YOUR_NAME}'s background and skills, which you can find in the content below.
#     - Focus solely on the question, and avoid providing unnecessary details or referencing the document directly.
#     - If the question falls outside the scope of the information provided in the document, respond with: 'I'm sorry, that's an irrelevant question.'

#     Relevant information you should consider:
#     {full_document_content}
#     """

#     response = generate_response(prompt)

#     # Check if the response seems incomplete or off-topic
#     if not response.strip().endswith(('.', '!', '?')) or \
#        len(response.strip()) < 50:
#         response = "I'm sorry, I couldn't find a relevant answer to your question. Could you please clarify?"

#     session["conversation_history"].append(f"User: {question}\nJarvis: {response}")
#     return response

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if "conversation_history" not in session:
#         session["conversation_history"] = []

#     response = ""
#     if request.method == "POST":
#         question = request.form["question"]
#         response = get_chatbot_response(question)
    
#     return render_template("index.html", response=response)

# @app.route("/clear")
# def clear():
#     session.pop("conversation_history", None)
#     return redirect("/")

# if __name__ == "__main__":
#     app.run(debug=True)




# from flask import Flask, render_template, request, session, redirect
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.vectorstores import FAISS
# from langchain_cohere import CohereEmbeddings
# import cohere
# import time

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# # Load the PDF and prepare the content
# loader = PyPDFLoader('Resume.pdf')
# documents = loader.load()
# full_document_content = " ".join([doc.page_content for doc in documents])
# YOUR_NAME = 'Ruthvik'

# # API key for Cohere
# COHERE_API_KEY = "VegoJTcGcEhVI5taUccJDtXuFmgRnjXqGsQjsXMQ"

# # Initialize embeddings and vector store
# embeddings = CohereEmbeddings(model="embed-multilingual-v3.0", cohere_api_key=COHERE_API_KEY)
# vector_store = FAISS.from_documents(documents, embeddings)

# # Initialize Cohere client directly
# cohere_client = cohere.Client(api_key=COHERE_API_KEY)

# # Function to generate a response using Cohere
# def generate_response(prompt):
#     try:
#         start_time = time.time()
#         response = cohere_client.generate(
#             model='command-r-plus',
#             prompt=prompt,
#             max_tokens=200,
#             temperature=0.6
#         )
#         end_time = time.time()
#         print(f"Response time: {end_time - start_time} seconds")
#         return response.generations[0].text if response.generations else "I'm sorry, I couldn't find an answer to that."
#     except Exception as e:
#         return f"An error occurred: {e}"

# # Function to determine if a question is likely irrelevant
# def is_question_irrelevant(question):
#     question_words = question.lower().split()
    
#     # Check for very short questions
#     if len(question_words) < 2:
#         return True
    
#     # Check if the question contains any words from the document
#     document_words = set(full_document_content.lower().split())
#     common_words = set(question_words) & document_words
    
#     # If there are no common words between the question and the document, consider it irrelevant
#     if not common_words:
#         return True

#     return False

# # Function to get a response from Jarvis
# def get_chatbot_response(question):
#     # Handle basic greetings and identity questions
#     if question.lower() in ["hello", "hi", "hey", "greetings", "who are you"]:
#         return f"Hello! I am Jarvis, {YOUR_NAME}'s personal assistant. How can I assist you today?"
#     elif question.lower() in ["who created you"]:
#         return f"{YOUR_NAME} brought me to life on August 22nd, 2024."

#     # Check if the question is likely irrelevant
#     if is_question_irrelevant(question):
#         return "That doesn't seem related to my knowledge. Could you ask something else?"

#     # Only use context from the session when relevant
#     if "conversation_history" not in session:
#         session["conversation_history"] = []

#     context = " ".join(session["conversation_history"][-3:])

#     # Building a clear and concise prompt without over-relying on context
#     prompt = f"""
#     As {YOUR_NAME}'s assistant, your task is to provide a direct and clear answer to the following question: '{question}'.
#     - Use the relevant information from {YOUR_NAME}'s background and skills provided below.
#     - Focus solely on answering the question directly.

#     Relevant information:
#     {full_document_content}
#     """

#     response = generate_response(prompt)

#     # Basic check to ensure relevance
#     if "I'm sorry" in response or len(response.strip()) < 20:
#         response = "I'm sorry, I couldn't find a relevant answer to your question."

#     session["conversation_history"].append(f"User: {question}\nJarvis: {response}")
#     return response

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if "conversation_history" not in session:
#         session["conversation_history"] = []

#     response = ""
#     if request.method == "POST":
#         question = request.form["question"]
#         response = get_chatbot_response(question)
    
#     return render_template("index.html", response=response)

# @app.route("/clear")
# def clear():
#     session.pop("conversation_history", None)
#     return redirect("/")

# if __name__ == "__main__":
#     app.run(debug=True)












#below works great but need to fix order

# import streamlit as st
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.vectorstores import FAISS
# from langchain_cohere import CohereEmbeddings
# import cohere
# import time

# # Load the PDF and prepare the content
# loader = PyPDFLoader('Resume.pdf')
# documents = loader.load()
# full_document_content = " ".join([doc.page_content for doc in documents])
# YOUR_NAME = 'Ruthvik'

# # API key for Cohere
# COHERE_API_KEY = "VegoJTcGcEhVI5taUccJDtXuFmgRnjXqGsQjsXMQ"

# # Initialize Cohere client directly
# cohere_client = cohere.Client(api_key=COHERE_API_KEY)

# # Function to generate a response using Cohere
# def generate_response(prompt):
#     try:
#         response = cohere_client.generate(
#             model='command-r-plus',
#             prompt=prompt,
#             max_tokens=200,
#             temperature=0.5
#         )
#         return response.generations[0].text if response.generations else "I'm sorry, I couldn't find an answer to that."
#     except Exception as e:
#         return f"An error occurred: {e}"

# # Function to check if a question is relevant based on document content
# def is_question_relevant(question):
#     # Check if the question contains any words from the document
#     document_words = set(full_document_content.lower().split())
#     question_words = set(question.lower().split())
    
#     # Consider the question relevant if there are common words between the question and the document
#     common_words = question_words & document_words
    
#     return len(common_words) > 0

# # Function to get a response from Jarvis
# def get_chatbot_response(question):
#     if question.lower() in ["hello", "hi", "hey", "greetings", "who are you"]:
#         return f"Hello! I am Jarvis, {YOUR_NAME}'s personal assistant. How can I assist you today?"
#     elif question.lower() in ["who created you"]:
#         return f"{YOUR_NAME} brought me to life on August 22nd, 2024."

#     # Check if the question is relevant
#     if not is_question_relevant(question):
#         return "That doesn't seem related to my knowledge. Could you ask something else?"

#     # Build the prompt
#     prompt = f"""
#     As {YOUR_NAME}'s assistant, your task is to provide a direct and clear answer to the following question: '{question}'.
#     - Use the relevant information from {YOUR_NAME}'s background and skills provided below.
#     - Focus solely on answering the question directly.

#     Relevant information:
#     {full_document_content}
#     """

#     response = generate_response(prompt)

#     # Ensure the response is relevant
#     if "I'm sorry" in response or len(response.strip()) < 20:
#         response = "I'm sorry, I couldn't find a relevant answer to your question."

#     return response

# # Streamlit UI
# st.set_page_config(page_title="Jarvis - Your Personal Assistant", layout="centered")

# st.title("Jarvis - Your Personal Assistant")
# st.write("Ask me anything about Ruthvik!")

# # Initialize session state for conversation history if it doesn't exist
# if 'conversation_history' not in st.session_state:
#     st.session_state.conversation_history = []

# # CSS styling for chat bubbles and text input
# st.markdown("""
#     <style>
#     .jarvis-bubble {
#         background-color: #e0f7fa;
#         border-radius: 15px;
#         padding: 10px;
#         margin-bottom: 10px;
#         max-width: 70%;
#         text-align: left;
#         box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
#         color: black;
#     }
#     .user-bubble {
#         background-color: #c8e6c9;
#         border-radius: 15px;
#         padding: 10px;
#         margin-bottom: 10px;
#         max-width: 70%;
#         text-align: right;
#         margin-left: auto;
#         box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
#         color: black;
#     }
#     .chat-container {
#         max-height: 400px;
#         overflow-y: auto;
#         padding-right: 15px;
#         padding-left: 15px;
#         background-color: #f5f5f5;
#         border-radius: 10px;
#         box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
#         padding: 20px;
#     }
#     .textbox {
#         padding: 10px;
#         border-radius: 15px;
#         border: 1px solid #ccc;
#         width: 100%;
#         color: black;
#     }
#     .button {
#         background-color: #007bff;
#         color: white;
#         padding: 10px 20px;
#         border-radius: 5px;
#         border: none;
#         cursor: pointer;
#         font-size: 16px;
#     }
#     .button:hover {
#         background-color: #0056b3;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Display the conversation history in a bubbled format
# chat_container = st.container()  # Create a container for chat

# # Create a form to handle the user input and response submission
# with st.form(key='question_form'):
#     question = st.text_input("Your question:", "", key="input_box", placeholder="Type your question here...", label_visibility="collapsed")

#     # Submit button inside the form
#     submit_button = st.form_submit_button(label="Ask Jarvis")

#     # Handle the form submission
#     if submit_button and question:
#         # Display the user's question immediately
#         st.session_state.conversation_history.append({"role": "user", "content": question})
        
#         # Create a placeholder for Jarvis's response
#         response_placeholder = chat_container.empty()

#         with chat_container:
#             for entry in st.session_state.conversation_history:
#                 if entry["role"] == "user":
#                     st.markdown(f'<div class="user-bubble">{entry["content"]}</div>', unsafe_allow_html=True)
#                 else:
#                     st.markdown(f'<div class="jarvis-bubble">{entry["content"]}</div>', unsafe_allow_html=True)

#         # Simulate a "processing" state
#         with response_placeholder:
#             st.markdown(f'<div class="jarvis-bubble">Jarvis is thinking...</div>', unsafe_allow_html=True)

#         # Generate Jarvis's response
#         response = get_chatbot_response(question)
#         st.session_state.conversation_history.append({"role": "jarvis", "content": response})

#         # Update the placeholder with the actual response
#         with response_placeholder:
#             st.markdown(f'<div class="jarvis-bubble">{response}</div>', unsafe_allow_html=True)

# # Clear session history (for a fresh start)
# if st.button("Clear Conversation", key="clear_button"):
#     st.session_state.conversation_history = []  # Reset conversation history
#     st.rerun()  # This will reload the app to reflect the cleared history






# import streamlit as st
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.vectorstores import FAISS
# from langchain_cohere import CohereEmbeddings
# import cohere
# import time

# # Load the PDF and prepare the content
# loader = PyPDFLoader('Resume.pdf')
# documents = loader.load()
# full_document_content = " ".join([doc.page_content for doc in documents])
# YOUR_NAME = 'Ruthvik'

# # API key for Cohere
# COHERE_API_KEY = "VegoJTcGcEhVI5taUccJDtXuFmgRnjXqGsQjsXMQ"

# # Initialize Cohere client directly
# cohere_client = cohere.Client(api_key=COHERE_API_KEY)

# # Function to generate a response using Cohere
# def generate_response(prompt):
#     try:
#         response = cohere_client.generate(
#             model='command-r-plus',
#             prompt=prompt,
#             max_tokens=200,
#             temperature=0.5
#         )
#         return response.generations[0].text if response.generations else "I'm sorry, I couldn't find an answer to that."
#     except Exception as e:
#         return f"An error occurred: {e}"

# # Function to check if a question is relevant based on document content
# def is_question_relevant(question):
#     # Check if the question contains any words from the document
#     document_words = set(full_document_content.lower().split())
#     question_words = set(question.lower().split())
    
#     # Consider the question relevant if there are common words between the question and the document
#     common_words = question_words & document_words
    
#     return len(common_words) > 0

# # Function to get a response from Jarvis
# def get_chatbot_response(question):
#     if question.lower() in ["hello", "hi", "hey", "greetings", "who are you"]:
#         return f"Hello! I am Jarvis, {YOUR_NAME}'s personal assistant. How can I assist you today?"
#     elif question.lower() in ["who created you"]:
#         return f"{YOUR_NAME} brought me to life on August 22nd, 2024."

#     # Check if the question is relevant
#     if not is_question_relevant(question):
#         return "That doesn't seem related to my knowledge. Could you ask something else?"

#     # Build the prompt
#     prompt = f"""
#     As {YOUR_NAME}'s assistant, your task is to provide a direct and clear answer to the following question: '{question}'.
#     - Use the relevant information from {YOUR_NAME}'s background and skills provided below.
#     - Focus solely on answering the question directly.

#     Relevant information:
#     {full_document_content}
#     """

#     response = generate_response(prompt)

#     # Ensure the response is relevant
#     if "I'm sorry" in response or len(response.strip()) < 20:
#         response = "I'm sorry, I couldn't find a relevant answer to your question."

#     return response

# # Streamlit UI
# st.set_page_config(page_title="Jarvis - Your Personal Assistant", layout="centered")

# st.title("Jarvis - Your Personal Assistant")
# st.write("Ask me anything about Ruthvik!")

# # Initialize session state for conversation history if it doesn't exist
# if 'conversation_history' not in st.session_state:
#     st.session_state.conversation_history = []

# # CSS styling for chat bubbles, text input, and blinking animation
# st.markdown("""
#     <style>
#     .jarvis-bubble {
#         background-color: #e0f7fa;
#         border-radius: 15px;
#         padding: 10px;
#         margin-bottom: 10px;
#         max-width: 70%;
#         text-align: left;
#         box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
#         color: black;
#         margin-left: 0;
#     }
#     .user-bubble {
#         background-color: #c8e6c9;
#         border-radius: 15px;
#         padding: 10px;
#         margin-bottom: 10px;
#         max-width: 70%;
#         text-align: right;
#         margin-left: auto;
#         box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
#         color: black;
#     }
#     .chat-container {
#         max-height: 400px;
#         overflow-y: auto;
#         padding-right: 15px;
#         padding-left: 15px;
#         background-color: #f5f5f5;
#         border-radius: 10px;
#         box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
#         padding: 20px;
#     }
#     .textbox {
#         padding: 10px;
#         border-radius: 15px;
#         border: 1px solid #ccc;
#         width: 100%;
#         color: black;
#     }
#     .button {
#         background-color: #007bff;
#         color: white;
#         padding: 10px 20px;
#         border-radius: 5px;
#         border: none;
#         cursor: pointer;
#         font-size: 16px;
#     }
#     .button:hover {
#         background-color: #0056b3;
#     }
#     .blinking-bubble {
#         background-color: #e0f7fa;
#         border-radius: 15px;
#         padding: 10px;
#         margin-bottom: 10px;
#         max-width: 70%;
#         height: 20px;
#         text-align: left;
#         box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
#         margin-left: 0;
#         animation: blink 1.5s infinite;
#     }
#     @keyframes blink {
#         0% { opacity: 0.2; }
#         50% { opacity: 1; }
#         100% { opacity: 0.2; }
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Display the conversation history in a bubbled format
# chat_container = st.container()  # Create a container for chat

# # Create a form to handle the user input and response submission
# with st.form(key='question_form'):
#     question = st.text_input("Your question:", "", key="input_box", placeholder="Type your question here...", label_visibility="collapsed")

#     # Submit button inside the form
#     submit_button = st.form_submit_button(label="Ask Jarvis")

#     # Handle the form submission
#     if submit_button and question:
#         # Display the user's question immediately
#         st.session_state.conversation_history.append({"role": "user", "content": question})
        
#         # Render the chat immediately after the user's input
#         with chat_container:
#             for entry in st.session_state.conversation_history:
#                 if entry["role"] == "user":
#                     st.markdown(f'<div class="user-bubble">{entry["content"]}</div>', unsafe_allow_html=True)
#                 else:
#                     st.markdown(f'<div class="jarvis-bubble">{entry["content"]}</div>', unsafe_allow_html=True)

#         # Simulate a "processing" state with blinking animation
#         response_placeholder = st.empty()
#         with response_placeholder:
#             st.markdown(f'<div class="blinking-bubble"></div>', unsafe_allow_html=True)
        
#         # Artificial delay to simulate thinking (optional)
#         time.sleep(2)  # Simulate processing time

#         # Generate Jarvis's response
#         response = get_chatbot_response(question)
#         st.session_state.conversation_history.append({"role": "jarvis", "content": response})

#         # Replace the blinking bubble with the actual response
#         response_placeholder.empty()  # Clear the previous "blinking" bubble
#         with chat_container:
#             st.markdown(f'<div class="jarvis-bubble">{response}</div>', unsafe_allow_html=True)

# # Clear session history (for a fresh start)
# if st.button("Clear Conversation", key="clear_button"):
#     st.session_state.conversation_history = []  # Reset conversation history
#     st.rerun()  # This will reload the app to reflect the cleared history










# import streamlit as st
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.vectorstores import FAISS
# from langchain_cohere import CohereEmbeddings
# import cohere
# import time

# # Load the PDF and prepare the content
# loader = PyPDFLoader('Resume.pdf')
# documents = loader.load()
# full_document_content = " ".join([doc.page_content for doc in documents])
# YOUR_NAME = 'Ruthvik'

# # API key for Cohere
# COHERE_API_KEY = "VegoJTcGcEhVI5taUccJDtXuFmgRnjXqGsQjsXMQ"

# # Initialize embeddings and vector store
# embeddings = CohereEmbeddings(model="embed-multilingual-v3.0", cohere_api_key=COHERE_API_KEY)
# vector_store = FAISS.from_documents(documents, embeddings)

# # Initialize Cohere client directly
# cohere_client = cohere.Client(api_key=COHERE_API_KEY)

# # Function to generate a response using Cohere
# def generate_response(prompt):
#     try:
#         response = cohere_client.generate(
#             model='command-r-plus',
#             prompt=prompt,
#             max_tokens=200,
#             temperature=0.5
#         )
#         return response.generations[0].text if response.generations else "I'm sorry, I couldn't find an answer to that."
#     except Exception as e:
#         return f"An error occurred: {e}"

# # Function to check if a question is relevant based on document content
# def is_question_relevant(question):
#     # Check if the question contains any words from the document
#     document_words = set(full_document_content.lower().split())
#     question_words = set(question.lower().split())
    
#     # Consider the question relevant if there are common words between the question and the document
#     common_words = question_words & document_words
    
#     return len(common_words) > 0

# # Function to get a response from Jarvis
# def get_chatbot_response(question):
#     if question.lower() in ["hello", "hi", "hey", "greetings", "who are you"]:
#         return f"Hello! I am Jarvis, {YOUR_NAME}'s personal assistant. How can I assist you today?"
#     elif question.lower() in ["who created you"]:
#         return f"{YOUR_NAME} brought me to life on August 22nd, 2024."

#     # Check if the question is relevant
#     if not is_question_relevant(question):
#         return "That doesn't seem related to my knowledge. Could you ask something else?"

#     # Build the prompt
#     prompt = f"""
#     As {YOUR_NAME}'s assistant, your task is to provide a direct and clear answer to the following question: '{question}'.
#     - Use the relevant information from {YOUR_NAME}'s background and skills provided below.
#     - Focus solely on answering the question directly.

#     Relevant information:
#     {full_document_content}
#     """

#     response = generate_response(prompt)

#     # Ensure the response is relevant
#     if "I'm sorry" in response or len(response.strip()) < 20:
#         response = "I'm sorry, I couldn't find a relevant answer to your question."

#     return response

# # Streamlit UI
# st.set_page_config(page_title="Jarvis - Your Personal Assistant", layout="centered")

# st.title("Jarvis - Your Personal Assistant")
# st.write("Ask me anything about Ruthvik!")

# # Initialize session state for conversation history if it doesn't exist
# if 'conversation_history' not in st.session_state:
#     st.session_state.conversation_history = []

# # CSS styling for chat bubbles, text input, and blinking animation
# st.markdown("""
#     <style>
#     .jarvis-bubble {
#         background-color: #e0f7fa;
#         border-radius: 15px;
#         padding: 10px;
#         margin-bottom: 10px;
#         max-width: 70%;
#         text-align: left;
#         box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
#         color: black;
#         margin-left: 0;
#     }
#     .user-bubble {
#         background-color: #c8e6c9;
#         border-radius: 15px;
#         padding: 10px;
#         margin-bottom: 10px;
#         max-width: 70%;
#         text-align: right;
#         margin-left: auto;
#         box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
#         color: black;
#     }
#     .chat-container {
#         max-height: 400px;
#         overflow-y: auto;
#         padding-right: 15px;
#         padding-left: 15px;
#         background-color: #f5f5f5;
#         border-radius: 10px;
#         box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
#         padding: 20px;
#     }
#     .textbox {
#         padding: 10px;
#         border-radius: 15px;
#         border: 1px solid #ccc;
#         width: 100%;
#         color: black;
#     }
#     .button {
#         background-color: #007bff;
#         color: white;
#         padding: 10px 20px;
#         border-radius: 5px;
#         border: none;
#         cursor: pointer;
#         font-size: 16px;
#     }
#     .button:hover {
#         background-color: #0056b3;
#     }
#     .blinking-bubble {
#         background-color: #e0f7fa;
#         border-radius: 15px;
#         padding: 10px;
#         margin-bottom: 10px;
#         max-width: 70%;
#         height: 20px;
#         text-align: left;
#         box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
#         margin-left: 0;
#         animation: blink 1.5s infinite;
#     }
#     @keyframes blink {
#         0% { opacity: 0.2; }
#         50% { opacity: 1; }
#         100% { opacity: 0.2; }
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Display the conversation history in a bubbled format
# chat_container = st.container()  # Create a container for chat

# # Create a form to handle the user input and response submission
# with st.form(key='question_form', clear_on_submit=True):
#     question = st.text_input("Your question:", "", key="input_box", placeholder="Type your question here...", label_visibility="collapsed")

#     # Submit button inside the form
#     submit_button = st.form_submit_button(label="Ask Jarvis")

#     # Handle the form submission
#     if submit_button and question:
#         # Display the user's question immediately
#         st.session_state.conversation_history.append({"role": "user", "content": question})
        
#         # Render the chat immediately after the user's input
#         with chat_container:
#             for entry in st.session_state.conversation_history:
#                 if entry["role"] == "user":
#                     st.markdown(f'<div class="user-bubble">{entry["content"]}</div>', unsafe_allow_html=True)
#                 else:
#                     st.markdown(f'<div class="jarvis-bubble">{entry["content"]}</div>', unsafe_allow_html=True)

#         # Create the response placeholder inside the chat container
#         with chat_container:
#             response_placeholder = st.empty()
#             response_placeholder.markdown(f'<div class="blinking-bubble"></div>', unsafe_allow_html=True)
        
#         # Artificial delay to simulate thinking (optional)
#         time.sleep(2)  # Simulate processing time

#         # Generate Jarvis's response
#         response = get_chatbot_response(question)
#         st.session_state.conversation_history.append({"role": "jarvis", "content": response})

#         # Replace the blinking bubble with the actual response
#         response_placeholder.empty()  # Clear the previous "blinking" bubble
#         with response_placeholder.container():
#             st.markdown(f'<div class="jarvis-bubble">{response}</div>', unsafe_allow_html=True)


# # Clear session history (for a fresh start)
# if st.button("Clear Conversation", key="clear_button"):
#     st.session_state.conversation_history = []  # Reset conversation history
#     st.rerun()  # This will reload the app to reflect the cleared history





# import streamlit as st
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.vectorstores import FAISS
# from langchain_cohere import CohereEmbeddings
# import cohere
# import time

# # Load the PDF and prepare the content
# loader = PyPDFLoader('Resume.pdf')
# documents = loader.load()
# YOUR_NAME = 'Ruthvik'

# # API key for Cohere
# COHERE_API_KEY = "VegoJTcGcEhVI5taUccJDtXuFmgRnjXqGsQjsXMQ"

# # Initialize embeddings and vector store
# embeddings = CohereEmbeddings(model="embed-multilingual-v3.0", cohere_api_key=COHERE_API_KEY)
# vector_store = FAISS.from_documents(documents, embeddings)

# # Initialize Cohere client directly
# cohere_client = cohere.Client(api_key=COHERE_API_KEY)

# # Function to generate a response using Cohere
# def generate_response(prompt):
#     try:
#         response = cohere_client.generate(
#             model='command-r-plus',
#             prompt=prompt,
#             max_tokens=200,  # Reduce max_tokens slightly to encourage natural sentence endings
#             temperature=0.6
#         )
#         return response.generations[0].text if response.generations else "I'm sorry, I couldn't find an answer to that."
#     except Exception as e:
#         return f"An error occurred: {e}"

# # Function to check if a response ends properly
# def ensure_proper_ending(response):
#     if response and not response.strip().endswith(('.', '!', '?')) and len(response.strip().split()) > 180:
#         response += " ...it seems I didn't finish. Would you like more details?"
#     return response

# # Function to retrieve relevant chunks using the vector store
# def retrieve_relevant_chunks(question):
#     # Convert the question into an embedding
#     query_embedding = embeddings.embed_query(question)
#     # Retrieve the most relevant document chunks
#     docs = vector_store.similarity_search_by_vector(query_embedding, k=5)
#     # Combine the retrieved chunks into a single string
#     return " ".join([doc.page_content for doc in docs])

# # Function to get a response from Jarvis
# def get_chatbot_response(question):
#     if question.lower() in ["hello", "hi", "hey", "greetings", "who are you"]:
#         return f"Hello! I am Jarvis, {YOUR_NAME}'s personal assistant. How can I assist you today?"
#     elif question.lower() in ["who created you"]:
#         return f"{YOUR_NAME} brought me to life on August 22nd, 2024."

#     # Retrieve the most relevant chunks of text
#     relevant_content = retrieve_relevant_chunks(question)

#     prompt = f"""
#     As {YOUR_NAME}'s assistant, your task is to provide a direct and clear answer to the following question: '{question}'.
#     - Use the relevant information from {YOUR_NAME}'s background and skills provided below.
#     - Focus solely on answering the question directly.

#     Relevant information:
#     {relevant_content}
#     """

#     response = generate_response(prompt)
#     response = ensure_proper_ending(response)

#     # Ensure the response is relevant
#     if "I'm sorry" in response or len(response.strip()) < 20:
#         response = "I'm sorry, I couldn't find a relevant answer to your question."

#     return response

# # Streamlit UI
# st.set_page_config(page_title="Jarvis - Your Personal Assistant", layout="centered")

# st.title("Jarvis - Your Personal Assistant")
# st.write("Ask me anything about Ruthvik!")

# # Initialize session state for conversation history if it doesn't exist
# if 'conversation_history' not in st.session_state:
#     st.session_state.conversation_history = []

# # CSS styling for chat bubbles, text input, and blinking animation
# st.markdown("""
#     <style>
#     .jarvis-bubble {
#         background-color: #e0f7fa;
#         border-radius: 15px;
#         padding: 10px;
#         margin-bottom: 10px;
#         max-width: 70%;
#         text-align: left;
#         box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
#         color: black;
#         margin-left: 0;
#     }
#     .user-bubble {
#         background-color: #c8e6c9;
#         border-radius: 15px;
#         padding: 10px;
#         margin-bottom: 10px;
#         max-width: 70%;
#         text-align: right;
#         margin-left: auto;
#         box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
#         color: black;
#     }
#     .chat-container {
#         max-height: 400px;
#         overflow-y: auto;
#         padding-right: 15px;
#         padding-left: 15px;
#         background-color: #f5f5f5;
#         border-radius: 10px;
#         box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
#         padding: 20px;
#     }
#     .textbox {
#         padding: 10px;
#         border-radius: 15px;
#         border: 1px solid #ccc;
#         width: 100%;
#         color: black;
#     }
#     .button {
#         background-color: #007bff;
#         color: white;
#         padding: 10px 20px;
#         border-radius: 5px;
#         border: none;
#         cursor: pointer;
#         font-size: 16px;
#     }
#     .button:hover {
#         background-color: #0056b3;
#     }
#     .blinking-bubble {
#         background-color: #e0f7fa;
#         border-radius: 15px;
#         padding: 10px;
#         margin-bottom: 10px;
#         max-width: 70%;
#         height: 20px;
#         text-align: left;
#         box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
#         margin-left: 0;
#         animation: blink 1.5s infinite;
#     }
#     @keyframes blink {
#         0% { opacity: 0.2; }
#         50% { opacity: 1; }
#         100% { opacity: 0.2; }
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Display the conversation history in a bubbled format
# chat_container = st.container()  # Create a container for chat

# # Create a form to handle the user input and response submission
# with st.form(key='question_form', clear_on_submit=True):
#     question = st.text_input("Your question:", "", key="input_box", placeholder="Type your question here...", label_visibility="collapsed")

#     # Submit button inside the form
#     submit_button = st.form_submit_button(label="Ask Jarvis")

#     # Handle the form submission
#     if submit_button and question:
#         # Display the user's question immediately
#         st.session_state.conversation_history.append({"role": "user", "content": question})
        
#         # Render the chat immediately after the user's input
#         with chat_container:
#             for entry in st.session_state.conversation_history:
#                 if entry["role"] == "user":
#                     st.markdown(f'<div class="user-bubble">{entry["content"]}</div>', unsafe_allow_html=True)
#                 else:
#                     st.markdown(f'<div class="jarvis-bubble">{entry["content"]}</div>', unsafe_allow_html=True)

#         # Create the response placeholder inside the chat container
#         with chat_container:
#             response_placeholder = st.empty()
#             response_placeholder.markdown(f'<div class="blinking-bubble"></div>', unsafe_allow_html=True)
        
#         # Artificial delay to simulate thinking (optional)
#         time.sleep(1)  # Simulate processing time

#         # Generate Jarvis's response
#         response = get_chatbot_response(question)
#         st.session_state.conversation_history.append({"role": "jarvis", "content": response})

#         # Replace the blinking bubble with the actual response
#         response_placeholder.empty()  # Clear the previous "blinking" bubble
#         with response_placeholder.container():
#             st.markdown(f'<div class="jarvis-bubble">{response}</div>', unsafe_allow_html=True)

# # Clear session history (for a fresh start)
# if st.button("Clear Conversation", key="clear_button"):
#     st.session_state.conversation_history = []  # Reset conversation history
#     st.rerun()  # This will reload the app to reflect the cleared history




# import streamlit as st
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.vectorstores import FAISS
# from langchain_cohere import CohereEmbeddings
# import cohere
# import time

# # Load the PDF and prepare the content
# loader = PyPDFLoader('Resume.pdf')
# documents = loader.load()
# YOUR_NAME = 'Ruthvik'

# # API key for Cohere
# COHERE_API_KEY = "VegoJTcGcEhVI5taUccJDtXuFmgRnjXqGsQjsXMQ"

# # Initialize embeddings and vector store
# embeddings = CohereEmbeddings(model="embed-multilingual-v3.0", cohere_api_key=COHERE_API_KEY)
# vector_store = FAISS.from_documents(documents, embeddings)

# # Initialize Cohere client directly
# cohere_client = cohere.Client(api_key=COHERE_API_KEY)

# # Function to generate a response using Cohere
# def generate_response(prompt):
#     try:
#         response = cohere_client.generate(
#             model='command-r-plus',
#             prompt=prompt,
#             max_tokens=300,  # Adjust this value if needed
#             temperature=0.5
#         )
#         return response.generations[0].text if response.generations else "I'm sorry, I couldn't find an answer to that."
#     except Exception as e:
#         return f"An error occurred: {e}"

# # Function to check if a response ends properly
# def ensure_proper_ending(response):
#     response = response.strip()
#     words = response.split()
    
#     # Check if the response ends with a proper punctuation mark and has a significant word count
#     if not response.endswith(('.', '!', '?')) and len(words) > 199:
#         # Mark that the response is incomplete
#         st.session_state.incomplete_response = response
#         response += " ...it seems I didn't finish. Would you like more details?"
#     else:
#         # If the response is complete, clear the incomplete flag
#         st.session_state.incomplete_response = None
    
#     return response



# # Function to retrieve relevant chunks using the vector store
# def retrieve_relevant_chunks(question):
#     query_embedding = embeddings.embed_query(question)
#     docs = vector_store.similarity_search_by_vector(query_embedding, k=5)
#     return " ".join([doc.page_content for doc in docs])

# # Function to get a response from Jarvis
# def get_chatbot_response(question):
#     if question.lower() in ["hello", "hi", "hey", "greetings", "who are you"]:
#         return f"Hello! I am Jarvis, {YOUR_NAME}'s personal assistant. How can I assist you today?"
#     elif question.lower() in ["who created you"]:
#         return f"{YOUR_NAME} brought me to life on August 22nd, 2024."
#     elif question.lower() == "yes" and st.session_state.get('incomplete_response'):
#         # Continue from the incomplete response
#         previous_response = st.session_state.incomplete_response
#         return generate_response(f"Please continue the following response: {previous_response}")

#     # Retrieve the most relevant chunks of text
#     relevant_content = retrieve_relevant_chunks(question)

#     prompt = f"""
#     As {YOUR_NAME}'s assistant, your task is to provide a direct and clear answer to the following question: '{question}'.
#     - Use the relevant information from {YOUR_NAME}'s background and skills provided below.
#     - Focus solely on answering the question directly.

#     Relevant information:
#     {relevant_content}
#     """

#     response = generate_response(prompt)
#     response = ensure_proper_ending(response)

#     if "I'm sorry" in response or len(response.strip()) < 20:
#         response = "I'm sorry, I couldn't find a relevant answer to your question."

#     return response

# # Streamlit UI
# st.set_page_config(page_title="Jarvis - Your Personal Assistant", layout="centered")

# st.title("Jarvis - Your Personal Assistant")
# st.write("Ask me anything about Ruthvik!")

# # Initialize session state for conversation history and incomplete responses if it doesn't exist
# if 'conversation_history' not in st.session_state:
#     st.session_state.conversation_history = []

# if 'incomplete_response' not in st.session_state:
#     st.session_state.incomplete_response = None

# # CSS styling for chat bubbles, text input, and blinking animation
# st.markdown("""
#     <style>
#     .jarvis-bubble {
#         background-color: #e0f7fa;
#         border-radius: 15px;
#         padding: 10px;
#         margin-bottom: 10px;
#         max-width: 70%;
#         text-align: left;
#         box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
#         color: black;
#         margin-left: 0;
#     }
#     .user-bubble {
#         background-color: #c8e6c9;
#         border-radius: 15px;
#         padding: 10px;
#         margin-bottom: 10px;
#         max-width: 70%;
#         text-align: right;
#         margin-left: auto;
#         box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
#         color: black;
#     }
#     .chat-container {
#         max-height: 400px;
#         overflow-y: auto;
#         padding-right: 15px;
#         padding-left: 15px;
#         background-color: #f5f5f5;
#         border-radius: 10px;
#         box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
#         padding: 20px;
#     }
#     .textbox {
#         padding: 10px;
#         border-radius: 15px;
#         border: 1px solid #ccc;
#         width: 100%;
#         color: black;
#     }
#     .button {
#         background-color: #007bff;
#         color: white;
#         padding: 10px 20px;
#         border-radius: 5px;
#         border: none;
#         cursor: pointer;
#         font-size: 16px;
#     }
#     .button:hover {
#         background-color: #0056b3;
#     }
#     .blinking-bubble {
#         background-color: #e0f7fa;
#         border-radius: 15px;
#         padding: 10px;
#         margin-bottom: 10px;
#         max-width: 70%;
#         height: 20px;
#         text-align: left;
#         box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
#         margin-left: 0;
#         animation: blink 1.5s infinite;
#     }
#     @keyframes blink {
#         0% { opacity: 0.2; }
#         50% { opacity: 1; }
#         100% { opacity: 0.2; }
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Display the conversation history in a bubbled format
# chat_container = st.container()  # Create a container for chat

# # Create a form to handle the user input and response submission
# with st.form(key='question_form', clear_on_submit=True):
#     question = st.text_input("Your question:", "", key="input_box", placeholder="Type your question here...", label_visibility="collapsed")

#     # Submit button inside the form
#     submit_button = st.form_submit_button(label="Ask Jarvis")

#     # Handle the form submission
#     if submit_button and question:
#         # Display the user's question immediately
#         st.session_state.conversation_history.append({"role": "user", "content": question})
        
#         # Render the chat immediately after the user's input
#         with chat_container:
#             for entry in st.session_state.conversation_history:
#                 if entry["role"] == "user":
#                     st.markdown(f'<div class="user-bubble">{entry["content"]}</div>', unsafe_allow_html=True)
#                 else:
#                     st.markdown(f'<div class="jarvis-bubble">{entry["content"]}</div>', unsafe_allow_html=True)

#         # Create the response placeholder inside the chat container
#         with chat_container:
#             response_placeholder = st.empty()
#             response_placeholder.markdown(f'<div class="blinking-bubble"></div>', unsafe_allow_html=True)
        
#         # Artificial delay to simulate thinking (optional)
#         time.sleep(1)  # Simulate processing time

#         # Generate Jarvis's response
#         response = get_chatbot_response(question)
#         st.session_state.conversation_history.append({"role": "jarvis", "content": response})

#         # Replace the blinking bubble with the actual response
#         response_placeholder.empty()  # Clear the previous "blinking" bubble
#         with response_placeholder.container():
#             st.markdown(f'<div class="jarvis-bubble">{response}</div>', unsafe_allow_html=True)

# # Clear session history (for a fresh start)
# if st.button("Clear Conversation", key="clear_button"):
#     st.session_state.conversation_history = []  # Reset conversation history
#     st.rerun()  #














import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings
import cohere
import time

# Load the PDF and prepare the content
loader = PyPDFLoader('Resume.pdf')
documents = loader.load()
YOUR_NAME = 'Ruthvik'

# API key for Cohere
COHERE_API_KEY = "VegoJTcGcEhVI5taUccJDtXuFmgRnjXqGsQjsXMQ"

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
