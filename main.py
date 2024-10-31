from STT.stt import my_stt
from RAG.ragpipeline import RagPipeline


rag = RagPipeline()


while True :
    my_speech = my_stt()
    if my_speech == "종료" :
        break
    else :
        print('[고객님]')
        print(my_speech)
        answer = rag.generate_answer(my_speech)
        print()
        print('[AI 접수원]')
        print(answer)
        print('---'*30)
        print()
