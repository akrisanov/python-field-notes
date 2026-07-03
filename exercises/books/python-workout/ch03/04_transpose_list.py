from itertools import zip_longest


def transpose_list(sentences: list[str]) -> list[str]:
    matrix = [sentence.split() for sentence in sentences]
    return [" ".join(col) for col in zip_longest(*matrix, fillvalue="")]


def transpose_list_alt(sentences: list[str]) -> list[str]:
    matrix = [sentence.split() for sentence in sentences]

    # without using a zipper the solution will be more verbose
    transposed_matrix = []

    for col in range(len(matrix[0])):
        column = []
        for row in range(len(matrix)):
            column.append(matrix[row][col])
        transposed_matrix.append(" ".join(column))

    return transposed_matrix


if __name__ == "__main__":
    original = ["abc def ghi", "jkl mno pqr", "stu vwx yz"]
    expected = ["abc jkl stu", "def mno vwx", "ghi pqr yz"]
    assert transpose_list(original) == expected
    assert transpose_list_alt(original) == expected
