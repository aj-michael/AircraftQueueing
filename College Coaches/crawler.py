import psycopg2
import sys
import urllib
from lxml import html
import string

def addFootballCoachesByYear(cursor):
    query = "select * from football;"
    cursor.execute(query)
    for tuple in cursor.fetchall():
        name = tuple[0]
        url = "http://www.sports-reference.com/cfb/coaches/"+name.replace(" ","-").lower()+"-1.html"
        page = html.fromstring(urllib.urlopen(url).read())
        for row in page.xpath("//tbody/tr"):
            year = row[0][0].text
            school = row[1][0].text.replace("'","")
            games = row[2].text
            wins = row[3].text
            losses = row[4].text
            ties = row[5].text
            pct = row[6].text
            srs = "NULL" if row[7].text == None else row[7].text
            sos = "NULL" if row[8].text == None else row[8].text
            appre = "0" if row[9].text == None else row[9].text
            aphigh = "0" if row[10].text == None else row[10].text
            appost = "0" if row[11].text == None else row[11].text
            bowlName = "NULL" if len(row[12]) == 0 else "'"+row[12][0].text.replace("'","")+"'"
            bowlVictory = "NULL" if len(row[12]) == 0 else "'"+row[12][1].text+"'"
    
            query = "insert into footballbyyear values ('"+name+"',"+year+",'"+school+"',"+games+","+wins+','+losses+','+ties+','+pct+','+srs+','+sos+','+appre+','+aphigh+','+appost+','+bowlName+','+bowlVictory+");"
            print query
            cursor.execute(query)
            conn.commit()

def addBasketballCoachesByYear(cursor):
    query = "select * from basketball;"
    cursor.execute(query)
    for tuple in cursor.fetchall():
        name = tuple[0]
        url = "http://www.sports-reference.com/cbb/coaches/"+name.replace(" ","-").replace(".","").lower()+"-1.html"
        print url
        page = html.fromstring(urllib.urlopen(url).read())
        if "Coaches with Last" in page.find(".//title").text:
            continue
        for row in page.xpath("//tbody/tr"):
            year = row[0][0].text[:4]
            school = row[1][0].text.replace("'","")
            conf = row[2][0].text
            games = row[3].text
            wins = row[4].text
            losses = row[5].text
            pct = row[6].text
            srs = "NULL" if row[7].text == None else row[7].text
            sos = "NULL" if row[8].text == None else row[8].text
            appre = "0" if row[9].text == None else row[9].text
            aphigh = "0" if row[10].text == None else row[10].text
            apfinal = "0" if row[11].text == None else row[11].text
            query = "insert into basketballbyyear values ('"+name+"',"+year+",'"+school+"','"+conf+"',"+games+","+wins+","+losses+","+pct+","+srs+","+sos+","+appre+","+aphigh+","+apfinal+");"
            print query
            cursor.execute(query)
            conn.commit()
        
            
        

def addFootballCoaches(cursor):
    for c in string.ascii_lowercase:
        url = "http://www.sports-reference.com/cfb/coaches/"+c+"-index.html"
        page = html.fromstring(urllib.urlopen(url).read())
        previousName = None
        for link in page.xpath("//tr[./td]"):
            name = link[1][0].text.replace("'","")
            href = link[1][0].get("href")
            startYear = link[2].text
            endYear = link[3].text
            school = link[4][0].text.replace("'","")
            years = link[5].text
            games = link[6].text
            wins = link[7].text
            losses = link[8].text
            ties = link[9].text
            pct = link[10].text
            bowlGames = link[11].text
            bowlWins = link[12].text
            bowlLosses = link[13].text
            bowlTies = link[14].text

            query = "insert into football values ('"+name+"',"+startYear+','+endYear+",'"+school+"',"+years+','+games+','+wins+','+losses+','+ties+','+pct+','+bowlGames+','+bowlWins+','+bowlLosses+','+bowlTies+");"
            print query
            if name == previousName:
                continue
            else:
                cursor.execute(query)
                conn.commit()
                previousName = name
    return

def addBasketballCoaches(cursor):
    for c in string.ascii_lowercase:
        url = "http://www.sports-reference.com/cbb/coaches/"+c+"-index.html"
        page = html.fromstring(urllib.urlopen(url).read())
        previousName = None
        for link in page.xpath("//tr[./td]"):
            name = link[1][0].text.replace("'","")
            href = link[1][0].get("href")
            startYear = link[2].text
            endYear = link[3].text
            school = link[4][0].text.replace("'","")
            years = link[5].text
            games = link[6].text
            wins = link[7].text
            losses = link[8].text
            pct = link[9].text
            confchamps = link[10].text
            conftournchamps = link[11].text
            ncaaappearances = '0' if link[12].text == None else link[12].text
            final4appearances = '0' if link[13].text == None else link[13].text
            ncaatournchamps = '0' if link[14].text == None else link[14].text
            if name == previousName or games == '0':
                continue
            query = "insert into basketball values ('"+name+"',"+startYear+','+endYear+",'"+school+"',"+years+','+games+','+wins+','+losses+','+pct+','+confchamps+','+conftournchamps+','+ncaaappearances+','+final4appearances+','+ncaatournchamps+");"
            print query
            cursor.execute(query)
            conn.commit()
            previousName = name
    return

conn_string = "host='localhost' dbname='coaches' user='postgres' password='postgres'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
addBasketballCoachesByYear(cursor)
cursor.close()
conn.close()
