from collections import defaultdict
from classes import Generatable, Group, Regexp, Nonterminal, Token, Sequence, Plus, Star, Optional, Literal_Range, Repeat, Terminal
from itertools import chain, repeat
import re

for_blank = re.compile(r'(\s)+')

def duplicate_strings(strings:list[str],num_of_max_dupl:int,num_of_min_dupl:int):
    ans = set()
    i = num_of_max_dupl
    while i >= num_of_min_dupl:
        ans.add(' '.join(chain.from_iterable(repeat(strings, i))))
        i -= 1
    return ans


def sub_make_combination_strings(rest_numberd_pairs,limit_length:int):
    if limit_length < 0:
        print('Minus length!')
        return None
    elif rest_numberd_pairs == []:
        return []
    else:
        ans = []
        s_pos,num_string_pairs = rest_numberd_pairs[0]
        if len(rest_numberd_pairs) == 1:
            for num,string in num_string_pairs:
                if num > limit_length:
                    break
                else:
                    ans.append([(s_pos,string)])
            return ans
        else:
            for num,string in num_string_pairs:
                if num > limit_length:
                    break
                else:
                    set_of_list_of_strings = sub_make_combination_strings(rest_numberd_pairs[1:],limit_length-num)
                    if set_of_list_of_strings == []:
                        break
                    else:
                        for list_pos_str in set_of_list_of_strings:
                            ans.append(list_pos_str + [(s_pos,string)])
            return ans
        
def clean_split(string:str):
    return string.strip().split()


def make_combination_strings(already_gen:list,numberd_pos_string_pairs:list,limit_length:int):

    list_of_list_of_strings = sub_make_combination_strings(numberd_pos_string_pairs,limit_length)

    ans = set()
    for one_list_of_strings in list_of_list_of_strings:
        concatenate_list = sorted(already_gen+one_list_of_strings)
        one_strings = ''
        for position, string in concatenate_list:
            if string != '':
                one_strings += string + ' '
        #made_string = ' '.join(map(lambda x: x[1],concatenate_list))
        ans.add(one_strings[:-1])

    return ans

