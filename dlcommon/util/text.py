"""
自然语言文本处理常用函数
"""
import re


class TextProcesser:
    _KEEP_ = 'Keep'
    _REMOVE_ = 'Remove'

    def __init__(self):
        self._keep_patterns = []
        self._actions = []
        self._patterns = []
        self.regxes = None

    def keep(self, charset):
        self._add_action(charset, TextProcesser._KEEP_)
        return self

    def keep_pattern(self, pattern):
        self._keep_patterns.append(pattern)
        return self

    def remove(self, charset):
        self._add_action(charset, TextProcesser._REMOVE_)
        return self

    def _add_action(self, charset, type):
        # 如果上一个Action是相同的type, 直接拼接
        if len(self._actions) > 0 and self._actions[len(self._actions) - 1][1] == type:
            self._actions[len(self._actions) - 1][0] += charset
        else:
            self._actions.append([charset, type])

    def process(self, text):
        result = text
        if self.regxes is None: self._build_regxes()
        for regx, type in self.regxes:
            if type == TextProcesser._KEEP_:
                result = ''.join([''.join(g) for g in regx.findall(result)])
            elif type == TextProcesser._REMOVE_:
                result = regx.sub('', result)
        return result

    def get_actions(self):
        return "\n".join(["{0}: {1}".format(action[1], action[0]) for action in self._actions])

    def get_patterns(self):
        return "\n".join(self._patterns)

    def _build_regxes(self):
        self.regxes = []
        keep_pattern = '|'.join(['({0})'.format(p) for p in self._keep_patterns])
        for charset, type in self._actions:
            pattern = "([{0}])".format(charset)
            if type == TextProcesser._KEEP_ and len(self._keep_patterns) != 0:
                pattern += '|' + keep_pattern
            self._patterns.append(pattern)
            self.regxes.append((re.compile(pattern), type))


class CommonCharset:
    NUMBER = r'0-9'

    LOWER_EN = r'a-z'
    UPPER_EN = r'A-Z'
    EN = LOWER_EN + UPPER_EN

    ZH = r"\u4e00-\u9fa5"  # 中文
    JP = r"\u0800-\u4e00"  # 日文
    KO = r"\x3130-\x318F\xAC00-\xD7A3"  # 韩文

    ZH_ALL = r'\u2E80-\u9FFF'  # 所有象形字符, 包括中文日文韩文

    EN_PUNC = ''
    ZH_PUNC = ''

    EN_STOP_PUNC = r',\.\?!:;\-~'
    CN_STOP_PUNC = r'，。\？！；：\-～、《》&…'
    STOP_PUNC = EN_STOP_PUNC + CN_STOP_PUNC

    BLANK = r'\s'


