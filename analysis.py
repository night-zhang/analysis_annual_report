import jieba, csv, os, fnmatch
from io import StringIO

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams


# 获取该目录下所有文件的名字
def openfile(path):
    txt_path_list = []
    files = os.listdir(path)
    for filename in files:
        if not fnmatch.fnmatch(filename, '*.txt'):
            continue
        if fnmatch.fnmatch(filename, '*英文版*') or fnmatch.fnmatch(filename, '90*') or fnmatch.fnmatch(filename,
                                                                                                     '*ST*') or fnmatch.fnmatch(
            filename, '*修订*') or fnmatch.fnmatch(filename, '*更新*') or fnmatch.fnmatch(filename,
                                                                                      '*广告*') or fnmatch.fnmatch(
            filename, '*取消*')or fnmatch.fnmatch(filename, '*印刷*'):
            continue
        if debug:
            print(filename)
        txt_path = os.path.join(path, filename)
        txt_path_list.append(txt_path)
    return txt_path_list



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




def get_txt(txt_path):
    txt = open(txt_path, "r", encoding='ANSI').read()
    txt = txt.replace("\n", "").replace(" ", "")
    if debug:
        print(txt_path)
    txt_count = len(txt)
    if debug:
        print("总字数：", txt_count)
    return txt, txt_count


# 开始分词
def do_jieba(txt):
    # 载入词典
    jieba.load_userdict("keywords\\link_words.txt")
    jieba.load_userdict("keywords\\accounting_words1.txt")
    # jieba.load_userdict("keywords\\accounting_words2.txt")
    # jieba.load_userdict("keywords\\accounting_words3.txt")
    jieba.load_userdict("keywords\\accounting_words3.txt")

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


# 提取关键词
def get_keywords():
    # link_words_, accounting_words1_, accounting_words2_, accounting_words3_, accounting_words4_ = [], [], [], [], []
    link_words_, accounting_words1_, accounting_words4_ = [], [], []
    # 连接词提取
    for i in open("keywords\\link_words.txt", "r", encoding="utf-8"):
        i = i.replace("\n", "")
        # if len(i) == 1:  # 单个词语不计算在内
        #     continue
        # else:
        link_words_.append(i)
    if debug:
        print("连接词:", link_words_)

    # 会计词提取1
    for i in open("keywords\\accounting_words1.txt", "r", encoding="utf-8"):
        i = i.replace("\n", "")
        if len(i) == 1:  # 单个词语不计算在内
            continue
        else:
            accounting_words1_.append(i)
    if debug:
        print("会计词1:", accounting_words1_)

    # 会计词提取2
    # for i in open("keywords\\accounting_words2.txt", "r", encoding="utf-8"):
    #     i = i.replace("\n", "")
    #     if len(i) == 1:  # 单个词语不计算在内
    #         continue
    #     else:
    #         accounting_words2_.append(i)
    # if debug:
    #     print("会计词2:", accounting_words2_)
    #
    # # 会计词提取3
    # for i in open("keywords\\accounting_words3.txt", "r", encoding="utf-8"):
    #     i = i.replace("\n", "")
    #     if len(i) == 1:  # 单个词语不计算在内
    #         continue
    #     else:
    #         accounting_words3_.append(i)
    # if debug:
    #     print("会计词3:", accounting_words3_)

    # 会计词提取4
    for i in open("keywords\\accounting_words4.txt", "r", encoding="utf-8"):
        i = i.replace("\n", "")
        if len(i) == 1:  # 单个词语不计算在内
            continue
        else:
            accounting_words4_.append(i)
    if debug:
        print("会计词3:", accounting_words4_)

    # return link_words_, accounting_words1_, accounting_words2_, accounting_words3_, accounting_words4_
    return link_words_, accounting_words1_, accounting_words4_

stop_words = []



