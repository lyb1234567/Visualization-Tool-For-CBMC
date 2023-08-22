import unittest
from unittest.mock import patch, mock_open
import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_folder)
from log_decorator import log_on_success,count_function
import log_decorator
from ControlFlowGraph.ControlFlowGraphGenerator import ControlGraphGenerator  # 请确保将你的模块名称替换为正确的名称
class TestControlGraphGenerator(unittest.TestCase):
    
    @log_on_success
    def setUp(self):
        # 设置一个默认的trace文件内容来进行测试
        self.trace_files=['/home/mirage/Visualization-Tool-For-CBMC/src/test/test_files/test_2_trace_1.json','/home/mirage/Visualization-Tool-For-CBMC/src/test/test_files/test_2_trace_2.json','/home/mirage/Visualization-Tool-For-CBMC/src/test/test_files/test_2_trace_3.json']
        self.sample_trace_data = """** Results:
Trace for something
State 1 file example.c line 5
i=5 (0101)
State 2 file example.c line 10
j=10 (1010)
Violated property:
file example.c line 20
Some assertion failed
"""
        self.cfg=ControlGraphGenerator()
    
    @log_on_success
    @count_function
    def test_load_trace_data(self):
        with patch("builtins.open", mock_open(read_data=self.sample_trace_data)) as mock_file:
            cgg = ControlGraphGenerator(trace_file="dummy_trace_file")
            result = cgg.load_trace_data()
            self.assertEqual(result, self.sample_trace_data)
            mock_file.assert_called_with("dummy_trace_file", 'r')
    @log_on_success
    @count_function
    def test_is_state(self):
        cgg = ControlGraphGenerator()
        self.assertTrue(cgg.is_state("State 123 file some_file.c line 45 thread 0 function some_func"))
        self.assertFalse(cgg.is_state("Non-state line"))
    @log_on_success
    @count_function
    def test_extract_line_number(self):
        cgg = ControlGraphGenerator()
        result = cgg.extract_line_number("State 123 file some_file.c line 45 thread 0 function some_func")
        self.assertEqual(result, 45)
    @log_on_success
    @count_function
    def test_extract_file(self):
        cgg = ControlGraphGenerator()
        result = cgg.extract_file("State 123 file some_file.c line 45 thread 0 function some_func")
        self.assertEqual(result, "some_file.c")
    @log_on_success
    @count_function
    def test_clean_assignment(self):
        cgg = ControlGraphGenerator()
        result = cgg.clean_assignment("i=5 (0101)")
        self.assertEqual(result, ["i=5", "0101)"])
    @log_on_success
    @count_function
    def test_extract_assignment_variable(self):
        cgg = ControlGraphGenerator()
        self.assertEqual(cgg.extract_assignment_variable("array[5] = 10"), "array")
        self.assertEqual(cgg.extract_assignment_variable("variable = 20"), "variable")
    @log_on_success
    @count_function
    def test_reduce_json_file(self):
        self.cfg.trace_json_file=self.trace_files[0]
        check_hidden=False
        reduce_trace=self.cfg.reduce_trace_json()
        for json_obj in reduce_trace:
            if json_obj.get('hidden')!=None:
                    if json_obj['hidden']:
                        check_hidden=True
        self.assertFalse(check_hidden)
    @log_on_success
    @count_function
    def test_add_iteration(self):
        assertion_trace={"assertion i<4":[ {'i=0': {'file': 'test_2.c', 'line': '17', 'binary_format': '00000000000000000000000000000000', 'variable': 'i'}},{'i=1': {'file': 'test_2.c', 'line': '17', 'binary_format': '00000000000000000000000000000001', 'variable': 'i'}}]}
        self.cfg.assertion_trace_total_test=assertion_trace
        self.cfg.add_iteration_to_statements('assertion i<4')
        check_iteration=True
        for trace in self.cfg.assertion_trace_total_test["assertion i<4"]:
            for key in trace.keys():
                if "iteration" not in key:
                    check_iteration=False
        self.assertTrue(check_iteration)
    @log_on_success
    @count_function
    def test_clean_trace_json(self):
        self.cfg.trace_json_file=self.trace_files[1]
        self.cfg.clean_trace_json_file()
        test={'assertion *value > 0': [{'value=1': {'file': 'test_2.c', 'line': '24', 'binary_format': '00000000000000000000000000000001', 'variable': 'value'}}, {'value=value!0@1': {'file': 'test_2.c', 'line': '25', 'variable': 'value'}}, {'value=0': {'file': 'test_2.c', 'line': '11', 'binary_format': '00000000000000000000000000000000', 'variable': 'value'}}, {'assertion *value > 0': {'file': 'test_2.c', 'line': '12'}}]}
        self.assertEqual(test,self.cfg.assertion_trace_total_test)
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
        
        # 使用TextTestRunner来执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    current_file_path = os.path.abspath(__file__)
    with open('/home/mirage/Visualization-Tool-For-CBMC/src/test/test_graph_viewer/test_results.txt', 'a') as file:
                file.write(f'{log_decorator.module_test_count}\n')
