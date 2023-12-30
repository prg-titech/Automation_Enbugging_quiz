import re
import subprocess

for_del = re.compile(r'Error compiling project \(Scala (\.|\d)+\, JVM\)\n|Compilation failed\n|Compiling project \(Scala (\.|\d)+\, JVM\)\n|Compiled project \(Scala (\.|\d)+\, JVM\)\n')
for_judge_snippet = re.compile(r'^((\[error\]|\[warn\])(\^|\s)+)$')
for_color = re.compile(r'\x1b\[(\d)+m')
for_error_warn = re.compile(r'(\[error\])|(\[warn\])')
for_head_line = re.compile(r'^:(\d+):(\d+)')

def message_cleaner(error_msg:str,for_sub_basemsg,remove_snippet:bool,code:str):
    ret_msg = set()
    no_color = for_color.sub('',error_msg)
    no_info = for_del.sub('',no_color)
    temp1 = for_sub_basemsg.sub('#####Split_place_of_one_error#####\\2',no_info)
    basemsgs = temp1.split('#####Split_place_of_one_error#####')
    if(basemsgs[len(basemsgs)-1].find('Exception in thread "main"') >=0):
        splitted_tail = basemsgs[len(basemsgs)-1].split('Exception in thread "main"')
        basemsgs = basemsgs[:-1] + [splitted_tail[0],splitted_tail[1].splitlines()[0]]

    for one_e_m in basemsgs:
        if one_e_m == '':
            continue
        else:
            suggest_line = None
            m_obj = for_head_line.match(one_e_m)
            if m_obj:
                suggest_line = int(for_head_line.sub('\\1',m_obj.group()))
                one_e_m = for_head_line.sub('',one_e_m)

            temp_msg = one_e_m.splitlines()

            # remove error snippet
            if remove_snippet:
                if for_judge_snippet.match(temp_msg[-1]):
                    temp_msg = temp_msg[:-2]
            else:
                if not for_judge_snippet.match(temp_msg[-1]):
                    if suggest_line != None:
                        lines_of_code = code.splitlines()
                        if len(lines_of_code) >= suggest_line:
                            error_snippet = lines_of_code[suggest_line-1]
                            temp_msg.append(error_snippet)

            ret_msg.add(for_error_warn.sub('',"\n".join(temp_msg)))
    return ret_msg

def write_code(place,code):
    file = open(place,'w')
    file.write(code)
    file.close()
    return

def use_cli(code,place,remove_snippet:bool):
    write_code(place,code)
    try:
        proc = subprocess.run(['scala-cli', place], capture_output=True, text=True,timeout=8)
    except subprocess.TimeoutExpired:
        print("timeout\n")
        defoutput = "time out error for 8 second"
        return {defoutput}
    else:
        defoutput = proc.stderr

    for_sub_basemsg = re.compile('(\\[error\\]|\\[warn\\]) {}((.|\\d)+)\\n'.format(re.escape(place)))
    return message_cleaner(defoutput,for_sub_basemsg,remove_snippet,code)

# def use_scastie(code):
#     returned_messages = access_scastie.get_message_form_scastie(code)
#     return returned_messages