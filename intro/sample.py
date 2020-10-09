def reverse_name(f_name, l_name):
    return reverse(f_name) + " " + reverse(l_name)


def reverse(s):
    if len(s) <= 0:
        return None

    left = 0
    right = len(s) - 1
    reverse_s = [None] * len(s)
    while left < right:
        temp = s[left]
        reverse_s[left] = s[right]
        reverse_s[right] = temp
        left += 1
        right -= 1

    return "".join(reverse_s)


print(reverse_name("Luis", "Gonzalez"))