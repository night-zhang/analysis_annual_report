# -*- encoding: utf-8 -*-
import pdfplumber
import os
import logging
import datetime
import time
from multiprocessing import Pool

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


def pdf_2_txt(file_name):
    # extract_content(r'test_pdf/2-万科A-2007年年度报告.pdf', "temp.txt")
    # begin = datetime.datetime.now()
    # logger.info("begin")

    stem, suffix = os.path.splitext(file_name)
    txt_file_name = r'result_txt/{}.txt'.format(stem)
    if os.path.lexists(txt_file_name):
        logger.info("{}已存在".format(txt_file_name))
        return
    extract_content(r'test_pdf/{}'.format(file_name), txt_file_name)


    # end = datetime.datetime.now()
    # logger.info("end")
    # logger.info("耗时共{}".format(end - begin))


def run__pool():  # main process

    cpu_worker_num = 10
    # process_args = os.listdir(r'test_pdf')

    # print(f'| inputs:  {process_args}')
    start_time = datetime.datetime.now()
    with Pool(cpu_worker_num) as p:
        outputs = p.map(pdf_2_txt, os.listdir(r'test_pdf'))
    print(f'| outputs: {outputs}  \n  TimeUsed: {datetime.datetime.now() - start_time}    \n')

    '''Another way (I don't recommend)
    Using 'functions.partial'. See https://stackoverflow.com/a/25553970/9293137
    from functools import partial
    # from functools import partial
    # pool.map(partial(f, a, b), iterable)
    '''


if __name__ == '__main__':
    run__pool()
