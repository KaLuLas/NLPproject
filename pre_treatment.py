# https://github.com/JacobPlaster/ann-writer/archive/master.zip
import re
import nltk


def text_pre_treat():
    file_name = 'book1'
    input_text = open(".\half_done\\" + file_name + ".txt", "r+", encoding="utf-8")
    output_text = open(".\half_done\\" + file_name + "_sent.txt", "w", encoding="utf-8")
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
    # output_text.write(output_string.join(output_text_list))
    sents = nltk.sent_tokenize(output_string.join(output_text_list))
    for sent in sents:
        output_text.write(sent + '\n')



def name_pre_treat():
    input_text = open(".\half_done\\PotterNameEnglish.txt", "r+", encoding="utf-8")
    output_text = open(".\half_done\\PotterNameEnglishOutput.txt", "w", encoding="utf-8")
    output_text_list = []
    line = input_text.readline()
    while line:
        line = input_text.readline()
        if len(line) > 2:
            end = line.find("–")
            end1 = line.find("-")
            if end == -1:
                end = end1
            output_text_list.append(line[0:end])
    # need a little bit more deletion
    name_string = "".join(output_text_list)
    name_set = sorted(set(name_string.split(" ")))
    output_text.write(" ".join(name_set))


text_pre_treat() # treat book*.txt
# name_pre_treat()  # treat PotterNameEnglish.txt
