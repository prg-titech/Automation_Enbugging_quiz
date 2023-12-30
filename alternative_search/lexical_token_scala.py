from ast import keyword
import itertools
import string
import re

check_upper = re.compile(r'([A-Z]|$)')
check_lower = re.compile(r'([a-z]|_)')

def get_fresh_val(ids:set):
    for alph in string.ascii_lowercase:
        if not (alph in ids):
            return alph
        elif not (alph+ids[0]) in ids:
            return alph+ids[0]
    return string.ascii_lowercase

class scala3_lexical_tokens():
    whitespace       = {'\\u0020' ,'\\u0009' ,'\\u000D' ,'\\u000A'}
    paren            = {'(' ,')' ,'[' ,']' ,'{' ,'}'}
    delim            = {'`' ,'\'' ,'"' ,'.' ,';' ,','}
    opchar           = {'!' ,'#' ,'%' ,'&' ,'*' ,'+' ,'-' ,'/' ,':' ,'<' ,'=' ,'>' ,'?' ,'@' ,'\\' ,'^' ,'|' ,'~'}
    #opchar2 = set(map(lambda x: x[0]+x[1],set(itertools.product(opchar,opchar))))
    
    # Small operator
    op_collection = {'+','+=','+=:','++','++:','++=','++=:','+:',':+','-','-=','--','--=','&','|','&~','/:','/:\\',':\\'}
    op_relational = {'==','!=','>=','<='}
    op_logical = {'&&','||'}
    op_arithmetic = {'**','*=','/=','+=','-='}
    op = opchar|op_collection|op_relational|op_logical|op_arithmetic
    #
    escapeseq    = {'\\b' ,'\\t' ,'\\n' ,'\\f' ,'\\r','\\"','\\\'','\\\\','\\u0000'}
    integernumeral   =  {'1L','1l'}
    floatingpointliteral = {'1F','1f', '1D' ,'1d'}
    booleanliteral   = {'true' ,'false'}
    characterliteral = {"'a'"}
    stringliteral = {'"a"','"""a"""'}
    nl = {'\n'}
    semi = {';'}.union(nl)
    colon = {':'}
    simpleliteral = integernumeral|set(map(lambda x:'-'+x,integernumeral))|floatingpointliteral|set(map(lambda x:'-'+x,floatingpointliteral))|booleanliteral| characterliteral| stringliteral
    literal = simpleliteral|{'null'}
    escape = {'\$\$', '\$"', '\$'}
    prefixoperater =  {"-" , "+" , "~" ,"!" }

    localmodifier = {"abstract","final" ,"sealed", "open", "implicit", "lazy", "inline"}

    endmarkertag = {"if","while","for","match","try","new","this","given","extension","val"}

    Types = {'Boolean','Byte','Short','Int','Long','Float','Double','Char','String','Nothing','Null','Unit'}
    Collection_type = {'List','Vector','LazyList','ArrayBuffer','ListBuffer','Map','Set'}

    Chatnobackquotrornewline = {"`a`"}

    id = set()
    varid = set()
    alphaid=set()
    plainid = set()
    keyword = {'abstract','case','catch','class','def','do','else','enum','export','extends','false','final','finally','for','given','if','implicit','import','lazy','match','new','null','object','override','package','private','protected','return','sealed','super','then','throw','trait','true','try','type','val','var','while','with','yield'}
    wildcard_id = set()

    def __init__(self,get_ids,splited_strs:list):
        for one_id in get_ids:
            if check_upper.match(one_id):
                self.alphaid.add(one_id)
            elif check_lower.match(one_id):
                self.varid.add(one_id)
            else:
                self.op.add(one_id)
        self.alphaid = self.alphaid.union(self.varid)
        self.plainid = self.alphaid | self.op
        self.id = self.plainid | self.Chatnobackquotrornewline | self.simpleliteral | {get_fresh_val(self.plainid)} | self.Types | self.Collection_type

        for one_str in splited_strs:
            if not one_str in self.keyword:
                self.wildcard_id.add(one_str)

        self.all_tokens = self.wildcard_id|self.id|self.semi|self.colon|self.keyword|self.endmarkertag|self.localmodifier|self.prefixoperater|self.escape|{'null'}|self.escapeseq