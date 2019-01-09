# -*- coding: utf-8 -*-

import os
import re
import nltk
import pandas as pd
from nltk.corpus import names

path = ".\\half_done\\"
print_appearance_dict = False
print_family_name_dict = False
appear_dict_radius = 4
threshold = 0
file_line_count = 0


def extract_name(file_name):
    name_dict = {}
    list_of_names = []
    extra_name = open(".\\half_done\\PotterNameEnglishOutput_save.txt", "r+", encoding="utf-8")
    list_of_male_names = names.words('male.txt')
    list_of_female_names = names.words('female.txt')
    list_of_names.extend(extra_name.read().split(" "))
    list_of_names.extend(list_of_male_names)
    list_of_names.extend(list_of_female_names)

    doc = open(file_name, "r", encoding='utf-8')
    doc_list = [line for line in doc]

    for line in enumerate(doc_list):
        index = line[0]
        line = line[1]
        # NOTICE: Two names near comma will not be mixed together cause their are two ' '
        # we'll be grateful if there are two spaces between each sentences
        pattern = r'(,|(?<!rs|Mr)\.|’|(?<=rs|Mr)\. )'
        line = re.sub(pattern, ' ', line)
        line = line.split(' ')

        tri_list = nltk.trigrams(line)
        save2 = ''
        save3 = ''
        Mlist = ["Mr", "Mrs", "Miss"]
        for (first, second, third) in tri_list:
            if first in list_of_names and first != save2:
                if first in Mlist:
                    if second in list_of_names and second != save3:
                        if third in list_of_names:
                            if second + ' ' + third in name_dict.keys():
                                # name_dict[second + ' ' + third][1] += 1
                                name_dict[second + ' ' + third].append(index)
                            else:
                                # name_dict[second + ' ' + third] = [round(index / len(doc_list) * 100, 2), 1]
                                name_dict[second + ' ' + third] = [index]
                            save2 = second
                            save3 = third
                        else:
                            if first + ' ' + second in name_dict.keys():
                                # name_dict[first + ' ' + second][1] += 1
                                name_dict[first + ' ' + second].append(index)
                            else:
                                # name_dict[first + ' ' + second] = [round(index / len(doc_list) * 100, 2), 1]
                                name_dict[first + ' ' + second] = [index]
                            save2 = second
                            save3 = ''
                else:
                    if second in list_of_names and second != save3:
                        if third not in list_of_names:
                            if first + ' ' + second in name_dict.keys():
                                # name_dict[first + ' ' + second][1] += 1
                                name_dict[first + ' ' + second].append(index)
                            else:
                                # name_dict[first + ' ' + second] = [round(index / len(doc_list) * 100, 2), 1]
                                name_dict[first + ' ' + second] = [index]
                            save2 = second
                            save3 = ''
                    else:
                        if first in name_dict.keys():
                            # name_dict[first][1] += 1
                            name_dict[first].append(index)
                        else:
                            # name_dict[first] = [round(index / len(doc_list) * 100, 2), 1]
                            name_dict[first] = [index]
                        save2 = ''
                        save3 = ''
    global file_line_count
    file_line_count = len(doc_list)
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
                    # family_name_dict[family_name][0] += info[1]
                    family_name_dict[family_name][0] += len(info)
                    family_name_dict[family_name][1].append((name[0], info))
                    no_family_name = False
                    break
            # add mentioned count
            if no_family_name:
                # Someone like professor Dumbledore is frequently called by his last name
                if name[0] in family_name_dict.keys():
                    # family_name_dict[name[0]][0] += info[1]
                    family_name_dict[name[0]][0] += len(info)
                    family_name_dict[name[0]][1].append((name[0], info))
                else:
                    # family_name_dict["NoFamilyName"][0] += info[1]
                    family_name_dict["NoFamilyName"][0] += len(info)
                    family_name_dict["NoFamilyName"][1].append((" ".join(name), info))
        else:
            # just in case
            if len(name) == 2 and name[1] in family_name_dict.keys():
                # family_name_dict[name[1]][0] += info[1]
                family_name_dict[name[1]][0] += len(info)
                family_name_dict[name[1]][1].append((" ".join(name), info))
    family_name_dict = dict(sorted(family_name_dict.items(), key=lambda x: x[0]))
    if print_family_name_dict:
        for family_name, info in family_name_dict.items():
            mat = "{:25}\t{:5}\t{:}"
            family_member = [member[0] for member in info[1]]
            print(mat.format(family_name, str(info[0]), " / ".join(family_member)))
    return family_name_dict


