from selenium import webdriver
import selenium.webdriver.support.ui as UI
import itertools
import psycopg2
import time

conn_string = "host='localhost' dbname='coaches' user='postgres' password='postgres'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

baseUrl = "http://web1.ncaa.org/stats/StatsSrv/careersearch"
browser = webdriver.Firefox()
browser.implicitly_wait(10)
browser.get(baseUrl)


select = UI.Select(browser.find_element_by_name('searchSport'))
playercoach = browser.find_elements_by_name('playerCoach')[1]
select.select_by_value('MBA')
playercoach.click()

charset = map(chr, range(97,123))
for prefix in map("".join, itertools.product(charset, charset)):
    name = browser.find_element_by_name('lastName')
    button = browser.find_element_by_class_name('button')
    name.clear()
    name.send_keys(prefix)
    button.click()

    tbodies = browser.find_elements_by_tag_name('tbody')
    if len(tbodies) < 9:
        pages = 0
    elif len(tbodies) > 9:
        pages = len(tbodies[8].find_elements_by_tag_name('tr')) - 1
    else:
        pages = 1
    for page in range(pages):
        tbodies = browser.find_elements_by_tag_name('tbody')
        if page > 0:
            print "prefix " + prefix + " has " + str(pages) + " pages"
            print "currently on page " + str(page)
            tbodies = browser.find_elements_by_tag_name('tbody')
            selectionrows = tbodies[8].find_elements_by_tag_name('tr')
            print "selectionrows has length " + str(len(selectionrows))
            selectionrows[page+1].find_element_by_tag_name('a').click()
            time.sleep(1)
            tbodies = browser.find_elements_by_tag_name('tbody')
        tbody = tbodies[-1]
        for rowIndex in range(len(tbody.find_elements_by_tag_name('tr'))-1):
            tbody = browser.find_elements_by_tag_name('tbody')[8]
            tbody = browser.find_elements_by_tag_name('tbody')[-1]
            row = tbody.find_elements_by_tag_name('tr')[rowIndex+1]
            if row.get_attribute('bgcolor') != None:
                continue
            cols = row.find_elements_by_tag_name('td')
            link = cols[0].find_element_by_tag_name('a')

            link.click()
           
            tbodies = browser.find_elements_by_tag_name('tbody')
            namerow = tbodies[2].find_elements_by_tag_name('tr')[1]
            coachname = namerow.find_elements_by_tag_name('td')[1].text.replace("'","")
            careerrows = tbodies[3].find_elements_by_tag_name('tr')
            careerrow = careerrows[len(careerrows)-1].find_elements_by_tag_name('td')
            years = careerrow[1].text
            record = careerrow[2].text.split("-")
            if len(record) == 2:
                record = record + ['0']
            twins, tlosses, tties = record
            tgames = str(sum(map(int, record)))
            tpct = careerrow[3].text
            startyear = None ; endyear = None 
            for innerrow in tbodies[4].find_elements_by_tag_name('tr')[1:]:
                try:
                    cols = innerrow.find_elements_by_tag_name('td')
                    year = cols[0].text[:4]
                    if startyear == None:
                        startyear = year
                    school = cols[1].text.replace("'","")
                    record = cols[2].text.split("-")
                    if len(record) == 2:
                        record = record + ['0']
                    wins, losses, ties = record
                    games = str(sum(map(int, record)))
                    pct = cols[3].text
                    championship = "0"
                    query = "insert into baseballbyyear values ('"+coachname+"',"+year+",'"+school+"',"+games+","+wins+","+losses+","+ties+","+pct+","+championship+");"
                    #print query
                    cursor.execute(query)
                    conn.commit()
                except Exception:
                    print "Exception for " + coachname
            
            query = "insert into baseball values ('"+coachname+"',"+startyear+","+year+",'"+school+"',"+years+","+tgames+","+twins+","+tlosses+","+tties+","+tpct+");"
            print query
            cursor.execute(query)
            conn.commit()

            browser.back()

browser.close()
cursor.close()
conn.close()
