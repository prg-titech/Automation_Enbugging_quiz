from collections import defaultdict
from make_fuzzer_lib import make_fuzzer_from_quiz_code
from fuzzing_lib import error_message_collector_with_fuzzing
from sample_quizzes import quiz1,quiz2,quiz3,quiz4,quiz5,quiz6,quiz7,quiz8

def do_error_message_fuzzing(quiz_list:list):
    fuzzer_maker = make_fuzzer_from_quiz_code(5,30)
    for one_quiz_tuple in quiz_list:
        quiz_code,answer_change,answer_errmsg,list_editable_places,error_place = one_quiz_tuple
        error_msg_collector = error_message_collector_with_fuzzing(quiz_code)
        answer_change_place,answer_change_code = answer_change
        fuzzer_maker.load_code(quiz_code,answer_change_code,answer_errmsg)

        if list_editable_places == []:
            search_pos_token_list = fuzzer_maker.default_pos_token_list
        else:
            search_pos_token_list = list(map(lambda x:(x[0],quiz_code[x[0]:x[1]]),list_editable_places))

        alternative_place_and_token = defaultdict(set)
        list_num = 0

        for start_pos,in_code_token in search_pos_token_list:
            if in_code_token != '\\n':
                print('pos: {}, token: {}'.format(start_pos,in_code_token))
                change_place = (start_pos,start_pos+len(in_code_token))
                generated_fuzz,dict_index = fuzzer_maker.make_grammatical_fuzzer(change_place,3,31)

                # Check output error messages
                all_grammatical_fuz = set()
                for one_index in dict_index:
                    all_grammatical_fuz |= generated_fuzz[one_index]
                
                same_error_tokens = error_msg_collector.oneplace_fuzzing(change_place,all_grammatical_fuz,in_code_token,answer_errmsg)
                if same_error_tokens != set():
                    print('### Found token(s) which can make the answer error message ###')
                    print(same_error_tokens)
                    alternative_place_and_token[list_num] |= same_error_tokens
                
                print('### Finish fuzzing of token "'+ in_code_token + '" place ###')
                
            list_num += 1
        
        print('### Finish all check ###')
        print(alternative_place_and_token)

text = '''def append(x:Int,list:List[Int]) : List[Int] = {
    x :: list
}'''

ans_change = ((53,54),'true')

ans_error_msg = '''Found:    (true : Boolean)
Required: Int'''

do_error_message_fuzzing([(text,ans_change,ans_error_msg,[(4,10)],(50,54))])
# quiz_list = [quiz1,quiz2,quiz3,quiz4,quiz5,quiz6,quiz7,quiz8]
# do_error_message_fuzzing(quiz_list)