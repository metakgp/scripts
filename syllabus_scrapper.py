import os
import requests
def get_syllabus(subject_code):
    url = 'https://erp.iitkgp.ernet.in/ERPWebServices/curricula/commonFileDownloader.jsp'
    data={}
    data['fileFullPath']='/DATA/ARCHIVE/SUBJECT/SYLLABUS/2009/{0}/{0}_1.pdf'.format(subject_code)
    data['pageno']='0'
    data['docId']=''
    response=requests.post(url,data)
    if(response.status_code !=200 or response.apparent_encoding=='ascii'): #when file is not available, we get html response
        print(response.status_code)
        print(response.text)
        return
    pdf_file_name = "{0}.pdf".format(subject_code)
    text_file_name= "{0}.txt".format(subject_code)
    with open(pdf_file_name,"wb") as handle:
        for data in response.iter_content():
            handle.write(data)
    os.system("pdftotext {0} {1}".format(pdf_file_name,text_file_name))
    with open(text_file_name, 'r') as content_file:
        content = content_file.read()
        return content
if __name__ == '__main__':
    print(get_syllabus('CS60063'))