class making_grammertical_example():

    def __init__(self,for_generate_grammar,default_search_length,default_search_depth):
        self.for_generate_grammar = for_generate_grammar
        all_keys = list(for_generate_grammar)
        i = 0
        self.generatable_tokens_dict = defaultdict(set)
        print("Making initial token dictionaly...")
        previous_dict = {}
        while i <= default_search_depth:
            new_dict = defaultdict(set)
            for one_key in all_keys:
                get_token_set = self.collect_example(one_key,default_search_length,i)
                new_dict[one_key.to_string()+ '_$_'+str(i)] = get_token_set
                #self.generatable_tokens_dict[one_key.to_string()+ '_$_'+str(i)] = get_token_set

            previous_dict = self.generatable_tokens_dict
            self.generatable_tokens_dict = new_dict

            print('Depth ' + str(i) + ' is end')
            i += 1
        #self.generatable_tokens_dict = m
            self.generatable_tokens_dict = previous_dict | self.generatable_tokens_dict
        print("End of making initial token dictionaly")

    def collect_strings_in_limit(self,one_alt,limit_length2,limit_depth2):
        if limit_length2 < 0:
            print('Minus length!')
            return None
        else:
            
            if isinstance(one_alt, Sequence):
                alternatives = one_alt.get_arg()
                num_count = 0
                pos = 0
                already_gen = []
                have_to_more_search = []
                for one_elem in alternatives:
                    if one_elem.is_end_point():
                        already_gen.append((pos,one_elem.to_string())) #generate()
                        num_count+=1
                    else:
                        have_to_more_search.append((pos,one_elem))
                    pos += 1
                
                if num_count > limit_length2:
                    return set()
                else:
                    candidate_pairs = []
                    at_least_length = 0
                    for pos, one_elem in have_to_more_search:
                        possible_sets = self.collect_strings_in_limit(one_elem,limit_length2-num_count-at_least_length,limit_depth2)
                        numbered_possible_set = []
                        for string in possible_sets:
                            numbered_possible_set.append((len(clean_split(string)),string))
                        if numbered_possible_set == []:
                            return set()
                        else:
                            numbered_possible_set.sort()
                            candidate_pairs.append((pos,numbered_possible_set))
                            at_least_length += numbered_possible_set[0][0]

                    return make_combination_strings(already_gen,candidate_pairs,limit_length2-num_count)
                
            elif isinstance(one_alt, Nonterminal):
                if limit_depth2 <= 0:
                    return set()
                else:
                    # use prepared data
                    search_name = one_alt.to_string()+ '_$_'+str(limit_depth2-1)
                    if search_name in self.generatable_tokens_dict:                        
                        return set(filter(lambda x: len(clean_split(x)) <= limit_length2,self.generatable_tokens_dict[search_name]))
                    else:
                        next_altanatives = self.for_generate_grammar.get(one_alt)
                        ans = set()
                        for next_alt in next_altanatives:
                            ans |= self.collect_strings_in_limit(next_alt,limit_length2,limit_depth2-1)
                        return ans
                
            elif isinstance(one_alt, Token):
                if limit_length2 == 0:
                    return set()
                else:
                    return {one_alt.to_string()}
                    #return {"Token"}
                
            elif isinstance(one_alt, Optional):
                if limit_length2 == 0:
                    return {''}
                else:
                    candidates = self.collect_strings_in_limit(one_alt.get_arg(),limit_length2,limit_depth2)
                    candidates.add('')
                    return candidates 
                
            elif isinstance(one_alt, Star):
                if limit_length2 == 0:
                    return {''}
                else:
                    candidates = self.collect_strings_in_limit(one_alt.get_arg(),limit_length2,limit_depth2)
                    ans = {''}
                    for one_candit in candidates:
                        if one_candit != '':
                            strings = clean_split(one_candit)
                            repetable_times = limit_length2 % len(strings)
                            ans |= duplicate_strings(strings,repetable_times,1)
                    return ans  
                
            elif isinstance(one_alt, Plus):
                candidates = self.collect_strings_in_limit(one_alt.get_arg(),limit_length2,limit_depth2)
                ans = set()
                for one_candit in candidates:
                    if one_candit == '':
                        ans.add('')
                    else:
                        strings = clean_split(one_candit)
                        repetable_times = limit_length2 % len(strings)
                        ans |= duplicate_strings(strings,repetable_times,1)
                return ans   
                
            elif isinstance(one_alt, Repeat):
                start = one_alt.start
                stop = one_alt.stop
                candidates = self.collect_strings_in_limit(one_alt.get_arg(),limit_length2,limit_depth2)
                ans = set()
                if start == 0:
                    ans.add('')
                    start = 1
                for one_candit in candidates:
                    if one_candit == '':
                        ans.add('')
                    else:
                        strings = clean_split(one_candit)
                        repetable_times = limit_length2 % len(strings)
                        if repetable_times >= start:
                            max_repeat = min(repetable_times,stop)
                            ans |= set(duplicate_strings(strings,max_repeat,start))
                return ans
            
            elif isinstance(one_alt, Group):
                alternatives = one_alt.get_arg()
                ans = set()
                for one_elem in alternatives:
                    ans |= self.collect_strings_in_limit(one_elem,limit_length2,limit_depth2)
                return ans
            
            elif one_alt.is_end_point():
                if limit_length2 == 0:
                    return set()
                else:
                    return {one_alt.to_string()} #generate()
            
            else:
                print(one_alt)
                print("Maybe not intending call collect_strings_in_limit in Sometype")
                return None

    def collect_example(self,start_key,default_limit_length,default_limit_depth):
        start_alternatives = self.for_generate_grammar[start_key]
        result = set()

        for one_alt in start_alternatives:
            strings = self.collect_strings_in_limit(one_alt,default_limit_length,default_limit_depth)
            for string in strings:
                result.add(string)

        return result
