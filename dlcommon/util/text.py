"""
自然语言文本处理常用函数
"""
import re


class TextProcesser:
    _KEEP_ = 'Keep'
    _REMOVE_ = 'Remove'

    @staticmethod
    def _sub(text, pattern):
        # TODO: 优化, 不要多次Compile
        regx = re.compile(pattern)
        return regx.sub('', text)

    @staticmethod
    def _decorate(pattern, type):
        if type == TextProcesser._KEEP_:
            return "[^{0}]".format(pattern)
        else:
            return "[{0}]".format(pattern)

    def __init__(self):
        self.__keep_pattern = r''
        self._actions = []

    def keep(self, pattern):
        self.__keep_pattern += pattern
        self._add_pattern(pattern, TextProcesser._KEEP_)
        return self

    def remove(self, pattern):
        self._add_pattern(pattern, TextProcesser._REMOVE_)
        return self

    def _add_pattern(self, pattern, type):
        # 如果上一个Pattern是相同的type, 直接拼接
        if len(self._actions) > 0 and self._actions[len(self._actions) - 1][1] == type:
            self._actions[len(self._actions) - 1][0] += pattern
        else:
            self._actions.append([pattern, type])

    def process(self, text):
        result = text
        for action in self._actions:
            result = self._sub(result, self._decorate(action[0], action[1]))
        return result

    def get_actions(self):
        return "\n".join(["{0}: {1}".format(action[1], action[0]) for action in self._actions])


class CommonPattern:
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

    EN_STOP_PUNC = r',\.\?!:;-~'
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
    def fluent_convert_integer(digit: str):
        """ 整数的正则表达式: (+|-)?\d+
        """
        int(digit)  # 先判断是不是整数

        def translate_level1(d1: str):
            """
            Note: 零需要特殊处理:
                  1. 从个位开始连续的0不翻译, 如100 -> 一百
                  2. 中间连续的0只翻译一个, 1001 -> 一千零一
                  3. 数字0不用带单位
                  4. 10~19(特殊处理)
            """
            assert len(d1) <= 4

            if digit == '0': return DigitTranslator.DIGIT_TEXT_MAPPER['0']

            # 10~19(特殊处理)
            if len(d1) == 2 and d1[0] == '1':
                return '十' + (DigitTranslator.DIGIT_TEXT_MAPPER[d1[1]] if d1[1] != '0' else '')

            result, i = [], 0
            current_digit = lambda: d1[len(d1) - i - 1]

            while i < len(d1):
                if i != 0 and current_digit() != '0':
                    result.append(DigitTranslator.CN_UNIT_L1[i - 1])
                result.append(DigitTranslator.DIGIT_TEXT_MAPPER[current_digit()])
                i = i + 1

            # 后处理去掉多余的零
            revised, i = [], 0
            ZERO = DigitTranslator.DIGIT_TEXT_MAPPER['0']
            while result[i] == ZERO: i += 1
            while i < len(result):
                if (result[i] == ZERO and result[i + 1] != ZERO) or result[i] != ZERO:
                    revised.append(result[i])
                i += 1

            revised.reverse()
            return ''.join(revised)

        return translate_level1(digit)

    @staticmethod
    def fluent_convert_float(digit: str):
        pass

    def __init__(self):
        self.stream_pattern = r'(P?<digit>\d+)(P?<quantifier>{0})'.format('|'.join(DigitTranslator.COMMON_QUANTIFIER))
        self.single_pattern = r'\d'
        self.single_regx = re.compile(self.single_pattern)
        self.stream_regx = re.compile(self.stream_pattern)

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
