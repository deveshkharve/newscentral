
def maxArea(height):

    # maxA = 0
    # maxPosition = (0 ,0)
    # for w1 in range(len(height)):
    #     h1 = height[w1]
    #     for w2 in range(len(height)):
    #
    #         h2 = height[w2]
    #         h = min(h2, h1)
    #         w = abs(w1 -w2)
    #         a = h* w
    #         if maxA < a:
    #             maxA = a
    #             maxPosition = (w1, w2)

    start = 0
    end = len(height)-1
    maxA = 0
    maxPos = (0,0)
    while start < end:
        ar = min(height[start], height[end]) * (end-start)
        if ar > maxA:
            maxA = ar
            maxPos = (start, end)

        if height[start] > height[end]:
            end -= 1
        else:
            start += 1

    print(maxA)
    return maxA

# maxArea([1,8,6,2,5,4,8,3,7])
def romanBase(num, char1, char2, ex1, ex2):
    char = ''
    if num < 4:
        i = 0
        while i < num:
            char += char1
            i += 1
    if num == 4:
        return ex1
    if num >= 5 and num < 9:
        char = char2
        char += romanBase(num - 5, char1, char2, ex1, ex2)
    if num == 9:
        char = ex2
    return char


def getRomanChar(num, base):
    if base == 1:
        return romanBase(num/base, 'I', 'V', 'IV', 'IX')
    elif base == 10:
        return romanBase(num/base, 'X', 'L', 'XL', 'XC')
    elif base == 100:
        return romanBase(num/base, 'C', 'D', 'CD', 'CM')
    elif base == 1000:
        return romanBase(num/base, 'M', 'N', 'MN', 'MZ')

def numToRoman(number):
    b = 1
    roman = []
    while number:
        r = number % (b*10)
        number = number - r
        roman.append(getRomanChar(r, b))
        b = b * 10

    st = ''
    for ch in roman[::-1]:
        if ch:
            st += ch
            print(ch, end="")
    return st

numToRoman(1994)

# print(getRomanChar(1))