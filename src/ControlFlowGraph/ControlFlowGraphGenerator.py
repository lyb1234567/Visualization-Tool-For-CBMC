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
        if self.trace_file!=None:
            self.load_trace_data()
            self.clean_tarce_file()
    # 导入trace.ext文件
    def load_trace_data(self):
        if self.trace_file:
            with open(self.trace_file,'r') as f:
                self.trace_data=f.read()
            return self.trace_data
    # 获取所有trace 信息
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
            [assertion_trace,temp_state]=self.get_assertion_trace(fileName)
            cur_state_info[trace_name]=temp_state
            self.assertion_trace_total.update(assertion_trace)
            self.state_info.update(cur_state_info)
        self.remove_trace_files()
    # 遍历某个文件的对应行数的信息，如果对应的variable,并且是在同一行，那么就判定为循环中的varibale
    # 所以输入格式就是类似于：
    # {'test.c': [{12: '  num1=11'}, {13: '  num2=9'}, {14: '  array={ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }'}, {15: '  num=10'}, {16: '  num=9'}]}
    def update_iteration(self,trace):
        pass
    # 删除所有trace文件
    def remove_trace_files(self):
        trace_files = glob.glob('trace_*.txt')
        # Delete all trace files
        for file in trace_files:
            try:
                os.remove(file)
            except Exception as e:
                pass
    # 获取所需要的assertion statement,最终返回两个元素
    # 1.某个assertion statement以及对应的trace列表格式如下{'assertion_statemen'：[trace1,trace2,trace3,trace4,trace5]}
    # 每一个trace都有它对应的信息，一般来说是三个信息：1.file 2.line 3.binary format,如果是assertion statement的话，就只有 file 和line
    # 2. 每一个文件中，每行代码对应的statement。对应的格式如下： {'filename_1.c':['line_num1':'xxx','line_num2':'xxxx],'filename_2.c':['line_num1':'xxx']}
    def get_assertion_trace(self,fileName):
        with open(fileName, 'r') as file:
            traces=[]
            assertion_trace={}
            file_line={}
            try:
                while True:
                    line=next(file)
                    if self.is_state(line):
                       temp_assignment_info={}
                       line_number=self.extract_line_number(line)
                       file_name=self.extract_file(line)
                       next(file)
                    #   获取十进制的值以及二进制的值
                       [assignment,binary_format]=self.clean_assignment(next(file))
                       binary_format=binary_format.replace(")","")
                       variable_name=self.extract_assignment_variable(assignment.strip())
                       temp_assignment_info[assignment]={}
                       temp_assignment_info[assignment]['variable']=variable_name
                       temp_assignment_info[assignment]['file']=file_name
                       temp_assignment_info[assignment]['line']=line_number
                       temp_assignment_info[assignment]['binary_format']=binary_format
                       traces.append(temp_assignment_info)
                       temp_assignment_line={}
                       temp_assignment_line[line_number]=assignment
                       if file_line.get(file_name)==None:
                           file_line[file_name]=[]
                           file_line[file_name].append(temp_assignment_line)
                       else:
                           file_line[file_name].append(temp_assignment_line)
                    if 'Violated property:' in line:
                        file_line_info=next(file)
                        line_number=self.extract_line_number(file_line_info)
                        file_name=self.extract_file(file_line_info)
                        assertion_line = next(file)
                        assertion_line = assertion_line.strip()
                        temp_assignment_info={}
                        temp_assignment_info[assertion_line]={}
                        temp_assignment_info[assertion_line]['file']=file_name
                        temp_assignment_info[assertion_line]['line']=line_number
                        traces.append(temp_assignment_info)
                        next(file)
            except StopIteration:
                pass
            assertion_key=None
            for key in traces[-1].keys():
                assertion_key=key 
            assertion_trace[assertion_key]=[]
            for i in range(len(traces)):
                assertion_trace[assertion_key].append(traces[i])
            return [assertion_trace,file_line]
    # 从sourceLocation 获得 file name
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
    # 判断是否是state information
    def is_state(self,statement):
        return "State" in statement
    # 获取当前statement中的line number 
    def extract_line_number(self,statement):
        pattern = r'line (\d+)'
        match = re.search(pattern, statement)
        if match:
            return int(match.group(1))
        else:
            return None
    # 获取十进制的值 比如：i=2,i=2 (00000000 00000000 00000000 00000010)
    def clean_assignment(self,assignment):
        return assignment.split(' (')
    # 从当前statement中获取文件名
    def extract_file(self,state_str):
        match = re.search(r'file (\S+)', state_str)
        if match:
            return match.group(1)
        else:
            return None
    # 从特定的trace中，特定的文件特定的行数中获取state information
    # 因为可能会存在loop，所以用叠加的方式
    def get_state_info(self,fileName,trace_name,line_number):
        res=""
        for dic in self.state_info[trace_name][fileName]:
            if dic.get(line_number)!=None:
                res=res+dic[line_number]+'\n'
        return res
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
    # 获取赋值statement 值的名字
    def extract_assignment_variable(self,assignment):
        pattern = r"([\w\[\]]+)[ ]*=[ ]*.+"
        match = re.match(pattern, assignment)
        if match:
            variable = match.group(1)
            # 如果变量是数组，去掉数组索引
            variable = re.sub(r'\[.*\]', '', variable)
            return variable
        else:
            return None


            
                    
                        
                
    
    

    