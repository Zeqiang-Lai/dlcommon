from dlcommon.util.text import TextProcesser, CommonCharset, DigitTranslator, split

if __name__ == '__main__':
    translator = DigitTranslator()
    while 1:
        x = input('> ')
        output = translator.fluent_convert_integer(x)
        print(output)
