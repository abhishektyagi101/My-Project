#!/usr/bin/env python
# coding: utf-8
# In[68]:
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

from zipfile import ZipFile
import os
import shutil
import json
import time
import pprint
import re
import boto3
from boltons.iterutils import remap
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
i=0
new_list_file=[]
true=1
false=0


#Download Jason file from PED
try:
    driver = webdriver.Chrome()
    driver.get("https://ped.uspto.gov/peds/#/search")
    time.sleep(20)
    driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div[5]/div[1]/div[3]/div/a[1]').click()
    time.sleep(100)
    print('download_started********')
except:
    print('file_not_downloaded')


#Get current year
now = datetime.datetime.now()
current_year=(now.year)
required_year=now.year-10
print('current_year',current_year)
print('required_year',required_year)


#identify download zip file
with os.scandir(r'C:\Users\Administrator\Downloads') as x:
    for entry in x:
        y=re.findall('.*delta.*',entry.name)
        if y:
            path1=entry.path
        else:
            pass
    print('zip path>>>',path1)


        

#filename = r'D:\Python\Json\2018.json'

with ZipFile(path1,'r') as zip_ref:
    zip_ref.extractall(r'C:\Users\Administrator\Downloads\target')
path=r'C:\Users\Administrator\Downloads\target'

print('unzipping completed')

a=[]
with os.scandir(path) as entries:
    for entry in entries:
        #print(entry.path)
        a.append(entry.path)
        
