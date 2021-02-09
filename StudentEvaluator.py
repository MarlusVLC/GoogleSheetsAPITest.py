#!/usr/bin/env python
# coding: utf-8


#pylint:disable=E1101
from __future__ import print_function
import math
import os
from functools import reduce
import pickle
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account

working_directory = os.getcwd() #the credentials.json and keys.json archives should be in this file
print(os.getcwd())

def overallStudentsStatus(values):
    studentsStatusList = []

    overallScore = values
    
    for studentData in overallScore:   
        studentStatus = ""
        average = 0
        
        print("#Matricula: ", studentData[0])
        print(" Nome: ", studentData[1])
        
        numberOfAbsences = int(studentData[2])
        print("  Número de faltas: ", numberOfAbsences)
        absenceRate = round(numberOfAbsences/60,3)
        print("  Taxa de faltas/aula: ", absenceRate*100, "%")
        
        studentScore = studentData[3:]
        
        for grade in studentScore:
            print("  Nota P",studentScore.index(grade),": ", int(grade))
            average += int(grade)
        print("  Total: ", average)
        
        average /= len(studentScore)*10                          
        print("  Média: ", round(average,2))
                   
   
            
        if average < 5:
            studentStatus = "Reprovado por nota"
        elif average < 7:
            studentStatus = "Exame Final"
            #5 <= (m + naf)/2      #Less than or equal? An inequation?
            #(m + naf) >= 10   ->   naf >= 10-m
            lag = math.ceil(10 - average)
        else:
            studentStatus = "Aprovado"
            
            
        if (absenceRate > 0.25):
            studentStatus = "Reprovado por falta" 
        print("  Situação: ", studentStatus ) 
        
        
        lag = math.ceil(10 - average) if studentStatus == "Exame Final" else 0 #last aproval grade    
        print("  Nota para Aprovação Final: ", lag)
        
        print(" ")

        studentsStatusList.append([studentStatus,lag])
    
    return studentsStatusList

















SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '12ywLG_PisTSPrPmf_AmheaEnbQumGseZVx2DyXJgOZ8'


   

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="engenharia_de_software!A4:F27").execute()

values = result.get('values', [])

request = sheet.values().update(
    spreadsheetId=SAMPLE_SPREADSHEET_ID, range="engenharia_de_software!G4",
    valueInputOption="USER_ENTERED", body={"values": overallStudentsStatus(values)}).execute()

#print(values)





