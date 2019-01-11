import re
import csv
import nltk
import tqdm
import random
from nltk.corpus import stopwords

path = ".\half_done\\"
save_csv_path = ".\csv\\"
stop_list = []
names = []
text = []


def related_word_freq(appear_list):
    pbar.update(1)
    bow = ""
    for line_num in appear_list:
        # # DEAL WITH WORDS: punctuation
        line = re.sub('[,\!?\.();’”“—-]+', '', text[line_num])
        bow += line
    words = nltk.word_tokenize(bow)
    # DEAL WITH WORDS: stopwords and name
    words = [word.lower() for word in words if word.lower() not in stop_list and word not in names]
    feature_freq = nltk.FreqDist(words)
    return feature_freq


def train(relation_record_dict, file_name_prefix, names_collec):
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
    global pbar
    pbar = tqdm.tqdm(total=len(relation_record_dict), ncols=60)
    feature_set = [(related_word_freq(appear_list), label_dict[relation])
                   for relation, appear_list in relation_record_dict.items()]
    pbar.close()
    sum = 0
    for i in range(50):
        print("round:", i)
        random.shuffle(feature_set)
        test_set = feature_set[:round(len(feature_set)/5)]
        train_set = feature_set[round(len(feature_set)/5):]
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        score = nltk.classify.accuracy(classifier, test_set)
        sum += score
        print("accuracy:", score)
    print("average:", sum/50)
    # classifier.show_most_informative_features(10)

