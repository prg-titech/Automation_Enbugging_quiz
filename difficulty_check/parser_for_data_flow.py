from lark import Lark,Token,Tree
from lark.visitors import Interpreter
from collections import defaultdict

class dataflow_compiler(Interpreter):
    def __init__(self,scope):
        self.scope = scope
        self.dependency_dict = defaultdict(list)

    def compilationunit(self, tree):
        return self.visit(tree.children[-1])
    
    def topstatus(self, tree):
        labels = []
        for one_labels in self.visit_children(tree):
            if type(labels) == list: 
                labels += one_labels
        return labels
    
    def topstat(self, tree):
        return self.visit(tree.children[-1])
    
    def oridef(self, tree):
        return self.visit(tree.children[-1])
    
    def clasdef(self,tree):
        cls_name = str(tree.children[0])
        labels = []
        bef_scope = self.scope
        self.scope += ('$$$' +cls_name)
        for one_child in tree.children[1:]:
            if type(one_child) == Tree:
                labels += self.visit(one_child)
        self.scope = bef_scope
        key_tuple = (cls_name,self.scope,tree.children[0].start_pos,tree.children[0])
        self.dependency_dict[key_tuple]=labels
        return [key_tuple]
    
    def clasconstr(self,tree):
        labels = []
        for one_child in tree.children:
            if type(one_child) == Tree:
                labels += self.visit(one_child)
        return labels

    def clstypeparamclause(self,tree):
        labels = []
        for one_child in tree.children:
            if type(one_child) == Tree:
                labels += self.visit(one_child)
        return labels
    
    def clstypeparam(self,tree):
        righthand_labels = self.visit(tree.children[1])
        key_tuple = (str(tree.children[0]),self.scope,tree.children[0].start_pos,tree.children[0])
        self.dependency_dict[key_tuple] = righthand_labels
        return [key_tuple]

    def clsparamclauses(self,tree):
        labels = []
        for one_child in tree.children:
            if type(one_child) == Tree:
                labels += self.visit(one_child)
        return labels
    
    def clsparamclause(self,tree):
        return self.visit(tree.children[-1])

    def clsparams(self,tree):
        labels = []
        for one_child in tree.children:
            if type(one_child) == Tree:
                labels += self.visit(one_child)
        return labels

    def clsparam(self,tree):
        return self.visit(tree.children[-1])
    
    def patdef(self, tree):
        varvallabels = self.visit(tree.children[0])
        is_typed = False
        is_expr = False
        if tree.children[1] != None:
            typelabels = self.visit(tree.children[1])
            if len(typelabels) == len(varvallabels):
                is_typed = True
        if tree.children[2] != None:
            exprlabels = self.visit(tree.children[2])
            if len(exprlabels) == len(varvallabels):
                is_expr = True
        i = 0
        r_list = []
        for one_varval in varvallabels:
            one_label = []
            if is_typed:
                if not is_expr:
                    one_label += [typelabels[i]]
                else:
                    self.dependency_dict[exprlabels[i]] += typelabels[i]
                    one_label += [exprlabels[i]]
            elif is_expr:
                one_label += [exprlabels[i]]
            # print(one_varval)
            # key_tuple = (one_varval,self.scope,one_varval.start_pos,one_varval)
            self.dependency_dict[one_varval] = one_label
            r_list.append(one_varval)
            i+=1
        return r_list
        

    def ids(self,tree):
        labels = []
        for one_child in tree.children:
                labels.append((str(one_child),self.scope,one_child.start_pos,one_child))
        return labels

    def defdef(self, tree):
        func_name = str(tree.children[0])
        labels = []
        bef_scope = self.scope
        self.scope += '$$$'+func_name
        if tree.children[1] != None:
            #labels += self.visit(tree.children[1])
            self.visit(tree.children[1])
        
        return_type_label = []
        if tree.children[2] != None:
            return_type_label = self.visit(tree.children[2])
            #labels += return_type_label

        if tree.children[3] != None:
            return_expr_label = self.visit(tree.children[3])
            for one_e in return_expr_label:
                self.dependency_dict[one_e] += return_type_label
            labels += return_expr_label
        else:
            labels += return_type_label

        self.scope = bef_scope
        key_tuple = (func_name,self.scope,tree.children[0].start_pos,tree.children[0])
        self.dependency_dict[key_tuple]=labels
        return [key_tuple]
    
    def expr(self,tree):
        return self.visit(tree.children[0])
    
    def expr1(self,tree):
        if len(tree.children) == 1:
            return self.visit(tree.children[0])
        else:
            left_hand_label = self.visit(tree.children[0])
            if tree.children[1] != None:  
                right_hand_label = self.visit(tree.children[1])
                for one_left in left_hand_label:
                    self.dependency_dict[one_left] += right_hand_label
            return left_hand_label
    
    def ifexpr(self,tree):
        labels = []
        for one_child in tree.children:
            if type(one_child) == Tree:
                labels += self.visit(one_child)
        return labels

    def whileexpr(self,tree):
        labels = []
        for one_child in tree.children:
            if type(one_child) == Tree:
                labels += self.visit(one_child)
        return labels

    def assignexpr(self,tree):
        var_name = str(tree.children[0])
        bef_scope = self.scope
        self.scope += ('$$$'+var_name)
        right_labels = self.visit(tree.children[1])
        self.scope = bef_scope
        key_tuple = (var_name,self.scope,tree.children[0].start_pos,tree.children[0])
        self.dependency_dict[key_tuple] = right_labels
        return [key_tuple]
    
    def ascription(self,tree):
        return self.visit(tree.children[0])
    
    def postfixexpr(self,tree):
        labels = []
        for one_child in tree.children:
            if type(one_child) == Tree:
                labels += self.visit(one_child)
            else:
                if one_child != None:
                    key_tuple = (str(one_child),self.scope,one_child.start_pos,one_child)
                    self.dependency_dict[key_tuple] = []
                    labels.append(key_tuple)
        return labels
    
    def infixexpr(self,tree):
        if len(tree.children) == 1:
                return self.visit(tree.children[0])
        if len(tree.children) == 2:
            left_hand_label = self.visit(tree.children[0])
            right_hand_label = self.visit(tree.children[-1])
            for one_right in right_hand_label:
                self.dependency_dict[one_right] += left_hand_label
            return right_hand_label
        else:
            left_hand_label = self.visit(tree.children[0])
            right_hand_label = self.visit(tree.children[-1])
            now_keys = self.dependency_dict.keys()
            id_name = str(tree.children[1])
            ok_list = list(filter(lambda x:x[0] == id_name and x[1] in self.scope,now_keys))
            if ok_list != []:
                key_tuple  = ('use:'+id_name,self.scope,tree.children[1].start_pos,tree.children[1])
                ok_list.sort(key=lambda x:x[2])
                ok_list.sort(key=lambda x:len(x[1]))
                self.dependency_dict[key_tuple]+=[ok_list[-1]]
            else:
                key_tuple = (id_name,self.scope,tree.children[1].start_pos,tree.children[1])
                # if id_name[-1] == ':':
            
            self.dependency_dict[key_tuple] += left_hand_label
            self.dependency_dict[key_tuple] += right_hand_label
            for one_left in left_hand_label:
                self.dependency_dict[one_left] += [key_tuple]
            for one_right in right_hand_label:
                self.dependency_dict[one_right] += [key_tuple]
            return [key_tuple]
    
    def simpleexpr(self,tree):
        if len(tree.children) == 0:
            return []
        elif len(tree.children) == 1:
            if type(tree.children[0]) == Tree:
                return self.visit(tree.children[0])
            else: 
                key_tuple = (str(tree.children[0]),self.scope,tree.children[0].start_pos,tree.children[0])
                self.dependency_dict[key_tuple] = []
                return [key_tuple]
        else:
            func_class_label =  self.visit(tree.children[0])
            arg_type_label = self.visit(tree.children[1])
            for one_l in func_class_label:
                self.dependency_dict[one_l] += arg_type_label
            return func_class_label
            
    def blockexpr(self,tree):
        labels = []
        for one_child in tree.children:
            if type(one_child) == Tree:
                labels += self.visit(one_child)
        return labels
    
    def block(self,tree):
        resultlabel = []
        for one_child in tree.children[:-1]:
            if type(one_child) == Tree:
                self.visit(one_child)
        if tree.children[-1] != None:
            resultlabel = self.visit(tree.children[-1])
        return resultlabel
    
    def blockstat(self,tree):
        return self.visit(tree.children[-1])
    
    def blockresult(self,tree):
        return self.visit(tree.children[0])
            
    def argumentexprs(self,tree):
        return self.visit(tree.children[0])

    def parargumentexprs(self,tree):
        labels = []
        for one_child in tree.children:
            if one_child != None:
                labels += self.visit(one_child)
        return labels
    
    def expresinparens(self,tree):
        labels = []
        for one_child in tree.children:
            if one_child != None:
                labels += self.visit(one_child)
        return labels

    def exprinparens(self,tree):
        if len(tree.children) == 1:
            return self.visit(tree.children[0])
        else:
            left_hand_label = self.visit(tree.children[0])
            right_hand_label = self.visit(tree.children[1])
            for one_left in left_hand_label:
                self.dependency_dict[one_left] += right_hand_label
            return left_hand_label
    
    def matchclause(self,tree):
        return self.visit(tree.children[0])
    
    def caseclauses(self,tree):
        labels = []
        for one_child in tree.children:
            labels += self.visit(one_child)
        return labels
    
    def caseclause(self,tree):
        self.visit(tree.children[0])
        return self.visit(tree.children[-1])
    
    def patern(self,tree):
        labels = []
        for one_child in tree.children:
            labels += self.visit(one_child)
        return labels

    def patern1(self,tree):
        return self.visit(tree.children[0])
    
    def patern2(self,tree):
        return self.visit(tree.children[0])
    
    def infixpatern(self,tree):
        labels = []
        infixs = []
        flatlabels = []
        for one_child in tree.children:
            if one_child != None:
                if type(one_child) == Tree:
                    ans_labels = self.visit(one_child)
                    labels.append(ans_labels)
                    flatlabels+= ans_labels
                elif one_child.type == 'ID':
                    now_keys = self.dependency_dict.keys()
                    ok_list = list(filter(lambda x:x[0] == str(one_child) and x[1] in self.scope,now_keys))
                    if ok_list != []:
                        key_tuple  = ('use:'+str(one_child),self.scope,one_child.start_pos,one_child)
                        ok_list.sort(key=lambda x:x[2])
                        ok_list.sort(key=lambda x:len(x[1]))
                        self.dependency_dict[key_tuple] = [ok_list[-1]]
                        infixs.append(key_tuple) 
                    else:
                        key_tuple = (str(one_child),self.scope,one_child.start_pos,one_child)
                        self.dependency_dict[key_tuple] = []
                        infixs.append(key_tuple)
                    
        i = 0
        for infix in infixs:
            if i < len(infixs)-1:
                self.dependency_dict[infix] += infixs[i+1]
                self.dependency_dict[infixs[i+1]] += infix

            for one_label in labels[i]:
                self.dependency_dict[one_label] += infix
            for one_label in labels[i+1]:
                self.dependency_dict[one_label] += infix
            i+=1
        return flatlabels

    def simplepatern(self,tree):
        if len(tree.children) == 1:
            if type(tree.children[0]) == Tree:
                return self.visit(tree.children[0])
            else:
                key_tuple  = (str(tree.children[0]),self.scope,tree.children[0].start_pos,tree.children[0])
                self.dependency_dict[key_tuple] = []
                return [key_tuple]
        else:
            cls_or_obj = self.visit(tree.children[0])
            if tree.children[1] != None:
                self.visit(tree.children[1])

            if tree.children[2] != None:
                patvars = self.visit(tree.children[2])
                for one_var in patvars:
                    self.dependency_dict[one_var] += cls_or_obj

            return cls_or_obj
        
    def simplelef(self,tree):
        now_keys = self.dependency_dict.keys()
        ok_list = list(filter(lambda x:x[0] == str(tree.children[0]) and x[1] in self.scope,now_keys))
        if ok_list != []:
            key_tuple  = ('use:'+str(tree.children[0]),self.scope,tree.children[0].start_pos,tree.children[0])
            ok_list.sort(key=lambda x:x[2])
            ok_list.sort(key=lambda x:len(x[1]))
            self.dependency_dict[key_tuple] = [ok_list[-1]]
            return [key_tuple]
        else:
            key_tuple = (str(tree.children[0]),self.scope,tree.children[0].start_pos,tree.children[0])
            self.dependency_dict[key_tuple] = []
            return [key_tuple]

    def simplepatern1(self,tree):
        return self.visit(tree.children[-1])
        
    def argumentpaterns(self,tree):
        labels = []
        for one_child in tree.children:
            if one_child != None:
                labels += self.visit(one_child)
        return labels
    
    def paterns(self,tree):
        labels = []
        for one_child in tree.children:
            if one_child != None:
                labels += self.visit(one_child)
        return labels

    def patvar(self,tree):
        if tree.children == []:
            return []
        else:
            key_tuple = (str(tree.children[0]),self.scope,tree.children[0].start_pos,tree.children[0])
            self.dependency_dict[key_tuple] = []
            return [key_tuple] 
    
    def prefixexpr(self,tree):
        righhandlabel = self.visit(tree.children[-1])
        if tree.children[0] != None:
            key_tuple = (str(tree.children[0]),self.scope,tree.children[0].start_pos,tree.children[0])
            self.dependency_dict[key_tuple] = righhandlabel
            return [key_tuple]
        else:
            return righhandlabel
        
    def defparamclauses(self,tree):
        labels = []
        for one_labels in self.visit_children(tree):    
            labels += one_labels
        return labels

    def defparamclause(self,tree):
        return self.visit(tree.children[0])

    def deftypeparamclause(self,tree):
        labels = []
        for one_child in tree.children[1:]:
            labels += self.visit(one_child)
        return labels
        
    def deftypeparam(self,tree):
        key_tuple = (str(tree.children[0]),self.scope,tree.children[0].start_pos,tree.children[0])
        labels = self.visit(tree.children[1])
        self.dependency_dict[key_tuple]=labels
        return [key_tuple]
    
    def deftermparamclause(self,tree):
        if tree.children[1] != None:
            return self.visit(tree.children[1])
        else:
            return []
    
    def deftermparams(self,tree):
        labels = []
        for one_labels in self.visit_children(tree):
            labels += one_labels
        return labels
    
    def deftermparam(self,tree):
        return self.visit(tree.children[0])
    
    def param(self,tree):
        key_tuple = (str(tree.children[0]),self.scope,tree.children[0].start_pos,tree.children[0])
        labels = []

        type_label = self.visit(tree.children[1])
        if tree.children[2] != None:
            return_expr_label = self.visit(tree.children[2])
            for one_e in return_expr_label:
                self.dependency_dict[one_e] += type_label
            labels += return_expr_label
        else:
            labels += type_label

        self.dependency_dict[key_tuple]=labels
        return [key_tuple]

    def paramtype(self,tree):
        return self.visit(tree.children[0])

    def tmpldef(self, tree):
        return self.visit(tree.children[-1])
    
    def objectdef(self, tree):
        key_tuple = (str(tree.children[0]),self.scope,tree.children[0].start_pos,tree.children[0])
        labels = []
        if tree.children[1] != None:
            bef_name = self.scope
            self.scope += ('$$$' + str(tree.children[0]))
            labels = self.visit(tree.children[1])
            self.scope = bef_name
        self.dependency_dict[key_tuple]= labels
        return [key_tuple]
        
    def template(self, tree):
        if tree.children[0] != None:
            return self.visit(tree.children[0])
        else:
            return []
        
    def templatebody(self,tree):
        labels = []
        for one_child in tree.children[1:]:
            if type(one_child) == Tree:
                one_labels = self.visit(one_child)
                labels += one_labels
        return labels
    
    def templatestat(self,tree):
        return self.visit(tree.children[-1])
    
    def typeparambounds(self,tree):
        if tree.children == []:
            return []
        else:
            labels = []
            for one_labels in self.visit_children(tree):
                labels += one_labels
            return labels
    
    def type(self,tree):
        return self.visit(tree.children[0])
        
    def funtype(self,tree):
        labels = []
        for one_labels in self.visit_children(tree):
            labels += one_labels
        return labels
    
    def funtypeargs(self,tree):
        if tree.children[0] != None:
            return self.visit(tree.children[0])
        else:
            return []
    
    def funargtypes(self,tree):
        labels = []
        for one_labels in self.visit_children(tree):
            labels += one_labels
        return labels

    def funargtype(self,tree):
        return self.visit(tree.children[0])

    def funparamclause(self,tree):
        labels = []
        for one_labels in self.visit_children(tree):
            labels += one_labels
        return labels

    def typedfunparam(self,tree):
        key_tuple = (str(tree.children[0]),self.scope,tree.children[0].start_pos,tree.children[0])
        labels = self.visit(tree.children[1])
        self.dependency_dict[key_tuple]=labels
        return [key_tuple]

    def infixtype(self,tree):
        return self.visit(tree.children[0])
  
    def refinedtype(self,tree):
        return self.visit(tree.children[0])

    def annottype(self,tree):
        return self.visit(tree.children[0])
    
    def simpletype(self,tree):
        if type(tree.children[0]) == Tree:
            labels = self.visit(tree.children[0])
            return labels
        else:
            #return [str(tree.children[0])]
            return [(str(tree.children[0]),self.scope,tree.children[0].start_pos,tree.children[0])]
    
    def simpletype1(self,tree):
        if len(tree.children) == 1:
            one_child = tree.children[0]
            if type(one_child) != Tree:
                now_keys = self.dependency_dict.keys()
                ok_list = list(filter(lambda x:x[0] == str(one_child) and x[1] in self.scope,now_keys))
                if ok_list != []:
                    key_tuple  = ('use:'+str(one_child),self.scope,one_child.start_pos,one_child)
                    ok_list.sort(key=lambda x:x[2])
                    ok_list.sort(key=lambda x:len(x[1]))
                    self.dependency_dict[key_tuple] = [ok_list[-1]]
                    return [key_tuple]
                else:
                    key_tuple = (str(one_child),self.scope,one_child.start_pos,one_child)
                    self.dependency_dict[key_tuple] = []
                    return [key_tuple]
            else:
                return self.visit(one_child)
        else:
            type_label = self.visit(tree.children[0])
            arg_label = self.visit(tree.children[1])
            for one_l in type_label:
                self.dependency_dict[one_l] += arg_label

            return type_label
    
    def typeargs(self,tree):
        return self.visit(tree.children[0])
    
    def types(self,tree):
        labels = []
        for one_labels in self.visit_children(tree):
            labels += one_labels
        return labels
    
    def __default__(self, tree):
        return []

    
def get_dependency_from_lark(code,lark_parser):

    tree = lark_parser.parse(code)
    #print(tree.pretty())
    comp = dataflow_compiler('')
    comp.visit(tree)
    # for k,v in dependency_dict.items():
    #     print(k)
    # #     print(v)
    return comp.dependency_dict
