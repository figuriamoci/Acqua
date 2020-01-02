import tabula
pdf_path = "https://github.com/chezou/tabula-py/raw/master/tests/resources/data.pdf"
tabula.read_pdf(pdf_path, stream=True)
