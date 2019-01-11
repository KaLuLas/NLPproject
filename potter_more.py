# -*- coding: utf-8 -*-

import os
import re
import nltk
import tqdm
import pickle
import numpy as np
import itertools
import pandas as pd

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import names
import pre_treatment
import relation_predict

path = ".\half_done\\"
save_csv_path = ".\csv\\"
save_pkl_path = ".\save\\"
file_name_prefix = ""
file_name = ""

appear_dict_radius = 4
threshold = 0
file_line_count = 0
# relation extraction related
figure_selected = 30
pd.set_option('max_rows', 20)

name_dict = {}
family_name_dict = {}
appearance_proj_dict = {}
relation_record_dict = {}
# Node / Edge in relation graph
freq_dict = {}
relation_score_dict = {}
build_relation_record_dict = False


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
    global relation_score_dict
    global relation_record_dict
    global build_relation_record_dict
    # read relation dict from pkl
    try:
        load_relation_record = open(save_pkl_path + file_name_prefix + "_relation_record.pkl", 'rb')
        res = input(save_pkl_path + file_name_prefix + "_relation_record.pkl already existed, "
                                                       "read from saved data?[y/n]")
        if res == 'n':
            raise IOError
        relation_record_dict = pickle.load(load_relation_record)
        load_relation_record.close()
        print("Load name_dict and file_count from saved data successful")
    # generate relation record dict
    except IOError:
        print(save_pkl_path + file_name_prefix + "_relation_record.pkl doesn't existed, no saved data available")
        input_dict = dict(sorted(input_dict.items(), reverse=True, key=lambda x: x[1]))
        select_figures = [figure_name for figure_name in input_dict.keys()]
        select_figures = select_figures[:figure_selected]
        relation_list = list(itertools.combinations(select_figures, 2))
        # save location where communication between figures take place
        relation_record_dict = {}.fromkeys(relation_list)
        for key in relation_record_dict.keys():
            relation_record_dict[key] = []

        # generate a progress bar
        pbar = tqdm.tqdm(total=len(appearance_proj_dict), ncols=60)
        for line, appear_list in appearance_proj_dict.items():
            pbar.update(1)
            for relation in relation_list:
                if set(relation).issubset(set(appear_list)):
                    relation_record_dict[relation].append(line)
        pbar.close()

        breakup = []
        for relation, relation_appear_list in relation_record_dict.items():
            if len(relation_appear_list) == 0:
                breakup.append(relation)
        for breakup_relation in breakup:
            del relation_record_dict[breakup_relation]
    # calculate how intimate they are
    relations = list(relation_record_dict.keys())
    scores = np.asarray(list(len(value) for value in relation_record_dict.values()))
    nor_scores = []
    for score in scores:
        score = round((score - scores.min()) / (scores.max() - scores.min()), 5)
        nor_scores.append(score)

    df_out = pd.DataFrame()
    df_out['Existed Relations'] = relations
    df_out['Score(Normalized)'] = nor_scores
    print(df_out.sort_values(by='Score(Normalized)', ascending=False))

    for relation, relation_appear_list in relation_record_dict.items():
        relation_score_dict[relation] = len(relation_appear_list)
    build_relation_record_dict = True


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
        for family_name, info in input_dict.items():
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
    elif display_type == 'characters_relation_graph(csv generate)':
        characters_relation_extract(input_dict)
        with open(save_csv_path + file_name[0:file_name.find(".")] + '_node.csv', 'w', encoding='utf-8') as file:
            file.write('id,label,weight\n')
            for name, freq in freq_dict.items():
                file.write(name + ',' + name + ',' + str(freq) + '\n')
        with open(save_csv_path + file_name[0:file_name.find(".")] + '_edge.csv', 'w', encoding='utf-8') as file:
            file.write('source,target,weight\n')
            for name, freq in relation_score_dict.items():
                file.write(name[0] + ',' + name[1] + ',' + str(freq) + '\n')
    elif display_type == 'train_relation_classifier':
        if build_relation_record_dict:
            relation_predict.train(relation_record_dict, file_name_prefix, name_dict.keys())
        else:
            print("[WARNING] Need to build relation record dict first")


