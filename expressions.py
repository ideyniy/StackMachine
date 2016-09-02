"""
a Simple xml parser fed stack machine,
producing results of operations into xml.

Stack machine implemented, based on
sources: http://csl.sublevel3.org/post/vm/
https://github.com/cslarsen/python-simple-vm
"""

from collections import deque
from xml.etree.ElementTree import ElementTree, Element, SubElement
from os import listdir
from os.path import isfile, join, splitext
import sys


class ConvertUtils(object):
    @staticmethod
    def to_int(string, supress_exception=True):
        value = None
        try:
            value = int(float(string))
        except ValueError as valueError:
            if not supress_exception:
                raise valueError
            else:
                pass
        except TypeError as typeError:
            if not supress_exception:
                raise typeError
            else:
                pass
        return value

    # @staticmethod
    # def to_string(stringToConvert):
    #     return  str(stringToConvert)

    @staticmethod
    def data_to_xml_node(data):
        elm = Element("expressions")
        for r_id, result in data:
            sub = SubElement(elm, "result", id=str(r_id))
            sub.text = str(result)
        return elm




class Machine(object):
    """
    a Stack Machine interpreting the following syntax:
    <expressions> : [(<operation>, [(<operand> or None, <expressions>),..], <result_id>),..]
    """

    def __init__(self):
        self.data_stack = deque()
        self.dispatch_map = dict(addition=int.__add__, subtraction=int.__sub__, multiplication=int.__mul__, division=int.__floordiv__)

    def pop(self):
        return self.data_stack.pop()

    def push(self, value):
        self.data_stack.append(value)

    def run(self, code):
        return [(res, self.dispatch((ins, op, None)) or self.pop())
                for ins, op, res in code]

    def dispatch(self, op):
        #print op
        if not op:
            pass
        elif isinstance(op, str) and op in self.dispatch_map:
            self.execute(op)
        elif isinstance(op, int):
            self.push(op)
        elif isinstance(op, tuple) and len(op) == 2:
            map(self.dispatch, op)
        elif isinstance(op, tuple) and len(op) == 3:
            ins, ops, _ = op
            map(self.dispatch, ops)
            for _ in range(len(ops)-1):
                self.dispatch(ins)
        elif isinstance(op, list):
            map(self.dispatch, op)
        else:
            raise RuntimeError("Unknown operation: '%s'" % op)

    def execute(self, op):
        last = self.pop()
        self.push(self.dispatch_map[op](self.pop(), last))


class XmlReader(object):
    """
    a Parser from XML to Machine interpretable code
    """
    def __init__(self, file_name):
        self.file_name = file_name

    def parse(self):
        root = ElementTree().parse(self.file_name)
        return self._elm_to_code(root)

    def _elm_to_code(self, elm):
        code = []
        expressions = elm
        for operation in expressions:
            operands = []
            for operand in operation:
                constant = ConvertUtils.to_int(operand.text.strip())
                sub_operation = self._elm_to_code(operand)
                operands.append((constant, sub_operation))
            result_id = ConvertUtils.to_int(operation.attrib.get("id"))
            #complex = ConvertUtils.to_string(operation.attrib.get("complex"))
            #code.append((operation.tag, operands, result_id, complex))
            code.append((operation.tag, operands, result_id))
        return code


class XmlWriter(object):
    """
    a Converter from the Stack Machine output into XML
    """
    def __init__(self, file_name, output_dir=None):
        self.file_name = '%s_result.xml' % file_name[:-4]
        if output_dir:
            self.file_name = join(output_dir, self.file_name)

    def write(self, data):
        tree = ElementTree()
        tree._setroot(ConvertUtils.data_to_xml_node(data))
        tree.write(self.file_name)


def get_input_files(dir, file_extension, result_postfix):
    return [f for f in listdir(dir) if (isfile(join(dir, f)) and not splitext(f)[0].endswith(result_postfix) and splitext(f)[1] == file_extension)]

if __name__ == "__main__":
    print('Usage python.exe expressions.py PathToInputDir PathToOutputDir')
    _, input_dir, output_dir = sys.argv
    input_files = get_input_files(input_dir, '.xml', '_result')
    vm = Machine()
    for xml_file in input_files:
        writer = XmlWriter(xml_file, output_dir)
        code = XmlReader(input_dir+xml_file).parse()
        print(code)
        res = vm.run(code)
        print(res)
        writer.write(res)




