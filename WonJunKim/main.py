import argparse
from utils import VideoFrameExtractor

def main():
    parser = argparse.ArgumentParser(description="OSS Term Project: Video to Image Converter")
    parser.add_argument("--src", required=True, help="입력 비디오 경로")
    parser.add_argument("--dst", default="./results", help="저장할 폴더 경로")
    parser.add_argument("--interval", type=int, default=10, help="프레임 저장 간격")
    
    args = parser.parse_args()
    
    print(f"--- Project by WonJunKim ---")
    converter = VideoFrameExtractor(args.src, args.dst, args.interval)
    converter.process()

if __name__ == "__main__":
    main()
