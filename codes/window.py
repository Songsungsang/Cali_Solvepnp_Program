"""
프로그램의 UI의 역할을 맡아주는 파일
실제 상호작욕은 controller에서 처리
"""

import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class MainWindow:
    def __init__(self):
        # 현재 경로의 window.ui 찾기
        ui_path = os.path.join(os.path.dirname(__file__), "window.ui")
        
        # ui 파일 열기
        ui_file = QFile(ui_path)
        ui_file.open(QFile.ReadOnly)
        
        # 3. QUiLoader를 이용해 ui 로드
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        
        ui_file.close()