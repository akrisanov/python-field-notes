from decimal import Decimal, InvalidOperation


def run_timing() -> tuple[float, int]:
    total = 0.0
    runs = 0

    while run := input("Enter 10 km run time: "):
        try:
            total += float(run)
            runs += 1
        except ValueError:
            print("Please enter a number")
            continue

    if runs == 0:
        return 0.0, 0

    avg_time = total / runs
    return avg_time, runs


def take_float(number: float, before: int, after: int) -> float:
    sign = -1 if number < 0 else 1
    integer_part = int((abs(number)))
    last_int_digits = integer_part % (10**before)

    fractional_part = abs(number) - integer_part
    shifted = fractional_part * (10**after)
    first_fr_digits = int(shifted + 1e-12) / 10**after

    return sign * (last_int_digits + first_fr_digits)


def sum(x: Decimal, y: Decimal) -> Decimal:
    return x + y


if __name__ == "__main__":
    # avg_time, runs = run_timing()
    # print(f"Average of {avg_time:.2f}, over {runs} runs")

    # print(take_float(1234.5678, 2, 3))
    # print(take_float(-1234.5678, 2, 3))

    try:
        x = Decimal(input("Enter x: "))
        y = Decimal(input("Enter y: "))
    except InvalidOperation:
        print("Enter a valid number")
        exit(-1)

    print(f"x + y = {sum(x, y)}")
