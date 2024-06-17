import time
import random


# UI 출력을 위한 클래스
# 인스턴스 생성 후 run 메소드를 실행하면 UI가 출력된다.
class UI:
    def __init__(self, title, lines, in_div="=", sep="\n", hlen=32, no_title=False):
        self.title = title  # 제목
        self.lines = lines  # 출력할 내용. 한 줄 씩 배열로 입력받는다.
        self.in_div = in_div  # 제목과 내용 사이 구분선으로 사용할 문자
        self.sep = sep  # 내용을 출력할 때 항목 사이에 사용할 구분자
        self.hlen = hlen  # 구분선의 길이
        self.no_title = no_title  # 제목 유무

    # UI 출력
    def run(self):
        print("=" * self.hlen)
        if not self.no_title:
            print(f" {self.title}")
            print(self.in_div * self.hlen)
        length = len(self.lines)
        for i in range(length):
            end = self.sep
            if i == length - 1:
                end = "\n"

            print(f" {self.lines[i]}", end=end)
        print("=" * self.hlen)


# 사용자에게 선택을 받는 UI 출력을 위한 클래스
class SelectUI(UI):
    def __init__(self, title, labels, actions, in_div="=", sep="\n", hlen=32):
        # labbels: 각 선택지 라벨
        # actions: 각 선택지를 선택했을 때 실행할 함수
        lines = []
        for i in range(len(labels)):
            lines.append(f"{i}. {labels[i]}")
        super().__init__(title, lines, in_div, sep, hlen)
        self.actions = actions

    def run(self):
        super().run()
        while True:
            selected = input("Select: ")

            action = None
            try:  # 사용자 입력이 유효한가 확인하기 위함
                selected = int(selected)  # 입력이 정수가 아니라면 에러
                action = self.actions[selected]  # 입력한 수가 선택지에 없다면 에러
            except:  # 유효하지 않은 경우
                print("Wrong Input!")

            if action:
                return action()  # 함수의 반환값을 상위로 전달


# 변수의 값들을 출력하기 위한 class
class InfoUI(UI):
    def __init__(self, title, labels, data, no_title=False):
        # labels: 각 데이터의 라벨 (리스트)
        # data: 출력할 값들 (리스트)
        super().__init__(title, [], no_title=no_title)
        self.data = data
        self.labels = labels
        self.update(data)

    # 라벨과 변수값을 조합해 출력할 문자열을 생성
    def update(self, data):
        lines = []
        for label, value in zip(self.labels, data):
            lines.append(f"{label}: {value}")
        self.lines = lines


class SlotMachine:
    def __init__(self):
        self.money = 1000
        self.recharge_count = 0
        self.total_earn_credit = 0

        self.main()

    def main(self):
        main_ui = SelectUI(
            "SlotMachine Game",
            ["Player Information", "Select Slot Game", "Recharge", "Exit"],
            [
                self.player_information,
                self.select_slot_game,
                self.recharge,
                self.exit,
            ],
        )

        while True:  # 종료될 때까지 메인 UI 반복 실행
            if main_ui.run() == -1:  # 종료가 필요하다면 함수가 -1을 반환
                break  # 종료

    def player_information(self):
        player_info_ui = InfoUI(
            "Player Infomation",
            ["Money", "Recharge Count", "Total Earn Credit"],
            [self.money, self.recharge_count, self.total_earn_credit],
        )
        player_info_ui.run()

    def select_slot_game(self):
        select_slot_game_ui = SelectUI(
            "Select Slot Game",
            ["Single Line Slot", "Single Line with Wild Slot", "Cancel"],
            [
                lambda: SingleLineSlot(
                    self
                ),  # 자기자신(SlotMachine)을 인자로 넘겨 Slot게임 인스턴스 생성
                lambda: SingleLineWithWildSlot(self),
                lambda: None,
            ],
            in_div="-",
        )
        select_slot_game_ui.run()

    def recharge(self):
        print(f"Current Money: {self.money}")
        if self.money < 500:  # 재충전 가능
            original_money = self.money
            self.money = 1000
            self.recharge_count += 1
            print(
                f"Recharge money ({original_money} -> {self.money}, Recharge count: {self.recharge_count})"
            )
        else:  # 재충전 불가
            print(f"Cannot recharge money ({self.money} >= 500)")

    def exit(self):
        if self.total_earn_credit > 5000:  # 종료 가능
            score = int(self.total_earn_credit / (self.recharge_count + 1))
            ui = InfoUI(
                "",
                ["Total Earn Credit", "Recharge Count", "Score"],
                [self.total_earn_credit, self.recharge_count, score],
                no_title=True,
            )
            ui.run()
            return -1  # -1 리턴해서 종료 필요함을 상위 함수에 전달
        else:  # 종료 불가
            print("Cannot Exit...")
            print(f"Total Earn Credit: {self.total_earn_credit} (<= 5000)")


class BetController:
    def __init__(self):
        self.bet_minimum = 100
        self.bet = self.bet_minimum

    def increase_bet(self, money):
        candidate = self.bet * 2
        if candidate <= money:  # increase 가능
            print(f"Increase Bet {self.bet} -> {candidate}")
            self.bet = candidate
        else:  # increase 불가
            print(f"Cannot Increase Bet ({money} < {candidate})")

    def decrease_bet(self):
        candidate = self.bet // 2  # 정수형(int) 결과를 위해 // 사용
        if candidate >= self.bet_minimum:  # decrease 가능
            print(f"Decrease Bet {self.bet} -> {candidate}")
            self.bet = candidate
        else:  # decrease 불가
            print(f"Cannot Increase Bet ({self.bet_minimum} > {candidate})")


