# app/routers/chatbot.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_service import RagPipeline
from app.services.robot_service import process_order_response  # 함수 임포트
import asyncio 

# 요청 데이터 구조 정의
class ChatRequest(BaseModel):
    question: str
    session_id: str = None

router = APIRouter()
rag_pipeline = RagPipeline()  # RAG 파이프라인 인스턴스 생성

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        print('[사용자]')
        print(request.question)
        answer = rag_pipeline.generate_answer(request.question, session_id=request.session_id)
        
        print('[AI]')
        print(answer)
        
        
        response_text = answer["answer"]
        asyncio.create_task(process_order_response_async(response_text))
        
        
        return {"answer": answer["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def process_order_response_async(response_text: str):
    # 로봇 제어 작업을 비동기로 처리
    process_order_response(response_text)