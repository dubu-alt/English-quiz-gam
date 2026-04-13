import json # JSON 파일 처리
import os   # 파일 존재 여부 확인
import sys  # 프로그램 제어

# import: 파이썬 표준 라이브러리를 불러옴
# json: 파일 데이터 저장 및 불러올 때 사용
# os: 파일 있는지 확인할 때 사용
# sys: 프로그램 종료할 때 사용

# ============================================================================
# Quiz 클래스 정의 관련
# ============================================================================
# 클래스(class): 관련된 데이터와 기능을 묶어서 정리하는 방법
# 퀴즈 하나를 하나의 객체로 생각하면 됨
# 예: 문제 + 선택지 4개 + 정답 = 1개의 퀴즈 객체

class Quiz:
    """
    개별 퀴즈를 나타내는 클래스
    
    속성(attribute):
        - question: 퀴즈 문제 (문자열)
        - choices: 4개의 선택지 (리스트)
        - answer: 정답 번호 1~4 (숫자)
    """
    
    def __init__(self, question, choices, answer):
        """
        __init__: 클래스가 처음 만들어질 때 자동으로 실행되는 메서드
        self: 이 객체 자신을 의미함
        
        예시:
            quiz1 = Quiz("What is 1+1?", ["1", "2", "3", "4"], 2)
            이렇게 하면 quiz1이라는 퀴즈 객체가 만들어짐
        """
        # self.question: 이 퀴즈 객체의 question이라는 속성에 값을 저장
        self.question = question
        # self.choices: 이 퀴즈 객체의 choices라는 속성에 선택지들을 저장
        self.choices = choices
        # self.answer: 이 퀴즈 객체의 answer라는 속성에 정답을 저장
        self.answer = answer
    
    def display(self, question_number=None):
        """
        퀴즈를 화면에 예쁘게 출력하는 메서드
        
        question_number: 문제 번호 (선택사항)
        
        동작:
            1. 문제 번호를 출력 (있으면)
            2. 문제를 출력
            3. 4개의 선택지를 1, 2, 3, 4 번호와 함께 출력
        """
        if question_number:
            # f-string: 문자열 안에 변수를 쉽게 넣을 수 있는 방법
            # f"문자 {변수} 문자" 형태로 사용
            print(f"\n[문제 {question_number}]")
        else:
            print()
        
        # 문제 출력
        print(self.question)
        
        # 선택지 출력
        # enumerate: 리스트의 각 요소와 함께 순번을 제공하는 함수
        # 예: enumerate(["A", "B", "C"]) → (1, "A"), (2, "B"), (3, "C")
        # idx는 0부터 시작하므로 idx+1을 사용해서 1부터 시작하게 함
        for idx, choice in enumerate(self.choices, 1):
            print(f"  {idx}. {choice}")
    
    def check_answer(self, user_answer):
        """
        사용자가 입력한 답이 정답과 같은지 확인하는 메서드
        
        user_answer: 사용자가 입력한 답 번호 (1~4)
        
        반환값(return):
            True: 정답일 때
            False: 오답일 때
        """
        # ==: 같은지 비교하는 연산자
        # if: 조건에 따라 다른 작업을 하는 명령어
        if user_answer == self.answer:
            return True  # 정답이면 True 반환
        else:
            return False  # 오답이면 False 반환
    
    def to_dict(self):
        """
        Quiz 객체를 딕셔너리로 변환하는 메서드
        
        왜 필요한가?
            - JSON 파일에 저장하려면 딕셔너리 형태여야 함
            - 객체를 직접 저장할 수 없음
        
        반환값: 딕셔너리 형태의 퀴즈 데이터
        """
        # 딕셔너리: {"키": 값} 형태로 데이터를 저장하는 자료구조
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        딕셔너리에서 Quiz 객체를 만드는 메서드 (역변환)
        
        @classmethod: 이 메서드는 인스턴스(self)가 아니라 클래스(cls) 자체에서 실행
        
        동작:
            JSON 파일에서 읽은 딕셔너리 → Quiz 객체로 변환
        
        예시:
            data = {"question": "1+1?", "choices": [...], "answer": 2}
            quiz = Quiz.from_dict(data)  # Quiz 객체 생성
        """
        # cls(): 클래스를 호출해서 새로운 객체를 만드는 것
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"]
        )

class QuizGame:
    """
    게임 전체를 관리하는 클래스
    
    역할:
        1. 메뉴 표시
        2. 사용자 입력받기
        3. 퀴즈 풀기
        4. 퀴즈 추가
        5. 데이터 저장/로드
    """
    
    def __init__(self, data_file="state.json"):
        """
        게임 초기화
        
        data_file: 데이터를 저장할 파일명 (기본값: state.json)
        """
        # 데이터 파일 경로 저장
        self.data_file = data_file
        
        # 퀴즈 리스트: 현재 등록된 모든 퀴즈를 저장할 리스트
        # 리스트: [1, 2, 3] 처럼 여러 값을 순서대로 저장
        self.quizzes = []
        
        # 최고 점수: 최고 점수 정보를 저장하는 딕셔너리
        self.best_score = {
            "correct": 0,      # 정답 개수
            "total": 0,        # 총 문제 수
            "percentage": 0.0  # 정답률 (%)
        }
        
        # 기본 퀴즈 데이터: 프로그램이 처음 실행될 때 사용
        # 8개의 영어 단어 퀴즈를 미리 정의함
        self.default_quizzes = [
            Quiz(
                "'happy'의 뜻은?",
                ["슬픈", "행복한", "화난", "피곤한"],
                2  # 정답: 2번 (행복한)
            ),
            Quiz(
                "'beautiful'의 뜻은?",
                ["못생긴", "아름다운", "작은", "큰"],
                2
            ),
            Quiz(
                "'brilliant'의 뜻은?",
                ["어두운", "천재적인", "나쁜", "느린"],
                2
            ),
            Quiz(
                "'courageous'의 뜻은?",
                ["겁먹는", "용감한", "약한", "게으른"],
                2
            ),
            Quiz(
                "'diligent'의 뜻은?",
                ["게으른", "근면한", "나쁜", "못생긴"],
                2
            ),
            Quiz(
                "'energetic'의 뜻은?",
                ["피곤한", "활기찬", "약한", "느린"],
                2
            ),
            Quiz(
                "'friendly'의 뜻은?",
                ["적대적인", "친근한", "나쁜", "차가운"],
                2
            ),
            Quiz(
                "'genuine'의 뜻은?",
                ["거짓된", "진정한", "나쁜", "이상한"],
                2
            ),
        ]
        
        # 프로그램 시작할 때 저장된 데이터 불러오기
        self.load_data()

    def display_menu(self):
        """
        메인 메뉴를 화면에 출력하는 메서드
        
        동작:
            화면에 메뉴 5가지를 보기 좋게 출력
        """
        # \n: 개행 (새로운 줄)
        # print(): 화면에 출력하는 함수
        print("\n" + "=" * 50)
        print("          영어 단어 퀴즈 게임")
        print("=" * 50)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 보기")
        print("4. 최고 점수 확인")
        print("5. 종료")
        print("=" * 50)
    
    def get_menu_choice(self):
        """
        사용자로부터 메뉴 선택을 입력받는 메서드
        
        동작:
            1. 사용자 입력받기
            2. 입력값이 1~5 사이의 숫자인지 확인
            3. 맞으면 그 숫자를 반환, 틀리면 다시 입력받기
        
        반환값: 1~5 사이의 숫자
        """
        # while True: 무한 반복 (조건이 거짓이 될 때까지)
        while True:
            try:
                # input(): 사용자로부터 입력받는 함수
                # .strip(): 앞뒤 공백을 제거하는 메서드
                choice = input("선택 (1-5): ").strip()
                
                # 빈 입력 확인
                if not choice:  # not: 거짓이면 참, 참이면 거짓 (반대)
                    print("빈 입력입니다. 1~5 사이의 숫자를 입력해주세요.")
                    continue  # 이 반복을 건너뛰고 while 루프의 처음으로 돌아감
                
                # int(): 문자열을 정수로 변환하는 함수
                # 만약 "abc" 같은 숫자가 아닌 것을 넣으면 에러 발생
                choice_num = int(choice)
                
                # 범위 확인
                # and: 두 조건이 모두 참이어야 참
                # or: 두 조건 중 하나라도 참이면 참
                if not (1 <= choice_num <= 5):
                    print("X 1~5 사이의 숫자를 입력해주세요.")
                    continue
                
                # 모든 조건을 통과했으면 숫자를 반환
                return choice_num
            
            # except: try 블록에서 에러가 발생했을 때 실행
            except ValueError:
                # 숫자가 아닌 것을 입력했을 때 발생하는 에러
                print("X 숫자를 입력해주세요.")

    def play_quiz(self):
        """
        퀴즈를 푸는 메서드
        
        동작:
            1. 퀴즈가 있는지 확인
            2. 각 퀴즈를 하나씩 출제
            3. 사용자 답 입력받기
            4. 정답/오답 판정
            5. 최종 점수 표시
            6. 최고 점수 갱신
        """
        # 퀴즈가 없으면 함수 종료
        if not self.quizzes:  # not: 빈 리스트는 거짓
            print("\nX 등록된 퀴즈가 없습니다.")
            return  # 함수 종료
        
        # 총 문제 수 출력
        print(f"\n📝 총 {len(self.quizzes)}개의 퀴즈가 있습니다.")
        # len(): 리스트의 길이를 반환하는 함수
        
        # 정답 개수를 세기 위한 변수
        correct_count = 0
        total_count = len(self.quizzes)
        
        # 각 퀴즈를 하나씩 처리
        # for 변수 in 리스트: 리스트의 각 요소를 차례대로 처리
        # enumerate(): 요소와 함께 순번(index)도 제공
        # 1부터 시작하도록 두 번째 인자로 1을 전달
        for idx, quiz in enumerate(self.quizzes, 1):
            # 퀴즈 출력 (1번, 2번, ... 형태로)
            quiz.display(idx)
            
            # 사용자 답 입력받기
            while True:
                try:
                    answer = input("답 (1-4): ").strip()
                    
                    if not answer:
                        print("빈 입력입니다. 1~4 사이의 숫자를 입력해주세요.")
                        continue
                    
                    answer_num = int(answer)
                    
                    if not (1 <= answer_num <= 4):
                        print("1~4 사이의 숫자를 입력해주세요.")
                        continue
                    
                    break  # 올바른 입력을 받으면 while 루프 탈출
                
                except ValueError:
                    print("숫자를 입력해주세요.")
            
            # 답 확인
            if quiz.check_answer(answer_num):
                print("정답입니다!")
                correct_count += 1  # +=: 기존 값에 1을 더하기
            else:
                # 오답일 때 정답을 알려줌
                print(f"오답입니다. 정답: {quiz.answer}번 ({quiz.choices[quiz.answer - 1]})")
        
        # 최종 결과 표시
        # /: 나누기
        percentage = (correct_count / total_count) * 100
        print("\n" + "=" * 50)
        print(f"결과: {correct_count}/{total_count} ({percentage:.1f}%)")
        # .1f: 소수점 첫째 자리까지만 표시
        print("=" * 50)
        
        # 최고 점수 갱신
        self.update_best_score(correct_count, total_count)
        
        # 데이터 저장
        self.save_data()
    
    def add_quiz(self):
        """
        새로운 퀴즈를 추가하는 메서드
        
        동작:
            1. 문제 입력받기
            2. 4개의 선택지 입력받기
            3. 정답 번호 입력받기
            4. 새로운 Quiz 객체 생성
            5. quizzes 리스트에 추가
            6. 파일에 저장
        """
        print("\n새 퀴즈 추가")
        print("-" * 50)
        
        # 문제 입력받기
        while True:
            # input(): 사용자 입력받기
            question = input("문제를 입력하세요: ").strip()
            if question:  # 문자열이 비어있지 않으면 참
                break  # while 루프 탈출
            print("빈 입력입니다. 문제를 입력해주세요.")
        
        # 선택지 입력받기
        choices = []  # 빈 리스트 생성
        for i in range(4):  # 4번 반복 (0, 1, 2, 3)
            while True:
                choice = input(f"선택지 {i+1}을(를) 입력하세요: ").strip()
                if choice:
                    break
                print("빈 입력입니다. 선택지를 입력해주세요.")
            
            # append(): 리스트에 요소를 추가하는 메서드
            choices.append(choice)
        
        # 정답 입력받기
        while True:
            try:
                answer = input("정답 번호 (1-4): ").strip()
                
                if not answer:
                    print("빈 입력입니다. 1~4 사이의 숫자를 입력해주세요.")
                    continue
                
                answer_num = int(answer)
                
                if not (1 <= answer_num <= 4):
                    print("1~4 사이의 숫자를 입력해주세요.")
                    continue
                
                break
            
            except ValueError:
                print("숫자를 입력해주세요.")
        
        # 새로운 Quiz 객체 생성
        new_quiz = Quiz(question, choices, answer_num)
        
        # 리스트에 추가
        self.quizzes.append(new_quiz)
        print("퀴즈가 추가되었습니다.")
        
        # 파일에 저장
        self.save_data()

    def display_quizzes(self):
        """
        등록된 모든 퀴즈를 목록으로 보여주는 메서드
        
        동작:
            1. 퀴즈가 있는지 확인
            2. 각 퀴즈의 문제와 선택지를 번호와 함께 출력
            3. 정답은 ✓ 마크로 표시
        """
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return
        
        print(f"\n📋 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 50)
        
        for idx, quiz in enumerate(self.quizzes, 1):
            # 퀴즈 번호와 문제 출력
            print(f"{idx}. {quiz.question}")
            
            # 4개의 선택지를 반복으로 출력
            for choice_idx, choice in enumerate(quiz.choices, 1):
                # 정답은 ✓, 아니면 공백
                mark = "✓" if choice_idx == quiz.answer else " "
                print(f"   [{mark}] {choice_idx}. {choice}")

    def display_best_score(self):
        """
        최고 점수를 보여주는 메서드
        
        동작:
            1. 점수가 있는지 확인
            2. 있으면 정답 개수, 총 문제 수, 정답률 출력
            3. 없으면 안내 메시지 출력
        """
        print("\n🏆 최고 점수")
        print("-" * 50)
        
        # best_score의 total이 0이면 아직 퀴즈를 풀지 않은 것
        if self.best_score["total"] == 0:
            print("아직 퀴즈를 풀지 않았습니다.")
        else:
            correct = self.best_score["correct"]
            total = self.best_score["total"]
            percentage = self.best_score["percentage"]
            print(f"최고 점수: {correct}/{total} ({percentage:.1f}%)")

    def update_best_score(self, correct, total):
        """
        최고 점수를 갱신하는 메서드
        
        동작:
            1. 현재 정답 수가 최고 기록보다 높으면
            2. 최고 점수 정보를 업데이트
        
        correct: 현재 정답 개수
        total: 현재 총 문제 수
        """
        # 정답률 계산
        percentage = (correct / total) * 100 if total > 0 else 0
        
        # 현재 점수가 최고 기록보다 높으면 갱신
        if correct > self.best_score["correct"]:
            self.best_score = {
                "correct": correct,
                "total": total,
                "percentage": percentage
            }

    def save_data(self):
        """
        게임 데이터를 JSON 파일에 저장하는 메서드
        
        동작:
            1. quizzes를 딕셔너리 리스트로 변환
            2. best_score 포함
            3. JSON 형식으로 파일에 저장
        
        왜 필요한가?
            - 프로그램을 종료했다가 다시 실행해도
            - 추가한 퀴즈와 최고 점수가 유지되도록 하기 위함
        """
        try:
            # 저장할 데이터 준비
            data = {
                # to_dict(): 각 Quiz 객체를 딕셔너리로 변환
                "quizzes": [quiz.to_dict() for quiz in self.quizzes],
                "best_score": self.best_score
            }
            
            # 파일에 쓰기
            # open(): 파일을 열기
            # 'w': 쓰기 모드
            # encoding='utf-8': 한글이 포함될 수 있으므로 UTF-8 사용
            with open(self.data_file, 'w', encoding='utf-8') as f:
                # json.dump(): 파이썬 객체를 JSON 형식으로 파일에 저장
                # ensure_ascii=False: 한글을 그대로 저장
                # indent=2: 보기 좋게 2칸씩 들여쓰기
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        # IOError, OSError: 파일 입출력 중 발생하는 에러
        except (IOError, OSError) as e:
            print(f"데이터 저장 중 오류가 발생했습니다: {e}")

    def load_data(self):
        """
        JSON 파일에서 데이터를 불러오는 메서드
        
        동작:
            1. state.json 파일이 있는지 확인
            2. 있으면 파일 읽기
            3. 없으면 기본 퀴즈 사용
            4. 파일이 손상되었으면 기본 퀴즈로 복구
        """
        # os.path.exists(): 파일이 있는지 확인 (있으면 참, 없으면 거짓)
        if not os.path.exists(self.data_file):
            print(f"💾 '{self.data_file}' 파일이 없어서 기본 퀴즈를 사용합니다.")
            self.quizzes = self.default_quizzes
            # 기본 퀴즈로 파일 생성
            self.save_data()
            return
        
        try:
            # 파일 읽기
            with open(self.data_file, 'r', encoding='utf-8') as f:
                # json.load(): JSON 파일을 읽어서 파이썬 객체로 변환
                data = json.load(f)
            
            # 퀴즈 데이터 복원
            # from_dict(): 딕셔너리에서 Quiz 객체 생성
            self.quizzes = [Quiz.from_dict(quiz_data) for quiz_data in data.get("quizzes", [])]
            
            # 최고 점수 복원
            self.best_score = data.get("best_score", {"correct": 0, "total": 0, "percentage": 0.0})
            
            # 저장된 퀴즈가 없으면 기본 퀴즈 사용
            if not self.quizzes:
                print("저장된 퀴즈가 없어서 기본 퀴즈를 사용합니다.")
                self.quizzes = self.default_quizzes
                self.save_data()
        
        # JSONDecodeError: JSON 파일이 손상되었을 때 발생
        except json.JSONDecodeError:
            print(f"'{self.data_file}' 파일이 손상되었습니다. 기본 퀴즈를 사용합니다.")
            self.quizzes = self.default_quizzes
            self.best_score = {"correct": 0, "total": 0, "percentage": 0.0}
            self.save_data()
        
        # 기타 파일 에러
        except (IOError, OSError) as e:
            print(f"데이터 로드 중 오류가 발생했습니다: {e}")
            self.quizzes = self.default_quizzes
            self.best_score = {"correct": 0, "total": 0, "percentage": 0.0}

    def run(self):
        """
        게임 메인 루프
        
        동작:
            1. 시작 메시지 출력
            2. while True로 무한 반복
            3. 메뉴 표시 → 선택받기 → 해당 기능 실행
            4. 종료할 때까지 반복
            5. 프로그램 종료 또는 에러 발생하면 데이터 저장 후 종료
        """
        print("\n영어 단어 퀴즈 게임에 오신 것을 환영합니다!")
        
        # while True: 무한 반복 (break를 만날 때까지)
        while True:
            try:
                # 메뉴 표시
                self.display_menu()
                
                # 사용자 선택받기
                choice = self.get_menu_choice()
                
                # if-elif-else: 선택에 따라 다른 작업 수행
                if choice == 1:
                    # 메뉴 1: 퀴즈 풀기
                    self.play_quiz()
                
                elif choice == 2:
                    # 메뉴 2: 퀴즈 추가
                    self.add_quiz()
                
                elif choice == 3:
                    # 메뉴 3: 퀴즈 목록 보기
                    self.display_quizzes()
                
                elif choice == 4:
                    # 메뉴 4: 최고 점수 확인
                    self.display_best_score()
                
                elif choice == 5:
                    # 메뉴 5: 종료
                    print("\n👋 게임을 종료합니다. 안녕히 가세요!")
                    # 데이터 저장
                    self.save_data()
                    # break: while 루프 탈출 (프로그램 종료)
                    break
            
            # KeyboardInterrupt: Ctrl+C를 눌렀을 때 발생
            except KeyboardInterrupt:
                print("\n\n Ctrl+C로 인한 중단이 감지되었습니다.")
                print("데이터를 저장하고 안전하게 종료합니다...")
                self.save_data()
                print("게임을 종료합니다.")
                break
            
            # EOFError: 입력 스트림이 종료되었을 때 발생
            # (주로 파이프라인이나 스크립트에서 입력이 끝났을 때)
            except EOFError:
                print("\n입력 스트림이 종료되었습니다.")
                print("데이터를 저장하고 안전하게 종료합니다...")
                self.save_data()
                print("👋 게임을 종료합니다.")
                break
            
            # 예상치 못한 에러 처리
            except Exception as e:
                print(f"예상치 못한 오류가 발생했습니다: {e}")
                print("계속하려면 엔터를 누르세요...")
                try:
                    input()
                except (KeyboardInterrupt, EOFError):
                    self.save_data()
                    break

def main():
    """
    프로그램의 진입점(entry point)
    
    이 함수가 호출되면:
        1. QuizGame 객체 생성
        2. run() 메서드 실행 (게임 시작)
    """
    # QuizGame(): 게임 객체 생성
    game = QuizGame()
    
    # game.run(): 게임 시작
    game.run()

if __name__ == "__main__":
    main()