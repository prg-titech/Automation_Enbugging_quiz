from difficulty_eval_lib import evaluating_quiz_difficulty
from sample_quizzes import quiz1,quiz2,quiz3,quiz4,quiz5,quiz6,quiz7,quiz8

def get_data_from_quiz(one_quiz):
    quiz_code,answer_change,answer_error_msg,editable_places,error_place = one_quiz

    difficulty_evaluator = evaluating_quiz_difficulty(quiz_code,answer_change,answer_error_msg,error_place)

    #print(difficulty_evaluator.about_assumed_answer.edit_script)
    print(difficulty_evaluator.about_assumed_answer.change_tree_struct)
    print(difficulty_evaluator.about_assumed_answer.dataflow_length)
    print(difficulty_evaluator.about_assumed_answer.dataflow_path)
    return



sample_quiz_list = [quiz1,quiz2,quiz3,quiz4,quiz5,quiz6,quiz7,quiz8]
for one_quiz in sample_quiz_list:
    get_data_from_quiz(one_quiz)