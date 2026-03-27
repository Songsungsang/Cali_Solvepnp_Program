from codes.window import MainWindow

class MainController:
    def __init__(self):
        # 1. View 인스턴스 생성
        self.view = MainWindow()
        
        # 2. 버튼 클릭 시 실행될 함수(Slot) 연결
        # 파이썬은 함수를 변수처럼 취급하므로 () 없이 이름만 적습니다.
        self.view.btn_action.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        """버튼 클릭 이벤트 핸들러"""
        print("🔔 [Controller] 버튼이 눌렸습니다. 로직을 실행합니다.")
        # 여기에 나중에 파일 탐색기나 OpenCV 로직이 들어갑니다.

    def show(self):
        """메인 창을 화면에 표시"""
        self.view.show()