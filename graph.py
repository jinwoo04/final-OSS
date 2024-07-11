from io import BytesIO, StringIO
import base64
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from zip_region import get_region_name
import numpy as np
import pandas as pd

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

def graph_img():
    PATH = "excel_files"
    cel_list = os.listdir(PATH)
    file_names = [get_region_name(file) for file in cel_list]
    temp = []
    reh = []
    pop = []
    r06 = []
    for cel in cel_list:
        book = load_workbook(os.path.join(PATH,cel), data_only=True)
        sheet = book.active
        a = float(sheet['B2'].value[:4])
        temp.append(a)
        b = int(sheet['B3'].value.split("%")[0])
        reh.append(b)
        c = int(sheet['B4'].value.split("%")[0])
        pop.append(c)
        d = float(sheet['c6'].value.split("mm")[0])
        r06.append(d)
    names = []
    for file in file_names:
        if file == "경상남도날씨":
            names.append('경남')
        elif file == "경상북도날씨":
            names.append('경북')
        elif file == "충청남도날씨":
            names.append('충남')
        elif file == "충청북도날씨":
            names.append('충북')
        else:
            names.append(file[:2]) 
    science = {
        "names" : names,
        "temp" : temp,
        "reh" : reh,
        "pop" : pop,
        "r06" : r06
    }
    w = 0.1
    sci = pd.DataFrame(science)
    nrow = sci.shape[0] # 행의 갯수
    idx = np.arange(nrow) #행의 갯수를 리스트로
    plt.figure(figsize = (10, 5))
    plt.bar(idx - w, sci['temp'],width=w,color='red',label="온도")
    plt.bar(idx + w, sci['r06'],width=w,color='b',label="강수량")
    plt.xlabel("지역",size = 13)
    plt.title("지역별 그래프")
    plt.xticks(np.arange(len(names)),names)
    plt.legend()
    plt.show()
    
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    img_str = base64.b64encode(img.read()).decode('utf-8')
    return img_str , names, r06
