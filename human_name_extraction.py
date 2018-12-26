# -*- coding: utf-8 -*-

import os
import re
import nltk
import codecs
import pandas as pd
from nltk.corpus import names

path = ".\\half_done\\"


def extract_name(file_name, need_print=False):
    name_dict = {}
    list_of_names = []
    extra_name = open(".\\half_done\\PotterNameEnglishOutput_save.txt", "r+", encoding="utf-8")
    list_of_male_names = names.words('male.txt')
    list_of_female_names = names.words('female.txt')
    list_of_names.extend(extra_name.read().split(" "))
    list_of_names.extend(list_of_male_names)
    list_of_names.extend(list_of_female_names)

    doc_str = codecs.open(file_name, "r", 'utf-8', 'ignore').read()
    cap_val_list = doc_str.split('\r\n')
    for line in enumerate(cap_val_list):
        index = line[0]
        # NOTICE: Two names near comma will not be mixed together cause their are two ' '
        # TODO: Pretreatment.py should do work below + delete empty and title
        # if line[1].startswith('Page'):
        #    continue
        line = line[1]
        line = re.sub(r'(Mrs. )', 'Mrs.', line)
        line = re.sub(r'(Mr. )', 'Mr.', line)
        # we'll be grateful if there are two spaces between each sentences
        # after precise pre-treatment(divided by sentence), this strategy is no longer needed
        line = re.sub(r'(,|\.|’)', ' ', line)
        line = line.split(' ')

        trilist = nltk.trigrams(line)
        save2 = ''
        save3 = ''
        Mlist = ["Mr", "Mrs", "Miss"]
        for (first, second, third) in trilist:
            if first in list_of_names and first != save2:
                if first in Mlist:
                    if second in list_of_names and second != save3:
                        if third in list_of_names:
                            if second + ' ' + third in name_dict.keys():
                                name_dict[second + ' ' + third][1] += 1
                            else:
                                name_dict[second + ' ' + third] = [round(index / len(cap_val_list) * 100, 2), 1]
                            save2 = second
                            save3 = third
                        else:
                            if first + ' ' + second in name_dict.keys():
                                name_dict[first + ' ' + second][1] += 1
                            else:
                                name_dict[first + ' ' + second] = [round(index / len(cap_val_list) * 100, 2), 1]
                            save2 = second
                            save3 = ''
                else:
                    if second in list_of_names and second != save3:
                        if third not in list_of_names:
                            if first + ' ' + second in name_dict.keys():
                                name_dict[first + ' ' + second][1] += 1
                            else:
                                name_dict[first + ' ' + second] = [round(index / len(cap_val_list) * 100, 2), 1]
                            save2 = second
                            save3 = ''
                    else:
                        if first in name_dict.keys():
                            name_dict[first][1] += 1
                        else:
                            name_dict[first] = [round(index / len(cap_val_list) * 100, 2), 1]
                        save2 = ''
                        save3 = ''

    if len(name_dict) >= 1:
        filename = (file_name.split('\\')[-1]).split('.pgr')[0]
        name_dict = dict(sorted(name_dict.items(), key=lambda x: x[0]))
        if need_print:
            print("Characters and their information: ")
            for name, value in name_dict.items():
                index = value[0]
                count = value[1]
                df_out = pd.DataFrame({"Filename": [filename], "Name": [name], "FirstOnStage": [str(index) + "%"],
                                       "Mentioned": [count]})
                print(df_out)
    return name_dict


def family_name_extract(name_dict):
    family_name_dict = {}
    for name, info in name_dict.items():
        name = str(name).split(" ")
        if len(name) == 2:
            if name[1] not in family_name_dict.keys():
                family_name_dict[name[1]] = [0, []]
    family_name_dict["NoFamilyName"] = [0, []]
    return family_name_dict


def build_family_tree(name_dict, family_name_dict):
    for name, info in name_dict.items():
        name = str(name).split(" ")
        if len(name) == 1:
            no_family_name = True
            # To check whether this character has a family
            # Notice: Assuming that the full name of this character is captured in name_dict
            for family_name in family_name_dict.keys():
                if " ".join([name[0], family_name]) in name_dict.keys():
                    family_name_dict[family_name][0] += info[1]
                    family_name_dict[family_name][1].append((name[0], info))
                    no_family_name = False
                    break
            # add mentioned count
            if no_family_name:
                # Someone like professor Dumbledore is frequently called by his last name
                if name[0] in family_name_dict.keys():
                    family_name_dict[name[0]][0] += info[1]
                    family_name_dict[name[0]][1].append((name[0], info))
                else:
                    family_name_dict["NoFamilyName"][0] += info[1]
                    family_name_dict["NoFamilyName"][1].append((" ".join(name), info))
        else:
            # just in case
            if len(name) == 2 and name[1] in family_name_dict.keys():
                family_name_dict[name[1]][0] += info[1]
                family_name_dict[name[1]][1].append((" ".join(name), info))
    return family_name_dict


files = os.listdir(path)
for file in files:
    file_name = 'book1_sent.txt'
    if file.startswith(file_name):
        print(file)
        # name_dict = extract_name(path + file, True)
        name_dict = extract_name(path + file)
        family_name_dict = family_name_extract(name_dict)
        family_name_dict = build_family_tree(name_dict, family_name_dict)
        family_name_dict = dict(sorted(family_name_dict.items(), key=lambda x: x[0]))
        file_pre = file[:file.find('.')]
        output_text = open(path + file_pre + "_name_extract.txt", "w", encoding="utf-8")
        for family_name, info in family_name_dict.items():
            mat = "{:12}\t{:}"
            output_text.write(mat.format(family_name, "".join(str(info))) + '\n')
            # print(mat.format(family_name, "".join(str(info))))
    else:
        pass
print("finished")