files = os.listdir(path)
print('Available files under path ', path, ':\n')
for file in enumerate(files):
    mat = "[{:3}] {:}"
    print(mat.format(file[0], file[1]))
try:
    file_name = input('\nWhich to read? (with correct file name):')
    if len(file_name) == 0:
        file_name = 'input_sent.txt'
    elif file_name not in files:
        raise ValueError("[ERROR] Invalid Filename")
except ValueError as ve:
    print(ve)

if file_name in files:
    file_name_prefix = file_name[0:file_name.find('.')]
    if '_sent' not in file_name:
        if file_name_prefix + '_sent.txt' not in files:
            pre_treatment.text_pre_treat(file_name_prefix)
            print("[PreTreat]Generated: \"", file_name, "_sent.txt\"")
        file_name = file_name_prefix + '_sent.txt'
        file_name_prefix = file_name[0:file_name.find('.')]

    # load pkl if exised
    try:
        load_name_dict = open(save_pkl_path + file_name_prefix + "_name_dict.pkl", 'rb')
        respond = input(save_pkl_path + file_name_prefix + "_name_dict.pkl already existed, read from saved data?[y/n]")
        if respond == 'n':
            raise IOError
        name_dict = pickle.load(load_name_dict)
        load_name_dict.close()

        load_file_count = open(save_pkl_path + file_name_prefix + "_line_count.pkl", 'rb')
        file_line_count = pickle.load(load_file_count)
        load_file_count.close()
        print("Load name_dict and file_count from saved data successful")
    except IOError:
        print(save_pkl_path + file_name_prefix + "_name_dict.pkl doesn't existed, no saved data available")
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
    # Weight of specific name don't need to be normalized for now
    # for name, appear_count in freq_dict.items():
    #    freq_dict[name] = round(appear_count / full_weight, 4)

    while True:
        command_dict = {'0': ["first_appear", name_dict],
                        '1': ["print_name_dict", name_dict],
                        '2': ["print_family_name_dict", family_name_dict],
                        '3': ["print_appearance_dict(after projection)", appearance_proj_dict],
                        '4': ["characters_word_cloud", freq_dict],
                        '5': ["characters_relation_graph(csv generate)", freq_dict],
                        '6': ["train_relation_classifier", relation_record_dict],
                        'Q': ["exit", name_dict]
                        }
        command_table = [(key, value[0]) for key, value in command_dict.items()]
        print('\nAvailable commands: ')
        for (index, command) in command_table:
            mat = "[{:>3}] {:}"
            print(mat.format(index, command))
        try:
            command = input('\nCommand selected: ')
            if command == 'Q':
                # Save name dictionary in pkl format
                dict_save = open(save_pkl_path + file_name_prefix + "_name_dict.pkl", 'wb')
                pickle.dump(name_dict, dict_save)
                dict_save.close()
                if build_relation_record_dict:
                    relation_record_save = open(save_pkl_path + file_name_prefix + "_relation_record.pkl", 'wb')
                    pickle.dump(relation_record_dict, relation_record_save)
                    relation_record_save.close()
                line_count_save = open(save_pkl_path + file_name_prefix + "_line_count.pkl", 'wb')
                pickle.dump(file_line_count, line_count_save)
                line_count_save.close()
                print("Save name_dict & relation_record_dict(if built) & file_count successful")
                exit()
            elif command not in command_dict.keys():
                raise KeyError("[ERROR] Invalid Command")
            selected_dict = command_dict[command][1]
            display(selected_dict, command_dict[command][0])
        except IOError:
            print("[ERROR] Save pkl file Failed")
        except KeyError as ke:
            print(ke)
else:
    pass



