import sys
from PySide6.QtWidgets import QApplication
from codes.controller import MainController

#main 함수
def main():
    controller.hello_world()

    # 프로그램 = 시작
    controller.start_program()

    controller.stop_program()


# 이 파일을 직접 실행할때 main 함수 실행
if __name__ == "__main__":
    main()