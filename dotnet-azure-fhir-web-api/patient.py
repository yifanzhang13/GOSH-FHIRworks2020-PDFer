from __future__ import print_function
from fpdf import FPDF
import sys
import json
import time

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('fhir.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'IB', 12)
        # Move to the right
        self.cell(70)
        # Title
        self.cell(30, 8, 'Patient Report', 1, 0, 'C')
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
    print(len(l))

    for k in l:
        i = i + k
    # string -> json dictionary
    param_json = json.loads(i)

    def getLastUpdated():
        meta = param_json['meta']
        value = ''
        if 'lastUpdated' in meta:
            value = meta['lastUpdated']
        return value

    def getID():
        if 'id' in param_json:
            return param_json['id']
    
    def getMultiBirth():
        if 'multipleBirthBoolean' in param_json:
            return param_json['multipleBirthBoolean']

    def getUse():
        family = ''
        if 'family' in param_json:
            family = param_json['family']
        return family

    def getName():
        name = param_json['name']
        name_list = []
        prefiex_name = ''
        family = ''
        given_name = ''
        for data in name:
            if 'prefix' in data:
                prefiex = data['prefix']
                prefiex_name = prefiex[0]
            if 'use' in data:
                use = data['use']
            if 'family' in data:
                family = data['family']
            if 'given' in data:
                given = data['given']
                given_name = given[0]
            fullname = use+' name: '+prefiex_name+given_name+' '+family
            name_list.append(fullname)
        return name_list

    def getBirthDate():
        value = ''
        if 'birthDate' in param_json:
            value = param_json['birthDate']
        return value

    def getGender():
        value = ''
        if 'gender' in param_json:
            value = param_json['gender']
        return value

    def getMarital():
        if 'maritalStatus' in param_json:
            status = param_json['maritalStatus']
            text = ''
            if 'text' in status:
                text = status['text']
                if text == 'M':
                    return 'Married'
                elif text == 'S':
                    return 'Single'
                elif text == "Never Married":
                    return "Never Married"
                else:
                    return text
            else:
                return text
        else:
            return ''

    def getContact():
        telecom = param_json['telecom']
        telecomList = []
        system = ''
        value = ''
        use = ''
        for index,data in enumerate(telecom):
            if 'system' in data:
                system = data['system']
            if 'value' in data:
                value = data['value']
            if 'use' in data:
                use = data['use']
            telecomList.append('('+str(index+1)+'): '+use+' '+system+": "+value)
        return telecomList

    def getAddress():
        addresses = param_json['address']
        lines = ''
        addressList = []
        city = ''
        state = ''
        postcode = ''
        country = ''
        for index, data in enumerate(addresses):
            for line in data['line']:
                lines = lines + line
            if 'city' in data:
                city = data['city']
            if 'state' in data:
                state = data['state']
            if 'postalCode' in data:
                postcode = data['postalCode']
            if 'country' in data:
                country = data['country']
            address = '('+str(index+1)+'): '+lines+' / '+city+' / '+state+' / '+postcode+' / '+country
            addressList.append(address)
        return addressList

    def getCommunication():
        communication = param_json['communication']
        communicationList = []
        language = ''
        text = ''
        for index, data in enumerate(communication):
            if 'language' in data:
                language = data['language']
            if 'text' in language:
                text = language['text']
            communicationList.append('('+str(index+1)+'): '+text)
        return communicationList

    def getIdentifiers():
        # identifiers is a list which contains 0,1,2,3
        identifiers = param_json['identifier']
        result_list = []
        identifier_list = []
        for index,data in enumerate(identifiers):
            text = 'MISSING_TEXT'
            if 'type' in data:
                typee = data['type']
                text = typee['text']
            system = data['system']
            value = data['value']
            result0 = text
            result1 = 'system = '+system
            result2 = ' value = '+value
            result_list.append(result0)
            result_list.append(result1)
            result_list.append(result2)
            identifier_list.append(result_list)
        return identifier_list

    def getExtensions():
        # extensions is a list stores 0,1...6
        extensions = param_json['extension']
        result_list = []
        # extension is 0,1..6
        for index, extension in enumerate(extensions):
            result = []
            if 'url' in extension:
                url = extension['url']
                result.append('url = '+url)
            if 'valueString' in extension:
                valueString = extension['valueString']
                result.append('valueString = '+valueString)
            if 'valueCode' in extension:
                valueCode = extension['valueCode']
                result.append('valueCode = '+valueCode)
            if 'valueDecimal' in extension:
                valueDecimal = extension['valueDecimal']
                result.append('valueDecimal = '+str(valueDecimal))
            if 'extension' in extension:
                dictt = extension['extension']
                for index,d in enumerate(dictt):
                    url = d['url']
                    result.append('['+str(index+1)+']: ')
                    result.append('url = '+url)
                    if 'valueCoding' in d:
                        dd = d['valueCoding']
                        system = dd['system']
                        code = dd['code']
                        display = dd['display']
                        result.append('system = '+system)
                        result.append('code = '+code)
                        result.append('display = '+display)
                    if 'valueString' in d:
                        valueString = d['valueString']
                        result.append('valueString = '+valueString)
            result_list.append(result)
        return result_list

    def pageContent():
        pdf.cell(30,8,'Last Updated at:',0,0,'L')
        pdf.cell(5)
        pdf.cell(30, 8, getLastUpdated(), 0, 1, 'L')

        pdf.cell(30, 8, 'Patient ID:', 0, 0, 'L')
        pdf.cell(5)
        pdf.cell(30, 8, getID(), 0, 1, 'L')

        pdf.cell(30, 8, 'Patient Name:', 0, 0, 'L')
        pdf.cell(5)
        name_list = getName()
        for index,data in enumerate(name_list):
                x = '('+str(index+1)+'): ' + data
                pdf.cell(30,8,x,0,2,'')
        # blank cell
        pdf.cell(30,0,'',0,1,'L')
                        
        pdf.cell(30, 8, 'Birthdate:', 0, 0, 'L')
        pdf.cell(5)
        pdf.cell(30, 8, getBirthDate(), 0, 1, 'L')

        pdf.cell(30, 8, 'Multiple Birth:', 0, 0, 'L')
        pdf.cell(5)
        pdf.cell(30, 8, str(getMultiBirth()), 0, 1, 'L')

        pdf.cell(30, 8, 'Gender:', 0, 0, 'L')
        pdf.cell(5)
        pdf.cell(30, 8, getGender(), 0, 1, 'L')

        pdf.cell(30, 8, 'Marital Status:', 0, 0, 'L')
        pdf.cell(5)
        pdf.cell(30, 8, getMarital(), 0, 1, 'L')

        pdf.cell(30, 8, 'Contact:', 0, 0, 'L')
        pdf.cell(5)
        telecomList = getContact()
        for telecom in telecomList:
            pdf.cell(30,8,telecom,0,1,'L')

        pdf.cell(30, 8, 'Address:', 0, 0, 'L')
        pdf.cell(5)
        addressList = getAddress()
        for address in addressList:
            pdf.cell(30,8,address,0,1,'L')

        pdf.cell(30, 8, 'Language:', 0, 0, 'L')
        pdf.cell(5)
        communicationList = getCommunication()
        for language in communicationList:
            pdf.cell(30, 8, language, 0, 1, 'L')

        pdf.cell(30,8,'Identifier',0,0,'L')
        pdf.cell(5)
        identifier_list = getIdentifiers()
        for index,data in enumerate(identifier_list):
                x = '('+str(index+1)+'): '
                pdf.cell(30,8,x,0,2,'L')
                for result in data:
                    pdf.cell(30,8,result,0,2,'L')
                    if ' value = ' in result:
                        pdf.cell(30,8,'-------------------------------------------------------------------',0,2,'L')
        pdf.cell(30,0,'',0,1,'L')
        
        pdf.cell(30, 8, 'Extension:', 0, 0, 'L')
        pdf.cell(5)
        list1 = getExtensions()
        for index,l in enumerate(list1):
            x = '('+str(index+1)+'): '
            pdf.cell(30,8,x,0,2,'L')
            for ll in l:
                pdf.cell(30,8,ll,0,2,'L')
            pdf.cell(30,8,'-------------------------------------------------------------------',0,2,'L')

    pageContent()
    print('Patient File Generation complete!')
    pdf.output("sample.pdf",'F')