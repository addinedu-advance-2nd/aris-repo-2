from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.camera_service import open_camera, close_camera, get_camera_frame
import asyncio
import cv2
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()

# ThreadPoolExecutor를 통해 WebSocket 송출 작업 분리
executor = ThreadPoolExecutor(max_workers=2)

@router.websocket("/ws/stream")
async def camera_stream(websocket: WebSocket, camera_id: int):
    """WebSocket을 통해 특정 카메라 스트림을 제공합니다."""
    await websocket.accept()
    print(f"Client connected for Camera {camera_id} stream.")

    cap = open_camera(camera_id)
    if cap is None:
        await websocket.send_text("Failed to open camera.")
        await websocket.close()
        return

    try:
        while True:
            # 절대 스트리밍이 끊기지 않게 하기 위해
            frame = await asyncio.get_event_loop().run_in_executor(executor, get_camera_frame, camera_id)
            if frame is None:
                print(f"Failed to capture frame from Camera {camera_id}. Retrying...")
                await asyncio.sleep(0.05)  # 프레임 캡처 실패 시 재시도
                continue

            # 프레임을 JPEG로 인코딩
            _, jpeg_frame = cv2.imencode('.jpg', frame)
            jpeg_frame = jpeg_frame.tobytes()

            # WebSocket을 통해 프레임 전송
            try:
                await websocket.send_bytes(jpeg_frame)
            except WebSocketDisconnect:
                print(f"Client disconnected from Camera {camera_id}.")
                break

            await asyncio.sleep(0.05)  # 20 FPS 제한

    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        close_camera(camera_id)
        await websocket.close()
        print(f"Camera {camera_id} stream closed.")
