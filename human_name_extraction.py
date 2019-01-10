# -*- coding: utf-8 -*-

import os
import re
import nltk
import tqdm
import numpy as np
import itertools
import pandas as pd

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import names
import pre_treatment

path = ".\half_done\\"

appear_dict_radius = 4
threshold = 0
file_line_count = 0
# relation extraction related
figure_selected = 30
pd.set_option('max_rows', 20)

name_dict = {}
family_name_dict = {}
appearance_proj_dict = {}
# Node in relation graph
freq_dict = {}
# Edge in relation graph
relation_score_dict = {}


def extract_name(file_name):
    print("\nBuilding Name Dictionary from \"", file_name[len(path):], "\"...")
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

    for line in tqdm.tqdm(range(len(doc_list)), ncols=60):
        index = line
        line = doc_list[line]
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
                                name_dict[second + ' ' + third].append(index)
                            else:
                                name_dict[second + ' ' + third] = [index]
                            save2 = second
                            save3 = third
                        else:
                            if first + ' ' + second in name_dict.keys():
                                name_dict[first + ' ' + second].append(index)
                            else:
                                name_dict[first + ' ' + second] = [index]
                            save2 = second
                            save3 = ''
                else:
                    if second in list_of_names and second != save3:
                        if third not in list_of_names:
                            if first + ' ' + second in name_dict.keys():
                                name_dict[first + ' ' + second].append(index)
                            else:
                                name_dict[first + ' ' + second] = [index]
                            save2 = second
                            save3 = ''
                    else:
                        if first in name_dict.keys():
                            name_dict[first].append(index)
                        else:
                            name_dict[first] = [index]
                        save2 = ''
                        save3 = ''
    global file_line_count
    file_line_count = len(doc_list)
    print("Name Dictionary Successfully Built")
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
                    family_name_dict[family_name][0] += len(info)
                    family_name_dict[family_name][1].append((name[0], info))
                    no_family_name = False
                    break
            # add mentioned count
            if no_family_name:
                # Someone like professor Dumbledore is frequently called by his last name
                if name[0] in family_name_dict.keys():
                    family_name_dict[name[0]][0] += len(info)
                    family_name_dict[name[0]][1].append((name[0], info))
                else:
                    family_name_dict["NoFamilyName"][0] += len(info)
                    family_name_dict["NoFamilyName"][1].append((" ".join(name), info))
        else:
            # just in case
            if len(name) == 2 and name[1] in family_name_dict.keys():
                family_name_dict[name[1]][0] += len(info)
                family_name_dict[name[1]][1].append((" ".join(name), info))
    family_name_dict = dict(sorted(family_name_dict.items(), key=lambda x: x[0]))
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

    return appearance_proj_dict


def characters_relation_extract(input_dict):
    input_dict = dict(sorted(input_dict.items(), reverse=True, key=lambda x: x[1]))
    select_figures = [figure_name for figure_name in input_dict.keys()]
    select_figures = select_figures[:figure_selected]
    relation_list = list(itertools.combinations(select_figures, 2))
    relation_score_dict = {}.fromkeys(relation_list)
    for key in relation_score_dict.keys():
        relation_score_dict[key] = 0
    for line, appear_list in appearance_proj_dict.items():
        for relation in relation_list:
            if set(relation).issubset(set(appear_list)):
                relation_score_dict[relation] += 1

    breakup = []
    for relation, score in relation_score_dict.items():
        if score == 0:
            breakup.append(relation)
    for breakup_relation in breakup:
        del relation_score_dict[breakup_relation]

    relations = list(relation_score_dict.keys())
    scores = np.asarray(list(relation_score_dict.values()))
    nor_scores = []
    for score in scores:
        score = round((score - scores.min()) / (scores.max() - scores.min()), 5)
        nor_scores.append(score)

    df_out = pd.DataFrame()
    df_out['Existed Relations in Passage'] = relations
    df_out['Score(Normalized)'] = nor_scores
    print(df_out.sort_values(by='Score(Normalized)', ascending=False))
    return relation_score_dict


