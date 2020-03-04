import unittest

from dlcommon.util.text import TextProcesser, CommonCharset, DigitTranslator, split


class TextProcessorTestCase(unittest.TestCase):
    def test_keep(self):
        processer = TextProcesser().keep(CommonCharset.ZH)
        self.assertEqual('今天天气真不错', processer.process('今天天气真不错。asdfsa**&@$)*@^82764'))

    def test_remove(self):
        processer = TextProcesser().remove(CommonCharset.NUMBER)
        self.assertEqual('今天天气真不错。', processer.process('今天2010天气真不错。'))

    def test_combine(self):
        processer = TextProcesser().keep(CommonCharset.NUMBER).remove(r'123')
        self.assertEqual('456789', processer.process('123456789'))

    def test_keep_pattern(self):
        processer = TextProcesser().keep(CommonCharset.ZH).keep(CommonCharset.STOP_PUNC).keep_pattern(r'\+\d+')
        self.assertEqual('你好，杰克。+23456', processer.process('你好，杰克。adsf+23456'))


class DigitTranslatorTestCase(unittest.TestCase):

    def test_fluent_convert_integer_l1(self):
        test_cases = [
            ('0', '零'), ('1', '一'), ('10', '十'), ('11', '十一'),
            ('100', '一百'), ('101', '一百零一'), ('110', '一百一十'), ('111', '一百一十一'),
            ('1000', '一千'), ('1001', '一千零一'), ('1010', '一千零一十'), ('1100', '一千一百'),
            ('1011', '一千零一十一'), ('1101', '一千一百零一'), ('1110', '一千一百一十'), ('1111', '一千一百一十一'),
        ]
        for input, target in test_cases:
            translator = DigitTranslator()
            output = translator.fluent_convert_integer(input)
            self.assertEqual(target, output)

    def test_l1_translator(self):
        test_cases = [('0000', '零'), ('0010', '零一十'), ('0100', '零一百')]
        translator = DigitTranslator().l1_translator
        for input, target in test_cases:
            output = translator(list(input))
            self.assertEqual(target, output)

    def test_tens_like_handler(self):
        test_cases = [
            ('10010', '一万零一十'),
            ('100010', '十万零一十'),
            ('100100010', '一亿零一十万零一十'),
            ('1000100010', '十亿零一十万零一十'),
            ('10001000100010', '十兆零一十亿零一十万零一十'),
        ]
        for input, target in test_cases:
            translator = DigitTranslator()
            output = translator.fluent_convert_integer(input)
            self.assertEqual(target, output)


class MiscTestCase(unittest.TestCase):
    def test_split(self):
        out = split('123456784567', 4)
        self.assertEqual(['1234', '5678', '4567'], out)
        out = split('23456784567', 4)
        self.assertEqual(['234', '5678', '4567'], out)
        out = split(list('23456784567'), 4)
        self.assertEqual([list('234'), list('5678'), list('4567')], out)


if __name__ == '__main__':
    unittest.main()
