from lark_parser import get_grammer_for_generate_enbf
import detect_change_place_lib
from lexical_token_scala import scala3_lexical_tokens 
from lark import Lark
from snippet_maker_lib import making_grammertical_example
from for_worksheet import attach_head,attach_tail,make_compilable_code,get_attached_place,get_original_start_pos
import re

for_blank_and_newline = re.compile(r'((\s|\n)+)')

def get_key_from_grammer(grammer,change_key_name:str):
    start_key = ''
    for key,value in grammer.items():
        if key.to_string() == change_key_name:
            start_key = key
            break
    return start_key

def make_parser(lark_file_place:str,keep_token:bool):
    with open(lark_file_place, encoding="utf-8") as grammar:
        parser = Lark(grammar.read(),keep_all_tokens=keep_token)
        return parser

class make_fuzzer_from_quiz_code:
    def __init__(self,default_search_length,default_search_depth):
        self.parser_for_changeplace = make_parser("./scala3_ebnf_custom.lark",True)
        parser_for_lark = make_parser("./lark.lark",False)
        self.grammer_for_generate = get_grammer_for_generate_enbf(parser_for_lark,"./scala3_ebnf_custom.lark")
        self.snippet_maker = making_grammertical_example(self.grammer_for_generate,default_search_length,default_search_depth)

    def load_code(self,code:str,answer_change:str,answer_msg:str):
        self.default_code = code
        attached_code = make_compilable_code(code)
        self.tree_node, self.token_dict, pos_token_list = detect_change_place_lib.make_tree_and_dict_from_lark(self.parser_for_changeplace,attached_code)
        
        # Add tokens in answer and errormsg
        splited_strs = for_blank_and_newline.split(answer_change + ' ' + answer_msg)
        self.lexical_tokens = scala3_lexical_tokens(self.token_dict['ID'],splited_strs)

        # remove attach head and attach tail
        not_attach_start = len(attach_head)
        not_attach_end = len(attached_code) - len(attach_tail)
        self.default_pos_token_list = list(map(lambda x: (get_original_start_pos(attached_code,x[0]),x[1]),filter(lambda x:x[0]>=not_attach_start and x[0] < not_attach_end,pos_token_list)))

    
    def make_grammatical_fuzzer(self,default_change_place,search_length,search_depth):
        change_place = get_attached_place(self.default_code,default_change_place)
        change_key_name,change_key_string = detect_change_place_lib.get_change_place_token(self.tree_node,change_place)
        
        if change_key_name == '':
            return {},set()
        
        ans_dict = {}
        print(change_key_name)

        if hasattr(self.lexical_tokens,change_key_name.lower()):
            ans_dict['in_terminal'] = getattr(self.lexical_tokens,change_key_name.lower()) | self.lexical_tokens.wildcard_id
            return ans_dict,{'in_terminal'}
        else:
            start_key = get_key_from_grammer(self.grammer_for_generate,change_key_name)
            if isinstance(start_key,str):
                ans_dict['one_string'] = {change_key_string}
                return ans_dict,{'one_string'}
            else:
                print('Start collecting valid grammer...')
                examples = self.snippet_maker.collect_example(start_key,search_length,search_depth)
                print('Finish collecting valid grammer.')
                #return examples
            
                for one_strings in examples:
                    if one_strings == '':
                        ans_dict[''] = {''}
                    else:
                        string_list = one_strings.split()
                        head = string_list[0]
                        tail_list = string_list[1:]

                        if head[0] == '"' and head[-1] == '"':
                            temp_set = {head[1:-1]}
                        else:
                            #temp_set = {next(iter(getattr(self.lexical_tokens,head.lower())|self.lexical_tokens.wildcard_id))} # TEMP: pick only one token
                            temp_set = getattr(self.lexical_tokens,head.lower())|self.lexical_tokens.wildcard_id   

                        for one_str in tail_list:
                            if one_str[0] == '"' and one_str[-1] == '"':
                                temp_set = set(map(lambda x:x+' '+one_str[1:-1],temp_set))
                            else:
                                temp_temp_set = set()
                                #for one_str_from_dict in {next(iter(getattr(self.lexical_tokens,one_str.lower())|self.lexical_tokens.wildcard_id))}:  # TEMP: pick only one token  | self.lexical_tokens.wildcard_id
                                for one_str_from_dict in getattr(self.lexical_tokens,one_str.lower())|self.lexical_tokens.wildcard_id:  # TEMP: pick only one token  | self.lexical_tokens.wildcard_id
                                    temp_temp_set |= set(map(lambda x:x+' '+one_str_from_dict,temp_set))
                                temp_set = temp_temp_set

                        ans_dict[one_strings] = temp_set
                return ans_dict,examples
