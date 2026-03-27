"""
프로그램의 UI의 역할을 맡아주는 파일
실제 상호작욕은 controller에서 처리
"""

from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 창 제목과 기본 크기 설정
        self.setWindowTitle("Cali & PnP Tool")
        self.resize(800, 600)

        # 중앙 위젯 생성
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 세로 정렬 레이아웃 설정
        self.layout = QVBoxLayout(self.central_widget)

        # 이미지를 보여줄 라벨 (처음엔 텍스트 표시)
        self.image_label = QLabel("이미지를 불러와 주세요")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black; background-color: #f0f0f0;")
        self.layout.addWidget(self.image_label)

        # 동작 버튼
        self.btn_action = QPushButton("파일 열기")
        self.layout.addWidget(self.btn_action)