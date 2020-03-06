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
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'IB', 10)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

if __name__ == '__main__':
    dic = {}
    def json_txt(dic_json):
        if isinstance(dic_json, dict):
            for key in dic_json:
                if isinstance(dic_json[key], dict):
                    print("****key--：%s value--: %s" % (key, dic_json[key]))
                    json_txt(dic_json[key])
                    dic[key] = dic_json[key]
                else:
                    print("****key--：%s value--: %s" % (key, dic_json[key]))
                    dic[key] = dic_json[key]


    def dict_generator(indict, pre=None):
        pre = pre[:] if pre else []
        if isinstance(indict, dict):
            for key, value in indict.items():
                if isinstance(value, dict):
                    if len(value) == 0:
                        yield pre + [key, '{}']
                    else:
                        for d in dict_generator(value, pre + [key]):
                            yield d
                elif isinstance(value, list):
                    if len(value) == 0:
                        yield pre + [key, '[]']
                    else:
                        for v in value:
                            for d in dict_generator(v, pre + [key]):
                                yield d
                elif isinstance(value, tuple):
                    if len(value) == 0:
                        yield pre + [key, '()']
                    else:
                        for v in value:
                            for d in dict_generator(v, pre + [key]):
                                yield d
                else:
                    yield pre + [key, value]
        else:
            yield indict

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
    items = param_json.items()

    def getLastUpdated():
        meta = param_json['meta']
        value = meta['lastUpdated']
        return value

    def getID():
        return param_json['id']

    def getUse():
        family = param_json['family']
        return family

    def getName():
        name = param_json['name']
        name_list = []
        for data in name:
            use = data['use']
            family = data['family']
            given = data['given']
            given_name = given[0]
            prefiex = data['prefix']
            prefiex_name = prefiex[0]
            fullname = use+' name: '+prefiex_name+given_name+' '+family
            name_list.append(fullname)
        return name_list

    def getBirthDate():
        return param_json['birthDate']

    def getGender():
        return param_json['gender']

    def getContact():
        telecom = param_json['telecom']
        telecomList = []
        for index,data in enumerate(telecom):
            system = data['system']
            value = data['value']
            use = data['use']
            telecomList.append('('+str(index+1)+'): '+use+' '+system+": "+value)
        return telecomList

    def getAddress():
        addresses = param_json['address']
        lines = ''
        addressList = []
        for index, data in enumerate(addresses):
            for line in data['line']:
                lines = lines + line
            city = data['city']
            state = data['state']
            postcode = data['postalCode']
            country = data['country']
            address = '('+str(index+1)+'): '+lines+' '+city+' '+state+' '+postcode+' '+country
            addressList.append(address)
        return addressList

    def getCommunication():
        communication = param_json['communication']
        communicationList = []
        for index, data in enumerate(communication):
            language = data['language']
            text = language['text']
            communicationList.append('('+str(index+1)+'): '+text)
        return communicationList

    def getIdentifiers():
        # identifiers is a list which contains 0,1,2,3
        identifiers = param_json['identifier']
        result_list = []
        identifier_list = []
        for index,data in enumerate(identifiers):
            text = 'MISSING TEXT'
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

    getIdentifiers()


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
        # 空行，否则birthdate会对其
        pdf.cell(30,0,'',0,1,'L')
                        

        pdf.cell(30, 8, 'Birthdate:', 0, 0, 'L')
        pdf.cell(5)
        pdf.cell(30, 8, getBirthDate(), 0, 1, 'L')

        pdf.cell(30, 8, 'Gender:', 0, 0, 'L')
        pdf.cell(5)
        pdf.cell(30, 8, getGender(), 0, 1, 'L')

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
                        # pdf.cell(30,8,'****************************************************************************',0,2,'L')
                
        




        








    # json_txt(param_json) Print key = value
    # for i in dict_generator(param_json):
    #     txt = '.'.join(i[0:-1]), ':', i[-1]
    #     txt1 = '.'.join(i[0:-1])+' --->  '+str(i[-1])
    #     # 自动转行
    #     pdf.write(10,txt1)
    #     pdf.cell(10,10,'',0,1,'L')

    pageContent()
    print('File Generation complete!')
    pdf.output("sample.pdf",'F')