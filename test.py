# -*- coding: utf-8 -*-
import json
import string
from functools import cmp_to_key
import random
typelist = ['Simple Question (Direct)_',
            'Verification (Boolean) (All)_',
            'Quantitative Reasoning (Count) (All)_',
            'Logical Reasoning (All)_',
            'Comparative Reasoning (Count) (All)_',
            'Quantitative Reasoning (All)_',
            'Comparative Reasoning (All)_'
            ]

class Retriever():
    def __init__(self):
        with open("CSQA_result_question_type_944k.json", "r", encoding='UTF-8') as CSQA_List:
            self.dict944k = json.load(CSQA_List)
        with open("CSQA_result_question_type_count944k.json", "r", encoding='UTF-8') as CSQA_List_weak:
            self.dict944k_weak = json.load(CSQA_List_weak)

    def Retrieve(self, N, key_name, key_weak, question):
        if key_name in self.dict944k:
            candidate_list = self.dict944k[key_name]
            sort_candidate = sorted(candidate_list, key=cmp_to_key(self.MoreSimilarity))
            topNList = sort_candidate if len(sort_candidate) <= N else sort_candidate[0:N]

            if len(topNList) < N:
                print(len(topNList), " found of ", N)
                if key_weak in self.dict944k_weak:
                    weak_list = self.dict944k_weak[key_weak]
                    sort_candidate_weak = sorted(weak_list, key=cmp_to_key(self.MoreSimilarity))
                    for c_weak in sort_candidate_weak:
                        if len(topNList) == N:
                            break
                        if c_weak not in topNList:
                            topNList.append(c_weak)
                            print(len(topNList))
            return topNList

    def MoreSimilarity(self, sentence1 , sentence2):
        return self.Calculatesimilarity(sentence1, question) < self.Calculatesimilarity(sentence2, question)

    def Calculatesimilarity(self, sentence1, sentence2):
        trantab = str.maketrans({key: None for key in string.punctuation})
        s1 = str(sentence1.values()).translate(trantab)
        s2 = sentence2.translate(trantab)
        list1 = s1.split(' ')
        list2 = s2.split(' ')
        intersec = set(list1).intersection(set(list2))
        union = set([])
        union.update(list1)
        union.update(list2)
        jaccard = float(len(intersec)) / float(len(union)) if len(union) != 0 else 0
        return jaccard

retriever =  Retriever()

result_dict = {}
with open("RL_train_TR.question", "r", encoding='UTF-8') as questions:
    load_dict = json.load(questions)
    keys = list(load_dict.keys())
    random.shuffle(keys)

    shuffled_load_dict = dict()
    for key in keys:
        shuffled_load_dict.update({key: load_dict[key]})

    q_topK_map = {}

    current_type = 0

    for i in range(0, 6):
        current_type = i
        current_type_count = 0
        for key, value in shuffled_load_dict.items():
            entity_count = len(value['entity'])
            relation_count = len(value['relation'])
            type_count = len(value['type'])
            question = value['question']
            relation_list = value['relation']
            relation_str = '_'.join(relation_list)

            type_name = typelist[0]
            for typei in typelist:
                if typei in key:
                    type_name = typei
            if type_name == typelist[current_type]:
                current_type_count += 1

                if current_type_count >= 20:
                    break
                else:
                    key_name = '{0}{1}_{2}_{3}_{4}'.format(type_name, entity_count, relation_count, type_count,
                                                           relation_str)
                    key_weak = '{0}{1}_{2}_{3}'.format(type_name, entity_count, relation_count, type_count)

                    topNlist = retriever.Retrieve(20, key_name, key_weak, question)

                    key_question = key + ' : ' + question
                    item_key = {key_question: topNlist}
                    q_topK_map.update(item_key)


    with open('top20_N.json', 'w', encoding='utf-8') as f:
        json.dump(q_topK_map, f, indent=4)


