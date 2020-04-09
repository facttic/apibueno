from io import StringIO
import re

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


output_string = StringIO()
with open('samplesCovid/06-04-20-reporte-matutino-covid-19.pdf', 'rb') as in_file:
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)

documento =output_string.getvalue()

class DatoSalida:
    nombre = ""
    confirmados = 0
    acumulados = 0

    def __repr__(self):
        return 'Provincia: ' + self.nombre + "Confirmados: " + str(self.confirmados) + " Acumulados: " + str(self.acumulados)

out = ["completo", "Nombre", "Confirmados", "Acumulados", "Dead", "Recovered"]

for line in documento.splitlines():

    if re.findall('^-.*', line):
        # soloProvincias += line + '\r'
        a_list = line.split()
        # print(a_list)
        dato = DatoSalida()
        for parte in a_list:
            if parte.isalpha():
                dato.nombre += parte + ' '
            if dato.nombre and not dato.confirmados and parte.isnumeric():
                dato.confirmados = parte
            if dato.nombre and dato.confirmados and parte.isnumeric():
                dato.acumulados = parte
        print(dato)
