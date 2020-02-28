from dlcommon.util.text import TextProcesser, CommonCharset

processer = TextProcesser()
processer.keep(CommonCharset.ZH).keep(CommonCharset.STOP_PUNC).keep(CommonCharset.NUMBER).remove('丶')

with open('text_test_cases.txt', 'r') as f:
    lines = f.readlines()
    with open('result.txt', 'w') as fout:
        for line in lines:
            result = processer.process(line)
            fout.write(result+'\n')
