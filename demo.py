# -*- encoding: utf-8 -*-
from io import StringIO

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import jieba


# 读取pdf的函数，返回内容
def readPdf(pdf_file):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr=rsrcmgr, outfp=retstr, laparams=laparams)

    process_pdf(rsrcmgr=rsrcmgr, device=device, fp=pdf_file)
    device.close()

    content = retstr.getvalue()
    retstr.close()

    return content


# 开始分词
def do_jieba(txt):
    # 载入词典
    jieba.load_userdict("accounting_words1.txt")

    words = jieba.lcut(txt)  # 使用精确模式对文本进行分词
    counts = {}  # 通过键值对的形式存储词语及其出现的次数

    for word in words:
        # if len(word) == 1:  # 单个词语不计算在内
        #     continue
        # else:
        counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1

    jieba_result = list(counts.items())  # 将键值对转换成列表
    jieba_result.sort(key=lambda x: x[1], reverse=True)  # 根据词语出现的次数进行从大到小排序
    return jieba_result


# 计算字数
def calculate_words(items):
    accounting_count1 = 0

    for i in items:
        if i[0] in accounting_words1:
            if debug:
                print(i, len(i[0]))
            accounting_count1 += i[1] * len(i[0])
    if debug:
        print("会计词总字数1：", accounting_count1)

    return accounting_count1


# 提取关键词
def get_keywords():
    # link_words_, accounting_words1_, accounting_words2_, accounting_words3_, accounting_words4_ = [], [], [], [], []
    link_words_, accounting_words1_, accounting_words4_ = [], [], []
    # 连接词提取
    for i in open("link_words.txt", "r", encoding="utf-8"):
        i = i.replace("\n", "")
        # if len(i) == 1:  # 单个词语不计算在内
        #     continue
        # else:
        link_words_.append(i)
    if debug:
        print("连接词:", link_words_)

    # 会计词提取1
    for i in open("accounting_words1.txt", "r", encoding="utf-8"):
        i = i.replace("\n", "")
        if len(i) == 1:  # 单个词语不计算在内
            continue
        else:
            accounting_words1_.append(i)
    if debug:
        print("会计词1:", accounting_words1_)


    # 会计词提取4
    for i in open("accounting_words4.txt", "r", encoding="utf-8"):
        i = i.replace("\n", "")
        if len(i) == 1:  # 单个词语不计算在内
            continue
        else:
            accounting_words4_.append(i)
    if debug:
        print("会计词3:", accounting_words4_)

    # return link_words_, accounting_words1_, accounting_words2_, accounting_words3_, accounting_words4_
    return link_words_, accounting_words1_, accounting_words4_


if __name__ == '__main__':
    debug = 1

    pdf_file = open(r'test_pdf/2-万科A-2007年年度报告.pdf', 'rb')
    content = readPdf(pdf_file)
    # print(content)
    print(type(content))

    pdf_file.close()

    link_words, accounting_words1, accounting_words4 = get_keywords()

    txt = content.replace("\n", "")
    txt_count = len(txt)
    # 年报和字数
    jieba_result = do_jieba(txt)
    # print(jieba_result)
    accounting_count1 = calculate_words(jieba_result)
    print(accounting_count1)