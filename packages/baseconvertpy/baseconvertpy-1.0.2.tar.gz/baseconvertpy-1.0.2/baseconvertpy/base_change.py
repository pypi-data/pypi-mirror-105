import string
from math import floor

charset = string.digits + string.ascii_letters


def to_baseX(num, base, chars=charset):
    if base <= 0 or base > len(chars):
        # TODO Create Error
        return 0
    final = ""
    q = num

    while floor(q) > 0:
        r = q % base
        q = floor(q / base)
        res = chars[r]
        final = final + res

    return final[::-1]


def to_base10(num, base, chars=charset):
    res = int(str(num)[0])

    for char in str(num)[1:]:
        char = chars.find(char)
        res = res * base + char

    return res


def convert(num, new_base, original_base=10, chars=charset):
    if num == 0:
        return 0
    num = to_base10(num, original_base, chars)
    num = to_baseX(num, new_base, chars)
    return num
