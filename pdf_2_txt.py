# -*- encoding: utf-8 -*-
import pdfplumber
import os
import logging
import datetime


logger = logging.getLogger(name='r')  # 不加名称设置root logger
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# 使用FileHandler输出到文件
fh = logging.FileHandler('log/example.log', encoding="utf-8", )
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# 使用StreamHandler输出到屏幕
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

# 添加两个Handler
logger.addHandler(ch)
logger.addHandler(fh)


def extract_content(pdf_path, txt_path):
    with pdfplumber.open(pdf_path) as pdf_file:
        content = ''
        for i in range(len(pdf_file.pages)):
            page_text = pdf_file.pages[i]
            page_content = page_text.extract_text()
            if page_content:
                content = content + page_content + "\n"
                with open(txt_path, "w", encoding="utf-8") as file:
                    file.write(content)
                    file.close()
    logger.info("{}生成成功".format(txt_path))


if __name__ == '__main__':
    # extract_content(r'test_pdf/2-万科A-2007年年度报告.pdf', "temp.txt")
    begin = datetime.datetime.now()
    logger.info("begin")

    for f in os.listdir(r'test_pdf'):  # listdir返回文件中所有目录
        stem, suffix = os.path.splitext(f)
        txt_file_name = r'result_txt/{}.txt'.format(stem)
        if os.path.lexists(txt_file_name):
            logger.info("{}已存在".format(txt_file_name))
            continue
        extract_content(r'test_pdf/{}'.format(f), txt_file_name)
        # print(stem, suffix)

    end = datetime.datetime.now()
    logger.info("end")

    logger.info("耗时共{}".format(end - begin))