class SlotBase:
    def __init__(self, slot_machine):
        self.slot_machine = slot_machine
        self.bet_controller = BetController()
        self.name = "none"
        self.symbols = []
        self.win_multipliers = []

    def main(self):
        ui = SelectUI(
            self.name,
            ["Spin", "Increase Bet", "Decrease Bet", "Help", "Exit"],
            [self.spin, self.increase_bet, self.decrease_bet, self.help, self.exit],
            in_div="-",
            sep=" /",
            hlen=66,
        )
        while True:  # 종료 원할 때까지 반복 실행
            if ui.run() == -1:  # 함수가 -1 반환 시 == 종료가 필요할 때 ==> 반복 종료
                break

    def increase_bet(self):
        self.bet_controller.increase_bet(self.slot_machine.money)

    def decrease_bet(self):
        self.bet_controller.decrease_bet()

    # 슬롯 결과 심볼 3개를 선택하는 메소드
    # 하위 클래스에서 오버라이딩 함.
    def choices(self):
        pass

    # 슬롯 결과(choices)를 전달 받아 승패를 판단하는 메소드
    # 하위 클래스에서 오버라이딩 함.
    def win_lose(self, choices):
        pass

    # 스핀 메뉴 선택 시 실행되는 함수.
    # 공통되는 로직은 이곳에 구현했다. (보고서 4.1 참고)
    def spin(self):
        if self.slot_machine.money < self.bet_controller.bet:  # 잔액 부족
            print(
                f"Cannot Spin ({self.slot_machine.money} < {self.bet_controller.bet})"
            )
            return

        self.slot_machine.money -= self.bet_controller.bet
        print("Spin...")

        time.sleep(0.5)

        choices = self.choices()  # 스핀 결과 나온 심볼들

        def print_l(*text):  # 결과 출력을 위한 함수. 왼쪽에 공백을 삽입해 줌.
            left_padding = " " * 4
            print(left_padding, *text)

        print_l("=" * 13)
        print_l(" Spin Result ")
        print_l("=" * 13)
        print_l(
            f"| {self.symbols[choices[0]]} | {self.symbols[choices[1]]} | {self.symbols[choices[2]]} |"
        )
        print_l("=" * 13)

        time.sleep(0.2)

        win_lose, earn_credit = self.win_lose(choices)  # 승패 판단

        print_l("=" * 13)
        if win_lose:  # Win
            self.slot_machine.money += earn_credit
            self.slot_machine.total_earn_credit += earn_credit

            print_l("Win!")
            print_l(f"Earn Credit: {earn_credit}")
            print_l(f"Total Earn Credit: {self.slot_machine.total_earn_credit}")
            print_l(f"Money: {self.slot_machine.money}")
        else:  # Lose
            print_l("Lose...")
            print_l(f"Money: {self.slot_machine.money}")

        time.sleep(0.3)

    def help(self):
        pass

    def exit(self):
        print(f"Exit {self.name}")
        return -1


class SingleLineSlot(SlotBase):
    def __init__(self, slot_machine):
        super().__init__(slot_machine)

        self.name = "Single Line Slot"
        self.symbols = ["@", "$", "7"]
        self.win_multipliers = [4, 8, 20]

        self.main()

    def choices(self):
        symbol_count = len(self.symbols)
        spin_result = []

        # 심볼 선택. 단순히 0~2 사이 정수를 3번 뽑는다.
        # 'self.symbols[뽑한 값]'이 선택된 심볼이다.
        for _ in range(3):
            choice = random.randint(0, symbol_count - 1)
            spin_result.append(choice)

        return spin_result

    def win_lose(self, choices):
        if choices[0] == choices[1] == choices[2]:  # Win, 모든 값이 같을 때
            earn_credit = self.bet_controller.bet * self.win_multipliers[choices[0]]
            return (True, earn_credit)
        else:
            return (False, 0)

    def help(self):
        print("[ HELP ]")
        print(f" This is {self.name}")
        print(f" Symbols are {self.symbols}")
        print(f" Win Multipliers are {self.win_multipliers}")


class SingleLineWithWildSlot(SlotBase):
    def __init__(self, slot_machine):
        super().__init__(slot_machine)

        self.name = "Single Line with Wild Slot"
        self.symbols = ["@", "$", "7", "W"]
        self.win_multipliers = [2, 4, 6]

        self.main()

    def choices(self):
        symbol_count = len(self.symbols)
        spin_result = []

        choice = random.randint(0, symbol_count - 2)  # 첫번째 슬롯 : W 제외
        spin_result.append(choice)
        for _ in range(2):  # 2, 3번째 슬롯 : Single Line Slot과 동일
            choice = random.randint(0, symbol_count - 1)
            spin_result.append(choice)

        return spin_result

    def win_lose(self, choices):
        # 0번 값은 W가 아니므로, 0번 값을 비교를 위한 기준점으로 삼음.
        # 1번이 0번과 같거나, W인가? and 2번이 0번과 같거나 W인가?
        if (choices[0] == choices[1] or choices[1] == 3) and (
            choices[0] == choices[2] or choices[2] == 3
        ):  # Win
            earn_credit = self.bet_controller.bet * self.win_multipliers[choices[0]]
            return (True, earn_credit)
        else:
            return (False, 0)

    def help(self):
        print("[ HELP ]")
        print(f" This is {self.name}")
        print(f" Symbols are {self.symbols}")
        print(f" Win Multipliers are {self.win_multipliers}")


if __name__ == "__main__":
    SlotMachine()
