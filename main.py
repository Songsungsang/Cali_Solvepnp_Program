import sys
from PySide6.QtWidgets import QApplication
from codes.controller import MainController

#main 함수
def main():
    # 애플리케이션 생성
    app = QApplication(sys.argv)

    # 프로그램 창 생성 및 화면에 표시
    controller = MainController()
    controller.show()

    # 사용자 종료까지 입력값 무한대기
    sys.exit(app.exec())


# 이 파일을 직접 실행할때 main 함수 실행
if __name__ == "__main__":
    main()