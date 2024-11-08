# app/routers/chatbot.py
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.services.rag_service import RagPipeline
from concurrent.futures import ThreadPoolExecutor
import asyncio 

# 요청 데이터 구조 정의
class ChatRequest(BaseModel):
    question: str
    session_id: str = None

router = APIRouter()
rag_pipeline = RagPipeline()  # RAG 파이프라인 인스턴스 생성

# ThreadPoolExecutor 생성 (최대 2개의 스레드 사용)
executor = ThreadPoolExecutor(max_workers=2)

async def async_generate_answer(question: str, session_id: str = None):
    """RAG 모델 응답을 별도 스레드에서 비동기로 실행"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, rag_pipeline.generate_answer, question, session_id)


@router.post("/chat")
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    try:
        print('[사용자]')
        print(request.question)
        # answer = rag_pipeline.generate_answer(request.question, session_id=request.session_id)
        # answer = await asyncio.to_thread(rag_pipeline.generate_answer, request.question, session_id=request.session_id)
        answer = await async_generate_answer(request.question, session_id=request.session_id)
        
        response_text = answer["answer"]
        print('[AI]')
        print(response_text)
        
        return {"answer": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
