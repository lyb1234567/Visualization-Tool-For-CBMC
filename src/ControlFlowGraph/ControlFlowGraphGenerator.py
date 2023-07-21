import json
import os
import glob
from enum import Enum
import re
class Assertion_Type(Enum):
    FUNCTION_CALL = 1
    VARIABLE = 2
    ARRAY = 3
class ControlGraphGenerator():
    def __init__(self,trace_json_file=None,trace_file=None,assertion_variables=None):
        self.trace_json_file=trace_json_file
        self.trace_file=trace_file
        self.json_data=None
        self.trace_data=None
        self.reduce_trace=[]
        # assertion_trace的数据结构应该是{'assertion_statement':[trace1,trace2,trace3]}
        self.assertion_trace_total={}
        self.assertion_variables=assertion_variables
    def load_trace_data(self):
        if self.trace_file:
            with open(self.trace_file,'r') as f:
                self.trace_data=f.read()
            return self.trace_data
    def clean_tarce_file(self):
        text = self.trace_data.split('** Results:', 1)[-1]
        text = text.split('**', 1)[0]
        traces =re.split(r'Trace for [^\n]*\n', text)[1:]
        for i in range(len(traces)):
            fileName='trace_{}.txt'.format(i+1)
            with open(fileName,'w') as f:
                f.write(traces[i])
            assertion_trace=self.get_assertion_trace(fileName)
            self.assertion_trace_total.update(assertion_trace)
        self.remove_trace_files()
    def remove_trace_files(self):
        trace_files = glob.glob('trace_*.txt')
        # Delete all trace files
        for file in trace_files:
            try:
                os.remove(file)
            except Exception as e:
                pass
    def get_assertion_trace(self,fileName):
        with open(fileName, 'r') as file:
            traces=[]
            assertion_trace={}
            try:
                while True:
                    line=next(file)
                    if 'State' not in line and (not line.startswith('-') and (line !='\n')) and ('Violated property:' not in line):
                        traces.append(line)
                    if 'Violated property:' in line:
                        next(file)
                        assertion_line = next(file)
                        assertion = assertion_line.strip()
                        traces.append(assertion)
                        next(file)
            except StopIteration:
                pass
            assertion_trace[traces[-1]]=[]
            for i in range(len(traces)-1):
                assertion_trace[traces[-1]].append(traces[i])
            return assertion_trace
    def find_file_in_sourceLocation(self,data_dict):
        if isinstance(data_dict, dict):
            if "sourceLocation" in data_dict and isinstance(data_dict["sourceLocation"], dict) and "file" in data_dict["sourceLocation"]:
                return data_dict["sourceLocation"]["file"]
            for value in data_dict.values():
                result = self.find_file_in_sourceLocation(value)
                if result:
                    return result
        elif isinstance(data_dict, list):
            for item in data_dict:
                result = self.find_file_in_sourceLocation(item)
                if result:
                    return result
        return False
    # 清洗trace json file的结构，将不需要的key去掉
    def reduce_trace_json(self):
        if self.trace_json_file !=None:
            with open(self.trace_json_file,'r') as f:
                json_data=json.load(f)
            for json_obj in json_data:
                if json_obj.get('hidden')!=None:
                    if not json_obj['hidden']:
                        fileName=self.find_file_in_sourceLocation(json_obj)
                        if fileName!=False:
                            if os.path.exists(fileName) or fileName.startswith('<builtin'):
                                 self.reduce_trace.append(json_obj)
            with open(self.trace_json_file, 'w') as f:
                json.dump(self.reduce_trace, f)
            return self.reduce_trace


            
                    
                        
                
    
    

    