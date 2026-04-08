from codes.window import MainWindow, UploadDialog
import codes.utils as utils
import codes.cali as cali
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox, QGraphicsView

class UploadDialogController:
    # 기본값 선언, 기본값을 "folder"로 하되, 파라미터로 mode를 받을 수 있도록
    def __init__(self, parent=None, mode="folder"):
        self.view = UploadDialog(parent)

        # 결과 저장용 데이터 변수
        self.mode = mode           # 현재 모드 ("folder" 또는 "file")
        self.selected_path = ""    # 폴더든 파일이든 선택된 경로를 저장
        self.view.dialog.radio_left.setChecked(True) # 이미지 방향 기본값 왼쪽으로 설정
        self.is_left = True

        # 모드에 따라 창 제목과 안내 문구를 다르게 설정
        if self.mode == "folder":
            self.view.dialog.setWindowTitle("이미지 폴더 및 방향 설정")
            self.view.dialog.path_input.setPlaceholderText("이미지 폴더를 선택하세요...")
        else:
            self.view.dialog.setWindowTitle("단일 이미지 및 방향 설정")
            self.view.dialog.path_input.setPlaceholderText("이미지 파일을 선택하세요...")

        # 이벤트 연결
        self.view.dialog.btn_open.clicked.connect(self.on_open_clicked)
        self.view.dialog.btn_confirm.clicked.connect(self.on_confirm_clicked)
        self.view.dialog.btn_cancel.clicked.connect(self.view.dialog.reject)

    def on_open_clicked(self):
        # 모드에 따라 탐색기의 종류(폴더 vs 파일)를 다르게 띄우도록
        if self.mode == "folder":
            path = QFileDialog.getExistingDirectory(self.view.dialog, "이미지 폴더 선택")
        else:
            # 파일 모드
            path, _ = QFileDialog.getOpenFileName(
                self.view.dialog, 
                "이미지 파일 선택", 
                "", 
                "Image Files (*.png *.jpg *.jpeg *.bmp)"
            )

        if path:
            self.selected_path = path
            self.view.dialog.path_input.setText(path)

    def on_confirm_clicked(self):
        if not self.selected_path:
            QMessageBox.warning(self.view.dialog, "경고", "열기 버튼을 눌러 경로를 먼저 지정해주세요!")
            return

        self.is_left = self.view.dialog.radio_left.isChecked()
        self.view.dialog.accept()

