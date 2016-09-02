import sys
import unittest
import expressions as expr
from xml.etree.ElementTree import ElementTree, Element, SubElement

# Please change this variable to yours!
unittest_data_dir = 'C:\\Users\\netov\\Documents\\Solution\\unittests-data\\'
simple_xml = unittest_data_dir+'simplevaluation-test\simple.xml'
long_value = unittest_data_dir + 'simplevaluation-test\long_value.xml'
complex_xml = unittest_data_dir + 'complexvaluation-test\complex.xml'
float_xml = unittest_data_dir+'complexvaluation-test\/float.xml'
negative_xml = unittest_data_dir+'complexvaluation-test\/negative.xml'
zero_values_xml = unittest_data_dir+'complexvaluation-test\/zero_values.xml'

class TestConvertUtils(unittest.TestCase):

    def test_to_int_equal(self):
        self.assertEqual(expr.ConvertUtils.to_int('123'), 123)

    def test_to_int_non_equal(self):
        self.assertNotEqual(expr.ConvertUtils.to_int('321'), 123)

    # Calculations with float
    def test_float_to_int(self):
        self.assertEquals(expr.ConvertUtils.to_int("2.02"), 2.02)

    # Check complex tag parsed
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
            res = expr.ConvertUtils.data_to_xml_node(None)

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


class TestInputFiles(unittest.TestCase):

    def test_input_files_returns_list(self):
        global unittest_data_dir
        files = expr.get_input_files(unittest_data_dir+'filelisting-test', '.xml', '_result')
        self.assertEqual(True, isinstance(files, list))

    def test_input_files_expected_error(self):
        global unittest_data_dir
        with self.assertRaises(WindowsError):
            expr.get_input_files('UNKNOWN_DIR', '.xml', '_result')

    def test_input_files(self):
        #global unittest_data_dir
        files = expr.get_input_files(unittest_data_dir+'filelisting-test', '.xml', '_result')
        self.assertEqual('file1.xml', files[0])
        self.assertEqual('file2.xml', files[1])
        self.assertEqual('file3.xml', files[2])

class TestMultDivideZero(unittest.TestCase):

    def test_zero_value(self):
        code = expr.XmlReader(zero_values_xml).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 13)
        self.assertEqual(res[0][1], 0)
        self.assertEqual(res[1][0], 14)
        self.assertEqual(res[1][1], 0)

class TestMaxInt(unittest.TestCase):

    def test_long_values(self):
        code = expr.XmlReader(long_value).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 1)
        self.assertEqual(res[0][1], 2147483649)

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

class TestValuationComplexNegative(unittest.TestCase):

    def test_complex_negative_valuation(self):
        code = expr.XmlReader(negative_xml).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 10)
        self.assertEqual(res[0][1], -5)
        self.assertEqual(res[1][0], 11)
        self.assertEqual(res[1][1], 5)
        self.assertEqual(res[2][0], 12)
        self.assertEqual(res[2][1], -48)
        self.assertEqual(res[3][0], 13)
        self.assertEqual(res[3][1], 0)
        self.assertEqual(res[4][0], 14)
        self.assertEqual(res[4][1], -6)

class TestValuationComplexFloat(unittest.TestCase):

    def test_float_valuation(self):
        global unittest_data_dir
        input_file = unittest_data_dir+'complexvaluation-test\/float.xml'
        code = expr.XmlReader(input_file).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 10)
        self.assertEqual(res[0][1], 10.01)

if __name__ == '__main__':
    unittest.main()

