import sys

if __name__ == "__main__":
    args = sys.argv

    if len(args) > 1:
        digit_string = args[1]
        try:
            # using list comprehensions and the sum function
            result = sum([int(digit) for digit in digit_string])
        except ValueError as ex:
            result = f"Ошибка сложения цифр введенной строки: {ex}"
        print(result)
    else:
        print("Пожалуйста введите не пустую строку.")