class MainController:
    def __init__(self):
        # View 인스턴스 = 메인 화면 생성
        self.view = MainWindow()
        
        # 컨트롤러의 변수들 초기선언
        self.image_paths = [] # 이미지 경로 빈 리스트로 초기화
        self.image_total = 0  # 총 이미지 수 초기화
        self.current_image_index = 0 # 현재 인덱스 초기화

        # 캘리브레이션 탭의 버튼들에 대한 처리
        # 버튼 클릭시 이 이벤트로 연결 
        self.view.ui.cali_image_upload.clicked.connect(self.on_cali_upload_clicked) # 이미지 업로드
        self.view.ui.prevImage.clicked.connect(self.on_prev_clicked) # 이전
        self.view.ui.nextImage.clicked.connect(self.on_next_clicked) # 다음
        self.view.ui.cali_start.clicked.connect(self.on_cali_clicked) # 캘리브레이션 실행

        # cali 이미지 뷰에 대한 기능 처리
        utils.enable_image_zoom(self.view.ui.cali_image_view)                   # 줌 기능
        self.view.ui.cali_image_view.setDragMode(QGraphicsView.ScrollHandDrag)  # 사진 드래그 기능

    # 버튼 클릭에 대한 실제 처리
    # utils, cali, solvepnp 등에게 실제 처리 맡기기
    # 이미지 업로드
    # 팝업창을 띄우고 결과(이미지 리스트, 방향) 반환
    def open_upload_dialog(self, mode):
        # 다이얼로그 컨트롤러 생성, 모드 전달
        upload_popup = UploadDialogController(self.view.ui, mode=mode)
        
        if upload_popup.view.dialog.exec() == QDialog.Accepted:
            selected_path = upload_popup.selected_path
            direction = "L" if upload_popup.is_left else "R"
            
            # 폴더 모드: utils를 통해 안의 사진들을 긁어옴
            if mode == "folder":
                paths = utils.get_images_from_folder(selected_path)
                if not paths:
                    utils.show_warning_msg(self.view.ui, "알림", "선택한 폴더에 이미지 파일이 없습니다.")
                    return None, None
                return paths, direction
                
            # 파일 모드: 한 장의 사진 경로를 그대로 리스트에 담아 반환
            elif mode == "file":
                return [selected_path], direction
                
        return None, None # 취소한 경우
    
    # 캘리브레이션 이미지 업로드, 폴더 입력
    def on_cali_upload_clicked(self):
        # 폴더 모드로 이미지 업로드
        paths, direction = self.open_upload_dialog(mode="folder")
        
        if paths:
            self.image_paths = paths
            self.cali_left_right = direction
            self.current_image_index = 0
            self.image_total = len(self.image_paths)
            
            # (기존 UI 업데이트 로직 실행)
            self.view.ui.cali_image_status.setText(f"{self.image_total}장 로드 완료 ({'왼쪽' if direction=='L' else '오른쪽'})")
            self.view.ui.cali_image_path.setText(self.image_paths[0])
            self.view.ui.cali_image_number.setText(f"1 / {self.image_total}")
            utils.display_image(self.view.ui.cali_image_view, self.image_paths[0])

    def on_prev_clicked(self):
        # 이미지가 없거나, 이미 첫 번째 번호면 무시
        if not self.image_paths or self.current_image_index <= 0:
            return


        self.current_image_index -= 1
        self.update_image_view()

    def on_next_clicked(self):
        # 이미지가 없거나, 이미 마지막 장이면 무시
        if not self.image_paths or self.current_image_index >= self.image_total - 1:
            return
        

        self.current_image_index += 1
        self.update_image_view()

    # 화면에 보여줄 이미지 업데이트
    def update_image_view(self):
        # 이미지 경로 없을시 리턴
        if not self.check_image_loaded():
            return
        
        print(f"{self.current_image_index} 번째 이미지")
        # 현재 경로와 이미지 전체 숫자
        current_path = self.image_paths[self.current_image_index]
        total_count = len(self.image_paths)

        # 이미지 표시
        utils.display_image(self.view.ui.cali_image_view, current_path)
        # 경로와 사진 번호 텍스트 업데이트
        self.view.ui.cali_image_path.setText(current_path)
        self.view.ui.cali_image_number.setText(f"{self.current_image_index + 1} / {total_count}")

    # 캘리브레이션 수행
    def on_cali_clicked(self):
        self.view.ui.cali_status.setText("캘리브레이션 진행 중")

        # 이미지 경로 없을시 리턴
        if not self.check_image_loaded():
            return

        # 박스들에서 입력값 불러오기
        width = self.view.ui.board_width.value()
        height = self.view.ui.board_height.value()
        sq_size = self.view.ui.square_size.value()
        left_right = self.cali_left_right
        
        # 입력값들 캘리브레이션에 입력
        cali_image_path = cali.run_calibration(width, height, sq_size, left_right, self.image_paths)

        # 완료시 캘리브레이션된 이미지 보여주기 및 관련 값 수정
        self.view.ui.cali_status.setText("캘리브레이션 진행 완료")
        self.image_paths = cali_image_path
        self.image_total = len(self.image_paths)
        self.current_image_index = 0
        self.update_image_view()

    # 이미지 업로드 검사
    def check_image_loaded(self):
        # 이미지 업로드 여부 확인, 없을 경우 경고창 띄움
        if not self.image_paths:
            utils.show_warning_msg(self.view.ui, "업로드 오류", "이미지를 먼저 업로드해주세요!")
            return False
        return True

    def show(self):
        # 실제 화면에 창을 띄우는 명령
        self.view.ui.show()