from motion_Aris import ArisController
import time




def main():
    controller = ArisController('192.168.1.167')

    while True:
        
        print("\n아이스크림 위치")
        print("1. 왼쪽")
        print("2. 가운데")
        print("3. 오른쪽")
        print("0. 나가기")

        position = input("아이스크림 위치 번호를 알려주세요: ")
        
        print("\n토핑 메뉴")
        print("1. 아몬드")
        print("2. 시리얼")
        print("3. 코코볼")
        print("0. 나가기")

        choice = input("좋아하는 토핑의 번호 1,2,3중에 골라주세요: ")
        

        if position == "1":
            print("\n")
            print("아이스크림 기계가 작동중입니다. 뒤로 물러나 주세요")
            controller.Pickup_Ice1()
            controller.deliverIceCream()
            controller.ToppingChoice(choice)
            controller.ice1_Putback()
            print("아이스크림이 완료 되었습니다. 맛있게 드세요")
            controller.pressEnd()
        
        elif position == "2":
            print("\n")
            print("아이스크림 기계가 작동중입니다. 뒤로 물러나 주세요")
            controller.Pickup_Ice2()
            controller.deliverIceCream()
            controller.ToppingChoice(choice)
            controller.ice2_Putback()
            print("아이스크림이 완료 되었습니다. 맛있게 드세요")
            controller.pressEnd()

        elif position == "3":
            print("\n")
            print("아이스크림 기계가 작동중입니다. 뒤로 물러나 주세요")
            controller.Pickup_Ice3()
            controller.deliverIceCream()
            controller.ToppingChoice(choice)
            controller.ice3_Putback()
            print("아이스크림이 완료 되었습니다. 맛있게 드세요")
            controller.pressEnd()

        elif choice == "0":
            print("아이스크림 기계를 종료합니다")
            break
        
        else:
            print("메뉴 번호만 입력해주세요")
        


if __name__ == "__main__":
    main()