class DigitTranslator:
    COMMON_QUANTIFIER = """
       串 	事 	册 	丘 	乘 	下 	丈 	丝 	两
       举 	具 	美 	包 	厘 	刀 	分 	列 	则
       剂 	副 	些 	匝 	队 	陌 	陔 	部 	出
       个 	介 	令 	份 	伙 	件 	任 	倍 	儋
       卖 	亩 	记 	双 	发 	叠 	节 	茎 	莛
       荮 	落 	蓬 	蔸 	巡 	过 	进 	通 	造
       遍 	道 	遭 	对 	尊 	头 	套 	弓 	引
       张 	弯 	开 	庄 	床 	座 	庹 	帖 	帧
       席 	常 	幅 	幢 	口 	句 	号 	台 	只
       吊 	合 	名 	吨 	和 	味 	响 	骑 	门
       间 	阕 	宗 	客 	家 	彪 	层 	尾 	届
       声 	扎 	打 	扣 	把 	抛 	批 	抔 	抱
       拨 	担 	拉 	抬 	拃 	挂 	挑 	挺 	捆
       掬 	排 	捧 	掐 	搭 	提 	握 	摊 	摞
       撇 	撮 	汪 	泓 	泡 	注 	浔 	派 	湾
       溜 	滩 	滴 	级 	纸 	线 	组 	绞 	统
       绺 	综 	缕 	缗 	场 	块 	坛 	垛 	堵
       堆 	堂 	塔 	墩 	回 	团 	围 	圈 	孔
       贴 	点 	煎 	熟 	车 	轮 	转 	载 	辆
       料 	卷 	截 	户 	房 	所 	扇 	炉 	炷
       觉 	斤 	笔 	本 	朵 	杆 	束 	条 	杯
       枚 	枝 	柄 	栋 	架 	根 	桄 	梃 	样
       株 	桩 	梭 	桶 	棵 	榀 	槽 	犋 	爿
       片 	版 	歇 	手 	拳 	段 	沓 	班 	文
       曲 	替 	股 	肩 	脬 	腔 	支 	步 	武
       瓣 	秒 	秩 	钟 	钱 	铢 	锊 	铺 	锤
       锭 	锱 	章 	盆 	盏 	盘 	眉 	眼 	石
       码 	砣 	碗 	磴 	票 	罗 	畈 	番 	窝
       联 	缶 	耦 	粒 	索 	累 	緉 	般 	艘
       竿 	筥 	筒 	筹 	管 	篇 	箱 	簇 	角
       重 	身 	躯 	酲 	起 	趟 	面 	首 	项
       领 	顶 	颗 	顷 	袭 	群 	袋
       """.split()

    DIGIT_TEXT_MAPPER = {
        "0": "零",
        "1": "一",
        "2": "二",
        "3": "三",
        "4": "四",
        "5": "五",
        "6": "六",
        "7": "七",
        "8": "八",
        "9": "九",
    }

    CN_UNIT_L1 = '十百千'
    CN_UNIT_L2 = '万亿兆京垓秭穰沟涧正载'

    @staticmethod
    def get_digit_trasnlator(block_translator, zero_digit_checker, zero_text_checker, units, special_handler=None):
        """ 默认翻译前缀"0",如果不想翻译,请自行去掉前缀0后再输入translator
        """
        def translator(blocks: list):
            """
             Note: 零需要特殊处理:
                  1. 从个位开始连续的0不翻译, 如100 -> 一百
                  2. 中间连续的0只翻译一个, 1001 -> 一千零一
                  3. 数字0不用带单位
                  4. 10~19(特殊处理)
            """
            if int(''.join(blocks)) == 0: return DigitTranslator.DIGIT_TEXT_MAPPER['0']

            if special_handler is not None:
                result = special_handler(blocks, block_translator, zero_digit_checker, zero_text_checker, units)
                if result is not None: return result

            result, i = [], 0
            current_block = lambda: blocks[len(blocks) - i - 1]

            while i < len(blocks):
                if i != 0 and not zero_digit_checker(current_block()):
                    result.append(units[i - 1])
                result.append(block_translator(current_block()))
                i = i + 1

            # 后处理去掉多余的零
            revised, i = [], 0
            while zero_text_checker(result[i]): i += 1  # 去掉末尾的零
            while i < len(result):
                if (zero_text_checker(result[i]) and i + 1 == len(result)) \
                    or (zero_text_checker(result[i]) and not zero_text_checker(result[i + 1])) \
                    or not zero_text_checker(result[i]):
                    revised.append(result[i])
                i += 1

            revised.reverse()
            return ''.join(revised)

        return translator

    def __init__(self):
        self.stream_pattern = r'(P?<digit>\d+)(P?<quantifier>{0})'.format('|'.join(DigitTranslator.COMMON_QUANTIFIER))
        self.single_pattern = r'\d'
        self.single_regx = re.compile(self.single_pattern)
        self.stream_regx = re.compile(self.stream_pattern)

        self.l1_translator = DigitTranslator.get_digit_trasnlator(lambda x: DigitTranslator.DIGIT_TEXT_MAPPER[x],
                                                                  lambda block: block == '0',
                                                                  lambda text: text ==
                                                                               DigitTranslator.DIGIT_TEXT_MAPPER['0'],
                                                                  DigitTranslator.CN_UNIT_L1,
                                                                  special_handler=self._tens_like_handler)
        self.l2_translator = DigitTranslator.get_digit_trasnlator(self.l1_translator,
                                                                  lambda block: block == '0000',
                                                                  lambda text: text ==
                                                                               DigitTranslator.DIGIT_TEXT_MAPPER['0'],
                                                                  DigitTranslator.CN_UNIT_L2)

    def _tens_like_handler(self, blocks, block_translator, zero_digit_checker, zero_text_checker, units):
        if len(blocks) == 2 and blocks[0] == '1':
            return units[0] + (block_translator(blocks[1]) if blocks[1] != '0' else '')
        return None

    def translate(self, text):
        """
        将文本中的数字换成中文
        策略:
          - 量词结尾的数字以串形式读
          - 其他数字逐个数字读
        :param text: 文本
        :return: 转换后的文本
        """
        text = self.convert_stream(text)
        text = self.convert_single(text)
        return text

    def convert_single(self, text: str):
        """
        将文本中的数字一一对应地转换成文本。
        例: 123 -> 一二三
        :param text: 文本
        :return: 转换后的文本
        """
        return self.single_regx.sub(lambda matchobj: DigitTranslator.DIGIT_TEXT_MAPPER[matchobj.group(0)], text)

    def convert_stream(self, text: str):
        """
        将文本中的数字流利的转换成对应的文本, 只会转换量词结尾的数字.
        例: 123个 -> 一百二十三个
        :param text: 文本
        :return: 转换后的文本
        """
        return self.stream_regx.sub(lambda matchobj: matchobj.group('digit'),
                                    text)

    def fluent_convert_integer(self, digit: str):
        """ 整数的正则表达式: (+|-)?\d+
            分两个层次翻译:
            1. 十百千: 每隔一位插入一个单位
            2. 万亿兆京垓秭穰沟涧正载: 每隔四位插入一个单位
        """

        num = int(digit)  # 先判断是不是整数, 顺便去掉前缀0
        digit = str(num)
        blocks = split(digit, 4)
        if len(blocks) > len(DigitTranslator.CN_UNIT_L2) + 1:
            raise ValueError('The digit is too large, please use direct_convert_integer instead')
        return self.l2_translator(blocks)

    @staticmethod
    def fluent_convert_float(digit: str):
        pass


def split(list_like, step: int) -> list:
    """
    将一个list或str按step的间距划分, 从尾部开始划分.
    例:
    >>> split('1234567', 4)
    ['123','4567']

    :param list_like: str或list
    :param step: 间距
    :return: 划分后的结果
    """
    array = list_like
    result, i = [], len(array)
    while i > 0:
        result.append(array[max(0, i - step):i])
        i -= step
    result.reverse()
    return result
