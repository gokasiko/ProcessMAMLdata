# -*- coding: utf-8 -*-
import json

typelist = ['Simple Question (Direct)_',
            'Verification (Boolean) (All)_',
            'Quantitative Reasoning (Count) (All)_',
            'Logical Reasoning (All)_',
            'Comparative Reasoning (Count) (All)_',
            'Quantitative Reasoning (All)_',
            'Comparative Reasoning (All)_'
            ]

with open("CSQA_result_question_type_count944k.json", "r", encoding='UTF-8') as CSQA_List:
    load_dict = json.load(CSQA_List)
    for key, value in load_dict.items():
        print(key)

        type_name = typelist[0]
        for type in typelist:
            if type in key:
                type_name = type

    # allcount = 0
    # for key, value in result_dict.items():
    #     allcount += len(value)
    #     print(key, value[0], len(value))
    # print(allcount)
    # with open('CSQA_result.json', 'w') as f:
    with open('CSQA_result_question_type_count944k_order.json', 'w') as f:
        json.dump(result_dict, f, indent=2)
