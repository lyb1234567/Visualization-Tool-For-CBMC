import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_folder)
from ControlFlowGraphGenerator import ControlGraphGenerator

if __name__=="__main__":
    json_file='test.json'
    controlgraph=ControlGraphGenerator(json_file)
    print(controlgraph.CFG['CFG_file_source_1'])
    