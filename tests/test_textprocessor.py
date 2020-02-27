from dlcommon.util.text import TextProcesser, CommonPattern

processer = TextProcesser()
processer.keep(CommonPattern.ZH).keep(CommonPattern.STOP_PUNC).keep(CommonPattern.NUMBER).remove('丶')

with open('text_test_cases.txt', 'r') as f:
    lines = f.readlines()
    with open('result.txt', 'w') as fout:
        for line in lines:
            result = processer.process(line)
            fout.write(result+'\n')
