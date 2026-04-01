from codes.window import MainWindow
import codes.utils as utils
import codes.cali as cali

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
        # handle_upload 실행, 결과인 이미지 경로 받아오기
        paths = utils.handle_upload(self.view.ui)

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

        # utils의 업데이트 수행 함수 호출
        utils.update_ui_with_image(
            self.view.ui.cali_image_view, # 이미지 띄울 화면
            self.view.ui.cali_image_path, # 경로 라벨
            self.view.ui.cali_image_number, # 이미지 번호 라벨
            self.image_paths, # 이미지 경로
            self.current_image_index # 현재 이미지 번호
        )

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
        
        # 입력값들 캘리브레이션에 입력
        cali_image_path = cali.run_calibration(width, height, sq_size, self.image_paths)

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