import random

#------------------------------------------------------------------------------------------------------------
# Below function is a reference.
# Do not fix the reference function below.
# Use this function to implement the wordle game.
# Refer to comments in this function when you write your own comments.

def load_word_list(path):
    """
    Args:
        path: path to text file which contains answers
    Return:
        word_list: list of words which contains answers
    """
    
    # Load the text file from path
    f = open(path, "r")
    lines = f.readlines()
    f.close()
    
    # Delete newline ('\n') in the list
    word_list = []
    for line in lines:
        word_list.append(line.strip())
    
    # Return list of words
    return word_list


#------------------------------------------------------------------------------------------------------------


def print_status(history, life, answer):
    print()
    print("--------------------")
    print("History:")
    # 입력했던 단어들 출력
    for word in history:
        print(get_colored_string(word, answer))
    # 빈 칸 출력
    for _ in range(6 - len(history)):
        print(" _ " * 5)

    print()

    print(f"Life: {life}")
    print("--------------------")


def get_colored_char(char, color_code):
    """
    글자와 색상 코드를 입력 받아 해당 색상 코드로 배경색이 입혀진 글자를 반환하는 함수.
    Args:
        char: 배경색을 입힐 글자
        color_code: 배경색의 색상 코드
    Return:
        colord_char: 배경색이 입혀진 글자
    """
    return f"\033[{color_code}m {char.upper()} \033[0m"


def get_colored_string(word, answer):
    result = ""

    for i in range(5):
        if word[i] == answer[i]:  # 초록색 배경 case
            result += get_colored_char(word[i], 42)
        elif word[i] in answer:  # 노란색 배경 case
            result += get_colored_char(word[i], 43)
        else:  # 회색 배경 case
            result += get_colored_char(word[i], 47)

    return result


def is_valid(word, word_list, history):
    """
    Return:
        (is_valid, error_message): 유효한지 여부와 유효하지 않을 경우 에러 메시지를 튜플로 반환
    """
    if len(word) != 5:
        return (False, "Input word is not a five-letter word!")
    elif word in history:
        return (False, "Input word has already been typed!")
    elif word not in word_list:
        return (False, "Input word is not in the word list!")
    else:
        return (True, "")


def is_correct(word, answer):
    return word == answer


def input_word(word_list, history):
    """
    사용자로부터 추측 단어를 입력받는 함수
    Args:
        word_list: 단어 리스트
        history: 지금까지 입력했던 유효한 단어
    Return:
        word: 입력 받은 단어. 단, quit 시 -1 반환.
    """

    while True:
        word = input("Type a word: ").lower()

        # 중도 포기 처리
        if word == "quit":
            return -1

        is_valid_word, error_msg = is_valid(word, word_list, history)

        if not is_valid_word:
            # 유효하지 않은 단어의 경우, 에러 메시지 출력 후 반복문에 의해 다시 입력 요청
            print(f"Error: {error_msg}")
            print("Choose another word!")
        else:
            # 유효한 단어의 경우, 입력받은 단어를 바로 return 해 반복 종료.
            return word


def run_game(word_list):
    """
    게임 한 판을 실행하는 함수.
    Args:
        word_list: 단어 리스트
    Return:
        None
    """

    history = []
    life = 6

    # 정답 단어 선택
    answer_word = random.choice(word_list)

    print_status(history, life, answer_word)

    while True:
        guess_word = input_word(word_list, history)

        # 중도 포기 처리
        if guess_word == -1:
            break

        history.append(guess_word)

        is_correct_word = is_correct(guess_word, answer_word)

        # 정답이 아닌 경우에만 life 감소
        if not is_correct_word:
            life -= 1

        print_status(history, life, answer_word)

        if is_correct_word:  # 정답인 경우
            print("Great! You got the answer")
            print(f"The answer was {answer_word}")
            break
        if life <= 0:  # 시도 횟수를 모두 소진한 경우
            print("Too bad! You miss the answer")
            print(f"The answer was {answer_word}")
            break


def main():
    """
    프로그램 전체를 관리하는 함수
    Args:
        None
    Return:
        None
    """
    print("Wordle game starts!")

    word_list = load_word_list("./word_list.txt")

    while True:
        # 게임 실행
        run_game(word_list)

        is_more_game = input("Do you want to play more games? (yes/no): ")
        if is_more_game != "yes":
            # 추가 게임을 원치 않을 경우 반복문 종료.
            print()
            print("See you next!")
            break

if __name__ == "__main__": 
    main()
