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
        self.set_font('Arial', 'IB', 16)
        # Set the color of text 
        self.set_text_color(65, 105, 225)
        # Move to the right
        self.cell(70)
        # Title
        self.cell(30, 8, 'Observation Report', 0, 0, 'C')
        # Current time of generated file
        self.cell(50)
        localtime = time.asctime(time.localtime(time.time()))
        currentTime = localtime
        self.cell(30,8,currentTime,0,2,'C')
        # Line break
        self.ln(10)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'IB', 8)
        # Text color in gray
        self.set_text_color(65, 105, 225)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

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
    
    def getDateTime():
        if 'effectiveDateTime' in param_json:
            return param_json['effectiveDateTime']
        else:
            return ''

    def getIssued():
        if 'issued' in param_json:
            return param_json['issued']
        else:
            return ''

    def getCode():
        if 'code' in param_json:
            code = param_json['code']
            if 'text' in code:
                return code['text']
            else:
                return ''
        else:
            return ''
    
    def getValue():
        result = ''
        value = ''
        unit = ''
        if 'valueQuantity' in param_json:
            quantity = param_json['valueQuantity']
            if 'value' in quantity:
                value = quantity['value']
            if 'unit' in quantity:
                unit = quantity['unit']
            result = str(value) + ' ' + unit
            return result
        else:
            return result
    
    def getUpdate():
        if 'meta' in param_json:
            meta = param_json['meta']
            if 'lastUpdated' in meta:
                return meta['lastUpdated']
            else:
                return ''
        else:
            return ''
    
    def getVersion():
        if 'meta' in param_json:
            meta = param_json['meta']
            if 'versionId' in meta:
                return str(meta['versionId'])
            else:
                return ''
        else:
            return ''
        
    def getReference():
        if 'subject' in param_json:
            subject = param_json['subject']
            if 'reference' in subject:
                return subject['reference']
            else:
                return ''
        else:
            return ''
    
    def drawObservation():
        pdf.set_font('Arial','B',10)
        pdf.set_text_color(65, 105, 225)
        pdf.cell(30,8,getCode()+': '+getValue(),0,0,'L')
    
    def setDefault():
        pdf.set_font('Arial','',10)
        pdf.set_text_color(0,0,0)
    
    def pageContent():
        pdf.set_font('Arial','B',10)
        pdf.cell(30, 8, 'Last updated:', 0, 0, 'L')
        setDefault()
        pdf.cell(5)
        pdf.cell(30, 8, getUpdate(), 0, 1, 'L')

        pdf.set_font('Arial','B',10)
        pdf.cell(30, 8, 'Report version:', 0, 0, 'L')
        setDefault()
        pdf.cell(5)
        pdf.cell(30, 8, getVersion(), 0, 1, 'L')

        pdf.set_font('Arial','B',10)
        pdf.cell(30, 8, 'Observation ID:', 0, 0, 'L')
        setDefault()
        pdf.cell(5)
        pdf.cell(30, 8, getID(), 0, 1, 'L')

        pdf.set_font('Arial','B',10)
        pdf.cell(30, 8, 'Reference ID:', 0, 0, 'L')
        setDefault()
        pdf.cell(5)
        pdf.cell(30, 8, getReference(), 0, 1, 'L')

        pdf.set_font('Arial','B',10)
        pdf.cell(30, 8, 'Date Time:', 0, 0, 'L')
        setDefault()
        pdf.cell(5)
        pdf.cell(30, 8, getDateTime(), 0, 1, 'L')

        pdf.set_font('Arial','B',10)
        pdf.cell(30, 8, 'Issued Time:', 0, 0, 'L')
        setDefault()
        pdf.cell(5)
        pdf.cell(30, 8, getIssued(), 0, 1, 'L')

        drawObservation()
        setDefault()
        pdf.cell(50)
    
    pageContent()
    print('Observation File Generation complete!')
    pdf.output("observation.pdf",'F')