import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_folder)
from ControlFlowGraphGenerator import ControlGraphGenerator

if __name__=="__main__":
    import json
    trace_file='trace.txt'
    data = [
    {"name": "John", "age": 25, "gender": "Male"},
    {"name": "Jane", "age": 23, "gender": "Female"},
    {"name": "Bob", "age": 27, "gender": "Male"},
]
    trace_file="trace.txt"
    cfg=ControlGraphGenerator(trace_file=trace_file)
    # assertion_stmt='assertion i<4'
    # print(cfg.get_assertion_info(assertion_statement='assertion x > 3',fileName='file2.c',line_number=9))
    # print(cfg.assertion_trace_total['assertion x > 3'])
    # fileName='test_2.c'
    # trace_name='trace_4'
    # line_number=23
    # print(cfg.state_info['trace_4'])
    # print(cfg.state_info[trace_name])
    # print(cfg.state_info[trace_name][fileName])
    # statement='value=1'
    # print(cfg.extract_assignment_variable(statement))
    # for key,value in cfg.state_info['trace_4'].items():
    #     temp={}
    #     temp[key]=value
    #     print(cfg.add_iteration_info(temp['test_2.c']))