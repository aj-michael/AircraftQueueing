from selenium import webdriver
import psycopg2

conn_string = "host='localhost' dbname='coaches' user='postgres' password='postgres'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

baseUrl = "http://en.wikipedia.org/wiki/College_World_Series"
browser = webdriver.Firefox()
browser.implicitly_wait(10)
browser.get(baseUrl)

tbody = browser.find_element_by_tag_name('tbody')
rows = tbody.find_elements_by_tag_name('tr')
for row in rows:
    cols = row.find_elements_by_tag_name('td')
    year = cols[0].text
    winner = cols[2].text
    runnerup = cols[4].text
    print year
    year = str(int(year)-1) 
    
    query = "select name from baseballbyyear where year="+year+" and school='"+runnerup+"';"
    cursor.execute(query)
    loser = cursor.fetchone()
    if loser != None:
        loser = loser[0]
    print year + "Championship"
    print "Winner: " + winner
    if loser == None:
        print "Could not find loser in database"
    else:
        print "Loser: " + loser
    #query = "update baseballbyyear set cwin=1 where year="+year+" and name='"+winner+"';"
    query = "update baseball set cwins=cwins+1, capps=capps+1 where name='"+winner+"';"
    print query
    cursor.execute(query)
    conn.commit()

    if loser != None:
        #query = "update baseballbyyear set closs=1 where year="+year+" and name='"+loser+"';"
        query = "update baseball set closses=closses+1, capps=capps+1 where name='"+loser+"';"
        print query
        cursor.execute(query)
        conn.commit()

browser.close()
cursor.close()
conn.close()
