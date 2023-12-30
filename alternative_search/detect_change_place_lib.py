from collections import defaultdict
from lark import Tree,Lark
from anytree import Node, RenderTree

def make_tree(tree,default_node):
    tokendict = defaultdict(set)
    pos_token_list = []
    def sub_make(subtree,default_node,id):
        now_id = id
        this_node = Node(subtree.data.value,parent=default_node,id_num = now_id,t_type = subtree.data.value,is_Tree = True)
        now_id += 1
        for one_child in subtree.children:
            if one_child !=None:
                if type(one_child) != Tree:
                    tokendict[one_child.type].add(one_child.value)
                    pos_token_list.append((one_child.start_pos,one_child.value))
                    Node(one_child.value,parent=this_node,pos = one_child.start_pos,id_num = now_id,t_type = one_child.type,is_Tree = False)
                    now_id += 1
                else:
                    now_id = sub_make(one_child,this_node,now_id) 
        return now_id
    
    sub_make(tree,default_node,0)
    return tokendict,pos_token_list

def make_tree_and_dict_from_lark(parser_for_changeplace,code):
    tree = parser_for_changeplace.parse(code)
    start_node = Node("root",parent=None,id_num = -1,t_type = 'temp_startpoint',is_Tree = True)
    tokendict,pos_token_list = make_tree(tree,start_node)

    # for pre, fill, node in RenderTree(start_node):
    #     print('%s%s' %(pre, node.name))

    return start_node,tokendict,pos_token_list

def get_change_place_token(default_node:Node,change_place:(int,int)):
    change_start,change_end = change_place

    before_change_place =default_node
    next_of_change_place = default_node
    change_string_node = None

    for pre, fill, node in RenderTree(default_node):
        if not node.is_Tree:
            if node.pos == change_start:
                change_string_node = node
            elif node.pos >= change_end:
                next_of_change_place = node
                break
            elif node.pos < change_start:
                before_change_place = node
 
    change_key = ()
    before_ancestors = before_change_place.ancestors
    after_ancestors = next_of_change_place.ancestors
    
    if change_string_node == None:
        print("###Not found Node which have same position with searching pos!###")
        return None
    else:
        for pre, fill, node in RenderTree(default_node):
            if (not (node in after_ancestors or node in before_ancestors)) and (node in change_string_node.ancestors or node == change_string_node):
                change_key = (node.t_type,node.name)
                break
            #print('%s%s' %(pre, node.name))
        if change_key == ():
            print("###NOT FOUND Change Key!###")
            return ('','')

        return change_key
