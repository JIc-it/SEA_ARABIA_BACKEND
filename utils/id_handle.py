def increment_one_letter(char):
    if char.isalpha():
        char = char.upper()
        char_ascii = ord(char) + 1
        if char_ascii > ord('Z'):
            char_ascii = ord('A')
        new_char = chr(char_ascii)
        return new_char
    else:
        return char


def increment_two_letters(input_str):
    if len(input_str) == 2 and input_str.isalpha():
        input_str = input_str.upper()
        char1, char2 = input_str[0], input_str[1]
        char2_ascii = ord(char2) + 1
        if char2_ascii > ord('Z'):
            char2_ascii = ord('A')
            char1_ascii = ord(char1) + 1
            if char1_ascii > ord('Z'):
                char1_ascii = ord('A')
            return chr(char1_ascii) + chr(char2_ascii)
        else:
            return char1 + chr(char2_ascii)
    else:
        return input_str


def increment_single_digit(num):
    if isinstance(num, int) and 0 <= num <= 9:
        num += 1
        if num == 10:
            num = 0
        return num
    else:
        return num


def increment_two_digits(num):
    if isinstance(num, int) and 0 <= num <= 99:
        num += 1
        if num == 100:
            num = 0
        return num
    else:
        return num
