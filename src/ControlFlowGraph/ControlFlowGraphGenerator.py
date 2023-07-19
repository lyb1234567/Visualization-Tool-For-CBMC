import json
import os
from enum import Enum

class Assertion_Type(Enum):
    FUNCTION_CALL = 1
    VARIABLE = 2
class ControlGraphGenerator():
    def __init__(self,json_file,assertion_variables=None):
        self.json_file=json_file
        self.json_data=None
        self.CFG={}
        self.assertion_variables=assertion_variables
        self.load_data()
        self.cfg_generator_dict()
    def load_data(self):
        with open(self.json_file,'r') as f:
            self.json_data=json.load(f)
        return self.json_data
    def __str__(self):
        return self.CFG
    def get_variable_line(self,CFG_Source,fileName,variable):
        if CFG_Source[fileName].get(variable):
            return CFG_Source[fileName]['variable_line']
    def function_variable_line(self,CFG_Source,fileName,variable):
        pass 
    # try to find fileName in sourceLocation, if there is no such a fileName, it will return false,otherwise it will return 
    # fileName
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
    # insert function and corresponding function information: name, line number into the CFG source
    def insert_function(self,step,CFG_file_source,fileName):
        if step['stepType']=="function-call":
            if step.get('function') !=None or step['sourceLocation'].get('function')!=None:
                if step.get('function')!=None:
                    functionName=step['function']['displayName']
                    functionline=step['function']['sourceLocation']['line']
                    if CFG_file_source[fileName].get('function') ==None:
                        CFG_file_source[fileName]['function']={}
                        CFG_file_source[fileName]['function']['functionName']=[]
                        CFG_file_source[fileName]['function']['functionName'].append(functionName)
                    else:
                        if CFG_file_source[fileName]['function'].get('functionName')==None:
                            CFG_file_source[fileName]['function']['functionName']=[]
                            CFG_file_source[fileName]['function']['functionName'].append(functionName)
                        else:
                            CFG_file_source[fileName]['function']['functionName'].append(functionName)
                    if CFG_file_source[fileName]['function'].get('function_line')==None:
                        CFG_file_source[fileName]['function']['function_line']={}
                        CFG_file_source[fileName]['function']['function_line'][functionName]=[]
                        CFG_file_source[fileName]['function']['function_line'][functionName].append(int(functionline))
                    else:
                        if CFG_file_source[fileName]['function']['function_line'].get(functionName)==None:
                            CFG_file_source[fileName]['function']['function_line'][functionName]=[]
                            CFG_file_source[fileName]['function']['function_line'][functionName].append(int(functionline))
                        else:
                            CFG_file_source[fileName]['function']['function_line'][functionName].append(int(functionline))
                elif step.get('function')==None and step['sourceLocation'].get('function')!=None:
                    functionName=step['sourceLocation']['function']
                    functionline=step['sourceLocation']['line']
                    if CFG_file_source[fileName].get('function') ==None:
                        CFG_file_source[fileName]['function']={}
                        CFG_file_source[fileName]['function']['functionName']=[]
                        CFG_file_source[fileName]['function']['functionName'].append(functionName)
                    else:
                        if CFG_file_source[fileName]['function'].get('functionName')==None:
                            CFG_file_source[fileName]['function']['functionName']=[]
                            CFG_file_source[fileName]['function']['functionName'].append(functionName)
                        else:
                            CFG_file_source[fileName]['function']['functionName'].append(functionName)
                    if CFG_file_source[fileName]['function'].get('function_line')==None:
                        CFG_file_source[fileName]['function']['function_line']={}
                        CFG_file_source[fileName]['function']['function_line'][functionName]=[]
                        CFG_file_source[fileName]['function']['function_line'][functionName].append(int(functionline))
                    else:
                        if CFG_file_source[fileName]['function']['function_line'].get(functionName)==None:
                            CFG_file_source[fileName]['function']['function_line'][functionName]=[]
                            CFG_file_source[fileName]['function']['function_line'][functionName].append(int(functionline))
                        else:
                            CFG_file_source[fileName]['function']['function_line'][functionName].append(int(functionline))
        else:
            return
    # insert the variabel infromation: variable name,variable line number
    def insert_variable(self,step,CFG_file_source,fileName):
        if step['stepType']=='assignment':
            if step.get('assignmentType')!=None:
                if step['assignmentType']=='variable':
                    if step.get('lhs')!=None:
                        variable=step['lhs']
                        variable_line=step['sourceLocation']['line']
                        if CFG_file_source[fileName].get('variable')==None:
                            CFG_file_source[fileName]['variable']={}
                            CFG_file_source[fileName]['variable']['variableName']=[]
                            CFG_file_source[fileName]['variable']['variableName'].append(variable)
                        else:
                            if CFG_file_source[fileName]['variable'].get('variableName')==None:
                                CFG_file_source[fileName]['variable']['variableName']=[]
                                CFG_file_source[fileName]['variable']['variableName'].append(variable)
                            else:
                                CFG_file_source[fileName]['variable']['variableName'].append(variable)
                        
                        if CFG_file_source[fileName]['variable'].get('variable_line')==None:
                            CFG_file_source[fileName]['variable']['variable_line']={}
                            CFG_file_source[fileName]['variable']['variable_line'][variable]=[]
                            CFG_file_source[fileName]['variable']['variable_line'][variable].append(int(variable_line))
                        else:
                            if CFG_file_source[fileName]['variable']['variable_line'].get(variable)==None:
                                CFG_file_source[fileName]['variable']['variable_line'][variable]=[]
                                CFG_file_source[fileName]['variable']['variable_line'][variable].append(int(variable_line))
                            else:
                                CFG_file_source[fileName]['variable']['variable_line'][variable].append(int(variable_line))
        else:
            return
    def insert_function_actual_parameter(self,step,CFG_file_source,fileName):
        pass
        # try:
        #     if step['stepType']=='assignment'and  step['stepType']=='actual-parameter':
        #         actual_parameter=step['lhs']
        #         if CFG_file_source[fileName].get('function')
        # except:
        #     return 

    def insert_assertion_statement(self,result,CFG_file_source):
        if result.get('description'):
            fileName=result['sourceLocation']['file']
            assertion_statement=result['description']
            if CFG_file_source.get(fileName)==None:
                CFG_file_source[fileName]={}
            if CFG_file_source[fileName].get('assertion_statement')==None:
                 CFG_file_source[fileName]['assertion_statement']=[]
                 CFG_file_source[fileName]['assertion_statement'].append(assertion_statement)
            else:
                CFG_file_source[fileName]['assertion_statement'].append(assertion_statement)
            if CFG_file_source[fileName].get('assertion_statement_line')==None:
                CFG_file_source[fileName]['assertion_statement_line']={}
                CFG_file_source[fileName]['assertion_statement_line'][assertion_statement]=result['sourceLocation']['line']
            else:
                CFG_file_source[fileName]['assertion_statement_line'][assertion_statement]=result['sourceLocation']['line']
        else:
            return 
    def cfg_generator_dict(self):
        cnt=0
        if self.json_data!=None:
            for data in self.json_data:
            # For each step in the trace...
                if data.get('result')!=None:
                    for result in data['result']:
                        if result.get('trace')==None:
                            continue
                        cnt=cnt+1
                        CFG_file_source_name='CFG_file_source_'+str(cnt)
                        CFG_file_source={}
                        self.insert_assertion_statement(result,CFG_file_source)
                        for step in result['trace']:
                            if not step['hidden']:
                                fileName=self.find_file_in_sourceLocation(step)
                                if fileName !=False:
                                        if os.path.exists(fileName):
                                                if CFG_file_source.get(fileName)==None:
                                                    CFG_file_source[fileName]={}
                                                    self.insert_function(step,CFG_file_source,fileName)
                                                    self.insert_variable(step,CFG_file_source,fileName)
                                                else:
                                                    self.insert_function(step,CFG_file_source,fileName)
                                                    self.insert_variable(step,CFG_file_source,fileName)
                        self.CFG[CFG_file_source_name]=CFG_file_source
    

    