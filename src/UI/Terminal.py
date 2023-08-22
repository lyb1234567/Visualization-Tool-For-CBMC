from PyQt5.QtWidgets import QMainWindow,QAction, QFileDialog, QInputDialog, QTabWidget, QDockWidget, QFileSystemModel,QPlainTextEdit,QVBoxLayout,QMessageBox,QApplication
from PyQt5.QtCore import QProcess,Qt,QEvent
from PyQt5.QtGui import QTextCursor,QCursor
import subprocess
import os
import sys
import re
import glob
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_folder)
from UI.utils import extract_command,extract_file_name_without_extension,print_result,wait_for_file,extract_file_name
from JsonViwer.MainJsonWindow import JsonWindow as jsonWindow
from ControlFlowGraph.ControlFlowGraphGenerator import ControlGraphGenerator,Source_Type
from enum import Enum
class TextType(Enum):
    FILE=1
class Terminal(QPlainTextEdit):
    def __init__(self, parent=None,editor_window=None):
        super(Terminal, self).__init__(parent)
        self.installEventFilter(self)
        self.process = QProcess(self)
        self.jsonwindow=None
        self.editor_window=editor_window
        self.jsonFileChange=False
        self.cfg=None
        self.process.readyRead.connect(self.dataReady)
        self.process.start('cmd.exe')
        self.text_cursor=self.textCursor()
        self.clear()
        self.trace_point_info=[]
        self.command_history=[]
        self.command_index=0
        self.cursorPositionChanged.connect(self.handle_cursor_position_changed)
        self.cur_assertion_statement=None
        self.commands_info = {
            'clear': 'Clear the terminal.',
            'info tracepoint': 'Print all tracepoint information.',
            'tracepoint': 'Usage: tracepoint <filename> <line_number>. Set a tracepoint at a specific line in a file.',
            'run': 'Usage: run <file1> <file2> ... <fileN>. Run the given files.',
            'help':'Usage: help <command name>. Show the useage of specific line'
        }
    # 打印目前已有的tracepoint 信息
    def print_trace_point_info(self):
        num_trace_point=len(self.trace_point_info)
        res=""
        for i in range(num_trace_point):
            trace_info_dict=self.trace_point_info[i]
            assert(isinstance(trace_info_dict,dict))
            for key in trace_info_dict.keys():
                file_name=key
                line_number=trace_info_dict[key]
                res=res+" {0} tracepoint".format(i+1)+" at "+" {0}: line {1}".format(file_name,line_number)+"\n"
        if not res:
            return "There are no tracepoints set!!"
        return res
    def is_valid_file_path(self,path):
        if os.path.isfile(path):
            return True
        elif os.path.isabs(path) and os.path.isfile(os.path.basename(path)):
            return True
        return False
    def is_valid_file_path_with_line(self,path):
        # Regular expression pattern for file path with line number
        pattern = r'^(.*),\s*line\s+(\d+)$'
        
        match = re.match(pattern, path)
        if match:
            # Extract file path and line number
            file_path, line_number = match.groups()
            # Check if the file path is valid and line number is a positive integer
            if os.path.isfile(file_path) and int(line_number) > 0:
                return (True, file_path, int(line_number))
        else:
            # Check if the path is a valid file path (without line number)
            if os.path.isfile(path):
                 return (True, path, None)
        return False
    def mousePressEvent(self, event):
            # Call the superclass' mousePressEvent to handle the default behavior
            super(Terminal, self).mousePressEvent(event)
            # Check if the Control key is being held down
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                # If the Control key is being held down and the user has selected some text,
                # make the text clickable (or perform whatever action you want to implement)
                selected_text = self.textCursor().selectedText()
                if selected_text:
                    try:
                        check_file_line,file_path,line_number=self.is_valid_file_path_with_line(selected_text)
                        # Perform your action here, e.g., print the selected text
                        if check_file_line:
                            self.editor_window.openFile(cfg=self.cfg,file_path=file_path,line_number=line_number,SOURCE_TYPE=Source_Type.TRACE_SOURCE,assertion_statement=self.cur_assertion_statement)
                        elif self.is_valid_file_path(file_path) and not check_file_line:
                            self.editor_window.openFile(file_path=file_path)
                        else:
                            print(f"'{selected_text}' is not a valid file path.")
                    except:
                            pass
    def eventFilter(self, source, event):
            if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Control:
                QApplication.setOverrideCursor(QCursor(Qt.PointingHandCursor))
            elif event.type() == QEvent.KeyRelease and event.key() == Qt.Key_Control:
                QApplication.restoreOverrideCursor()
            return super(Terminal, self).eventFilter(source, event)
    def handle_cursor_position_changed(self):
        # cursor = self.textCursor()
        # print('Cursor position:', cursor.position())
        pass
    # 记录断点的文件名和位置，当用户选择某个asssertion statement的trace的时候，
    # 会遍历这个字典，获取所有的trace信息，并且打印出来
    # 更新的信息格式如下：{'filename':line_number}，比如{'file2.c':12}
    def set_tracepoint(self,file_name,line_number):
        self.trace_point_info.append({file_name:line_number})
    # 清空所有break point的信息，比如把某个trace 图关闭之后
    def clear_tracepoint(self):
        self.trace_point_info.clear()
    def dataReady(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(str(self.process.readAll(), 'utf-8'))
        self.ensureCursorVisible()
    def replace_last_line(self, new_line):
        # Get all text
        text = self.toPlainText()
        # Split it into lines
        lines = text.split('\n')
        # Get the last line
        last_line = lines[-1]
        # Find the last occurrence of '>'
        index = last_line.rfind('>')
        if index != -1:
            # If found, replace everything after it with the new line
            last_line = last_line[:index+1] + ' ' + new_line.strip()
            # Replace the last line
            lines[-1] = last_line
            # Join the lines and set the new text
            self.setPlainText('\n'.join(lines))
            self.text_cursor.movePosition(self.textCursor().position())
            self.setTextCursor(self.text_cursor)
    # 获取当前输入的命令或者内容
    def get_current_input(self):
        # Get all text
        text = self.toPlainText()
        # Split it into lines
        lines = text.split('\n')
        # Get the last line
        last_line = lines[-1]
        # Find the last occurrence of '>'
        return last_line.split('>')[-1].strip()
    def get_file_lst(self,input_str):
        # The regular expression pattern for matching filenames and other strings
        pattern = r"\b\w+\.\w+\b|\b\w+\b"

    # Find all matches in the input string
        matches = re.findall(pattern, input_str)

        return matches
    def on_tab_pressed(self):
        current_input = self.get_current_input()
        if current_input.startswith('run ') or current_input.startswith('tracepoint '):
            if current_input.startswith('tracepoint'):
                arguments=current_input.split(' ')
                # 如果目前只输入了两个参数，那么就可以尝试补全，如果超过两个参数了，那么就不操作
                if len(arguments)==2:
                    previouscontent = current_input.split(' ', 1)[0]
                    possible_filename = current_input.split(' ', 1)[1]
                    possible_completions = glob.glob(possible_filename + '*')
                    common_prefix=self.commonprefix(possible_completions)
                    new_line=previouscontent.strip()+" "+common_prefix.strip()
                    self.replace_last_line(new_line)
            # 当使用run 命令时，如果是多个文件，就提取参数最后一个座位
            elif current_input.startswith('run'):
                arguments=self.get_file_lst(current_input)
                arguments=[element for element in arguments if element!='']
                file_to_be_completed=arguments[-1]
                previouscontent = ""
                for i in range(len(arguments)-1):
                    previouscontent=previouscontent+arguments[i]+" "
                possible_filename = file_to_be_completed
                possible_completions = glob.glob(possible_filename + '*')
                common_prefix=self.commonprefix(possible_completions)
                new_line=previouscontent.strip()+" "+common_prefix.strip()
                self.replace_last_line(new_line)
            
    # 返回可能补全的文件名的公共部分比如：在['test.c', 'test_1.c', 'test_2.c', 'test_3.c']，就应当返回test
    def commonprefix(self,possible_files_lst):
        possible_files_lst = [file for file in possible_files_lst if file.endswith('.c')]
        if not possible_files_lst: 
            return ''
        else:
            s1 = min(possible_files_lst)
            s2 = max(possible_files_lst)
            for i, c in enumerate(s1):
                if c != s2[i]:
                    return s1[:i]
            return s1
    def keyPressEvent(self, event):
        cursor = self.textCursor()
        blockNumber = cursor.blockNumber()
        positionInBlock = cursor.positionInBlock()
        last_line = self.document().lastBlock().text()
        if ">" in last_line:
            index_of_gt = last_line.index(">") + 1  # consider space after ">"
        else:
            index_of_gt = 0
    # Disallow modification before ">" character
        if blockNumber == self.document().blockCount() - 1 and positionInBlock <= index_of_gt:
            if event.key() in {Qt.Key_Backspace, Qt.Key_Left, Qt.Key_Delete, Qt.Key_Right}:
                return
        if event.key() == Qt.Key_Up:
            if self.command_index > 0:
                self.command_index -= 1
                self.replace_last_line(self.command_history[self.command_index-1])
                self.text_cursor.movePosition(self.textCursor().position())
                self.setTextCursor(self.text_cursor)
        elif event.key() == Qt.Key_Down:
            if self.command_index <= len(self.command_history) - 1:
                self.command_index += 1
                self.replace_last_line(self.command_history[self.command_index-1])
                self.text_cursor.movePosition(self.textCursor().position())
                self.setTextCursor(self.text_cursor)
        if event.key() == Qt.Key_Tab:
            # 在这里处理 Tab 键的按下事件
            self.on_tab_pressed()
            event.accept()
        elif event.key() == Qt.Key_Return:
            command = self.toPlainText().split('\n')[-2]
            last_command=self.toPlainText().split('\n')[-1]
            last_command=extract_command(last_command)
            self.command_history.append(last_command)
            self.command_index = len(self.command_history)
            if last_command.strip() == 'clear':
                self.process.write(command.encode('utf-8'))
                self.process.write(b'\n')
                self.clear()
            elif last_command.strip()=='help':
                beginning_message="These shell commands are defined internally.  Type `help' to see this list.\n Type `help name' to find out more about the function `name'.\n"
                self.appendPlainText(beginning_message)
                for command, info in self.commands_info.items():
                    self.appendPlainText(f'{command}: {info}')
                self.process.write(b'\n')
            elif last_command.strip().startswith('help '):
                command_to_help = last_command.split('help')[1].strip()
                info = self.commands_info.get(command_to_help, f'No information available for command {command_to_help}.')
                self.appendPlainText(f'{command_to_help}: {info}')
                self.process.write(b'\n')
            elif last_command.strip() == 'info tracepoint':
                trace_info=self.print_trace_point_info()
                self.appendPlainText(trace_info)
                self.process.write(b'\n')
            elif last_command.strip().startswith('tracepoint'):
                args = last_command.split(' ')
                if len(args) == 3:
                    file_name, line_number = args[1], args[2]
                    self.set_tracepoint(file_name, line_number)
                    self.process.write(b'\n')
                else:
                    self.appendPlainText('Invalid command. Usage: tracepoint <filename> <line_number>')
                    self.process.write(b'\n')
            elif last_command.strip().startswith('run'):
                file_lst=last_command.split(' ')[1:]
                file_lst=[file for file in file_lst if file != '']
                if len(file_lst)==0:
                   QMessageBox.warning(self,"Warning", "Need a file to run!")
                   self.process.write(b'\n')
                elif len(file_lst)==1:
                    file_name=extract_file_name(file_lst[0])
                    if os.path.exists(file_name):
                        command='cbmc {0} --trace --json-ui > {1}.json'.format(file_lst[0],file_name)
                        command_trace_file='cbmc {0} --trace > trace.txt'.format(file_lst[0],file_name)
                        result = subprocess.run([command], shell=True, capture_output=True, text=True)
                        subprocess.run([command_trace_file], shell=True, capture_output=True, text=True)
                        jsonfile="{0}.json".format(file_name)
                        self.cfg=ControlGraphGenerator(trace_file='trace.txt')
                        self.editor_window.cfg=self.cfg
                        if not self.jsonwindow or  self.jsonFileChange:
                            self.jsonwindow=jsonWindow(jsonfile,editor_window=self.editor_window,cfg=self.cfg,run_by_editor=True)
                            self.jsonwindow.treeViewer.ExpandAllFailure()
                            self.jsonFileChange=True
                        self.jsonwindow.show()
                        if result.stdout:
                            self.appendPlainText(result.stdout)
                            self.process.write(b'\n')
                        elif result.stderr:
                            self.appendPlainText(result.stderr)
                            self.process.write(b'\n')
                        else:
                            self.appendPlainText(command)
                            self.process.write(b'\n')
                    else:
                        QMessageBox.warning(self,"Warning", "{0} is not in the directory!!".format(file_name))
                        self.process.write(b'\n')
                else:
                    
                    file_combined=""
                    file_not_exists=""
                    all_exists=True
                    non_exist_lst=[]
                    # 检查文件名是否存在，如果存在就执行，不存在提示
                    for file in file_lst:
                        if not os.path.exists(file):
                            non_exist_lst.append(file)
                            all_exists=False
                            file_not_exists=file_not_exists+file+", "
                        else:
                            file_combined=file_combined+file+" "
                    if all_exists:
                        outputFile, ok = QInputDialog.getText(self, 'Output file', 'Enter output file name')
                        if outputFile and ok:
                            build_goto_file="goto-cc "+file_combined+"-o "+outputFile
                            if build_goto_file:
                                subprocess.run([build_goto_file], shell=True, capture_output=True, text=True)
                                generate_json_file='cbmc {0} --trace --json-ui > {1}.json'.format(outputFile,outputFile)
                                generate_trace_file = 'cbmc {0} --trace > trace.txt'.format(outputFile)
                            result = subprocess.run([generate_json_file], shell=True, capture_output=True, text=True)
                            subprocess.run([generate_trace_file], shell=True, capture_output=True, text=True)
                            if result.stdout:
                                self.appendPlainText(result.stdout)
                                self.process.write(b'\n')
                            elif result.stderr:
                                self.appendPlainText(result.stderr)
                                self.process.write(b'\n')
                            else:
                                self.appendPlainText(generate_json_file)
                                self.process.write(b'\n')
                            jsonfile="{0}.json".format(outputFile)
                            wait_for_file(jsonfile)
                            self.cfg=ControlGraphGenerator(trace_file='trace.txt')
                            self.editor_window.cfg=self.cfg
                            if os.path.exists(jsonfile):
                                if not self.jsonwindow or self.jsonFileChange:
                                    self.jsonwindow=jsonWindow(jsonfile,editor_window=self.editor_window,cfg=self.cfg,run_by_editor=True)
                                    self.jsonFileChange=True
                                self.jsonwindow.show()
                        else:
                            self.process.write(b'\n')
                    else:
                        QMessageBox.warning(self,"Warning", "{0} not in the directory!!".format(file_not_exists))
                        self.process.write(b'\n')
            else:
                result = subprocess.run([last_command], shell=True, capture_output=True, text=True)
                if result.stdout:
                    self.appendPlainText(result.stdout)
                    self.process.write(b'\n')
                else:
                    self.appendPlainText(result.stderr)
                    self.process.write(b'\n')
        super(Terminal, self).keyPressEvent(event)