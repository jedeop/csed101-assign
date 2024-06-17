import os
import math

LIST_HEADER = [
    "Student",
    "Name",
    "Midterm",
    "Final",
    "Average",
    "Grade",
]  # 학생 목록의 header
GRADES = ["A", "B", "C", "D", "F"]  # 유효한 학점들


# 학점 계산하는 함수
def calc_grade(score):
    if score >= 90:
        return GRADES[0]
    elif score >= 80:
        return GRADES[1]
    elif score >= 70:
        return GRADES[2]
    elif score >= 60:
        return GRADES[3]
    else:
        return GRADES[4]


# 파일로부터 데이터를 읽어 이차원 리스트로 저장하는 함수
def read_data(filename):
    file = open(filename, "r")
    students = []
    for stu in file:  # 한 줄 씩 읽기
        sid, name, mid, final = stu.split("\t")
        mid, final = int(mid), int(final)
        avg_score = (mid + final) / 2  # 평균 계산
        grade = calc_grade(avg_score)  # 학점 계산
        students.append([sid, name, mid, final, avg_score, grade])
    file.close()

    sort_by_avg(students)  # 정렬

    return students


# 목록 한 줄을 출력하는 함수
def print_list_item(row, padding):
    for i in range(len(row)):
        pad = padding[i] - len(
            str(row[i])
        )  # 일정한 길이 위해 오른쪽에 추가해야 할 space의 개수
        text = str(row[i]) + " " * pad
        print(text, end=" ")
    print()


# 목록 header를 출력하는 함수
def print_list_head(head, padding):
    print_list_item(head, padding)
    print(
        "-" * (sum(padding) + len(padding) - 1)
    )  # 구분선. 길이 = 모든 padding + item 사이 공백 한개씩


# 목록을 출력하는 함수
def print_list(head, body, padding):
    print_list_head(head, padding)
    for row in body:
        print_list_item(row, padding)


# 학생 목록의 각 column의 길이를 구하는 함수.
# 이름 column의 경우 가장 긴 이름보다 조금 더 길게.
def get_padding_for_all_stu(students):
    max_name_length = 6  # 최소 길이
    for row in students:
        length = len(row[1])
        if length > max_name_length:
            max_name_length = length
    return [10, max_name_length + 2, 8, 8, 8, 8]


# 평균 점수로 정렬하는 함수
def sort_by_avg(students):
    students.sort(key=lambda stu: stu[4], reverse=True)


def show(students):
    if not students:  # 예외 처리 ; 목록에 아무도 없을 때
        print("LIST IS EMPTY.")
        return

    print_list(LIST_HEADER, students, get_padding_for_all_stu(students))


# 주어진 학번에 해당하는 학생 정보 반환하는 함수
def find_student_by_sid(students, sid):
    for row in students:
        if row[0] == sid:
            return row
    return None


# 주어진 학점에 해당하는 모든 학생들을 반환하는 함수
def find_all_students_by_grade(students, grade):
    result = []
    for row in students:
        if row[5] == grade:
            result.append(row)
    return result


def search(students):
    if not students:  # 예외 처리 ; 목록에 아무도 없을 때
        print("LIST IS EMPTY.")
        return

    sid = input("Student ID: ")
    result = find_student_by_sid(students, sid)
    if result:
        print_list(LIST_HEADER, [result], get_padding_for_all_stu(students))
    else:  # 예외 처리 ; 찾는 학생 목록에 없음
        print("NO SUCH PERSON.")


def change_score(students):
    if not students:  # 예외 처리 ; 목록에 아무도 없을 때
        print("LIST IS EMPTY.")
        return

    sid = input("Student ID: ")
    student = find_student_by_sid(students, sid)
    if not student:  # 예외 처리 ; 찾는 학생 목록에 없음
        print("NO SUCH PERSON.")
        return

    mid_or_final = input("Mid/Final: ").lower()
    if mid_or_final == "mid":
        score_index = 2
    elif mid_or_final == "final":
        score_index = 3
    else:  # 예외 처리 ; mid/final 외의 값
        print("INVALID INPUT.")
        return

    new_score = int(input("Input new score: "))
    if not (0 <= new_score <= 100):  # 예외 처리 ; 0~100 외의 값
        print("INVALID SCORE.")
        return

    padding = get_padding_for_all_stu(students)
    print_list_head(LIST_HEADER, padding)
    print_list_item(student, padding)  # 변경 전 항목 출력

    # 점수, 평균, 학점 업데이트
    student[score_index] = new_score

    avg_score = (student[2] + student[3]) / 2
    grade = calc_grade(avg_score)
    student[4] = avg_score
    student[5] = grade

    print("Score changed.")
    print_list_item(student, padding)  # 변경 후 항목 출력

    sort_by_avg(students)