def name_dict_select(name_dict, thres):
    del_index = []
    for name, info in name_dict.items():
        if len(info) <= thres:
            del_index.append(name)
    for index in del_index:
        del name_dict[index]
    return name_dict


def build_appearance_dict(family_name_dict, radius):
    global file_line_count
    appearance_dict = {}.fromkeys([line for line in range(file_line_count)])
    for key in appearance_dict.keys():
        appearance_dict[key] = set()
    for family_name, info in family_name_dict.items():
        for member_name, appear in info[1]:
            for index in appear:
                appearance_dict[index].add(member_name)

    # Projection
    appearance_proj_dict = {}.fromkeys([line for line in range(file_line_count)])
    for key in appearance_proj_dict.keys():
        appearance_proj_dict[key] = set()
    for key in appearance_dict.keys():
        if key - radius >= 0 and key + radius < file_line_count:
            for line in range(key - radius, key + radius + 1):
                appearance_proj_dict[key] = appearance_dict[key] | appearance_dict[line]

    if print_appearance_dict:
        for line, appear_member in appearance_proj_dict.items():
            if len(appear_member):
                mat = "{:<5}: {:}"
                print(mat.format(line, " / ".join(appear_member)))
    return appearance_proj_dict


def display(input_dict, display_type='first_appear'):
    if display_type == 'first_appear':
        input_dict = dict(sorted(input_dict.items(), key=lambda x: x[1][0]))
        print('Appearance Sequence: ')
        seq = pd.Series(key for key in input_dict.keys())
        pd.set_option('max_rows', 200)
        print(seq)
    elif display_type == 'print_name_dict':
        global file_line_count
        if len(input_dict) >= 1:
            # filename = (file_name.split('\\')[-1]).split('.pgr')[0]
            input_dict = dict(sorted(input_dict.items(), key=lambda x: x[0]))
            print("Characters and their information: ")
            for name, info in input_dict.items():
                index = round(info[0] / file_line_count * 100, 2)
                count = len(info)
                df_out = pd.DataFrame({"Name": [name], "FirstOnStage": [str(index) + "%"], "Mentioned": [count]})
                print(df_out)
    elif display_type == 'print_family_name_dict':
        # TODO print family name dict
        pass
    elif display_type == 'print_appearance_dict(after projection)':
        # TODO print appearance dict
        pass

files = os.listdir(path)
command_dict = {'0': "first_appear", '1': "print_name_dict", '2': "print_family_name_dict",
                '3': "print_appearance_dict(after projection)"}
for file in files:
    # TODO file selection
    file_name = 'book1_sent.txt'
    if file.startswith(file_name):
        print(file)
        name_dict = extract_name(path + file)
        # name dictionary treatment: threshold
        name_dict = name_dict_select(name_dict, threshold)
        family_name_dict = family_name_extract(name_dict)
        family_name_dict = build_family_tree(name_dict, family_name_dict)
        appearance_proj_dict = build_appearance_dict(family_name_dict, appear_dict_radius)
        while True:
            command = input('Available commands: ' + str(command_dict))
            # TODO: dict might be different
            selected_dict = name_dict
            display(selected_dict, command_dict[command])
    else:
        pass
print("finished")


