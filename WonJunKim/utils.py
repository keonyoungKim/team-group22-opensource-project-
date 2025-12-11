import cv2
import os
from tqdm import tqdm

class VideoFrameExtractor:
    def __init__(self, source_path, save_dir, interval=10):
        self.source_path = source_path
        self.save_dir = save_dir
        self.interval = interval

    def process(self):
        # 영상 파일이 실제로 있는지 확인
        if not os.path.exists(self.source_path):
            print(f"[Error] 파일을 찾을 수 없습니다: {self.source_path}")
            return

        # 저장할 폴더가 없으면 자동 생성
        os.makedirs(self.save_dir, exist_ok=True)
        
        # OpenCV로 영상 불러오기
        cap = cv2.VideoCapture(self.source_path)
        if not cap.isOpened():
            print("[Error] 영상을 열 수 없습니다.")
            return

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"[Info] 전체 프레임 수: {total_frames}장")
        print(f"[Info] 저장 간격: {self.interval} 프레임마다 저장")
        
        count = 0
        saved = 0
        
        # 진행률 표시바 (tqdm) 생성
        pbar = tqdm(total=total_frames, desc="Processing")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 지정한 간격(interval)마다 이미지 저장
            if count % self.interval == 0:
                filename = os.path.join(self.save_dir, f"frame_{saved:04d}.jpg")
                cv2.imwrite(filename, frame)
                saved += 1
            
            count += 1
            pbar.update(1)
                
        cap.release()
        pbar.close()
        print(f"\n[Done] 총 {saved}장의 이미지가 '{self.save_dir}' 폴더에 저장되었습니다.")