print(a)
for each_entry in a:
    #print(each_entry)
    z=re.findall('.+\\\(.+?)\.',each_entry)
    print('*************************',z)
    print(type(z))
    if required_year>=int(z[0]):
        pass
    else:
        print(each_entry)
        with open(each_entry,encoding="utf8") as json_file:
            #data = json.load(json_file)
            #pprint.pprint(data)

            for line in json_file:
                #print (i)
                #print (len(line))
                #print ("\n")
                if len(line) > 3:
                    i=i+1
                    #time.sleep(1)
                    line=line.replace('{ "PatentBulkData" : [ ','')
                    line=line.replace(',{"patentCaseMetadata":','{"patentCaseMetadata":')
                    #line=line.replace('\"\"','')
                    dic=eval(line)
                    #print(type(dic))
                    #data = json.load(line)
                    try:
                        app_number=''
                        app_number=(dic['patentCaseMetadata']['applicationNumberText']['value'])
                        #print ('app_number:',app_number)
                    except KeyError:
                        pass
                    try:
                        filing_date=''
                        filing_date=(dic['patentCaseMetadata']['filingDate'])
                        #print ('filing_date:',filing_date)
                    except KeyError:
                        pass
                    try:
                        art_unit=''
                        art_unit=(dic['patentCaseMetadata']['groupArtUnitNumber']['value'])
                        #print('art_unit:',art_unit)
                    except KeyError:
                        pass
                    try:
                        confirmation_number=''
                        confirmation_number=(dic['patentCaseMetadata']['applicationConfirmationNumber'])
                        #print('confirmation_number:',confirmation_number)
                    except KeyError:
                        pass
                    try:
                        status=''
                        status=(dic['patentCaseMetadata']['applicationStatusCategory'])
                        #print('status:',status)
                    except KeyError:
                        pass
                    try:
                        docket=''
                        docket=(dic['patentCaseMetadata']['applicantFileReference'])
                        #print('docket:',docket)
                    except KeyError:
                        pass
                    try:
                        entity=''
                        entity=(dic['patentCaseMetadata']['businessEntityStatusCategory'])
                        #print('entity:',entity)
                    except KeyError:
                        pass
                    try:
                        title=''
                        title=(dic['patentCaseMetadata']['inventionTitle']['content'][0])
                        #print('title:',title)
                    except KeyError:
                        pass
                    try:
                        pub_number=''
                        pub_number=(dic['patentCaseMetadata']['patentPublicationIdentification']['publicationNumber'])
                        #print('pub_number:',pub_number)
                    except KeyError:
                        pass
                    try:
                        pub_date=''
                        pub_date=(dic['patentCaseMetadata']['patentPublicationIdentification']['publicationDate'])
                        #print('pub_date:',pub_date)
                    except KeyError:
                        pass
                    try:
                        patent_number=''
                        patent_number=(dic['patentCaseMetadata']['patentGrantIdentification']['patentNumber'])
                        #print('patent_number:',patent_number)
                    except KeyError:
                        pass
                    try:
                        issue_date=''
                        issue_date=(dic['patentCaseMetadata']['patentGrantIdentification']['grantDate'])
                        #print('issue_date:',issue_date)
                    except KeyError:
                        pass
                    try:
                        relatedDocumentData=''
                        relatedDocumentData=(dic['patentCaseMetadata']['relatedDocumentData'])
                        #print('relatedDocumentData:',relatedDocumentData)
                    except KeyError:
                        pass
                    try:
                        prosecution=''
                        prosecution=(dic['prosecutionHistoryDataBag']['prosecutionHistoryData'])
                        #print('prosecution:',prosecution)
                    except KeyError:
                        pass
                    try:
                        party=''
                        examiner=''
                        applicant=''
                        inventor=''
                        attorney=''
                        party=(dic['patentCaseMetadata']['partyBag']['applicantBagOrInventorBagOrOwnerBag'])
                        #pprint.pprint(party)
                        #print (party[4])
                        for element in party:
                            a=element.keys()
                            a=str(a)
                            #print(type(a))
                            #print(a)
                            if a == "dict_keys(['primaryExaminerOrAssistantExaminerOrAuthorizedOfficer'])":
                                examiner=element
                                #print (examiner)
                                #print('---********----')
                            if a == "dict_keys(['inventorOrDeceasedInventor'])":
                                inventor=element
                                #print (inventor)
                                #print('---********----')
                            if a == "dict_keys(['applicant'])":
                                applicant=element
                                #print (applicant)
                                #print('---********----')
                            if a == "dict_keys(['partyIdentifierOrContact'])":
                                attorney=element
                                #print (attorney)
                                #print('---********----')   
                    except KeyError:
                        pass
                    new_file={}
                    new_file['app_number']=app_number
                    #print(len(app_number))
                    #print(len(patent_number))
                    new_file['filing_date']=filing_date
                    new_file['art_unit']=art_unit
                    new_file['confirmation_number']=confirmation_number
                    new_file['status']=status
                    new_file['docket']=docket
                    new_file['entity']=entity
                    new_file['title']=title
                    new_file['pub_number']=pub_number
                    #print('------',pub_number)
                    #print('length--',len(pub_number))
                    if len(pub_number)>0:
                        pub_number=pub_number.strip()
                        pub_number=pub_number.replace('\n','')
                        d=pub_number[0].isdigit()
                        e=pub_number[1].isdigit()
                        two = pub_number[:2]
                        if d==True and e==True:
                            JS=''
                        elif two=='RE':
                            JS=''
                        elif d==False and e==False and two!='RE':
                            JS=two
                            pub_number=pub_number.replace(two,'')
                        else:
                            JS=''
                        if pub_number[-1].isalpha():
                            kindcode=pub_number[-1]
                            pub_num=pub_number.replace(kindcode,'')
                            new_file['pub_jurisdiction']=JS
                            new_file['pub_number_mod']=pub_num
                            new_file['pub_kindcode']=kindcode

                        elif pub_number[-2].isalpha():
                            kindcode=pub_number[(len(pub_number)-2):len(pub_number)]
                            pub_num=pub_number.replace(kindcode,'')
                            new_file['pub_jurisdiction']=JS
                            new_file['pub_number_mod']=pub_num
                            new_file['pub_kindcode']=kindcode

                        else:   
                            kindcode=''
                            pub_num=pub_number.replace(kindcode,'')
                            new_file['pub_jurisdiction']=JS
                            new_file['pub_number_mod']=pub_num
                            new_file['pub_kindcode']=kindcode
                    else:
                        JS=''
                        pub_num=''
                        kindcode=''
                        new_file['pub_jurisdiction']=JS
                        new_file['pub_number_mod']=pub_num
                        new_file['pub_kindcode']=kindcode
                
                    new_file['pub_date']=pub_date
                    new_file['patent_number']=patent_number
                    if len(patent_number)>0:
                
                        patent_number=patent_number.strip()
                        patent_number=patent_number.replace('\n','')
                        d=patent_number[0].isdigit()
                        e=patent_number[1].isdigit()
                        two = patent_number[:2]
                        if d==True and e==True:
                            JS=''
                        elif two=='RE':
                            JS=''
                        elif d==False and e==False and two!='RE':
                            JS=two
                            patent_number=patent_number.replace(two,'')
                        else:
                            JS=''
                        if patent_number[-1].isalpha():
                            kindcode=patent_number[-1]
                            patent_number=patent_number.replace(kindcode,'')
                            new_file['patent_jurisdiction']=JS
                            new_file['patent_number_mod']=patent_number
                            new_file['patent_kindcode']=kindcode

                        elif patent_number[-2].isalpha():
                            kindcode=patent_number[(len(patent_number)-2):len(patent_number)]
                            patent_number=patent_number.replace(kindcode,'')
                            new_file['patent_jurisdiction']=JS
                            new_file['patent_number_mod']=patent_number
                            new_file['patent_kindcode']=kindcode
                        else:   
                            kindcode=''
                            patent_number=patent_number.replace(kindcode,'')
                            new_file['patent_jurisdiction']=JS
                            new_file['patent_number_mod']=patent_number
                            new_file['patent_kindcode']=kindcode
                    else:
                        JS=''
                        pub_num=''
                        kindcode=''
                        new_file['patent_jurisdiction']=JS
                        new_file['patent_number_mod']=patent_number
                        new_file['patent_kindcode']=kindcode
            
                
                    new_file['issue_date']=issue_date
                    new_file['examiner']=examiner
                    new_file['inventor']=inventor
                    new_file['applicant']=applicant
                    new_file['attorney']=attorney
                    #print('--now print-dictionary------')
                    #print(new_file)
                    drop_falsey = lambda path, key, value: bool(value)
                    new_file = remap(new_file, visit=drop_falsey)
                    #print(clean)
                    #new_list_file.append(new_file)
                    table = dynamodb.Table('USPTO_APP_DATA')
                    table.put_item(Item=new_file)


    
        #with open(z[0]+'_processed.json', 'w') as outfile:
            #json.dump(new_list_file, outfile,indent=2)
print('deleting zip and unzipped files')
os.remove(path1)
shutil.rmtree(path, ignore_errors=True)
        
            


# In[ ]:




