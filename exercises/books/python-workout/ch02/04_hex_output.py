from re import A


def hex_output(hexnum: str) -> int:
    decnum = 0
    for power, digit in enumerate(reversed(hexnum)):
        decnum += int(digit, 16) * (16**power)
    return decnum


def hex_output_ord(hexnum: str) -> int:
    decnum = 0

    for power, digit in enumerate(reversed(hexnum)):
        if "0" <= digit <= "9":
            value = ord(digit) - ord("0")
        elif "a" <= digit <= "f":
            value = ord(digit) - ord("a") + 10
        elif "A" <= digit <= "F":
            value = ord(digit) - ord("A") + 10
        else:
            raise ValueError(f"Invalid hex digit: {digit}")

        decnum += value * (16**power)

    return decnum


def print_name_triangle(name: str):
    for i in range(len(name)):
        print(name[: i + 1])


if __name__ == "__main__":
    # hexnum = input("Enter a hex number to convert: ")
    # print(hex_output_ord(hexnum))

    name = input("What's your name? ")
    print_name_triangle(name)
