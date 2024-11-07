
from utils.motion_Aris import ArisController
import time

controller = ArisController('192.168.1.167')


# 주문 응답을 처리하고 로봇 동작을 수행하는 함수
def process_order_response(response_text):
    # 응답 문자열에서 각 항목을 줄바꿈 기준으로 분리
    lines = response_text.strip().split("\n")
    
    # 각 줄에서 제품명을 확인하고, 조건에 맞는 로봇 동작 호출
    for line in lines:
        line = line.strip()
        
        # 각 제품명이 해당 줄에 있는지 확인
        if "코코볼" in line:
            print("Detected: 코코볼")
            print("\n")
            print("아이스크림 기계가 작동중입니다. 뒤로 물러나 주세요")
            controller.Pickup_Ice1()
            controller.deliverIceCream()
            controller.ToppingChoice('1')
            controller.ice1_Putback()
            print("아이스크림이 완료 되었습니다. 맛있게 드세요")
            controller.pressEnd()
            
        elif "시리얼" in line:
            print("Detected: 시리얼")
            print("\n")
            print("아이스크림 기계가 작동중입니다. 뒤로 물러나 주세요")
            controller.Pickup_Ice1()
            controller.deliverIceCream()
            controller.ToppingChoice('2')
            controller.ice1_Putback()
            print("아이스크림이 완료 되었습니다. 맛있게 드세요")
            controller.pressEnd()
        elif "아몬드" in line:
            print("Detected: 아몬드")
            print("\n")
            print("아이스크림 기계가 작동중입니다. 뒤로 물러나 주세요")
            controller.Pickup_Ice1()
            controller.deliverIceCream()
            controller.ToppingChoice('3')
            controller.ice1_Putback()
            print("아이스크림이 완료 되었습니다. 맛있게 드세요")
            controller.pressEnd()

        else:
            print(f"제품이 확인되지 않은 줄: {line}")