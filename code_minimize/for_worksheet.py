import re

attach_head = '''object test{
    def main(args: Array[String]) = { }
'''
attach_tail = '''
}'''

indent = '    '

for_fourindent = re.compile(r'^\s\s\s\s')

def make_compilable_code(code:str):
    return attach_head+add_indent(code)+attach_tail

def add_indent(code:str):
    return '\n'.join(list(map(lambda x: indent+x,code.splitlines())))

def remove_indent(code_list:list[str]):
    return '\n'.join(list(map(lambda x: for_fourindent.sub('',x),code_list)))

def get_attached_place(code:str,original_palce):
    ori_start,ori_end = original_palce
    incriment = (code[:ori_start].count('\n')+1)*len(indent) + len(attach_head)
    return (ori_start+incriment,ori_end+incriment)
