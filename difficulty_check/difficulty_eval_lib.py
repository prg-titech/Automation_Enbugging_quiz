import re
from lark import Lark
from make_tree_from_lark_ast import make_tree_from_lark
from tree_change_lib import get_edit_script,count_e_script,clean_e_script
from get_data_flow import get_dataflow
from for_worksheet import make_compilable_code,get_attached_place
from write_read_message_lib import read_error_msgs_set

def make_parser(lark_file_place:str,keep_token:bool):
    with open(lark_file_place, encoding="utf-8") as grammar:
        parser = Lark(grammar.read(),keep_all_tokens=keep_token)
        return parser    

match_blank = re.compile(r'\n')
match_for_pare = re.compile(r' *')

def lcs(list1:list,list2:list):
    dp = [[0] * (len(list2)+1) for i in range(len(list1)+1)]

    for i, vi in enumerate(list1):
        for j, vj in enumerate(list2):
            if vi == vj:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i+1][j], dp[i][j+1])
    #print(dp[len(list1)][len(list2)])

    ans = []
    i = len(list1) - 1
    j = len(list2) - 1
    while i >= 0 and j >= 0:
        if list1[i] == list2[j]:
            ans.append(list1[i])
            i -= 1
            j -= 1
        elif dp[i+1][j+1] == dp[i][j+1]:
            i -= 1
        elif dp[i+1][j+1] == dp[i+1][j]:
            j -= 1
    ans.reverse()
    return ans

def remove_blank(list_of_lines:list):
    answer = []
    for x in list_of_lines:
        if match_for_pare.fullmatch(x) == None:
            answer.append(x)
    return answer 

def how_near_message(base_msg:str,target_msg:str):
    if target_msg == '':
        return 0
    else:
        lines_base_msg = remove_blank(base_msg.splitlines())
        lines_target_msg = remove_blank(target_msg.splitlines())
        max_line_base = len(lines_base_msg)
        max_line_target = len(lines_target_msg)
        l = 0
        line_scores = []
        match_tokens = []
        countable_line = max_line_base
        while l < max_line_base and l < max_line_target:
            tokens_base_msg = lines_base_msg[l].split()
            tokens_target_msg = lines_target_msg[l].split()

            max_tokens_base = len(tokens_base_msg)
            if max_tokens_base == 0:
                line_scores.append(0)
                match_tokens.append([])
            else:
                score = 0
                match_line = lcs(tokens_base_msg,tokens_target_msg)
                score  = len(match_line)
                match_tokens.append(match_line)

                how_same = score/max_tokens_base
                line_scores.append(how_same)

            l += 1
        return (sum(line_scores)/countable_line,max_tokens_base,match_tokens)



class quiz_code_difficulty:
     def __init__(self,quiz_code):
        self.quiz_code_chars = len(quiz_code)
        self.quiz_code_lines = quiz_code.count('\n')+1

