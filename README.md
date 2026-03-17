# 📄 AI Document Chatbot

Hi! Welcome to my AI Document Chatbot project. This is a web application that lets you upload documents (PDF, Word, or Text files) and have a conversation with them. It uses AI to read the text, understand the context, and answer your specific questions based *only* on the document you uploaded.

## 🌟 Live Demo
You can test the live application right here: **[[Streamlit App Link](https://ai-document-chatbot-project.streamlit.app/)]**
*(Note: The AI API key is already securely configured on the backend, so you can just upload a file and start chatting immediately!)*

## 🛠️ How It Works (The Architecture)
This app is built using a **RAG (Retrieval-Augmented Generation)** pipeline. Here is the simple breakdown of what happens under the hood when you upload a file:

1. **Reading the File:** The app uses LangChain to extract the raw text from your PDF, DOCX, or TXT file.
2. **Chunking:** Since large documents have too much text to send to an AI all at once, the text is split into smaller, overlapping chunks.
3. **Creating Embeddings:** Those chunks of text are converted into numbers (vector embeddings) using a HuggingFace model (`all-MiniLM-L6-v2`) so the computer can quickly search them based on meaning.
4. **Vector Database:** The embeddings are stored in a local FAISS database for lightning-fast retrieval.
5. **Answering:** When you ask a question, the app finds the most relevant chunks of text from the database and sends them to the **Llama 3.1** model (via the Groq API) to generate a highly accurate, hallucination-free answer.

## ✨ Key Features
* **Multi-Format Upload:** Works natively with `.pdf`, `.docx`, and `.txt` files.
* **Smart Summarization:** Uses a "Map-Reduce" method to summarize large documents that would normally exceed standard AI memory limits.
* **Context-Aware Chat:** The AI is strictly instructed to answer based on the document provided.
* **Exportable History:** You can download your entire chat conversation as a text file for offline review.
* **Secure & Fast:** Built with Streamlit's secrets management and powered by Groq's ultra-low latency inference engine.

## 💻 Running it Locally
If you want to run this project on your own machine, follow these steps:

1. Clone this repository to your computer.
2. Create a virtual environment and activate it: `python -m venv venv`
3. Install the required packages: `pip install -r requirements.txt`
4. Create a `.streamlit` folder, and inside it, create a `secrets.toml` file. Add your Groq API key like this: `GROQ_API_KEY = "your_api_key_here"`
5. Run the app: `streamlit run app.py`
