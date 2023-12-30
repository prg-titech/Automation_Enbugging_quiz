from DD import DD 
import subprocess
import difflib
import copy
import time
from compile_run_scala import use_cli

def get_error_msg(code:str,num):
    msg = use_cli(code,'./deltadebug_place/delta_debug{}.scala'.format(num),False)
    time.sleep(0.2)
    return msg

class MyDD(DD): 
    def __init__(self,default_input,defaultmsgs): 
        DD.__init__(self) 
        self.debug_count = 0
        self.default_input = default_input
        self.defaultmsgs = defaultmsgs

    def _test(self, deltas):

        #print(deltas)
        copy_default = copy.deepcopy(self.default_input)
        copy_default.extend(deltas)
        copy_default.sort()

        deletenext = False
        
        input = ''

        for (index,id,character) in copy_default:
            if(id == 1):
                if(deletenext):
                    deletenext = False
                    continue
                else:
                    input = input + character + '\n'
            elif(id == 2):
                input = input + character + '\n'
            elif(id == 0):
                deletenext = True
            else:
                print("error!!!")
        
        self.debug_count += 1
        outputs = get_error_msg(input,self.debug_count)
        print(outputs)

        if outputs == set():
            status = 0
        else:
            status = 1

        print("Exit code", status)

        # if status == 0:
        #     return self.PASS
        # elif self.defaultmsgs == outputs:
        #     return self.FAIL
        # return self.UNRESOLVED

        isallerorrfound = True

        for error in self.defaultmsgs:
            if not error in outputs:
                # print(error + '\nis NOT found in outputs')
                isallerorrfound = False
                break
            
        if status == 0:
            return self.PASS
        elif isallerorrfound:
            return self.FAIL
        return self.UNRESOLVED

def scala_error_minimize(not_error_code,error_code):
    defaultmsgs = get_error_msg(error_code,0)

    if defaultmsgs == set():
        status = 0
    else:
        status = 1

    print("### Default message is below ###")
    print(defaultmsgs)

    default_input = []
    deltas = [] 
    index = 1 

    # For character base debugging
    # (default_input,deltas) = small_formatter.get_deltas(not_error_code,error_code)

    # For line base dubugging
    diftext = difflib.ndiff(not_error_code.splitlines(), error_code.splitlines())

    for data in diftext:
        #print(data)
        if data[0:1] in ['+']:
            deltas.append((index, 2, data[2:]))
        elif data[0:1] in ['-']:
            deltas.append((index, 0, data[2:]))
            default_input.append((index, 1, data[2:]))
        elif data[0:1] in ['?']:
            continue
        else:
            default_input.append((index,1,data[2:]))
        index = index + 1
    
    mydd = MyDD(default_input,defaultmsgs)
    
    print("Simplifying failure-inducing input...")

    try:
        deltas = mydd.ddmin(deltas)
    except AssertionError as err:
        print('Happening assertion error when ddmin')
        return ('','','','')
    

    additionals = []
    deletes = []
    outcome_code = []
    deletenext = False

    outcome_deltas = default_input+deltas
    outcome_deltas.sort()

    for (index,id,character) in outcome_deltas:
        if(id == 1):
            if(deletenext):
                deletenext = False
                continue
            else:
                outcome_code.append((index,character))
        elif(id == 2):
            outcome_code.append((index,character))
            additionals.append((index,character))
        elif(id == 0):
            deletenext = True
            deletes.append((index,character))

        else:
            print("error!!!")

    outcome_code.sort()

    return ('\n'.join(list(map(lambda x: x[1], outcome_code))),defaultmsgs,deletes,additionals)
