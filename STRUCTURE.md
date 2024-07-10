### 구조 설명

<hr/>

기상청 RSS를 활용한 파이썬 기반 알림 자동화 기구

<hr/>

<br/>

### 기능 설명

<hr/>
app.py
기능: 기상청 RSS 데이터를 크롤링하여 가장 가까운 시간의 날씨 정보를 가져옵니다.

excel_file_generator.py
기능: 크롤링한 날씨 데이터를 기반으로 엑셀 파일을 생성하고 서식에 맞게 배치합니다.

특징: 6시간 예상 강수량이 10mm를 넘을 경우 빨간색으로 표시합니다.

graph_generator.py - 특정 권역별로 기온과 강수량 그래프를 생성하는 코드.

zip_file_creator.py - 선택한 엑셀 파일을 ZIP 파일로 생성하는 코드로, 생성된 ZIP 파일을 자동으로 이메일로 전송함.

email_sender.py - ZIP 파일을 이메일로 전송하는 기능을 구현한 코드.

graph_generator.py - 특정 권역별로 기온과 강수량 그래프를 생성. 

zip_file_creator.py - 선택한 엑셀 파일을 ZIP 파일로 생성. 생성된 ZIP 파일을 자동으로 이메일로 전송.

email_sender.py - ZIP 파일을 이메일로 전송하는 기능을 구현한 코드.

<hr/>
