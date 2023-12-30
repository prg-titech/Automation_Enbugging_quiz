import copy
from anytree import Node, RenderTree, LevelOrderIter, PostOrderIter
from functools import partial
import re

for_comment = re.compile(r'\/\/(.|\s)*$')

def lcs_for_match(list1:list,list2:list,equal_func):
    dp = [[0] * (len(list2)+1) for i in range(len(list1)+1)]

    for i, vi in enumerate(list1):
        for j, vj in enumerate(list2):
            if equal_func(vi,vj):
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i+1][j], dp[i][j+1])
    #print(dp[len(list1)][len(list2)])

    ans = []
    rest_1 = []
    rest_2 = [] 
    i = len(list1) - 1
    j = len(list2) - 1
    while i >= 0 and j >= 0:
        if equal_func(list1[i],list2[j]):
            ans.append((list1[i],list2[j]))
            i -= 1
            j -= 1
        elif dp[i+1][j+1] == dp[i][j+1]:
            i -= 1
            rest_1.append(list1[i+1])
        elif dp[i+1][j+1] == dp[i+1][j]:
            j -= 1
            rest_2.append(list2[j+1])
    ans.reverse()
    return (ans,rest_1,rest_2)

def sub_fastmatch(nodes1,nodes2,equal_func,matchs):
    (match_leaf,rest_1,rest_2) = lcs_for_match(nodes1,nodes2,equal_func)

    matchs.extend(match_leaf)

    not_match_1 = []
    not_match_2 = copy.deepcopy(rest_2)
    for one_node_1 in rest_1:
        i = 0
        while i < len(not_match_2):
            one_node_2 = not_match_2[i]
            if equal_func(one_node_1,one_node_2):
                matchs.append((one_node_1,one_node_2))
                not_match_2.pop(i)
                i = -1
                break
            i +=1

        if not (i == -1):
            not_match_1.append(one_node_1)

    return (matchs,not_match_1,not_match_2)


def fast_match(tree1:Node,tree2:Node,labels1:list,labels2:list,equal_func,leaf_equal_func):
    matchs = [(tree1,tree2)]
    leafs1 = []
    leafs2 = []
    labeling_nodes1 = [[] for i in range(len(labels1))]
    labeling_nodes2 = [[] for i in range(len(labels2))]
    
    # make chain (both leaf and internal node)

    for pre, fill, node in RenderTree(tree1):
        if node.is_leaf:
            leafs1.append(node)
        else:
            labeling_nodes1[labels1.index(node.label)].append(node)

    for pre, fill, node in RenderTree(tree2):
        if node.is_leaf:
            leafs2.append(node)
        else:
            labeling_nodes2[labels2.index(node.label)].append(node)

    # start leaf matching
    (matchs,not_match_leaf1,not_match_leaf_2)  = sub_fastmatch(leafs1,leafs2,leaf_equal_func,matchs)
    # print(not_match_leaf1)
    # print(not_match_leaf_2)

    # end leaf matching

    # start internal node matching 
    for each_label in labels1:
        if each_label in labels2:
            (matchs,not_match_1,not_match_2)  = sub_fastmatch(labeling_nodes1[labels1.index(each_label)],
                                                              labeling_nodes2[labels2.index(each_label)],
                                                              partial(equal_func,matching = matchs),matchs)
        # else:
        #     not_match_1 = labeling_nodes1[labels1.index(each_label)]
    
    # print(not_match_1)
    return matchs

def search_match_in_tree1(t2:Node,matching:list):
    for (n1,n2) in matching:
        if n2 == t2:
            return n1
    return None

def search_match_in_tree2(t1:Node,matching:list):
    for (n1,n2) in matching:
        if n1 == t1:
            return n2
    return None

def in_matching(node1:Node,node2:Node,matching:list):
    for (n1,n2) in matching:
        if n1 == node1:
            return (n2 == node2)
    return False

def findPos(x:Node,matching:list):
    y = x.parent
    if y == None:
        x_and_sibling = [x]
    else:
        x_and_sibling = list(y.children)
    pos_x = x_and_sibling.index(x)
    if pos_x == 0:
        x_and_sibling[0].in_order = True
        return 1
    else:
        i = pos_x
        while 0 <= i:
            now_node = x_and_sibling[i]
            if now_node.in_order:
                v = now_node
                break
            i -= 1
        for (n1,n2) in matching:
            if n2 == v:
                u = n1
                break
        u_sibling = u.parent.children
        number_of_u = 1
        for child in u_sibling:
            if child == u:
                return number_of_u+1
            number_of_u += 1
        print("### Maybe impossible case ('u' isn't in u sibling) ###")
        return number_of_u+1


def alignChildren(node1:Node,node2:Node,matching,e):
    children_1 = list(node1.children)
    children_2 = list(node2.children)
    for child in children_1:
        child.in_order = False
    for child in children_2:
        child.in_order = False

    (s,rest1,rest2) = lcs_for_match(children_1,children_2,partial(in_matching,matching = matching))
    for (n1,n2) in s:
        n1.in_order = True
        n2.in_order = True

    for child_1 in children_1:
        pair_of_c1 = search_match_in_tree2(child_1,matching)
        if (pair_of_c1 != None) and (pair_of_c1 in children_2) and (not ((child_1,pair_of_c1) in s)):
                k = findPos(pair_of_c1,matching)
                e.append(("MOV",child_1,node1,k,child_1.parent,child_1.parent.children.index(child_1)+1))
                mov(child_1,node1,k)
                child_1.in_order = True
                pair_of_c1.in_order = True
    return e


