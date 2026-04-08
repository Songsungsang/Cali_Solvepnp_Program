from codes.window import MainWindow
import codes.utils as utils
import codes.cali as cali
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PySide6.QtUiTools import QUiLoader
import os

class UploadDialogController:
    def __init__(self, parent=None):
        # 1. upload_dialog.ui 파일 로드하기
        ui_path = os.path.join(os.path.dirname(__file__), "upload_dialog.ui")
        ui_file = QFile(ui_path)
        ui_file.open(QFile.ReadOnly)
        
        loader = QUiLoader()
        self.dialog = loader.load(ui_file, parent) 
        ui_file.close()

        # 이 self.dialog가 바로 화면에 뜰 팝업창 객체입니다. (parent를 넣어 중앙에 뜨게 함)
        self.dialog.radio_left.setChecked(True)

        # 2. 결과 데이터 저장용 변수
        self.folder_path = ""
        self.is_left = True

        # 3. 이벤트 연결 (Designer에서 지어준 objectName 사용)
        self.dialog.btn_open.clicked.connect(self.on_open_clicked)
        self.dialog.btn_confirm.clicked.connect(self.on_confirm_clicked)
        self.dialog.btn_cancel.clicked.connect(self.dialog.reject) # 취소 누르면 창 닫기

    def on_open_clicked(self):
        folder = QFileDialog.getExistingDirectory(self.dialog, "이미지 폴더 선택")
        if folder:
            self.folder_path = folder
            self.dialog.path_input.setText(folder) # ui의 QLineEdit에 경로 글자 쓰기

    def on_confirm_clicked(self):
        if not self.folder_path:
            QMessageBox.warning(self.dialog, "경고", "열기 버튼을 눌러 폴더를 먼저 선택해주세요!")
            return

        # 확인 버튼을 누르면 라디오 버튼 상태를 변수에 저장하고 창 닫기 (성공 상태로)
        self.is_left = self.dialog.radio_left.isChecked()
        self.dialog.accept()

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
        self.view.ui.cali_image_upload.clicked.connect(self.on_upload_clicked) # 이미지 업로드
        self.view.ui.prevImage.clicked.connect(self.on_prev_clicked) # 이전
        self.view.ui.nextImage.clicked.connect(self.on_next_clicked) # 다음
        self.view.ui.cali_start.clicked.connect(self.on_cali_clicked) # 캘리브레이션 실행

    # 버튼 클릭에 대한 실제 처리
    # utils, cali, solvepnp 등에게 실제 처리 맡기기
    # 이미지 업로드
    def on_upload_clicked(self):
        # 1. 방금 만든 다이얼로그 컨트롤러 생성
        upload_popup = UploadDialogController(self.view.ui)
        
        # 2. 창을 띄우고(exec), 사용자가 '확인'을 눌러서 성공(Accepted)했는지 체크
        if upload_popup.dialog.exec() == QDialog.Accepted:
            
            # 팝업창 안에 저장된 데이터 뽑아오기
            paths = utils.get_images_from_folder(upload_popup.folder_path)
            self.left_or_right = "L" if upload_popup.is_left else "R"
            
            print(f"📂 설정된 폴더: {paths}")
            print(f"📷 설정된 카메라 방향: {self.left_or_right}")

        # 결과가 있다면 UI 업데이트
        if paths:
            self.image_paths = paths  # 컨트롤러에 경로 저장
            self.image_total = len(self.image_paths)

            # UI 파일에 만들어둔 라벨들 업데이트
            self.view.ui.cali_image_status.setText(f"{self.image_total}장 로드 완료")
            self.view.ui.cali_image_path.setText(paths[0]) # 첫번째 이미지의 경로 표시
            self.view.ui.cali_image_number.setText(f"1 / {self.image_total}")

            # 디스플레이로 보여줄 이미지의 번호 첫번호 0으로 지정
            self.current_image_index = 0

            # 업로드 된 이미지 보여주기
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
        left_right = self.left_or_right
        
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