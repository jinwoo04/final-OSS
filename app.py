from flask import Flask, render_template, request, send_file, redirect,url_for
import os,re
from datetime import datetime
from zipfile import ZipFile
from mail_send import send_email
from zip_region import get_region_name
from oss_24 import mk_xlsx
from graph import graph_img

urls = [
    "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=5115061500",
    "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4182025000",
    "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4831034000",
    "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4729053000",
    "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=2920054000",
    "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=2772025000",
    "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=3023052000",
    "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=2644058000",
    "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=1168066000",
    "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=3611055000",
    "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=3114056000",
    "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=2871025000",
    "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4681025000",
    "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=5013025300",
    "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4425051000",
    "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4376031000"
]
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'text/html; charset=utf-8'
}

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
EXCEL_FOLDER = 'excel_files'

# 폴더가 존재하지 않으면 폴더를 생성한다.
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(EXCEL_FOLDER):
    os.makedirs(EXCEL_FOLDER)

# xlsx파일 존재시 전부 삭제
l = os.listdir(EXCEL_FOLDER)
if l:
    for i in l:
        os.remove(os.path.join(EXCEL_FOLDER,i))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather_list', methods=['GET','POST'])
def weather_list():
    #원하는 지역을 받아와서
    loc_list = request.form.getlist('loc')
    if loc_list:
        for loc in loc_list:
            #xlsx파일 생성
            mk_xlsx(urls[int(loc)])
        #만들어젠 xlsx파일 목록
        excel_files = [os.path.join(EXCEL_FOLDER, file)
                    for file in os.listdir(EXCEL_FOLDER)
                    if file.endswith('.xlsx')]
        #경로가 아닌 이름만
        file_names = [get_region_name(file) for file in excel_files]
        file_size = []
        #파일 사이즈
        for i in excel_files:
            file_size.append(os.path.getsize(i))
        return render_template('list.html', files=excel_files, file_names=file_names,file_size = file_size,l = len(file_names))
    else:
        return redirect(url_for('index'))

@app.route('/graph', methods=['GET','POST'])
def graph():
    img_data, names, r06 = graph_img()
    rr = []
    for r in r06:
        if r>=50:
            rr.append("결항")
        else:
            rr.append("출항")
    return render_template('graph.html',img_data=img_data,names = names,r06=rr)

@app.route('/download',methods=['GET','POST'])
def download():
    selected_files = request.form.getlist('files')
    if not selected_files:
        return "파일을 하나 이상 선택해 주세요."

    # ZIP 파일 이름 생성
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    
    # 선택된 파일들의 지역명 추출
    regions = [get_region_name(file) for file in selected_files]
    
    # 지역명 표시 준비
    if len(regions) == 1:
        region_display = regions[0]
    else:
        region_display = f"{regions[0]}_외_{len(regions) - 1}_건"
    
    # ZIP 파일 이름 생성
    zip_filename = f"{region_display}_날씨.zip"

    # ZIP 파일 생성
    zip_path = os.path.join(UPLOAD_FOLDER, zip_filename)
    with ZipFile(zip_path, 'w') as zipf:
        for file in selected_files:
            zipf.write(file, os.path.relpath(file, EXCEL_FOLDER))

    email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+')
    m = request.form.get('email')
    email = email_pattern.findall(m)
    if email:
        send_email(zip_path,email)
    return send_file(zip_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)

