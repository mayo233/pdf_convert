import pdfplumber
import fitz  # PyMuPDF
from pathlib import Path

# 処理するPDFファイル
input_pdf_path = Path(r"C:/Users/homur/OneDrive/Desktop/Suzuka22.pdf")
output_pdf_path = Path(r"C:/Users/homur/OneDrive/Desktop/Suzuka22_highlighted.pdf")

# PDFファイルを開く
doc = fitz.open(input_pdf_path)  # PyMuPDF でPDFを開く

with pdfplumber.open(input_pdf_path) as pdf:
    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]  # pdfplumber でページを取得
        text = page.extract_text()  # ページのテキストを抽出

        # "問題" の位置を検索
        found = False
        for word in page.extract_words():
            if "問題" in word['text']:  # "問題" が含まれる単語を探す
                found = True
                x0, y0, x1, y1 = word['x0'], word['top'], word['x1'], word['bottom']  # 単語の座標

                # ハイライトを適用（PyMuPDF）
                annot = doc[page_num].add_rect_annot(fitz.Rect(x0, y0, x1, y1))
                annot.set_colors(stroke=(1, 1, 0), fill=(1, 1, 0))  # 黄色で塗りつぶし
                annot.set_opacity(0.5)  # 半透明
                annot.update()

        if found:
            print(f"ページ {page_num + 1} で '問題' をハイライトしました")

# ハイライト付きPDFを保存
doc.save(output_pdf_path)
doc.close()

print(f"ハイライト済みのPDFを保存しました: {output_pdf_path}")
