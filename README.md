# 🌿 Ayurveda Q/A Chatbot

An intelligent chatbot that allows users to upload **text-based Ayurveda PDFs** and ask questions directly from the content using **semantic search** and **LLM-based responses**.

---

## ✨ Features

- ✅ Upload Ayurveda PDFs (text-based only)
- 🔍 Ask natural-language questions based on uploaded content
- ✂️ Chunk text smartly using LangChain
- 🧠 Semantic search with MiniLM embeddings
- ⚡ Fast retrieval using **FAISS**
- 🤖 Powered by **LLaMA 3** via **Groq API**
- 💬 Easy-to-use interface via **Streamlit**

---

## 🧰 Tech Stack

| Component        | Technology                             |
|------------------|-----------------------------------------|
| Frontend         | Streamlit                              |
| Backend          | FastAPI                                |
| Embeddings       | HuggingFace MiniLM-L6-v2               |
| Vector Search    | FAISS                                  |
| Language Model   | LLaMA 3 via Groq API                   |
| PDF Processing   | PyMuPDF + LangChain                    |
| Prompting        | LangChain + Custom PromptTemplate      |
| Environment Var  | python-dotenv                          |

---

## ⚙️ How It Works

1. **Upload**: User uploads a **text-based PDF**
2. **Text Extraction**: PDF is read using **PyMuPDF**
3. **Chunking**: Text is broken into smaller pieces using **RecursiveCharacterTextSplitter**
4. **Embedding**: Chunks are embedded using **HuggingFace MiniLM**
5. **Vector DB**: Chunks are stored in a **FAISS** vector store
6. **Q&A**: A user asks a question → most relevant chunks are retrieved → **LLaMA 3** answers using those

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ayurveda-chatbot.git
cd ayurveda-chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv ayurveda_env
ayurveda_env\Scripts\activate  
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your `.env` File

Create a `.env` file with your Groq key:

```env
GROQ_API_KEY=your_groq_api_key
```

### 5. Run the Backend

```bash
python app.py
```

### 6. Run the Streamlit Frontend

```bash
streamlit run streamlit_app.py
```


