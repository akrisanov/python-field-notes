def dec_str(str):
    line = '*'*len(str)
    return '\n'.join([line, str, line])

print(dec_str('Hi from the other side'))
