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


# ============================================================================
# QuizGame 클래스 정의
# ============================================================================
# 게임 전체를 관리하는 클래스
# Quiz 클래스는 "하나의 퀴즈"를 관리하고,
# QuizGame 클래스는 "모든 퀴즈와 게임 진행"을 관리함

=======

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