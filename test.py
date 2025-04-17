import math
import argparse
import sys

parser = argparse.ArgumentParser(description="Credit calculator")
parser.add_argument("--type")  # 不用 choices，自己校验
parser.add_argument("--payment", type=float)
parser.add_argument("--principal", type=float)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)
args = parser.parse_args()

# 自定义合法性检查函数
def invalid():
    if args.type not in ['annuity', 'diff']:
        return True
    if args.interest is None:
        return True
    if args.type == "diff" and args.payment is not None:
        return True
    values = [args.principal, args.payment, args.periods, args.interest]
    for v in values:
        if v is not None and v < 0:
            return True
    return False

# 错误参数处理
if invalid():
    print("Incorrect parameters")
    sys.exit()

# 月利率 i
i = args.interest / (12 * 100)

# 差额还款模式
if args.type == "diff":
    principal = args.principal
    periods = args.periods
    total = 0
    for m in range(1, periods + 1):
        Dm = math.ceil(principal / periods + i * (principal - (principal * (m - 1)) / periods))
        print(f"Month {m}: payment is {Dm}")
        total += Dm
    print(f"\nOverpayment = {int(total - principal)}")

# 等额本息模式
elif args.type == "annuity":
    P = args.principal
    A = args.payment
    n = args.periods

    if A is None:
        A = math.ceil(P * i * pow(1 + i, n) / (pow(1 + i, n) - 1))
        print(f"Your annuity payment = {A}!")
        print(f"Overpayment = {int(A * n - P)}")

    elif P is None:
        P = A / ((i * pow(1 + i, n)) / (pow(1 + i, n) - 1))
        P = math.floor(P)
        print(f"Your loan principal = {P}!")
        print(f"Overpayment = {int(A * n - P)}")

    elif n is None:
        n = math.ceil(math.log(A / (A - i * P), 1 + i))
        years = n // 12
        months = n % 12
        if years and months:
            print(f"It will take {years} years and {months} months to repay this loan!")
        elif years:
            print(f"It will take {years} years to repay this loan!")
        else:
            print(f"It will take {months} months to repay this loan!")
        print(f"Overpayment = {int(A * n - P)}")
