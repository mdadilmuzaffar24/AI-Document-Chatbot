# 📄 AI Document Chatbot

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.34.0-FF4B4B.svg)
![LangChain](https://img.shields.io/badge/LangChain-Integration-green.svg)
![Llama3](https://img.shields.io/badge/Meta-Llama_3.1-black.svg)
![Groq](https://img.shields.io/badge/Groq-LPU_Inference-f56529.svg)

Hi! Welcome to my AI Document Chatbot project. This is a web application that lets you upload documents (PDF, Word, or Text files) and have a conversation with them. It uses AI to read the text, understand the context, and answer your specific questions based *only* on the document you uploaded.

An advanced, cloud-hosted Retrieval-Augmented Generation (RAG) application that allows users to securely query, analyze, and summarize complex unstructured documents. Built with Python and Streamlit, this tool leverages state-of-the-art Large Language Models (LLMs) to provide precise, context-aware answers based strictly on user-uploaded data, effectively eliminating AI hallucinations.


## 🌟 Live Demo
You can test the live application right here: **[[Streamlit App Link](https://ai-document-chatbot-project.streamlit.app/)]**
*(Note: The AI API key is already securely configured on the backend, so you can just upload a file and start chatting immediately!)*

## 🏗️ System Architecture 
This project implements a complete RAG pipeline, transforming raw unstructured documents into a searchable vector space before passing contextual context to the LLM.

1. **Document Ingestion:** Natively processes `.pdf`, `.docx`, and `.txt` formats using LangChain document loaders.
2. **Text Chunking:** Utilizes `RecursiveCharacterTextSplitter` (Chunk Size: 1000, Overlap: 200) to optimize context windows and prevent data loss across chunk boundaries.
3. **Vector Embeddings:** Transforms text chunks into high-dimensional vectors using the HuggingFace `all-MiniLM-L6-v2` embedding model.
4. **Vector Store:** Stores embeddings in a local **FAISS** (Facebook AI Similarity Search) database for lightning-fast semantic retrieval.
5. **Inference Engine:** Retrieves the top-$K$ most relevant document chunks and injects them into the prompt for **Meta Llama 3.1 (8B-Instant)** via the Groq API, ensuring ultra-low latency generation.

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

* ## 💻 Tech Stack
* **Frontend:** Streamlit (Custom CSS/Dark Theme)
* **Orchestration:** LangChain
* **Embeddings:** HuggingFace / SentenceTransformers
* **Vector Database:** FAISS
* **LLM:** Llama 3.1 (Hosted on Groq)
* **Deployment:** Streamlit Community Cloud (Linux/Python 3.11 Environment)

## 💻 Running it Locally
If you want to run this project on your own machine, follow these steps:

1. Clone this repository to your computer.
2. Create a virtual environment and activate it: `python -m venv venv`
3. Install the required packages: `pip install -r requirements.txt`
4. Create a `.streamlit` folder, and inside it, create a `secrets.toml` file. Add your Groq API key like this: `GROQ_API_KEY = "your_api_key_here"`
5. Run the app: `streamlit run app.py`
