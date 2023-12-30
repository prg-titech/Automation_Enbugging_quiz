import re
import subprocess
from os import path
from glob import glob
from do_delta_debugging import scala_error_minimize
from for_worksheet import make_compilable_code,remove_attach_something
from compile_run_scala import use_cli

blank_code = ''

def do_sample_minimize():
    sample_code_place = './error_sample_place/*.scala'
    write_place = './error_sample_small_place/{}'
    files = glob(sample_code_place)
    for one_file_place in files:
        file_name = path.basename(one_file_place)
        small_error_write_space = write_place.format(file_name)
        if glob(small_error_write_space) != []:
            print('{} is already exist.'.format(file_name))
            continue
        else:
            one_file = open(one_file_place)
            error_code = one_file.read()
            one_file.close()
            (minimized_code,defaultmsgs,deletes,additionals) = scala_error_minimize(make_compilable_code(blank_code), make_compilable_code(error_code))
            outcome_code = remove_attach_something(minimized_code)
            writing_file = open(small_error_write_space,'w')
            writing_file.write(outcome_code)
            writing_file.close()
            print('End minimize {}'.format(file_name))

do_sample_minimize()