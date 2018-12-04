# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 13:32:20 2017

@author: anjalidharmik
"""

import codecs
import nltk
import pandas as pd
from nltk.corpus import names
from operator import itemgetter


def extract_name_and_gender(file_name):
    name_l = []
    list_of_names =[]
    list_of_male_names = names.words('male.txt')
    list_of_female_names = names.words('female.txt')
    list_of_names.extend(list_of_male_names)
    list_of_names.extend(list_of_female_names)

    doc_str = codecs.open(file_name, "r", 'utf-8', 'ignore').read()
    cap_val_list = doc_str.split('\r\n')
    for line in cap_val_list:
        line = line.replace('Page', '').split(' ')
        bialist = nltk.bigrams(line)

        save = ''
        for (first, last) in bialist:
            if first in list_of_names and first != save :
                gender = ''
                if first in list_of_male_names:
                    gender = 'M'
                elif first in list_of_female_names:
                    gender = 'F'
                if last in list_of_names:
                    name_l.append((first + ' ' + last, gender))
                    save = last
                else:
                    name_l.append((first, gender))

    if len(name_l) >= 1:
        filename = (file_name.split('\\')[-1]).split('.pgr')[0]
        name_l = sorted(set(name_l), key=itemgetter(0))
        for name_t in name_l:
            name = name_t[0]
            gender = name_t[1]
            df_out = pd.DataFrame({"Filename": [filename], "Name": [name], "Gender": [gender]})
            print(df_out)


file_name = '.\half_done\\raw_input.txt'
extract_name_and_gender(file_name)
