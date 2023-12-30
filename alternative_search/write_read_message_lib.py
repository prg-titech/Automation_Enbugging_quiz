from glob import glob
import hashlib
import os
import re

save_place = './save_error_messages/'
partition = '\n////partition////\n'
token_partition = '\n////partitionoftoken////\n'

def get_hash_from_code(code:str):
    hash_object = hashlib.sha256(code.encode())
    return hash_object.hexdigest()

def exist_list(hash,editable_place):
    save_place_code = save_place+'/{}'.format(hash)
    isfolder = glob(save_place_code)
    if isfolder == []:
        os.mkdir(save_place_code)
    save_place_code_editable = save_place_code + '/place{}_{}.txt'.format(editable_place[0],editable_place[1])
    is_file = glob(save_place_code_editable)
    return is_file != []

def write_error_msgs_set(token_msgset,hash,editable_place):
    save_place_code_editable = save_place + '/{}/place{}_{}.txt'.format(hash,editable_place[0],editable_place[1])
    file = open(save_place_code_editable,'w')
    for token, msgset in token_msgset:
        file.write(token_partition)
        file.write(token)
        for one_msg in msgset:
            file.write(partition)
            file.write(one_msg)
    file.close()
    return

def read_error_msgs_set(hash,editable_place):
    save_place_code_editable = save_place + '/{}/place{}_{}.txt'.format(hash,editable_place[0],editable_place[1])
    is_file = glob(save_place_code_editable)
    if is_file == []:
        print('Please fuzzing first at editable place {}-{}'.format(editable_place[0],editable_place[1]))
        return []
    else:
        file = open(save_place_code_editable,'r')
        token_msgs = file.read()
        token_msgs.split(token_partition)
        token_msgs = token_msgs[1:]
        answer_list = []
        for one_token_msgs in token_msgs:
            token_msgs_list = one_token_msgs.split(partition)
            answer_list.append((token_msgs_list[0],set(token_msgs_list[1:])))
        return answer_list