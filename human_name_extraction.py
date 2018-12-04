# -*- coding: utf-8 -*-

import os
import nltk
import codecs
import pandas as pd
from nltk.corpus import names

path = ".\\half_done\\"


def extract_name_and_gender(file_name):
    name_dict = {}
    list_of_names =[]
    list_of_male_names = names.words('male.txt')
    list_of_female_names = names.words('female.txt')
    list_of_names.extend(list_of_male_names)
    list_of_names.extend(list_of_female_names)

    doc_str = codecs.open(file_name, "r", 'utf-8', 'ignore').read()
    cap_val_list = doc_str.split('\r\n')
    for line in enumerate(cap_val_list):
        index = line[0]
        line = line[1].replace('Page', '').split(' ')
        bialist = nltk.bigrams(line)
        save = ''
        for (first, last) in bialist:
            if first in list_of_names and first != save:
                gender = ''
                if first in list_of_male_names:
                    gender = 'M'
                elif first in list_of_female_names:
                    gender = 'F'
                if last in list_of_names:
                    if first + ' ' + last not in name_dict.keys():
                        name_dict[first + ' ' + last] = (index, gender)
                    save = last
                else:
                    if first not in name_dict.keys():
                        name_dict[first] = (index, gender)

    if len(name_dict) >= 1:
        filename = (file_name.split('\\')[-1]).split('.pgr')[0]
        name_dict = dict(sorted(name_dict.items(), key=lambda x: x[1][0]))
        for name, value in name_dict.items():
            index = value[0]
            gender = value[1]
            df_out = pd.DataFrame({"Filename": [filename], "Line": [index], "Name": [name], "Gender": [gender]})
            print(df_out)


files = os.listdir(path)
for file in files:
    if file.startswith('book'):
        print(file)
        extract_name_and_gender(path + file)
    else:
        pass
print("finished")


