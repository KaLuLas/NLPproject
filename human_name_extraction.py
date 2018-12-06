# -*- coding: utf-8 -*-

import os
import re
import nltk
import codecs
import pandas as pd
from nltk.corpus import names

path = ".\\half_done\\"


def extract_name(file_name, need_print = False):
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
        line = line[1].replace('Page', '')
        line = re.sub(r'(Mrs. )', 'Mrs.', line)
        line = re.sub(r'(Mr. )', 'Mr.', line)
        line = re.sub(r'(,|\.)', ' ', line)
        line = line.split(' ')
        bialist = nltk.bigrams(line)
        # to avoid repetition
        save = ''
        for (first, last) in bialist:
            if first in list_of_names and last != "" and first != save:
                # gender = '?'
                # sex classifier abandoned
                # if first in list_of_male_names:
                #     gender = 'M'
                # elif first in list_of_female_names:
                #     gender = 'F'

                if last in list_of_names:
                    # recover from the re sub function
                    if first == "Mr" or first == "Mrs":
                        first = first + "."
                    if first + ' ' + last not in name_dict.keys():
                        name_dict[first + ' ' + last] = [round(index / len(cap_val_list) * 100, 2), 1]
                    else:
                        name_dict[first + ' ' + last][1] += 1
                    save = last
                elif first != "Mr" and first != "Mrs":
                    if first not in name_dict.keys():
                        name_dict[first] = [round(index / len(cap_val_list) * 100, 2), 1]
                    else:
                        name_dict[first][1] += 1

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
                family_name_dict[name[1]] = [info[1], []]
            else:
                # family_name_mentioned count
                # name_dict[name][1] : name mentioned
                family_name_dict[name[1]][0] += info[1]
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
            # Someone like professor Dumbledore is frequently called by his last name
            if name[0] in family_name_dict.keys():
                family_name_dict[name[0]][0] += info[1]
                family_name_dict[name[0]][1].append((name[0], info))
            # add mentioned count
            elif no_family_name:
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
    if file.startswith('book1'):
        print(file)
        # name_dict = extract_name(path + file, True)
        name_dict = extract_name(path + file)
        family_name_dict = family_name_extract(name_dict)
        family_name_dict = build_family_tree(name_dict, family_name_dict)
        family_name_dict = dict(sorted(family_name_dict.items(), key=lambda x: x[0]))
        for family_name, info in family_name_dict.items():
            mat = "{:12}\t{:}"
            print(mat.format(family_name, "".join(str(info))))
    else:
        pass
print("finished")


