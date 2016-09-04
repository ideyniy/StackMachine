import os
import unittest
import expressions as expr
from xml.etree.ElementTree import ElementTree, Element, SubElement

# Please change this variable to yours!
unittest_data_dir = 'C:\\Users\\netov\\PycharmProjects\\untitled1\\unittests-data\\'

simple_calculations = unittest_data_dir + 'simplevaluation-test\simple_calculations.xml'
base_complex = unittest_data_dir + 'complexvaluation-test\/base_complex.xml'

#Check size of long and adjust in long_int_plus_1.xml
long_int_plus_one = unittest_data_dir + 'simplevaluation-test\long_int_plus_1.xml'
float_values = unittest_data_dir + 'simplevaluation-test\/float_values.xml'
negative_values = unittest_data_dir + 'simplevaluation-test\/negative_values.xml'
zero_values = unittest_data_dir + 'simplevaluation-test\zero_values.xml'
misspelled_operation = unittest_data_dir+'simplevaluation-test\misspelled_operation.xml'
long_in_result = unittest_data_dir + 'simplevaluation-test\/long_in_result.xml'
float_in_result = unittest_data_dir+'simplevaluation-test\/float_in_result.xml'
same_top_ids = unittest_data_dir+'simplevaluation-test\same_top_ids.xml'
operations_of_operations = unittest_data_dir + 'complexvaluation-test\operations_of_operations.xml'
hundred_enclosed_operations = unittest_data_dir + 'complexvaluation-test\/hundred_enclosed_operations.xml'
recursion_depth = unittest_data_dir + 'complexvaluation-test\/recursion_depth.xml'

class TestConvertUtils(unittest.TestCase):

    def test_to_int_equal(self):
        self.assertEqual(expr.ConvertUtils.to_int('123'), 123)

    def test_to_int_non_equal(self):
        self.assertNotEqual(expr.ConvertUtils.to_int('321'), 123)

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

    #check if 'complex' tag parsed
    def test_complex_tag_exist(self):
        code = expr.XmlReader(base_complex).parse()
        result = 'true' in code[0]
        self.assertTrue(result)


    #check that incorrect path set as output.
    def test_xml_writer_to_wrong_folder(self):
        output_dir = "1"
        data = [(1, 9), (2, 1), (3, 240), (4, 6)]
        writer = expr.XmlWriter("", output_dir)
        self.assertTrue(writer.file_name == '_result.xml')

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
        code = expr.XmlReader(simple_calculations).parse()
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
        code = expr.XmlReader(base_complex).parse()
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


# check calculations with zero
class TestZeroValues(unittest.TestCase):

    def test_zero_values(self):
        code = expr.XmlReader(zero_values).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 13)
        self.assertEqual(res[0][1], 0)
        self.assertEqual(res[1][0], 14)
        self.assertEqual(res[1][1], 0)

# test long int in input
class TestLongIntPlusOne(unittest.TestCase):

    def test_long_int_plus_1(self):
        code = expr.XmlReader(long_int_plus_one).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 1)
        self.assertEqual(res[0][1], 2147483649L)

# test long int in result
class TestLongInResult(unittest.TestCase):
    def test_long_in_result(self):
        code = expr.XmlReader(long_in_result).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 1)
        self.assertEqual(res[0][1], 729000000000000L)

# test negative values
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

# test float in input
class TestFloatAsInput(unittest.TestCase):

    def test_float_calculated(self):
        code = expr.XmlReader(float_values).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 10)
        self.assertEqual(res[0][1], 10)

# test misspelled math operations
class TestMisspelledOperation(unittest.TestCase):

    def test_misspelled_operation(self):
        code = expr.XmlReader(misspelled_operation).parse()
        vm = expr.Machine()
        with self.assertRaises(RuntimeError):
            vm.run(code)

# test float in result
class TestFloatInResult(unittest.TestCase):

    def test_float_in_result(self):
        code = expr.XmlReader(float_in_result).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 14)
        self.assertEqual(res[0][1], 3.5)


# test same top IDs
class TestSameTopIDs(unittest.TestCase):

    def test_same_top_ids(self):
        code = expr.XmlReader(same_top_ids).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0], 10)
        self.assertEqual(res[0][1], 9)
        self.assertEqual(res[1][0], 10)
        self.assertEqual(res[1][1], 5)

# test complex operations
class TestOperationsOfOperations(unittest.TestCase):

    def test_hundred_operations_of_operations(self):
        code = expr.XmlReader(hundred_enclosed_operations).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertTrue(res[0][0],10)
        self.assertTrue(res[0][0],200)

    def test_operations_of_operations_(self):
        code = expr.XmlReader(operations_of_operations).parse()
        vm = expr.Machine()
        res = vm.run(code)
        self.assertEqual(res[0][0],10)
        self.assertEqual(res[0][1],6)

    def test_lots_enclosed_operations(self):
        code = expr.XmlReader(recursion_depth).parse()
        vm = expr.Machine()
        res = vm.run(code)
        print res

if __name__ == '__main__':
    unittest.main()

