import os
import unittest
import expressions as expr
from xml.etree.ElementTree import ElementTree, Element, SubElement

# Please change this variable to yours!
unittest_data_dir = 'C:\\Users\\netov\\PycharmProjects\\untitled1\\unittests-data\\'
simple_xml = unittest_data_dir+'simplevaluation-test\simple.xml'
max_int = unittest_data_dir + 'complexvaluation-test\long_values.xml'
complex_xml = unittest_data_dir + 'complexvaluation-test\complex.xml'
float_values = unittest_data_dir + 'complexvaluation-test\/float_values.xml'
negative_values = unittest_data_dir + 'complexvaluation-test\/negative_values.xml'
zero_values_xml = unittest_data_dir+'complexvaluation-test\zero_values.xml'
wrong_operations = unittest_data_dir+'complexvaluation-test\wrong_operations.xml'
big_values = unittest_data_dir+'complexvaluation-test\/big_result.xml'
float_in_result = unittest_data_dir+'complexvaluation-test\/big_result.xml'

class TestConvertUtils(unittest.TestCase):

    def test_to_int_equal(self):
        self.assertEqual(expr.ConvertUtils.to_int('123'), 123)

    def test_to_int_non_equal(self):
        self.assertNotEqual(expr.ConvertUtils.to_int('321'), 123)

    #mine
    def test_complex_tag(self):
        code = expr.XmlReader(complex_xml).parse()
        result = 'true' in code[0]
        self.assertTrue(result)

    def test_to_int_expect_value_error_exception(self):
        with self.assertRaises(ValueError):
            expr.ConvertUtils.to_int('123as.1', False)

    def test_to_int_expect_type_error_exception(self):
        with self.assertRaises(TypeError):
            expr.ConvertUtils.to_int([1,2,3], False)

    def test_data_to_elm_wrong_data(self):
        with self.assertRaises(TypeError):
            expr.ConvertUtils.data_to_xml_node(None)

    def test_data_to_elm_correct_instance(self):
        input_data = [(1, 2)]
        res = expr.ConvertUtils.data_to_xml_node(input_data)
        self.assertEqual(True, isinstance(res, Element))

    def test_data_to_elm_correct_len(self):
        input_data = [(1, 2), (3, 4), (5, 6)]
        res = expr.ConvertUtils.data_to_xml_node(input_data)
        children = res.getchildren()
        self.assertEqual(3, len(children))

    def test_data_to_elm_correct_ids(self):
        input_data = [(1, 2), (3, 4), (5, 6)]
        res = expr.ConvertUtils.data_to_xml_node(input_data)
        children = res.getchildren()
        self.assertEqual('1', children[0].get("id"))
        self.assertEqual('3', children[1].get("id"))
        self.assertEqual('5', children[2].get("id"))

    #mine
    def test_xml_writer_to_wrong_folder(self):
        output_dir = "1"
        data = [(1, 9), (2, 1), (3, 240), (4, 6)]
        with self.assertRaises(IOError):
            writer = expr.XmlWriter("", output_dir)
            writer.write(data)

class TestInputFiles(unittest.TestCase):

    def test_input_files_returns_list(self):
        files = expr.get_input_files(unittest_data_dir+'filelisting-test', '.xml', '_result')
        self.assertEqual(True, isinstance(files, list))

    def test_input_files_expected_error(self):
        with self.assertRaises(WindowsError):
            expr.get_input_files('UNKNOWN_DIR', '.xml', '_result')

    def test_input_files(self):
        files = expr.get_input_files(unittest_data_dir+'filelisting-test', '.xml', '_result')
        self.assertEqual('file1.xml', files[0])
        self.assertEqual('file2.xml', files[1])
        self.assertEqual('file3.xml', files[2])

class TestValuationSimple(unittest.TestCase):

    def test_simple_valuation(self):
        code = expr.XmlReader(simple_xml).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 1)
        self.assertEqual(res[0][1], 9)
        self.assertEqual(res[1][0], 2)
        self.assertEqual(res[1][1], 1)
        self.assertEqual(res[2][0], 3)
        self.assertEqual(res[2][1], 240)
        self.assertEqual(res[3][0], 4)
        self.assertEqual(res[3][1], 6)

class TestValuationComplex(unittest.TestCase):

    def test_complex_valuation(self):
        code = expr.XmlReader(complex_xml).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 10)
        self.assertEqual(res[0][1], 9)
        self.assertEqual(res[1][0], 11)
        self.assertEqual(res[1][1], 1)
        self.assertEqual(res[2][0], 12)
        self.assertEqual(res[2][1], 240)
        self.assertEqual(res[3][0], 13)
        self.assertEqual(res[3][1], 1814400)
        self.assertEqual(res[4][0], 14)
        self.assertEqual(res[4][1], 6)

#mine
class TestZeroValues(unittest.TestCase):

    def test_zero_values(self):
        code = expr.XmlReader(zero_values_xml).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 13)
        self.assertEqual(res[0][1], 0)
        self.assertEqual(res[1][0], 14)
        self.assertEqual(res[1][1], 0)

#mine
class TestMaxINT(unittest.TestCase):

    def test_max_int(self):
        code = expr.XmlReader(max_int).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 1)
        self.assertEqual(res[0][1], 2147483649L)

#mine
class TestNegativeValues(unittest.TestCase):

    def test_negative_values(self):
        code = expr.XmlReader(negative_values).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 10)
        self.assertEqual(res[0][1], -5)
        self.assertEqual(res[1][0], 11)
        self.assertEqual(res[1][1], 5)
        self.assertEqual(res[2][0], 12)
        self.assertEqual(res[2][1], -48)
        self.assertEqual(res[3][0], 13)
        self.assertEqual(res[3][1], -201600)
        self.assertEqual(res[4][0], 14)
        self.assertEqual(res[4][1], -6)

#mine
class TestFloatValues(unittest.TestCase):

    def test_float_values(self):
        code = expr.XmlReader(float_values).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 10)
        self.assertEqual(res[0][1], 10.01)

#mine
class TestWrongOperations(unittest.TestCase):

    def test_wrong_operations(self):
        code = expr.XmlReader(wrong_operations).parse()
        vm = expr.Machine()
        with self.assertRaises(RuntimeError):
            vm.run(code)

#mine
class TestBigResultCalculated(unittest.TestCase):

    def test_big_result_calculated(self):
        code = expr.XmlReader(big_values).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 1)
        self.assertEqual(res[0][1], 729000000000000L)

#mine
class TestFloatInResult(unittest.TestCase):

    def test_float_in_result(self):
        code = expr.XmlReader(float_in_result).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 1)
        self.assertEqual(res[0][1], 3.5)

if __name__ == '__main__':
    unittest.main()

