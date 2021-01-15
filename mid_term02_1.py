# 타이핑 게임 (오전분반 중간고사)
# 사운드 사용 및 DB연동

import random, time, sys

# 사운드 출력, 데이터베이스, 시간 관련 필요 모듈
import pygame
import sqlite3
import datetime

# DB 생성
conn = sqlite3.connect("./resources/records.db", isolation_level=None)
cursor = conn.cursor()

# 사운드 불러오기
pygame.init()
pygame.mixer.init()
correct_sound = pygame.mixer.Sound("./resources/131660__bertrof__game-sound-correct.wav")
wrong_sound = pygame.mixer.Sound("./resources/476177__unadamlar__wrong-choice.wav")

# 테이블 생성 (AUTOINCREMENT - 자동으로 1씩 증가)
cursor.execute("CREATE TABLE IF NOT EXISTS records (" +\
    "id INTEGER PRIMARY KEY AUTOINCREMENT, " +\
    "cor_cnt INTEGER, " +\
    "record TEXT, " +\
    "regdate TEXT)")

class GameStart:
    def __init__(self, user):
        self.user=user
    
    # 유저 입장 알림
    def user_info(self):
        print("User: {}님이 입장하였습니다.\n".format(self.user))

words = []                                                      # 영단어 리스트 (1000개 로드)

n = 1                                                           # 게임 시도 횟수
cor_cnt = 0                                                     # 정답 개수
try:
    word_file =  open("./resources/words.txt", "r")
except IOError as ioe:
    print("파일이 없습니다. 게임을 진행할 수 없습니다.")
else:
    for c in word_file:
        words.append(c.strip())
    word_file.close()

# 파일을 잘못 불러오거나 빈 파일이면 종료
if words is []:
    sys.exit()

# 게임 시작
print('\nGame Start!')
user_name = input("Ready? Input your name>> ")                  # Enter Game Start!!
user = GameStart(user_name)
user.user_info()

start = time.time()                                             # 시작 시간 체크

while n <= 3:                                                   # 3번 반복
    random.shuffle(words)                                       # 단어 리스트 뒤섞기
    q = random.choice(words)                                    # 뒤섞인 단어 리스트에서 랜덤으로 하나 선택

    print("{}번 문제".format(n), q)                               # 문제 표시
    
    x = input("Type Here>> ")                                    # 타이핑 입력

    if str(q).strip() == str(x).strip():                        # (공백 제거한) 입력 확인
        pygame.mixer.Sound.play(correct_sound)                  # 정답 사운드 재생
        print(">>Passed!\n")
        cor_cnt += 1                                            # 정답 개수 카운트
    else:
        pygame.mixer.Sound.play(wrong_sound)                    # 오답 사운드 재생
        print("Wrong!")
    
    n += 1                                                      # 다음 문제 전환

end = time.time()                                               # 끝나는 시간 체크
et = end - start                                                # 총 게임 시간 환산

print("\n집계중...\n")
time.sleep(0.5)

et = format(et, ".3f")                                          # 시간을 소수 셋째자리까지 출력

if cor_cnt >= 2:
    print("결과: 합격!")
else:
    print("불합격")

# 결과 기록 DB에 저장
cursor.execute("INSERT INTO records (cor_cnt, record, regdate) VALUES (?, ?, ?)",\
    (cor_cnt, et, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

# 수행 시간 출력
print("게임 시간:", et, "초,", "정답개수: {}".format(cor_cnt))

# DB 연결 종료
conn.close()

if __name__ == '__main__':
    pass