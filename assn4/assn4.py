# tkinter 모듈 import
import tkinter as tk


# 플레이어 정보 표시 화면
class Info(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        # Todo
        # 플레이어 턴 표시 화면 생성
        # 요구 사항에 맞춰 화면 디자인
        self.configure(width=500, height=100)
        self.label = tk.Label(self, text="Yellow Player turn", font=("Arial", 20))
        self.label.grid(sticky=tk.N + tk.S + tk.E + tk.W, pady=20)

    def update(self, text):  #! label의 문구를 수정하는 메소드
        self.label.configure(text=text)


# 공(Ball)과 공이 떨어지는 애니메이션에 관한 클래스
class Ball:
    # 생성자
    def __init__(self, canvas, x, y, color, radius=25):
        # Todo
        # Ball object를 만들기 위해서 인스턴스 변수의 값을 초기화
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.ball = self.canvas.create_oval(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
            fill=self.color,
            outline="blue",
        )
        self.x_target = x
        self.y_target = y

    # 공 이동 함수
    def move(self):
        # Todo
        # 현재 중심 좌표 계산
        x1, y1, x2, y2 = self.canvas.coords(self.ball)
        x = (x1 + x2) // 2
        y = (y1 + y2) // 2
        # 타겟과의 좌표 차이가 있으면 tk.Canvas.move() 함수 호출
        # 그렇지 않으면 멈춤
        if x != self.x_target or y != self.y_target:
            # x축으로 이동할 양 결정
            # target과 현재 위치 차이가 10보다 크면 10만큼, 아니면 차이나는 만큼 이동
            if -10 <= x - self.x_target <= 10:
                x_delta = -(x - self.x_target)
            elif x - self.x_target > 10:
                x_delta = -10
            else:
                x_delta = 10

            # y축으로 이동할 양 결정
            if -10 <= y - self.y_target <= 10:
                y_delta = -(y - self.y_target)
            elif y - self.y_target > 10:
                y_delta = -10
            else:
                y_delta = 10

            self.canvas.move(self.ball, x_delta, y_delta)
            self.canvas.after(20, self.move)

    def set_target(self, x_target, y_target):
        # Todo
        # 타겟 목적지 좌표 설정
        self.x_target = x_target
        self.y_target = y_target


# 게임 진행 화면(게임판, 사용자 입력 정보 화면)에 관한 클래스
class Board(tk.Canvas):
    # 생성자
    def __init__(self, root, info):  #! root, info 추가: 해당 위젯 변수
        tk.Canvas.__init__(self)
        # 디폴트 값 배정(행, 열, 각 칸의 크기, 시작 플레이어, 시작 공의 색깔, 게임 진행 상황 저장 리스트)
        self.ROWS = 6
        self.COLS = 7
        self.WIDTH = int(500 / 7)
        self.HEIGHT = int(400 / 6)
        self.player = 1
        self.c = "yellow"
        self.game_over = False
        self.stat = []
        for i in range(self.ROWS):
            stat_tmp = []
            for j in range(self.COLS):
                stat_tmp.append("white")
            self.stat.append(stat_tmp)

        self.root = root
        self.info = info

        # Todo
        # 요구 크기에 맞게 캔버스 설정(가로 500, 세로 450, 배경색 blue)
        self.configure(width=500, height=450, bg="blue")
        # 그리드 생성
        for i in range(1, self.COLS):  # 세로선
            self.create_line(
                self.WIDTH * i, 0, self.WIDTH * i, 400, fill="white", width=3
            )
        for i in range(1, self.ROWS):  # 가로선
            self.create_line(
                0, self.HEIGHT * i, 500, self.HEIGHT * i, fill="white", width=3
            )
        # 사용자 입력 정보 화면 생성
        self.create_rectangle(0, 400, 500, 450, fill="black")

        self.curr_col = 3

        x_center = self.WIDTH * (self.curr_col + 0.5)
        self.arrow = self.create_polygon(
            x_center,
            400,
            x_center - 30,
            450,
            x_center + 30,
            450,
            fill="white",
        )

        # <Motion> 및 클릭 이벤트와 바인딩
        self.bind("<Motion>", self.choice)
        self.bind("<Button-1>", self.Connect4)

    # 사용자 입력 정보 창
    def choice(self, event):
        # Todo
        # 이벤트에 따라 선택된 열을 계산
        self.curr_col = event.x // self.WIDTH
        # 사용자 이벤트에 따라 삼각형 이동
        x_center = self.WIDTH * (self.curr_col + 0.5)
        self.coords(
            self.arrow,
            x_center,
            400,
            x_center - 30,
            450,
            x_center + 30,
            450,
        )

    # 게임 진행 알고리즘
    def Connect4(self, event):
        # Todo

        # 착수 알고리즘
        # Game over가 아닐 시 진행
        if self.game_over:
            return
        # 한 열이 다 차있으면 플레이어 바꾸지 않게 조정
        # 열이 다 찼다 == 가장 위쪽 칸이 비어있지 않다
        if self.stat[0][self.curr_col] != "white":
            return
        # 그렇지 않은 경우 착수 메커니즘 구현
        x = self.WIDTH * (self.curr_col + 0.5)
        y_idx = 0
        for i in range(self.ROWS):  # 가장 마지막으로 값이 white인 index 찾기
            if self.stat[i][self.curr_col] == "white":
                y_idx = i
            else:
                break
        y = self.HEIGHT * (y_idx + 0.5)
        # 공 생성 및 이동
        ball = Ball(self, x, -50, self.c)
        ball.set_target(x, y)
        ball.move()
        # 게임 진행 상황 저장 리스트 업데이트
        self.stat[y_idx][self.curr_col] = self.c

        # 승부 결정 확인
        # 승리 또는 무승부 판정 함수 호출
        if self.Horizontal() or self.Vertical() or self.Diagonal1() or self.Diagonal2():
            # 승부 결정 됨
            # 마지막으로 착수한 플레이어가 승리
            self.game_over = True
            msg = f"{self.c} player win!".title()
            self.info.update(msg)
            self.Finish(msg)
            return
        elif self.Draw():
            # 무승부
            self.game_over = True
            msg = "Draw"
            self.info.update(msg)
            self.Finish(msg)
            return

        # 플레이어 전환
        self.player = 1 if self.player == 2 else 2
        self.c = "yellow" if self.player == 1 else "red"
        self.info.update(f"{self.c.title()} Player turn")

    # 가로 방향으로 연속하여 4개의 같은 공을 두었을 때 승부 판정
    def Horizontal(self):
        # Todo
        # 승부 판정 메커니즘 구현
        for y in range(self.ROWS):
            last = "none"
            length = 0
            for x in range(self.COLS):
                if self.stat[y][x] == "white":
                    last = "none"
                    length = 0
                    continue
                if self.stat[y][x] == last:
                    length += 1
                else:
                    last = self.stat[y][x]
                    length = 1
                if length == 4:
                    return True
        return False

    # 세로 방향으로 연속하여 4개의 같은 공을 두었을 때 승부 판정
    def Vertical(self):
        # Todo
        # 승부 판정 메커니즘 구현
        for x in range(self.COLS):
            last = "none"
            length = 0
            for y in range(self.ROWS):
                if self.stat[y][x] == "white":
                    last = "none"
                    length = 0
                    continue
                if self.stat[y][x] == last:
                    length += 1
                else:
                    last = self.stat[y][x]
                    length = 1
                if length == 4:
                    return True
        return False

    # 우상향으로 연속하여 4개의 같은 공을 두었을 때 승부 판정
    def Diagonal1(self):
        # Todo
        # 승부 판정 메커니즘 구현
        for y in range(self.ROWS):
            for x in range(self.COLS):
                if self.stat[y][x] == "white":
                    continue
                # 연속적으로 4개의 공간이 있는지 체크
                if x + 3 >= self.COLS:
                    continue
                if y - 3 < 0:
                    continue

                # 4개의 공이 같은지 확인
                check = True
                for i in range(1, 4):
                    if self.stat[y - i][x + i] != self.stat[y][x]:
                        # 같지 않은 경우
                        check = False
                        break
                if check:
                    return True

        return False

    # 우하향으로 연속하여 4개의 같은 공을 두었을 때 승부 판정
    def Diagonal2(self):
        # Todo
        # 승부 판정 메커니즘 구현
        for y in range(self.ROWS):
            for x in range(self.COLS):
                if self.stat[y][x] == "white":
                    continue
                # 연속적으로 4개의 공간이 있는지 체크
                if x + 3 >= self.COLS:
                    continue
                if y + 3 >= self.ROWS:
                    continue

                # 4개의 공이 같은지 확인
                check = True
                for i in range(1, 4):
                    if self.stat[y + i][x + i] != self.stat[y][x]:
                        # 같지 않은 경우
                        check = False
                        break
                if check:
                    return True

        return False

    # 무승부가 되었을 때 무승부 판정
    def Draw(self):
        # Todo
        # 무승부 판정 메커니즘 구현
        for i in range(self.COLS):
            if self.stat[0][i] == "white":  # 끝이 비어 있는 곳이 있다
                return False  # 무승부 아님

        return True  # 모든 곳이 가득 찼다 -> 무승부

    # 게임 종료창 생성 함수
    def Finish(self, text):
        # Todo
        # 요구사항에 맞춰 게임 종료창 생성
        toplevel = tk.Toplevel(self.root)
        toplevel.title("Game Over")
        toplevel.geometry("320x200")
        label = tk.Label(toplevel, text=text, font=("Arial", 20, "bold"), pady=25)
        label.pack()
        btn = tk.Button(toplevel, text="Quit", command=self.quit)
        btn.pack(padx=50, pady=10, ipadx=20, ipady=5)

    # 게임 종료창 버튼 기능 함수
    def quit(self):
        global root
        root.destroy()


# main 함수
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Assignment4_20240531")

    info = Info()
    info.grid(row=0, column=0)

    board = Board(root, info)
    board.grid(row=1, column=0)

    root.mainloop()
