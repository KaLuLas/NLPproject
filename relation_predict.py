import os
import re
import csv
import nltk
import tqdm
import pickle
from nltk.corpus import stopwords

path = ".\corpus\\"
save_csv_path = ".\csv\\"
save_pkl_path = ".\save\\"
save_error_report_path = ".\errors\\"
generate_error_report = False
show_each_score = False
stop_list = []
names = []
text = []


def get_words(appear_list):
    bow = ""
    for line_num in appear_list:
        line = re.sub('[,\!?\.();’”“—-]+', '', text[line_num])
        bow += line
    words = nltk.word_tokenize(bow)
    # words = [word.lower() for word in words if word.lower() not in stop_list and word not in names]
    return words


def bag_of_words(appear_list):
    pbar.update(1)
    words = get_words(appear_list)
    words = set(words)
    return dict([(word, True) for word in words])


def hapax_words(appear_list):
    pbar.update(1)
    words = get_words(appear_list)
    feature_freq = nltk.FreqDist(words)
    hapax_word = feature_freq.hapaxes()
    return dict([(word, True) for word in hapax_word])


def related_word_freq(appear_list):
    pbar.update(1)
    words = get_words(appear_list)
    feature_freq = nltk.FreqDist(words)
    return feature_freq


def find_errors(feature_set, classifier, count):
    errors = []
    full_report = ""
    for (relation, feature, label) in feature_set:
        guess = classifier.classify(feature)
        if guess != label:
            errors.append((label, guess, relation))
    for (label, guess, relation) in sorted(errors):
        report = 'correct= ' + label + ' guess= ' + guess + ' relation= ' + str(relation) + '\n'
        full_report += report
    with open(save_error_report_path + 'guess_report_iter' + str(count) + '.txt', 'w', encoding='utf-8') as file:
        file.write(full_report)
        print("Error report for iter " + str(count) + " saved")
        file.close()


def cross_validate(feature_set, patch, show):
    sum_score = 0
    feature_set_input = []
    slice = round(len(feature_set) / patch)
    for (relation, feature, label) in feature_set:
        feature_set_input.append((feature, label))
    for i in range(patch):
        start = i * slice
        if (i+1) * slice > len(feature_set_input):
            end = len(feature_set_input)
        else:
            end = (i+1) * slice
        test_set = feature_set_input[start:end]
        train_set = [pair for pair in feature_set_input if pair not in test_set]
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        score = nltk.classify.accuracy(classifier, test_set)
        sum_score += score
        if show:
            classifier.show_most_informative_features(10)
            print("iter", i, "accuracy:", score)
        # FIND ERROR MESSAGE
        if generate_error_report:
            find_errors(feature_set, classifier, i)
    aver = sum_score / patch
    print("average score:", aver)
    return aver


def train(relation_record_dict, file_name_prefix, names_collec, length, load_feature_set):
    global stop_list
    global names
    global text
    names = names_collec
    stop_list = stopwords.words('english')
    label_dict = {}
    try:
        file = open(path + file_name_prefix + '.txt', 'r', encoding='utf-8')
        text = [line for line in file]
        file.close()

        relation_table = open(save_csv_path + file_name_prefix + '_relation_label.csv', 'r')
        csv_reader = csv.reader(relation_table)
        for row in csv_reader:
            label_dict[(row[0], row[1])] = row[2]
        relation_table.close()
    except IOError:
        print("[ERROR] Relation Label for" + file_name_prefix + "Not Existed")

    try:
        if load_feature_set:
            load_feature_set_record = open(save_pkl_path + file_name_prefix + "_feature_set.pkl", 'rb')
            feature_set = pickle.load(load_feature_set_record)
            load_feature_set_record.close()
            print("Load feature_set from saved data successful")
        else:
            raise IOError
    # generate relation record dict
    except IOError:
        print("No saved data for feature_set available or necessary")
        global pbar
        pbar = tqdm.tqdm(total=len(relation_record_dict), ncols=60)
        feature_set = [(relation, related_word_freq(appear_list), label_dict[relation])
                       for relation, appear_list in relation_record_dict.items()
                       if relation in label_dict.keys()]
        pbar.close()
    feature_set_cut = sorted(feature_set, key=lambda x: len(relation_record_dict[x[0]]), reverse=True)[:length]
    print("Feature set size:", length)
    score = cross_validate(feature_set_cut, 10, show_each_score)
    if generate_error_report:
        error_report = os.listdir(save_error_report_path)
        error_report_join = set()
        for file_name in error_report:
            if 'join' not in file_name:
                file = open(save_error_report_path + file_name, 'r', encoding='utf-8')
                for line in file:
                    error_report_join.add(line)
                file.close()
        file = open(save_error_report_path + 'guess_report_join.txt', 'w', encoding='utf-8')
        file.write("".join(error_report_join))
        file.close()

    feature_set_save = open(save_pkl_path + file_name_prefix + "_feature_set.pkl", 'wb')
    pickle.dump(feature_set, feature_set_save)
    feature_set_save.close()

    return score


