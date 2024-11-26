import pandas as pd
import json

def exams_data(CRD_NUMBER,JSONDATA,engine):
    data = JSONDATA

    source = data['hits']['hits'][0]['_source']

    content = json.loads(source['content'])
    for data in content['stateExamCategory']:
        info = {
            'crd':CRD_NUMBER,
            'examcategory':data['examCategory'],
            'examname':data['examName'],
            'examtakendate':data['examTakenDate'],
            'examdcope':data['examScope'],
            'exam_type': 'stateExamCategory',
        }
        status, response = Upload_exam_data(info,engine)
        print(response)
    
    for data in content['principalExamCategory']:
        info = {
            'crd':CRD_NUMBER,
            'examcategory':data['examCategory'],
            'examname':data['examName'],
            'examtakendate':data['examTakenDate'],
            'examscope':data['examScope'],
            'exam_type':'principalExamCategory',
        }
        status, response = Upload_exam_data(info,engine)
        print(response)
    
    for data in content['productExamCategory']:
        info = {
            'crd':CRD_NUMBER,
            'examcategory':data['examCategory'],
            'examname':data['examName'],
            'examtakendate':data['examTakenDate'],
            'examdcope':data['examScope'],
            'exam_type': 'productExamCategory',
        }
        status, response = Upload_exam_data(info,engine)
        print(response)
    return "sucess"
    
   
    

def Upload_exam_data(data,engine):
    exam_data = pd.DataFrame([data])
    try:
        exam_data.to_sql('exam_data', engine, if_exists='append', index=False)
        return True,"Data successfully written to the table 'Exam_data'."
    except Exception as e:
        return False,f"An error occurred: {e} "