def add(students):
    sid = input("Student ID: ")

    student = find_student_by_sid(students, sid)
    # 예외 처리 ; 이미 존재하는 학번
    if student:
        print("ALREADY EXISTS.")
        return

    name = input("Name: ")
    mid = int(input("Midterm Score: "))
    final = int(input("Final Score: "))

    avg_score = (mid + final) / 2
    grade = calc_grade(avg_score)

    students.append([sid, name, mid, final, avg_score, grade])
    print("Student added.")

    sort_by_avg(students)


def search_grade(students):
    if not students:  # 예외 처리 ; 목록에 아무도 없을 때
        print("LIST IS EMPTY.")
        return

    grade = input("Grade to search: ")

    # 예외 처리 ; 잘못된 입력
    if grade not in GRADES:
        print("INVALID GRADE")
        return

    found_stus = find_all_students_by_grade(students, grade)

    padding = get_padding_for_all_stu(students)
    if not found_stus:  # 해당 학생이 없는 경우 NO RESULTS. 출력
        print_list_head(LIST_HEADER, padding)
        print("NO RESULTS.")
    else:
        print_list(LIST_HEADER, found_stus, padding)


def get_stats(students):
    if not students:  # 예외 처리 ; 목록에 아무도 없을 때
        print("LIST IS EMPTY.")
        return

    # 중앙값
    meds = ["Med"]
    stus_len = len(students)
    is_odd = stus_len % 2 == 1
    for i in range(2, 5):
        if is_odd:  # 학생 수 홀수
            med = students[int((stus_len - 1) / 2)][i]
        else:  # 학생 수 짝수
            med = (
                students[int(stus_len / 2)][i] + students[int((stus_len / 2) - 1)][i]
            ) / 2
        meds.append(med)

    # 평균
    avgs = ["Avg"]
    for i in range(2, 5):
        sum = 0
        for stu in students:
            sum += stu[i]
        avg = sum / stus_len
        avgs.append(avg)

    # 표준편차
    stds = ["Std"]
    for i in range(2, 5):
        sum = 0
        for stu in students:
            sum += (stu[i] - avgs[i - 1]) ** 2
        std = math.sqrt(sum / stus_len)
        stds.append(std)

    body = [meds, avgs, stds]

    # 포멧 바꾸기 (소수점 첫째 자리까지)
    for row in body:
        for i in range(1, 4):
            row[i] = f"{row[i]:5.1f}"

    print_list(["Stats", "Midterm", "Final", "Average"], body, [8, 8, 8, 8])


def remove(students):
    if not students:  # 예외 처리 ; 목록에 아무도 없을 때
        print("LIST IS EMPTY.")
        return

    sid = input("Student ID: ")
    student = find_student_by_sid(students, sid)
    if not student:  # 예외 처리 ; 찾는 학생 목록에 없음
        print("NO SUCH PERSON.")
        return
    print_list(LIST_HEADER, [student], get_padding_for_all_stu(students))

    print()
    yes_or_no = input(f"Remove {sid}? [yes/no] ")
    if yes_or_no == "no":
        print("Cancelled.")
        return
    elif yes_or_no == "yes":
        students.remove(student)
        print("Student removed.")


def quit(students):
    yes_or_no = input("Save data? [yes/no] ")
    if yes_or_no == "yes":
        file_name = input("File name: ")
        file = open(file_name, "w")
        for stu in students:
            text = f"{stu[0]}\t{stu[1]}\t{stu[2]}\t{stu[3]}\n"
            file.write(text)
        file.close()

    print()


def main():
    filename = input("Input the score file name: ")

    # 예외처리 ; 존재하지 않는 파일명
    if not os.path.exists(filename):
        print(f"The file '{filename}' does not exist.")
        return

    students = read_data(filename)

    show(students)
    print()

    # 명령어 입력 처리
    while True:
        command = input("# ").lower()

        if command == "show":
            show(students)
        elif command == "search":
            search(students)
        elif command == "changescore":
            change_score(students)
        elif command == "add":
            add(students)
        elif command == "searchgrade":
            search_grade(students)
        elif command == "getstats":
            get_stats(students)
        elif command == "remove":
            remove(students)
        elif command == "quit":
            quit(students)
            return  # 프로그램 종료
        else:  # 유효하지 않은 명령어
            print("INVALID COMMAND.")

        print()


if __name__ == "__main__":
    main()
