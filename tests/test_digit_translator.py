import unittest

from dlcommon.util.text import DigitTranslator


class DigitTranslatorTestCase(unittest.TestCase):
    def test_fluent_convert_integer(self):
        test_cases = [
            ('0', '零'),
            ('1', '一'),
            ('10', '十'),
            ('11', '十一'),
            ('100', '一百'),
            ('101', '一百零一'),
            ('110', '一百一十'),
            ('111', '一百一十一'),
            ('1000', '一千'),
            ('1001', '一千零一'),
            ('1010', '一千零一十'),
            ('1100', '一千一百'),
            ('1011', '一千零一十一'),
            ('1101', '一千一百零一'),
            ('1110', '一千一百一十'),
            ('1111', '一千一百一十一'),
        ]
        for input, target in test_cases:
            output = DigitTranslator.fluent_convert_integer(input)
            self.assertEqual(target, output)


if __name__ == '__main__':
    unittest.main()
