import sys


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 4:
        a, b, c = [int(k) for k in args[1:]]
        d = b*b - 4*a*c

        if d > 0:
            x1 = (-b + d**0.5) / (2*a)
            x2 = (-b - d**0.5) / (2*a)
        elif d == 0:
            x1 = x2 = - (b / (2*a))
        else:
            print("Корней на множестве действительных чисел нет.")
            sys.exit(1)

        print(int(x1))
        print(int(x2))
    else:
        print("Не переданы коэффициенты квадратного уровнения.")
