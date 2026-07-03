import sys

if __name__ == "__main__":
    args = sys.argv

    if len(args) > 1:
        digit_string = args[1]
        sum = 0
        try:
            for digit in digit_string:
                sum += int(digit)
            print(sum)
        except ValueError as ex:
            print(f"Ошибка сложения цифр введенной строки: {ex}")
    else:
        print("Пожалуйста введите не пустую строку.")
