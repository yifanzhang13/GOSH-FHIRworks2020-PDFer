from __future__ import print_function
from fpdf import FPDF
import sys
import json
import time
import re

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('fhir.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'IB', 12)
        # Move to the right
        self.cell(70)
        # Title
        self.cell(40, 8, 'Observation Report', 1, 0, 'C')
        # Current time of generated file
        self.cell(50)
        localtime = time.asctime(time.localtime(time.time()))
        currentTime = "Time: "+localtime
        self.cell(30,8,currentTime,0,2,'C')
        # Line break
        self.ln(10)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'IB', 10)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

if __name__ == '__main__':
    i = ""
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial','',10)

    time.sleep(2)

    print("Get the stdin data")
    l = sys.stdin.readlines()
    print(type(l))
    for k in l:
        i = i + k
    # string -> json dictionary
    param_json = json.loads(i)

    def getID():
        if 'id' in param_json:
            return param_json['id']
    
    def pageContent():
        pdf.cell(30, 8, 'Patient ID:', 0, 0, 'L')
        pdf.cell(5)
        pdf.cell(30, 8, getID(), 0, 1, 'L')
    
    pageContent()
    print('Observation File Generation complete!')
    pdf.output("observation.pdf",'F')