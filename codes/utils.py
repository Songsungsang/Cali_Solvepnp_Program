"""
이미지 넘기기, 이미지 업로드 등 
캘리브레이션과 solvepnp 작업을 뺀 작업들 모음
"""

# codes/utils.py
import os
from PySide6.QtWidgets import QFileDialog, QMessageBox, QGraphicsScene, QGraphicsView
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QObject, QEvent

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
    #graphics_view.fitInView(scene.itemsBoundingRect(), Qt.KeepAspectRatio)

# 줌 기능을 처리하는 이벤트 필터 클래스
class ZoomEventFilter(QObject):
    def __init__(self, view):
        super().__init__(view)
        self.view = view
        # 마우스 커서가 있는 위치를 중심으로 줌인/줌아웃 되도록 설정
        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def eventFilter(self, obj, event):
        # 뷰포트에서 마우스 휠 이벤트가 발생했을때
        if event.type() == QEvent.Wheel:
            angle = event.angleDelta().y()
            if angle > 0:
                factor = 1.15  # 휠을 위로 굴리면 15% 확대
            else:
                factor = 0.85  # 휠을 아래로 굴리면 15% 축소
            
            self.view.scale(factor, factor)
            return True # 이벤트 처리 완료
        
        return super().eventFilter(obj, event)

# zoom 함수를 위한 위한 헬퍼 함수
def enable_image_zoom(view_widget):
    # 지정된 QGraphicsView에 마우스 휠 줌 기능 장착
    zoom_filter = ZoomEventFilter(view_widget)
    view_widget.viewport().installEventFilter(zoom_filter)
    # 파이썬 메모리 정리(GC) 과정에서 필터가 삭제되지 않도록 위젯에 묶어둠
    view_widget._zoom_filter = zoom_filter

# 특정 오류시 경고 팝업 띄우기
def show_warning_msg(parent_window, title, message):
    QMessageBox.warning(parent_window, title, message)