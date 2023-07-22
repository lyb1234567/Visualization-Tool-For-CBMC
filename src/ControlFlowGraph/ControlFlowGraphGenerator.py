import json
import os
import glob
from enum import Enum
import re
class Assertion_Type(Enum):
    FUNCTION_CALL = 1
    VARIABLE = 2
    ARRAY = 3
class Source_Type(Enum):
    FAILURE_SOURCE=1
    TRACE_SOURCE=2
class ControlGraphGenerator():
    def __init__(self,trace_json_file=None,trace_file=None,assertion_variables=None):
        self.trace_json_file=trace_json_file
        self.trace_file=trace_file
        self.json_data=None
        self.trace_data=None
        self.reduce_trace=[]
        self.state_info={}
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
            trace_name="trace_"+str(i+1)
            cur_state_info={}
            fileName='trace_{}.txt'.format(i+1)
            with open(fileName,'w') as f:
                f.write(traces[i])
            assertion_trace=self.get_assertion_trace(fileName)[0]
            cur_state_info[trace_name]=self.get_assertion_trace(fileName)[1]
            self.state_info.update(cur_state_info)
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
            line_lst=[]
            try:
                while True:
                    line=next(file)
                    if self.is_assignment(line):
                        traces.append(line)
                    if self.is_state(line):
                       line_lst.append(self.extract_line_number(line))
                    if 'Violated property:' in line:
                        line_number=next(file)
                        line_lst.append(self.extract_line_number(line_number))
                        assertion_line = next(file)
                        assertion = assertion_line.strip()
                        traces.append(assertion)
                        next(file)
            except StopIteration:
                pass
            temp_dict=self.build_state_info(traces,line_lst)
            assertion_trace[traces[-1]]=[]
            for i in range(len(traces)):
                assertion_trace[traces[-1]].append(traces[i])
            return [assertion_trace,temp_dict]
    def build_state_info(self,traces, line_nums):
        temp_dict={}
        if not temp_dict:
            for line, line_num in zip(traces, line_nums):
                if line_num in temp_dict:
                    temp_dict[line_num].append(line)
                else:
                    temp_dict[line_num] = [line]
            return temp_dict
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
    def is_assignment(self,statement):
        return ("=" in statement) and (not ">=" in statement) and (not "==" in statement) and (not "<=" in statement)
    def is_state(self,statement):
        return "State" in statement
    def extract_line_number(self,statement):
        pattern = r'line (\d+)'
        match = re.search(pattern, statement)
        if match:
            return int(match.group(1))
        else:
            return None
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


            
                    
                        
                
    
    

    