import requests
from bs4 import BeautifulSoup
import re
from lib.ConferenceSession import ConferenceSession
import xlsxwriter

# index and other one time vars
index_url = 'https://apta.expoplanner.com/index.cfm?do=expomap.sessResults&Agenda_type_display=Educational%20Sessions&search_type=sessiontype&event_id=29'
r = requests.get(index_url)
html_content = r.text
soup = BeautifulSoup(html_content, 'lxml')
links = soup.find_all('a')
list_of_sessions = []

# Getting all the links from main page
for raw_elem in links:
    if 'session_id' in raw_elem.get('href'):
        temp_title = raw_elem.text.lstrip()
        temp_url = 'https://apta.expoplanner.com/'+raw_elem.get('href')
        temp_session = ConferenceSession(temp_title,temp_url)
        list_of_sessions.append(temp_session)

# list_of_sessions = list_of_sessions[0:10]
# Count logic
temp_count = 0
max_len = len(list_of_sessions)

# Excel writing setup
workbook = xlsxwriter.Workbook('ptcsm.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})

worksheet.write('A1', 'Title', bold)
worksheet.write('B1', 'URL', bold)
worksheet.write('C1', 'Level', bold)
worksheet.write('D1', 'Date', bold)
worksheet.write('E1', 'Time', bold)
worksheet.write('F1', 'Description', bold)
for session in list_of_sessions:
    # Count logic
    print('Processing ', temp_count, ' of ', max_len, ' .......')


    # Temp connections and soup
    temp = session.session_url
    req_2 = requests.get(url=temp, headers={'Connection':'close'})
    html_content_2 = req_2.text
    temp_soup = BeautifulSoup(html_content_2, 'lxml')

    # Get text from the Session page
    for elem in temp_soup.find_all('b'):
        if 'Session Level' in elem.text:
            session.session_level = elem.next_sibling.lstrip()
        if 'Date' in elem.text:
            session.session_date = elem.next_sibling.lstrip()
        if 'Time' in elem.text:
            session.session_time = elem.next_sibling.lstrip()
        if 'Description' in elem.text:
            session.session_desc = elem.next_sibling.next_sibling.lstrip()

    # Write row in excel
    worksheet.write('A'+str(temp_count+2), session.session_title)
    worksheet.write('B'+str(temp_count+2), session.session_url)
    worksheet.write('C'+str(temp_count+2), session.session_level)
    worksheet.write('D'+str(temp_count+2), session.session_date)
    worksheet.write('E'+str(temp_count+2), session.session_time)
    worksheet.write('F'+str(temp_count+2), session.session_desc)

    temp_count += 1

# for full_session in list_of_sessions:
#     print(full_session)
print('Done.')
workbook.close()
