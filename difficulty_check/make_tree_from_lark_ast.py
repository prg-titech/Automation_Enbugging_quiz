from anytree import Node, RenderTree, LevelOrderIter, PostOrderIter
import tree_change_lib
from lark import Tree

def get_children_label(tree):
    labels = ''
    for one_child in tree.children:
        if one_child == None:
            labels += 'None '
        elif type(one_child) != Tree:
            labels += one_child.type + ' '
        else:
            labels += one_child.data.value + ' '
    return labels

def make_tree(tree,default_node):
    all_labels = {'Root'}
    def sub_make(subtree,default_node,id):
        now_id = id
        node_value = get_children_label(subtree)
        this_node = Node(node_value,parent=default_node,id_num = now_id,label = subtree.data.value,is_Tree = True)
        all_labels.add(subtree.data.value)
        now_id += 1
        for one_child in subtree.children:
            if one_child !=None:
                if type(one_child) != Tree:
                    Node(one_child.value,parent=this_node,pos = one_child.start_pos,id_num = now_id,label = one_child.type,is_Tree = False)
                    all_labels.add(one_child.type)
                    now_id += 1
                else:
                    now_id = sub_make(one_child,this_node,now_id) 
        return now_id
    
    last_id = sub_make(tree,default_node,0)
    return last_id,all_labels

def common(node1,node2,matching):
    # shold implementing by dp
    in_1 = []
    in_2 = []
    for pre, fill, node in RenderTree(node1):
        if node.is_leaf:
            in_1.append(node)

    for pre, fill, node in RenderTree(node2):
        if node.is_leaf:
            in_2.append(node)
    
    if in_1 == [] and in_2 == []:
        print("### Maybe impossible case (this nodes don't have leaf) ###")
        return 1
    else:
        count = 0
        for (n1,n2) in matching:
            if (n1 in in_1) and (n2 in in_2):
                count += 1

        return  count / max(len(in_1),len(in_2))


def compare_child_leaf(node1,node2,matching):
    return common(node1,node2,matching) > 0.5

def leaf_compare(node1,node2):
    return node1.label == node2.label

def make_tree_from_lark(before_code:str,after_code:str,parser_for_changeplace):
    lark_ast1 = parser_for_changeplace.parse(before_code)
    lark_ast2 = parser_for_changeplace.parse(after_code)

    #print(tree.pretty())

    default_node1 = Node("Root",parent=None,id_num = -1,display = "Root",is_rule = True,label = 'Root')
    default_node2 = Node("Root",parent=None,id_num = -1,display = "Root",is_rule = True,label = 'Root')
    (end_id1,labels1) = make_tree(lark_ast1,default_node1)
    (end_id2,labels2) = make_tree(lark_ast2,default_node2)

    # for pre, fill, node in RenderTree(default_node1):
    #     print('%s%s' %(pre, node.name))

    # for pre, fill, node in RenderTree(default_node2):
    #     print('%s%s' %(pre, node.name))
    
    return (default_node1,default_node2,labels1,labels2,compare_child_leaf,leaf_compare)