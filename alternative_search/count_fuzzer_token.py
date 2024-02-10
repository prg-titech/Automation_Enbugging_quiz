from collections import defaultdict
from make_fuzzer_lib import make_fuzzer_from_quiz_code
from sample_quizzes import quiz1,quiz2,quiz3,quiz4,quiz5,quiz6,quiz7,quiz8#,quiz9,quiz10

def count_fuzzing(quiz_list:list):
    fuzzer_maker = make_fuzzer_from_quiz_code(3,30)
    i = 1
    all_token_list = []
    for one_quiz_tuple in quiz_list:
        print('quiz{}'.format(i))
        quiz_code,answer_change,answer_errmsg,list_editable_places,error_place = one_quiz_tuple
        answer_change_place,answer_change_code = answer_change
        fuzzer_maker.load_code(quiz_code,answer_change_code,answer_errmsg)

        all_tokens_num = len(fuzzer_maker.lexical_tokens.all_tokens)
        all_tokens_one_count = all_tokens_num*all_tokens_num*all_tokens_num+all_tokens_num*all_tokens_num+all_tokens_num
        if list_editable_places == []:
            search_pos_token_list = fuzzer_maker.default_pos_token_list
        else:
            search_pos_token_list = list(map(lambda x:(x[0],quiz_code[x[0]:x[1]]),list_editable_places))

        count_check_tokens = 0
        if_all_check = 0
        list_num = 0

        for start_pos,in_code_token in search_pos_token_list:
            if in_code_token != '\\n':
                print('pos: {}, token: {}'.format(start_pos,in_code_token))
                change_place = (start_pos,start_pos+len(in_code_token))
                generated_fuzz,dict_index = fuzzer_maker.make_grammatical_fuzzer(change_place,3,31)
                all_check_tokens = set()
                for one_index in dict_index:
                    all_check_tokens |= generated_fuzz[one_index]

                count_check_tokens+= len(all_check_tokens)
                if_all_check += all_tokens_one_count
                
                print('### Finish fuzzing of token "'+in_code_token + '" place ###')
                
            list_num += 1
        
        print('### Number of all_tokens_num is {} ###'.format(all_tokens_num))
        print('### Number of check tokens are {} ###'.format(count_check_tokens))
        print('### If check all tokens collaboration, all_number is {} ###'.format(if_all_check))
    
        i += 1

quiz_list = [quiz1,quiz2,quiz3,quiz4,quiz5,quiz6,quiz7,quiz8]
count_fuzzing(quiz_list)
#count_fuzzing([quiz10])