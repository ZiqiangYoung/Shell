"""
读取剪切板内容，调用在线翻译模块，获取翻译文本
输出到 docx 文档，保存到系统临时文件目录
windows 平台执行结束后会自动打开该文档
"""
import os
import time
import pyperclip

# noinspection PyPackageRequirements
from docx import Document, shared, oxml
from translate import create_translator


def clipboard_translate() -> None:
    translated: str
    text: str = pyperclip.paste()
    replace = text.replace('\r', ' ').replace('\n', ' ')

    with create_translator() as t:
        translated = t.translate(replace)

    output_dir: str = os.environ["temp"] + os.sep + "pdf_text_copy_translate"
    output_path: str = output_dir + os.sep + str(time.time()) + ".docx"

    doc = Document()
    doc.styles["Normal"].font.name = "等线 (中文正文)"
    doc.styles["Normal"].element.rPr.rFonts.set(oxml.ns.qn('w:eastAsia'), "等线 (中文正文)")
    doc.styles["Normal"].font.size = shared.Pt(12)
    doc.styles["Normal"].paragraph_format.line_spacing = shared.Pt(23)

    doc.add_paragraph(translated)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    doc.save(output_path)

    print("translated text was saved in \"" + output_path + "\"")

    os.system("start " + output_path)


if __name__ == '__main__':
    clipboard_translate()
