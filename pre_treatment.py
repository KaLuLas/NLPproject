# https://github.com/JacobPlaster/ann-writer/archive/master.zip
import re


def text_pre_treat():
    input_text = open(".\half_done\\raw_input.txt", "r+", encoding="utf-8")
    output_text = open(".\half_done\\input.txt", "w", encoding="utf-8")
    output_text_list = []
    output_string = ""
    test_string = input_text.readline()
    while test_string:
        if re.search("(^Page)|(^\s)|(^\ufeff)|(^[A-Z ]+$)", test_string) is None:
            # (Page ***) | (Empty Line) | (Start Line) | (Title Line)
            newline = re.sub("\n", "", test_string)
            # delete \n in each line
            output_text_list.append(newline)
        test_string = input_text.readline()

    # print(output_text_list)
    output_text.write(output_string.join(output_text_list))


def find_name():
    # function to find all possible names
    print()


text_pre_treat()
