from compile_run_scala import use_cli
import re
import time
import write_read_message_lib
from for_worksheet import make_compilable_code

for_blank = re.compile(r'(\s)+')

def get_error_msg(code:str,num):
    ans = use_cli(code,'./fuz_place/fuzzing{}.scala'.format(num),True)
    time.sleep(0.2)
    return ans

# Currently assuming that there is only one message is targeted.
class error_message_collector_with_fuzzing:
    def __init__(self,code:str):
        self.default_code = code
        self.counter = 0
        self.hash = write_read_message_lib.get_hash_from_code(code)

    def oneplace_fuzzing(self,change_place,fuzzes:set,default_token:str,answe_msg:str):
        if write_read_message_lib.exist_list(self.hash,change_place):
            token_and_error_sets = write_read_message_lib.read_error_msgs_set(self.hash,change_place)
            same_error_tokens = set()
            for one_token,error_sets in token_and_error_sets:
                for one_err in error_sets:
                    if for_blank.sub('',one_err) == check_answer:
                        same_error_tokens.add(one_token)
                return same_error_tokens
            
        else:
            check_answer = for_blank.sub('',answe_msg)
            change_start,change_end = change_place
            same_error_tokens = set()
            token_and_errorsets = []
            for one_token in fuzzes:
                if one_token != default_token:
                    self.counter += 1
                    print('...checking '+ one_token + ' output...')
                    error_sets = get_error_msg(make_compilable_code(self.default_code[:change_start]+one_token+self.default_code[change_end:]),self.counter)
                    for one_err in error_sets:
                        if for_blank.sub('',one_err) == check_answer:
                            same_error_tokens.add(one_token)
                    token_and_errorsets.append((one_token,error_sets))

            write_read_message_lib.write_error_msgs_set(token_and_errorsets,self.hash,change_place)
            return same_error_tokens