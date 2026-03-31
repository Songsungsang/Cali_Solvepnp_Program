import cv2
import numpy as np
import os
import glob

def run_calibration(width, height, square_size, image_paths):

    CHECKERBOARD = (width, height)

    # 3D 포인트들을 위한 실제 세상의 좌표계 정의
    SQUARE_SIZE = square_size # 본인이 가진 체커보드 한 칸의 실제 길이 (mm 단위)
    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2) * SQUARE_SIZE # 마지막에 한칸 길이만큼 곱함
    # 항목 변수. 코너 찾기의 최대 횟수, 코너 위치가 변경 되었다 인정할 최소 이동 거리 등
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # 결과물이 들어갈 폴더
    result_folder = "result/calibration"

    # 각 체커보드 이미지의 3D 포인트를 저장하기 위한 벡터
    objpoints = []
    # 각 체커보드 이미지의 2D 포인트를 저장하기 위한 벡터
    imgpoints = []

    for i, fname in enumerate(image_paths):
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # 체커보드의 모서리=코너들 찾음
        # 원하는 코너의 갯수들을 모두 찾으면 ret = True
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, 
            cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
        
        """
        If desired number of corner are detected,
        we refine the pixel coordinates and display
        them on the images of checker board
        """
        if ret == True:
            objpoints.append(objp)
            # refining pixel coordinates for given 2d points.
            corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
            
            imgpoints.append(corners2)
    
            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
            print("Image drawing...!")
            #resized_img = cv2.resize(img, (1000, 750))
            # 2. 저장할 파일명 구성 (예: checker_drawing/image_0.jpg)
            # i는 0부터 시작하므로 1부터 시작하고 싶다면 i+1을 사용하세요.
            save_path = os.path.join(checker_folder, f'image_{i}.jpg')

            # 3. 이미지 저장
            cv2.imwrite(save_path, img)
            print(f"저장 완료: {save_path}")
    
    h,w = img.shape[:2] # 이미지의 가로세로. 현재 코드에서 의미 없음. gray.shape[::-1]가 그 역할을 하는 중
    
    """
    Performing camera calibration by
    passing the value of known 3D points (objpoints)
    and corresponding pixel coordinates of the
    detected corners (imgpoints)
    """
    #실제 calibration 수행
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None)

    # 전체 이미지에 대한 개별 오차 계산
    # 1.6, 0.8등 유독 튀는 오차값이 ret 값에도 큰 영향을 줌.
    total_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        print(f"이미지 [{i}] 오차: {error:.4f}") # 각 사진의 오류 출력
        total_error += error

    print(f"\n최종 평균 오차: {total_error/len(objpoints):.4f}")
    print("----------- \n\n")
    print("Re-projection Error : ")
    print(ret)
    print("Camera matrix : \n")
    print(mtx)
    print("dist : ")
    print(dist)
    print("rvecs : \n")
    print(rvecs)
    print("tvecs : \n")
    print(tvecs)
    print("----------- \n\n")