def mov(x:Node,y:Node,k:int):
    x.parent = None
    y_chi = list(y.children)
    y_chi.insert(k-1,x)
    y.children = tuple(y_chi)
    return

def ins(x:Node,y:Node,k:int):
    y_chi = list(y.children)
    y_chi.insert(k-1,x)
    y.children = tuple(y_chi)
    return

def upd(x:Node,value):
    x.name = value

def tree_del(x:Node):
    x.parent = None

def edit_script(tree1:Node,tree2:Node,matching:list):
    e = []
    m_dash = matching
    for node2 in LevelOrderIter(tree2):
        w = search_match_in_tree1(node2,m_dash)
        y = node2.parent
        z = search_match_in_tree1(y,m_dash)
        # case not found match
        if w == None:
            k = findPos(node2,m_dash)
            w = Node(name=node2.name,parent=None,display = node2.label,label=node2.label)
            e.append(('INS',w,z,k))
            m_dash.append((w,node2))
            ins(w,z,k)
        elif not node2.is_root:
            v = w.parent
            if w.name != node2.name:
                e.append(('UPD',w,w.name,node2.name,v,v.children.index(w)+1))
                upd(w,node2.name)
            if not ((v,y) in m_dash):
                k = findPos(node2,m_dash)
                e.append(('MOV',w,z,k,v,v.children.index(w)+1))
                mov(w,z,k)

        e = alignChildren(w,node2,m_dash,e)

    for node1 in PostOrderIter(tree1):
        if search_match_in_tree2(node1,m_dash) == None:
            e.append(('DEL',node1,node1.parent,node1.parent.children.index(node1)+1))
            tree_del(node1)
    return (e,m_dash)

def arrangement_changes_forprint(e_script:list):
    ans = [[],[],[],[]]
    sub1 = [[]]
    sub2 = [[]]
    for one_edit in e_script:
        e = one_edit[0]
        if e == 'MOV':
            mov_not_is_sub = True
            for list_sub in sub1:
                if one_edit[2] in list_sub:
                    pos = sub1.index(list_sub) 
                    sub1[pos].append(one_edit[1])
                    sub2[pos].append(("MOV",one_edit[1].name,one_edit[2].name))
                    mov_not_is_sub = False
                    break
            if mov_not_is_sub:
                ans[0].append((one_edit[1].name,one_edit[2].name))
        elif e == 'INS':
            ins_not_is_sub = True
            for list_sub in sub1:
                if one_edit[2] in list_sub:
                    pos = sub1.index(list_sub)
                    sub1[pos].append(one_edit[1])
                    sub2[pos].append(("INS",one_edit[1].name,one_edit[2].name))
                    ins_not_is_sub = False
                    break
            if ins_not_is_sub:
                ans[1].append((one_edit[1].name,one_edit[2].name))
                sub1.append([one_edit[1]])
                sub2.append([("INS",one_edit[1].name,one_edit[2].name)])
        elif e == 'UPD':
            # ans[2].append((one_edit[2],one_edit[3]))
            upd_not_is_sub = True
            for list_sub in sub1:
                if one_edit[1].parent in list_sub:
                    pos = sub1.index(list_sub)
                    sub1[pos].append(one_edit[1])
                    sub2[pos].append(("UPD",one_edit[2],one_edit[3]))
                    upd_not_is_sub = False
                    break
            if upd_not_is_sub:
                ans[2].append((one_edit[2],one_edit[3],one_edit[1].parent.name))
                sub1.append([one_edit[1]])
                sub2.append([("UPD",one_edit[2],one_edit[3])])
        elif e == 'DEL':
            ans[3].append(one_edit[1].name)
    return (ans,sub1,sub2)

def count_e_script(e_script:list):
    count = [0,0,0,0]
    for one_edit in e_script:
        e = one_edit[0]
        if e == 'MOV':
            count[0] += 1
        elif e == 'INS':
            count[1] += 1
        elif e == 'UPD':
            count[2] += 1
        elif e == 'DEL':
            count[3] += 1
    return count

def clean_e_script(e_script:list):
    ans = []
    for one_edit in e_script:
        e = one_edit[0]
        if e == 'MOV':
            ans.append((one_edit[0],one_edit[1].name,one_edit[2].name))
        elif e == 'INS':
            ans.append((one_edit[0],one_edit[1].name,one_edit[2].name))
        elif e == 'UPD':
            ans.append((one_edit[0],one_edit[2],one_edit[3]))
        elif e == 'DEL':
            ans.append((one_edit[0],one_edit[1].name))
    return ans

def get_edit_script(before_root,after_root,lables1,labels2,equal_func,leaf_equal_func):
    # for pre, fill, node in RenderTree(e_root):
    #     print('%s%s' %(pre, node.name))

    # for pre, fill, node in RenderTree(n_root):
    #     print('%s%s' %(pre, node.name))

    first_matching = fast_match(before_root,after_root,list(lables1),list(labels2),equal_func,leaf_equal_func)

    (e_script,final_matching) = edit_script(before_root,after_root,first_matching)
    return e_script