class answer_difficulty:
     def __init__(self,quiz_code:str,answer_change,target_msg:str,error_place):
        answer_change_place,answer_change_code = answer_change
        answer_code = quiz_code[:answer_change_place[0]] + answer_change_code + quiz_code[answer_change_place[1]:]

        if answer_change_code in target_msg:
            self.change_in_message = 0
        else:
            self.change_in_message = 1

        self.amount_of_change = 1+len(answer_change_code)

        (before_root,after_root,lables1,labels2,equal_func,leaf_equal_func) = make_tree_from_lark(make_compilable_code(quiz_code),make_compilable_code(answer_code),make_parser('./scala3_ebnf_custom.lark',False))
        edit_script = get_edit_script(before_root,after_root,lables1,labels2,equal_func,leaf_equal_func)

        self.edit_script = clean_e_script(edit_script)
        self.change_tree_struct = count_e_script(edit_script)

        attached_error_pos = get_attached_place(answer_code,error_place)
        attached_change_place = get_attached_place(answer_code,(answer_change_place[0],answer_change_place[1]+len(answer_change_code)))
        dataflow_length_error,dataflow_path_error = get_dataflow(make_compilable_code(answer_code),make_parser('./scala3_ebnf_small.lark',False),attached_change_place,attached_error_pos)
        
        if dataflow_length_error == -1:
            print('Cannot find dataflow in error code')
            attached_change_place = get_attached_place(quiz_code,answer_change_place)
            if error_place[1] <= answer_change_place[0]:
                attached_error_pos = get_attached_place(quiz_code,error_place)
            else:
                change_length = answer_change_place[1]-answer_change_place[0]-len(answer_change_code)
                if error_place[0] >= answer_change_place[1]:
                    attached_error_pos = get_attached_place(quiz_code,(error_place[0]+change_length,error_place[1]+change_length))
                else:
                    attached_error_pos = get_attached_place(quiz_code,(error_place[0]+change_length,error_place[1]+change_length*2))

            dataflow_length_not_error,dataflow_path_not_error = get_dataflow(make_compilable_code(quiz_code),make_parser('./scala3_ebnf_small.lark',False),attached_change_place,attached_error_pos)
            if dataflow_length_not_error == -1:
                print('Cannot find dataflow in not error code')
            self.dataflow_length = dataflow_length_not_error
            self.dataflow_path = dataflow_path_not_error
        else:
            self.dataflow_length = dataflow_length_error
            self.dataflow_path = dataflow_path_error
        self.pysical_length = abs(answer_change_place[0] - error_place[0])
        print("End initialize")


class target_msg_difficulty:
    def __init__(self,target_msg:str):
        self.target_msg_chars = len(target_msg)
        self.target_msg_lines = target_msg.count('\n')+1


class evaluating_quiz_difficulty:
    def __init__(self,quiz_code,answer_change,target_msg,error_place):
        self.quiz_code = quiz_code
        self.answer_change = answer_change
        self.target_msg = target_msg
        self.error_place = error_place


        self.about_default_code = quiz_code_difficulty(self.quiz_code)
        self.about_assumed_answer = answer_difficulty(self.quiz_code,self.answer_change,self.target_msg,self.error_place)
        self.about_error_msg = target_msg_difficulty(self.target_msg)
        self.editableplace_score_dict = {} 

    def editable_place_msg_score(self,editable_place):
        token_msgset = read_error_msgs_set(self.code,editable_place)
        score_list = []
        for token,msg_set in token_msgset:
            temp_high_score = 0
            for one_msg in msg_set:
                score = how_near_message(self.target_msg,one_msg)
                if score > temp_high_score:
                    temp_high_score = score
            score_list.append(temp_high_score)

        score_list.sort(reverse=True)
        if len(score_list) < 20:
            sumscore = sum(score_list)/len(score_list)
        else:
            sumscore = sum(score_list[:20])/20
        return sumscore
    
    def editable_place_snippet_in_msg(self,editable_place):
        editable_snippet = self.quiz_code[editable_place[0]:editable_place[1]]
        if editable_snippet in self.target_msg:
            return 1
        else:
            separeted_snippet = editable_snippet.split()
            if len(separeted_snippet) == 0:
                return 0
            else:
                num_of_in_msg = 0
                for one_string in separeted_snippet:
                    if one_string in self.target_msg:
                        num_of_in_msg += 1

                return num_of_in_msg / len(separeted_snippet)

    def get_editableplace_score(self,editable_place):
        self.editableplace_score_dict[editable_place] = (self.editable_place_msg_score(editable_place),self.is_editable_place_snippet_in_msg(editable_place))
        return self.editableplace_score_dict[editable_place]


    def editable_places_score(self,editable_place_list):
        scores = []
        for one_place in editable_place_list:
            if not one_place in self.editableplace_score_dict:
                scores.append(self.get_editableplace_score(one_place))
            else:
                scores.append(self.editableplace_score_dict[one_place])
        return len(editable_place_list),scores