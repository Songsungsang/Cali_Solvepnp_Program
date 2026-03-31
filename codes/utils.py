"""
이미지 넘기기, 이미지 업로드 등 
캘리브레이션과 solvepnp 작업을 뺀 작업들 모음
"""

# codes/utils.py
import os
from PySide6.QtWidgets import QFileDialog, QMessageBox, QGraphicsScene
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

def handle_upload(parent_window):
    """
    사용자에게 파일/폴더 선택 여부를 묻고, 
    선택된 이미지 파일들의 절대 경로 리스트를 반환합니다.
    """
    # 1. 사용자에게 업로드 방식 묻기 (작은 팝업창)
    msg_box = QMessageBox(parent_window)
    msg_box.setWindowTitle("업로드 방식 선택")
    msg_box.setText("이미지를 어떻게 불러오시겠습니까?")
    
    # 버튼 2개 추가
    btn_files = msg_box.addButton("파일 여러 개 선택", QMessageBox.ActionRole)
    btn_folder = msg_box.addButton("폴더 통째로 선택", QMessageBox.ActionRole)
    msg_box.addButton("취소", QMessageBox.RejectRole)
    
    msg_box.exec() # 팝업 띄우고 대기
    
    file_paths = []

    # 2-A. [파일 여러 개 선택]을 누른 경우
    if msg_box.clickedButton() == btn_files:
        print("📂 [utils.py] 다중 파일 선택 모드")
        paths, _ = QFileDialog.getOpenFileNames(
            parent_window, 
            "이미지 파일 선택", 
            "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        file_paths = paths

    # 2-B. [폴더 통째로 선택]을 누른 경우
    elif msg_box.clickedButton() == btn_folder:
        print("📁 [utils.py] 폴더 선택 모드")
        folder_path = QFileDialog.getExistingDirectory(
            parent_window, 
            "이미지 폴더 선택"
        )
        
        if folder_path:
            # 폴더 안에서 이미지 확장자를 가진 파일만 걸러내기
            valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
            for file_name in os.listdir(folder_path):
                if file_name.lower().endswith(valid_extensions):
                    # 파일의 절대 경로를 만들어서 리스트에 추가
                    full_path = os.path.join(folder_path, file_name)
                    # 윈도우 역슬래시(\)를 슬래시(/)로 통일하여 경로 에러 방지
                    file_paths.append(full_path.replace('\\', '/'))

    # 3. 결과 정리
    if file_paths:
        print(f"✅ [utils.py] 총 {len(file_paths)}장의 이미지를 성공적으로 찾았습니다.")
    else:
        print("❌ [utils.py] 이미지 로딩이 취소되었거나 파일이 없습니다.")

    # 컨트롤러에게 경로 리스트(List) 반환
    return file_paths

def display_image(graphics_view, image_path):
    """
    QGraphicsView에 이미지를 크기에 맞춰 띄워주는 함수입니다.
    """
    if not image_path:
        return

    print(f"🖼️ [utils.py] 화면에 이미지를 그립니다: {image_path}")
    
    # 1. 도화지(Scene) 생성
    scene = QGraphicsScene()
    
    # 2. 이미지 파일(Pixmap) 불러오기
    pixmap = QPixmap(image_path)
    
    # 3. 도화지에 이미지 얹기
    scene.addPixmap(pixmap)
    
    # 4. 뷰(View)에 도화지 설정하기
    graphics_view.setScene(scene)
    
    # 5. 이미지가 뷰어 크기에 딱 맞게 자동 축소/확대되도록 설정 (비율 유지)
    graphics_view.fitInView(scene.itemsBoundingRect(), Qt.KeepAspectRatio)

def handle_prev_image(self):
    print("⬅️ 이전 이미지")

def handle_next_image(self):
    print("➡️ 다음 이미지")

# 특정 오류시 경고 팝업 띄우기
def show_warning_msg(parent_window, title, message):
    QMessageBox.warning(parent_window, title, message)