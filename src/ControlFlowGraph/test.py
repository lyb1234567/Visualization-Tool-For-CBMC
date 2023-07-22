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
    cfg.load_trace_data()
    cfg.clean_tarce_file()
    print(cfg.state_info)
    print(cfg.assertion_trace_total)