from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ayurveda_rag import create_retriever_from_pdf, generate_answer

# Global retriever
retriever = None

# Initialize FastAPI app
app = FastAPI()

# Allow frontend access(if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input model
class QARequest(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "Ayurveda PDF Chat API is running!"}

# Endpoint to upload PDF and create retriever
@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    global retriever
    contents = await file.read()
    retriever = create_retriever_from_pdf(contents)
    return {"message": "PDF uploaded and indexed successfully."}

# Endpoint to ask question
@app.post("/ask/")
async def ask_question(request: QARequest):
    if retriever is None:
        return {"error": "PDF not uploaded yet."}
    
    answer = generate_answer(request.question, retriever)
    return {"answer": answer}

# Run with python app.py (optional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=40000, reload=True)
