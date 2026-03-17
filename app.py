import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Document Chatbot", page_icon="📄", layout="wide")
st.title("📄 AI Document Chatbot")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Add a subtle hover effect and glow to all buttons */
    div.stButton > button:first-child {
        border-radius: 8px;
        transition: all 0.3s ease-in-out;
        border: 1px solid #4F46E5;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
        border-color: #6366F1;
    }
    
    /* Style the text input box */
    .stTextInput input {
        border-radius: 8px;
        border: 1px solid #334155;
    }
    .stTextInput input:focus {
        box-shadow: 0 0 0 2px #4F46E5;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "raw_docs" not in st.session_state:
    st.session_state.raw_docs = None


# --- SIDEBAR: API KEY & UPLOAD ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=50) # Adds a cool AI icon
    st.title("Settings")
    
    st.divider()
    
    st.markdown("### 📄 Document Upload")
    uploaded_file = st.file_uploader("Upload PDF, Word, or TXT", type=["pdf", "docx", "txt"])
    
    st.caption("Max file size: 200MB")    

# --- DOCUMENT PROCESSING FUNCTION ---
def process_document(file):
    # 1. BULLETPROOF TXT HANDLING (Bypasses the loader crash)
    if file.name.endswith(".txt"):
        # Forcibly decode the file and replace any corrupted characters
        text_content = file.getvalue().decode("utf-8", errors="replace")
        docs = [Document(page_content=text_content, metadata={"source": file.name})]
        return docs

    # 2. PDF & DOCX HANDLING
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as temp_file:
        temp_file.write(file.getvalue())
        temp_file_path = temp_file.name

    if file.name.endswith(".pdf"):
        loader = PyPDFLoader(temp_file_path)
    elif file.name.endswith(".docx"):
        loader = Docx2txtLoader(temp_file_path)
    
    docs = loader.load()
    os.remove(temp_file_path) # Clean up temp file
    return docs

# --- MAIN LOGIC ---
if uploaded_file:  # <--- FIXED: Removed the undefined groq_api_key condition here
    # 1. Process File & Create Vector Store (Only if new file uploaded)
    if st.button("Process Document"):
        with st.spinner("Processing document and generating embeddings..."):
            docs = process_document(uploaded_file)
            st.session_state.raw_docs = docs
            
            # Split text into manageable chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(docs)
            
            # Create embeddings using SentenceTransformers
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            
            # Store in FAISS Vector Database
            st.session_state.vector_store = FAISS.from_documents(splits, embeddings)
            st.success("Document processed successfully! You can now ask questions or summarize.")

    # 2. Secure LLM Setup
    try:
        llm = ChatGroq(
            groq_api_key=st.secrets["GROQ_API_KEY"], 
            model_name="llama-3.1-8b-instant", 
            temperature=0.2
        )
    except Exception as e:
        st.error("API Key not found. Please ensure it is added to Streamlit Secrets.")
        st.stop()

    # 3. Summarization Feature
    if st.session_state.raw_docs:
        if st.button("📝 Summarize Document"):
            with st.spinner("Generating summary..."):
                # Using map_reduce to handle large documents that might exceed token limits
                summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
                summary = summary_chain.invoke(st.session_state.raw_docs)
                
                st.subheader("Document Summary")
                st.write(summary["output_text"])
                
                # Download button for summary
                st.download_button(
                    label="Download Summary",
                    data=summary["output_text"],
                    file_name="document_summary.txt",
                    mime="text/plain"
                )

    st.divider()

    # 4. Beautiful Chat Interface
    st.header("💬 Chat with your Document")

    # Display existing chat history with avatars
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Native Chat Input Box at the bottom of the screen
    if user_query := st.chat_input("Ask a question about your uploaded document..."):
        
        # 1. Display the user's message immediately
        with st.chat_message("user"):
            st.markdown(user_query)
        
        # 2. Add user message to state
        st.session_state.chat_history.append({"role": "user", "content": user_query})

        if st.session_state.vector_store:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Set up the RAG chain
                    retriever = st.session_state.vector_store.as_retriever()
                    
                    system_prompt = (
                        "You are an assistant for question-answering tasks. "
                        "Use the following pieces of retrieved context to answer the question. "
                        "If you don't know the answer, say that you don't know based on the document. "
                        "\n\nContext:\n{context}"
                    )
                    prompt = ChatPromptTemplate.from_messages([
                        ("system", system_prompt),
                        ("human", "{input}"),
                    ])
                    
                    question_answer_chain = create_stuff_documents_chain(llm, prompt)
                    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
                    
                    # Get response
                    response = rag_chain.invoke({"input": user_query})
                    answer = response["answer"]
                    
                    # Display the AI's answer
                    st.markdown(answer)
            
            # 3. Add AI message to state
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

    # 5. Download Output (Moved to a sleek expander)
    if st.session_state.chat_history:
        with st.expander("⚙️ Chat Options & Downloads"):
            chat_text_export = ""
            for chat in st.session_state.chat_history:
                role_name = "You" if chat["role"] == "user" else "AI"
                chat_text_export += f"{role_name}: {chat['content']}\n\n"
                
            st.download_button(
                label="📥 Download Chat History",
                data=chat_text_export,
                file_name="chat_history.txt",
                mime="text/plain",
                use_container_width=True
            )

elif not uploaded_file:
    st.info("👈 Please upload a document to begin.")