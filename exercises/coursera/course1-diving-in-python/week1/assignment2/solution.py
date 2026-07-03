import sys

if __name__ == "__main__":
    args = sys.argv

    if len(args) > 1:
        try:
            stairs = int(args[1])
            if stairs <= 0:
                print("Количество ступенек должно быть положительным числом.")
            else:
                steps = 1
                while steps <= stairs:
                    print(" " * (stairs - steps), "#" * steps, sep="")
                    steps += 1
        except ValueError as ex:
            print("Количество ступенек должно быть числом.")
    else:
        print("Укажите количество ступенек лестницы.")
