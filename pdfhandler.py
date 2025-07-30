from pypdf import PdfReader, PdfWriter
import os

def split_pdf_by_outline(input_pdf_path, output_dir):
    reader = PdfReader(input_pdf_path)
    outlines = reader.outline
    page_count = len(reader.pages)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    def get_title_and_page(item):
        title = item.title.strip().replace('/', '_')  # 防止文件名非法
        page_number = reader.get_destination_page_number(item)
        return title, page_number

    titles_pages = []
    for item in outlines:
        if isinstance(item, list):
            continue  # 忽略多级目录（这里只按一级目录拆分）
        title, page_number = get_title_and_page(item)
        titles_pages.append((title, page_number))

    titles_pages.append(("END", page_count))  # 方便最后一章的终止页处理

    for i in range(len(titles_pages) - 1):
        title, start_page = titles_pages[i]
        _, end_page = titles_pages[i + 1]

        writer = PdfWriter()
        for page in range(start_page, end_page):
            writer.add_page(reader.pages[page])

        output_path = os.path.join(output_dir, f"{i+1:02d}_{title}.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)
        print(f"导出：{output_path}")

# 使用示例
split_pdf_by_outline(r"C:\Users\sunny\Documents\books\托马斯微积分（英文原版14版）.pdf", r"C:\Users\sunny\Documents\books\tms")
