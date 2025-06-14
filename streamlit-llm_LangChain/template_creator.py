import os

# 원본 코드 파일에서 주석과 함수 정의는 유지하고, 나머지 코드 라인은 빈 줄로 대체하여 새로운 파일로 저장합니다.
def extract_comments_and_def_with_blank_lines(input_file: str, output_file: str):
    """
    Python 코드 파일에서 주석과 함수 정의는 유지하고, 코드 라인은 빈 줄로 대체하여 새로운 파일로 저장합니다.
    
    :param input_file: 원본 Python 코드 파일 경로
    :param output_file: 주석과 함수 정의, 빈 줄만 포함된 새로운 파일 경로
    """
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            stripped_line = line.strip()
            if stripped_line.startswith("#"):
                # 주석 라인은 그대로 기록
                outfile.write(line)
            elif stripped_line == "":
                # 빈 줄은 그대로 유지
                outfile.write(line)
            elif stripped_line.startswith("def "):
                # 함수 정의 라인은 그대로 유지
                outfile.write(line)
            else:
                # 코드 라인은 빈 줄로 대체
                outfile.write("\n")

# 현재 디렉터리의 모든 .py 파일 처리 (template_로 시작하는 파일은 제외)
def process_all_py_files():
    """
    현재 디렉터리의 모든 .py 파일을 읽어서 주석과 함수 정의는 유지하고,
    나머지 코드는 빈 줄로 대체한 후 'template_' 접두사를 붙여 저장합니다.
    'template_'로 시작하는 파일은 제외됩니다.
    """
    current_dir = os.getcwd()  # 현재 디렉터리 경로 가져오기
    py_files = [
        f for f in os.listdir(current_dir) 
        if f.endswith('.py') and not f.startswith('template_')
    ]  # .py 확장자 파일 중 'template_'로 시작하지 않는 파일만 선택

    for file in py_files:
        input_file = os.path.join(current_dir, file)  # 입력 파일 경로
        output_file = os.path.join(current_dir, f"template_{file}")  # 출력 파일 경로 (template_ 접두사 추가)
        print(f"Processing: {input_file} → {output_file}")
        extract_comments_and_def_with_blank_lines(input_file, output_file)

    print("\n✅ 'template_'로 시작하지 않는 모든 .py 파일이 변환되었습니다.")

# 메인 실행
if __name__ == "__main__":
    process_all_py_files()
