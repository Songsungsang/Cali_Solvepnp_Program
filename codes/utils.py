"""
이미지 넘기기, 이미지 업로드 등 
캘리브레이션과 solvepnp 작업을 뺀 작업들 모음
"""

# codes/utils.py
import os
from PySide6.QtWidgets import QFileDialog, QMessageBox, QGraphicsScene
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

def get_images_from_folder(folder_path):
    """
    주어진 폴더 경로 안에서 이미지 파일들만 찾아 절대 경로 리스트로 반환합니다.
    """
    file_paths = []
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
    
    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith(valid_extensions):
                full_path = os.path.join(folder_path, file_name)
                file_paths.append(full_path.replace('\\', '/'))
                
    return file_paths

def display_image(graphics_view, image_path):
    """
    QGraphicsView에 이미지를 크기에 맞춰 띄워주는 함수입니다.
    """
    if not image_path:
        return

    print(f"[utils.py] 화면에 이미지를 그립니다: {image_path}")
    
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

# 특정 오류시 경고 팝업 띄우기
def show_warning_msg(parent_window, title, message):
    QMessageBox.warning(parent_window, title, message)