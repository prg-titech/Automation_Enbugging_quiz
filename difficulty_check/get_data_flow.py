from parser_for_data_flow import get_dependency_from_lark
from lark import Lark
import networkx as nx


def trace_dependency(dep_graph,changing_keys,error_keys):
    shortest = 10000000000
    way = []
    for one_error_key in error_keys:
        can_reach_error_dict = nx.single_target_shortest_path(dep_graph,one_error_key)
        for key,val in can_reach_error_dict.items():
            if key in changing_keys:
                now_short = len(val)
                if shortest > now_short:
                    shortest = now_short
                    way = val
    if shortest == 10000000000:
        print("Cannot found dependency")
        return -1,[]
    else:
        return shortest-1, way


def make_depenency_graph(dependency_dict:dict):
    dep_graph = nx.DiGraph()
    dep_graph.add_nodes_from(dependency_dict.keys())
    for one_key,values in dependency_dict.items():
        for one_val in values:
            dep_graph.add_edge(one_val,one_key)
    return dep_graph
    


def get_dataflow(code,lark_parser,change_place,error_place):
    dependency_dict = get_dependency_from_lark(code,lark_parser)

    change_start,change_end = change_place
    error_start,error_end = error_place

    changing_keys = set()
    error_keys = []
    for k in dependency_dict:
        if k[2] >= change_start and k[2] < change_end:
            changing_keys.add(k)
        if k[2] >= error_start and k[2] < error_end:
            error_keys.append(k)

    if error_keys == []:
        print('Cannot find error key')
        return -1,[]
    else:
        dep_graph = make_depenency_graph(dependency_dict)
        top_keys = []
        i = 0
        return trace_dependency(dep_graph,changing_keys,error_keys)