def display(input_dict, display_type='first_appear'):
    if display_type == 'first_appear':
        input_dict = dict(sorted(input_dict.items(), key=lambda x: x[1][0]))
        print('Appearance Sequence: ')
        seq = pd.Series(key for key in input_dict.keys())
        print(seq)
    elif display_type == 'print_name_dict':
        global file_line_count
        if len(input_dict) >= 1:
            input_dict = dict(sorted(input_dict.items(), key=lambda x: x[0]))
            print("Characters and their information: ")
            name = []
            first_appearance = []
            mentioned = []
            for key, value in input_dict.items():
                name.append(key)
                first_appearance.append(round(value[0] / file_line_count * 100, 2))
                mentioned.append(len(value))
            df_out = pd.DataFrame()
            df_out['Name'] = name
            df_out['FirstMentioned(%)'] = first_appearance
            df_out['Mentioned'] = mentioned
            print(df_out)
    elif display_type == 'print_family_name_dict':
        print("Family Name Dictionary:")
        for family_name, info in family_name_dict.items():
            mat = "{:25}\t{:5}\t{:}"
            family_member = [member[0] for member in info[1]]
            print(mat.format(family_name, str(info[0]), " / ".join(family_member)))
    elif display_type == 'print_appearance_dict(after projection)':
        for line, appear_member in input_dict.items():
            if len(appear_member):
                mat = "{:<5}: {:}"
                print(mat.format(line, " / ".join(appear_member)))
    elif display_type == 'characters_word_cloud':
        wc = WordCloud(background_color='white')
        wc.generate_from_frequencies(input_dict)
        plt.figure()
        plt.imshow(wc)
        plt.axis('off')
        plt.show()
    elif display_type == 'characters_relation_graph':
        relation_score_dict = characters_relation_extract(input_dict)


files = os.listdir(path)
print('Available files under path ', path, ':\n')
for file in enumerate(files):
    mat = "[{:3}] {:}"
    print(mat.format(file[0], file[1]))
file_name = input('\nWhich to read? (with correct file name):')
# TODO exception
if len(file_name) == 0:
    file_name = 'book1_sent.txt'

if file_name in files:
    if '_sent' not in file_name:
        pre_treatment.text_pre_treat(file_name[0:file_name.find('.')])
        file_name = file_name[0:file_name.find('.')] + '_sent.txt'
        print("Generate: \"", file_name, "\"")
    name_dict = extract_name(path + file_name)
    # name dictionary treatment: threshold
    name_dict = name_dict_select(name_dict, threshold)
    family_name_dict = family_name_extract(name_dict)
    family_name_dict = build_family_tree(name_dict, family_name_dict)
    appearance_proj_dict = build_appearance_dict(family_name_dict, appear_dict_radius)

    full_weight = 0
    for name, appear_list in name_dict.items():
        full_weight += len(appear_list)
        freq_dict[name] = len(appear_list)
    for name, appear_count in freq_dict.items():
        freq_dict[name] = round(appear_count / full_weight, 4)

    while True:
        command_dict = {'0': ["first_appear", name_dict],
                        '1': ["print_name_dict", name_dict],
                        '2': ["print_family_name_dict", family_name_dict],
                        '3': ["print_appearance_dict(after projection)", appearance_proj_dict],
                        '4': ["characters_word_cloud", freq_dict],
                        '5': ["characters_relation_graph", freq_dict]
                        }
        command_table = [(key, value[0]) for key, value in command_dict.items()]
        print('\nAvailable commands: ')
        for (index, command) in command_table:
            mat = "[{:>3}] {:}"
            print(mat.format(index, command))
        command = input('\nCommand selected: ')
        # TODO exception
        selected_dict = command_dict[command][1]
        display(selected_dict, command_dict[command][0])
else:
    pass



