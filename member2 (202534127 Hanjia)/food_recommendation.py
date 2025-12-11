import os
import csv
from transformers import AutoTokenizer

# 현재 이 .py 파일의 위치를 기준으로 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "menu_db.csv")

# Huggingface tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

def load_menu_csv(filepath=DB_PATH):
    menu_data = []
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            menu_data.append(row)
    return menu_data

# 키워드 추출 함수
def extract_keywords(text):
    keywords = []
    if "한식" in text: keywords.append("한식")
    if "중식" in text: keywords.append("중식")
    if "일식" in text: keywords.append("일식")
    if "양식" in text: keywords.append("양식")

    if "차가운" in text or "냉" in text: keywords.append("차가운")
    if "따뜻한" in text or "뜨거운" in text or "국물" in text: keywords.append("따뜻한")

    if "매운" in text or "매콤" in text: keywords.append("매콤한")
    if "순한" in text or "안 매운" in text: keywords.append("순한")

    if "밥" in text: keywords.append("밥")
    if "면" in text: keywords.append("면")

    return keywords

# 메뉴 추천 함수
def recommend_menu(keywords, menu_data):
    results = []
    for item in menu_data:
        if all(k in item.values() for k in keywords):
            results.append(item)
    return results

# 안내 메시지
def print_style_guide():
    print("\n 고를 수 있는 음식 스타일:")
    print("  - 종류: 한식, 중식, 일식, 양식")
    print("  - 온도: 따뜻한, 차가운")
    print("  - 맵기: 매콤한, 순한")
    print("  - 주재료: 밥, 면")
    print("예시: '따뜻한 면 요리, 중식이 먹고 싶어'")
    print("종료하려면 '종료'를 입력하세요.\n")

# 메인 실행
def main():
    menu_data = load_menu_csv()
    print("간단한 음식 추천 시스템입니다.")
    print_style_guide()

    while True:
        user_input = input("먹고 싶은 음식 스타일을 말해보세요: ")

        if user_input.strip().lower() in ["종료", "exit", "quit"]:
            print("시스템을 종료합니다. 안녕히 가세요!")
            break

        # Huggingface tokenizer 형식적 사용
        tokens = tokenizer.tokenize(user_input)
        print("입력 토큰:", tokens)

        keywords = extract_keywords(user_input)
        if not keywords:
            print("입력에서 인식된 키워드가 없습니다. 다시 시도해 주세요.")
            continue

        matched = recommend_menu(keywords, menu_data)
        if matched:
            print("\n추천 메뉴:")
            for item in matched:
                print(f"  - {item['name']} ({item['type']} / {item['temp']} / {item['spicy']} / {item['main']})")
        else:
            print("조건에 맞는 메뉴를 찾을 수 없습니다. 😢")

        print("\n" + "-"*50)
        print_style_guide()

# 실행
if __name__ == "__main__":
    main()