# 计算字数
def calculate_words(items):
    link_count = 0
    accounting_count1 = 0
    accounting_count2 = 0
    accounting_count3 = 0
    accounting_count4 = 0
    for i in items:
        if i[0] in link_words and i[0] not in stop_words:
            if debug:
                print(i, len(i[0]))
            link_count += i[1] * len(i[0])
    if debug:
        print("连接词总字数：", link_count)

    for i in items:
        if i[0] in accounting_words1:
            if debug:
                print(i, len(i[0]))
            accounting_count1 += i[1] * len(i[0])
    if debug:
        print("会计词总字数1：", accounting_count1)

    # for i in items:
    #     if i[0] in accounting_words2:
    #         if debug:
    #             print(i, len(i[0]))
    #         accounting_count2 += i[1] * len(i[0])
    # if debug:
    #     print("会计词总字数2：", accounting_count2)
    #
    # for i in items:
    #     if i[0] in accounting_words3:
    #         if debug:
    #             print(i, len(i[0]))
    #         accounting_count3 += i[1] * len(i[0])
    # if debug:
    #     print("会计词总字数3：", accounting_count3)

    for i in items:
        if i[0] in accounting_words4:
            if debug:
                print(i, len(i[0]))
            accounting_count4 += i[1] * len(i[0])
    if debug:
        print("会计词总字数3：", accounting_count4)

    # return link_count, accounting_count1, accounting_count2, accounting_count3
    return link_count, accounting_count1, accounting_count4

# 计算个数
def calculate_number(items):
    link_number = 0
    accounting_number1 = 0
    accounting_number4 = 0
    for i in items:
        if i[0] in link_words:
            if debug:
                print(i, len(i[0]))
            link_number += (1 + i[1])
    if debug:
        print("连接词总个数：", link_number)

    for i in items:
        if i[0] in accounting_words1:
            if debug:
                print(i, len(i[0]))
            accounting_number1 += (1 + i[1])
    if debug:
        print("会计词总个数1：", accounting_number1)


    for i in items:
        if i[0] in accounting_words4:
            if debug:
                print(i, len(i[0]))
            accounting_number4 += (1 + i[1])
    if debug:
        print("会计词总个数4：", accounting_number4)

    # return link_count, accounting_count1, accounting_count2, accounting_count3
    return link_number, accounting_number1, accounting_number4


# 保存数据到csv文件
def save_to_csv(field_list, data):
    # 1. 创建文件对象
    f = open('analysis_result.csv', 'w', encoding='utf-8-sig', newline="")
    # f.write(codecs.BOM_UTF8)

    # 2. 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)

    # 3. 构建列表头
    csv_writer.writerow(field_list)

    # 4. 写入csv文件内容
    # csv_writer.writerow(["l", '18', '男'])
    # csv_writer.writerow(["c", '20', '男'])
    # csv_writer.writerow(["w", '22', '女'])
    for i in data:
        csv_writer.writerow(i)

    # 5. 关闭文件
    f.close()


if __name__ == '__main__':
    debug = 0
    # 获取关键词
    # link_words, accounting_words1, accounting_words2, accounting_words3 = get_keywords()
    link_words, accounting_words1, accounting_words4 = get_keywords()
    # 设置表头
    # field_list = ["股票代码", "年份", "总字数", "连词字数", "会计词典1字数", "会计词典2字数", "会计词典3字数"]
    field_list = ["股票代码", "年份", "总字数", "连词个数", "会计词典1个数", "会计词典4个数"]
    # 最终结果
    csv_result = []

    # 文件夹名
    # path_list = ["txt2012", "txt2013", "txt2014", "txt2015", "txt2016", "txt2017", "txt2018"]
    path_list = ["test_pdf"]
    for path in path_list:
        year = path[3:]  # 年份
        txt_path_list = openfile(path)
        for i in txt_path_list:
            shares_num = i[8:14]  # 股票号
            txt, txt_count = get_txt(i)  # 年报和字数
            jieba_result = do_jieba(txt)
            # link_count, accounting_count1, accounting_count2, accounting_count3 = calculate_words(jieba_result)  # "连词字数", "会计词典1字数", "会计词典2字数", "会计词典3字数"
            link_count, accounting_count1, accounting_count4 = calculate_number(jieba_result)  # "连词字数", "会计词典1字数", "会计词典2字数", "会计词典3字数"
            # csv_result.append([shares_num, year, txt_count, link_count, accounting_count1, accounting_count2, accounting_count3])
            # print([shares_num, year, txt_count, link_count, accounting_count1, accounting_count2, accounting_count3])
            csv_result.append([shares_num, year, txt_count, link_count, accounting_count1, accounting_count4])
            print([shares_num, year, txt_count, link_count, accounting_count1, accounting_count4])

            # break
        # break

    print(csv_result)
    save_to_csv(field_list, csv_result)
    print("save to csv success!")
