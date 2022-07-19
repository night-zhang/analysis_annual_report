# -*- encoding: utf-8 -*-
from io import StringIO

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams


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


pdf_file = open(r'test_pdf/2-万科A-2007年年度报告.pdf', 'rb')
content = readPdf(pdf_file)
print(content)
print(type(content))

pdf_file.close()


