import numpy
import csv
import psycopg2
import sys


RESULTS = 25

def compareBaseballExtrapolate(stats,yearData,i,j):
    #name,startyear,endyear,lastschool,years,games,wins,losses,pct,confchamps,conftournchamps,ncaaapp,final4,ncaachamp=stats
    name,startyear,endyear,lastschool,years,games,wins,losses,ties,pct,cwins,closses,capps=stats
    iRows = yearData[name[i]]
    jRows = yearData[name[j]]
    iGames = [row[3] for row in iRows]
    jGames = [row[3] for row in jRows]
    iWins = [row[4] for row in iRows]    
    jWins = [row[4] for row in jRows]

    if years[i] > years[j]:
        indices = numpy.arange(len(jRows))
        A = numpy.array([indices,numpy.ones(len(jRows))])
        w = numpy.linalg.lstsq(A.T, jWins)[0]
        diff = 0
        for x in range(years[i]):
            if x >= len(iWins):
                continue
            diff = diff + iWins[x]
            if x >= years[j]:
                extrapolatedWins = x*w[0]+w[1]
                diff = diff - extrapolatedWins
            else:
                if x < len(jWins):
                    diff = diff - jWins[x]
        result = 1.0 if diff > 0 else 0.0
    elif years[i] < years[j]:
        indices = numpy.arange(len(iRows))
        A = numpy.array([indices,numpy.ones(len(iRows))])
        w = numpy.linalg.lstsq(A.T, iWins)[0]
        diff = 0
        for x in range(years[j]):
            if x >= years[i]:
                extrapolatedWins = x*w[0]+w[1]
                diff = diff + extrapolatedWins
            else:
                if x >= len(iWins):
                    continue
                diff = diff + iWins[x]
            if x >= len(jWins):
                continue
            diff = diff - jWins[x]
        result = 1.0 if diff > 0 else 0.0
    else:
        result = 1.0 if sum(iWins) / float(len(iWins)) > sum(jWins) / float(len(jWins)) else 0.0
    return result

def compareBasketballExtrapolate(stats,yearData,i,j):
    name,startyear,endyear,lastschool,years,games,wins,losses,pct,confchamps,conftournchamps,ncaaapp,final4,ncaachamp=stats
    iRows = yearData[name[i]]
    jRows = yearData[name[j]]

    iGames = [row[4] for row in iRows]
    jGames = [row[4] for row in jRows]
    iWins = [row[5] for row in iRows]    
    jWins = [row[5] for row in jRows]

    if years[i] > years[j]:
        indices = numpy.arange(len(jRows))
        A = numpy.array([indices,numpy.ones(len(jRows))])
        w = numpy.linalg.lstsq(A.T, jWins)[0]
        diff = 0
        for x in range(years[i]):
            diff = diff + iWins[x]
            if x >= years[j]:
                extrapolatedWins = x*w[0]+w[1]
                diff = diff - extrapolatedWins
            else:
                diff = diff - jWins[x]
        result = 1.0 if diff > 0 else 0.0
    elif years[i] < years[j]:
        indices = numpy.arange(len(iRows))
        A = numpy.array([indices,numpy.ones(len(iRows))])
        w = numpy.linalg.lstsq(A.T, iWins)[0]
        diff = 0
        for x in range(years[j]):
            if x >= years[i]:
                extrapolatedWins = x*w[0]+w[1]
                diff = diff + extrapolatedWins
            else:
                diff = diff + iWins[x]
            diff = diff - jWins[x]
        result = 1.0 if diff > 0 else 0.0
    else:
        result = 1.0 if sum(iWins) / float(len(iWins)) > sum(jWins) / float(len(jWins)) else 0.0
    return result

def compareFootballExtrapolate(stats,yearData,i,j):
    name,start,end,school,years,games,wins,losses,ties,pct,bowls,bowlwins,bowllosses,bowlties=stats
    iRows = yearData[name[i]]
    jRows = yearData[name[j]]

    iGames = [row[3] for row in iRows]
    jGames = [row[3] for row in jRows]
    iWins = [row[4] for row in iRows]    
    jWins = [row[4] for row in jRows]
    iSrs = [row[8] for row in iRows]
    jSrs = [row[8] for row in jRows]
    iBowls = [0 if row[13] == None else 1 for row in iRows]
    jBowls = [0 if row[13] == None else 1 for row in jRows]

    if years[i] > years[j]:
        indices = numpy.arange(len(jRows))
        A = numpy.array([indices,numpy.ones(len(jRows))])
        w = numpy.linalg.lstsq(A.T, jWins)[0]
        diff = 0
        for x in range(years[i]):
            diff = diff + iWins[x]
            if x >= years[j]:
                extrapolatedWins = x*w[0]+w[1]
                diff = diff - extrapolatedWins
            else:
                diff = diff - jWins[x]
        result = 1.0 if diff > 0 else 0.0
    elif years[i] < years[j]:
        indices = numpy.arange(len(iRows))
        A = numpy.array([indices,numpy.ones(len(iRows))])
        w = numpy.linalg.lstsq(A.T, iWins)[0]
        diff = 0
        for x in range(years[j]):
            if x >= years[i]:
                extrapolatedWins = x*w[0]+w[1]
                diff = diff + extrapolatedWins
            else:
                diff = diff + iWins[x]
            diff = diff - jWins[x]
        result = 1.0 if diff > 0 else 0.0
    else:
        result = 1.0 if sum(iWins) / float(len(iWins)) > sum(jWins) / float(len(jWins)) else 0.0
    return result
   

def compareFootballPress(stats,yearData,i,j):
    name,start,end,school,years,games,wins,losses,ties,pct,bowls,bowlwins,bowllosses,bowlties,srs,sos=stats
    iRows = yearData[name[i]]
    jRows = yearData[name[j]]
   
    iPres   = [row[10] if row[10] > 0 else 1000 for row in iRows]
    jPres   = [row[10] if row[10] > 0 else 1000 for row in jRows] 
    iBests  = [row[11] if row[11] > 0 else 1000 for row in iRows]
    jBests  = [row[11] if row[11] > 0 else 1000 for row in jRows]
    iFinals = [row[12] if row[12] > 0 else 1000 for row in iRows]
    jFinals = [row[12] if row[12] > 0 else 1000 for row in jRows]
   
    iCombined = zip(iPres, iBests, iFinals)
    jCombined = zip(jPres, jBests, jFinals)
    
    iCount = sum(x < 1000 for x in iBests)
    jCount = sum(x < 1000 for x in jBests) 

    iPct = iCount / float(len(iBests))
    jPct = jCount / float(len(jBests))

    if iCount == 0:
        result = 0.0
    elif iCount > 0 and jCount == 0:
        result = 1.0
    elif iPct > jPct and iCount > jCount:
        result = 1.0
    elif max(iBests) > max(jBests):
        result = 1.0
    else:
        result = 0.0
    return result
     
def compareBasketballPress(stats,yearData,i,j):
    name,startyear,endyear,lastschool,years,games,wins,losses,pct,confchamps,conftournchamps,ncaaapp,final4,ncaachamp,srs,sos=stats
    iRows = yearData[name[i]]
    jRows = yearData[name[j]]

    iPres   = [row[10] if row[10] > 0 else 1000 for row in iRows]
    jPres   = [row[10] if row[10] > 0 else 1000 for row in jRows] 
    iBests  = [row[11] if row[11] > 0 else 1000 for row in iRows]
    jBests  = [row[11] if row[11] > 0 else 1000 for row in jRows]
    iFinals = [row[12] if row[12] > 0 else 1000 for row in iRows]
    jFinals = [row[12] if row[12] > 0 else 1000 for row in jRows]
   
    iCombined = zip(iPres, iBests, iFinals)
    jCombined = zip(jPres, jBests, jFinals)
    
    iCount = sum(x < 1000 for x in iBests)
    jCount = sum(x < 1000 for x in jBests) 

    iPct = iCount / float(len(iBests))
    jPct = jCount / float(len(jBests))

    if iCount == 0:
        result = 0.0
    elif iCount > 0 and jCount == 0:
        result = 1.0
    elif iPct > jPct and iCount > jCount:
        result = 1.0
    elif max(iBests) > max(jBests):
        result = 1.0
    else:
        result = 0.0
    return result


def compareFootballChamps(stats,i,j):
    name,start,end,school,years,games,wins,losses,ties,pct,bowls,bowlwins,bowllosses,bowlties=stats
    if i == j:
        result = 1.0
    elif bowlwins[i] > bowlwins[j] + 2:
        result = 1.0
    elif bowlwins[i] > 0 and bowlwins[j] == 0:
        result = 1.0
    elif bowls[i] > bowls[j] + 4:
        result = 1.0
    elif bowls[i] > 0 and bowls[j] == 0:
        result = 1.0
    elif years[i] < years[j]:
        result = 1.0
    else:
        result = 0.0
    return result

def compareBaseballChamps(stats,i,j):
    #name,start,end,school,years,games,wins,losses,ties,pct,bowls,bowlwins,bowllosses,bowlties=stats
    name,start,end,school,years,games,wins,losses,ties,pct,cwins,closses,capps=stats
    if i == j:
        result = 1.0
    elif cwins[i] > cwins[j]+1:
        result = 1.0
    elif cwins[i] > 0 and cwins[j] == 0:
        result = 1.0
    elif capps[i] > capps[j] + 2:
        result = 1.0
    elif capps[i] > 0 and capps[j] == 0:
        result = 1.0
    elif years[i] < years[j] - 5:
        result = 1.0
    else:
        result = 0.0
    return result

def compareBasketballChamps(stats,i,j):
    name,startyear,endyear,lastschool,years,games,wins,losses,pct,confchamps,conftournchamps,ncaaapp,final4,ncaachamp=stats
    if i == j:
        result = 0.0
    elif ncaachamp[i] > ncaachamp[j] + 2:
        result = 1.0
    elif ncaachamp[i] > 0 and ncaachamp[j] == 0:
        result = 1.0
    elif conftournchamps[i] > conftournchamps[j] + 2:
        result = 1.0
    elif conftournchamps[i] > 0 and conftournchamps[j] == 0:
        result = 1.0
    elif final4[i] > final4[j] + 2:
        result = 1.0
    elif final4[i] > 0 and final4[j] == 0:
        result = 1.0
    elif ncaaapp[i] > ncaaapp[j] + 3:
        result = 1.0
    elif confchamps[i] > confchamps[j] + 3:
        result = 1.0
    else:
        result = 0.0
    return result

def football(cursor): 
    query = "select * from footballbyyear;"
    cursor.execute(query)
    yearData = {}
    for tuple in cursor.fetchall():
        name = tuple[0]
        if name not in yearData:
            yearData[name] = {tuple}
        else:
            yearData[name] = yearData[name] | {tuple}
        

    query = "select * from football where totalyears >= 10;"
    cursor.execute(query)
    coaches = [] ; stats = [] ; A = [] ; yearStats = []
    for tuple in cursor.fetchall():
        if tuple[0] not in yearData:
            continue
        coaches = coaches + [tuple[0]]
        stats = stats + [tuple]
    stats = map(list, zip(*stats))
    for i in range(len(coaches)):
        if i % 100 == 0:
            sys.stderr.write("start row "+str(i)+" of "+str(len(coaches))+" ("+str(i*100.0/len(coaches))+"%)\n")
        A = A + [[]]
        for j in range(len(coaches)):
            #entry = compareFootballChamps(stats,i,j)
            #entry = compareFootballExtrapolate(stats,yearData,i,j)
            entry = compareFootballPress(stats,yearData,i,j)
            A[i] = A[i] + [entry]
    sys.stderr.write("Matrix initialization complete (100%)\n")
    
    bestCoaches = [] ; rank = 1
    while True:
        bestList = []
        for c in range(len(A)):
            if sum([A[ri][c] for ri in range(len(A))]) == 0:
                bestList = bestList + [c]
        if len(bestList) > 0:
            bestCoaches = bestCoaches + [(coaches[b],rank) for b in bestList]
            rank = rank + len(bestList)
            A = [[A[ri][ci] for ci in range(len(A)) if ci not in bestList] for ri in range(len(A)) if ri not in bestList]
            coaches = [coaches[i] for i in range(len(coaches)) if i not in bestList]
        else:
            break
    for c in range(len(A[0])):
        s = 0
        for r in range(len(A)):
            s = s + A[r][c]
        if s > 0:
            for r in range(len(A)):
                A[r][c] = A[r][c] / s
    scores = [sum(row) for row in A]
    results = zip(coaches,scores)
    results.sort(key=lambda x : x[1], reverse=True)
    print "Undisputed best coaches:"
    for result in bestCoaches:
        print result
    for result in results[:RESULTS]:
        print result

def baseball(cursor): 
    query = "select * from baseballbyyear;"
    cursor.execute(query)
    yearData = {}
    for tuple in cursor.fetchall():
        name = tuple[0]
        if name not in yearData:
            yearData[name] = {tuple}
        else:
            yearData[name] = yearData[name] | {tuple}
        

    query = "select * from baseball;"
    cursor.execute(query)
    coaches = [] ; stats = [] ; A = [] ; yearStats = []
    for tuple in cursor.fetchall():
        if tuple[0] not in yearData:
            continue
        coaches = coaches + [tuple[0]]
        stats = stats + [tuple]
    stats = map(list, zip(*stats))
    for i in range(len(coaches)):
        if i % 100 == 0:
            sys.stderr.write("start row "+str(i)+" of "+str(len(coaches))+" ("+str(i*100.0/len(coaches))+"%)\n")
        A = A + [[]]
        for j in range(len(coaches)):
            #entry = compareBaseballChamps(stats,i,j)
            entry = compareBaseballExtrapolate(stats,yearData,i,j)
            A[i] = A[i] + [entry]
    sys.stderr.write("Matrix initialization complete (100%)\n")
    
    bestCoaches = [] ; rank = 1
    while True:
        bestList = []
        for c in range(len(A)):
            if sum([A[ri][c] for ri in range(len(A))]) == 0:
                bestList = bestList + [c]
        if len(bestList) > 0:
            bestCoaches = bestCoaches + [(coaches[b],rank) for b in bestList]
            rank = rank + len(bestList)
            A = [[A[ri][ci] for ci in range(len(A)) if ci not in bestList] for ri in range(len(A)) if ri not in bestList]
            coaches = [coaches[i] for i in range(len(coaches)) if i not in bestList]
        else:
            break
    for c in range(len(A[0])):
        s = 0
        for r in range(len(A)):
            s = s + A[r][c]
        if s > 0:
            for r in range(len(A)):
                A[r][c] = A[r][c] / s
    scores = [sum(row) for row in A]
    results = zip(coaches,scores)
    results.sort(key=lambda x : x[1], reverse=True)
    print "Undisputed best coaches:"
    for result in bestCoaches:
        print result
    for result in results[:RESULTS]:
        print result
 
def basketball(cursor):
    query = "select * from basketballbyyear;"
    cursor.execute(query)
    yearData = {}
    for tuple in cursor.fetchall():
        name = tuple[0]
        if name not in yearData:
            yearData[name] = {tuple}
        else:
            yearData[name] = yearData[name] | {tuple}

    query = "select * from basketball where years >= 10;"
    cursor.execute(query)
    coaches = [] ; stats = [] ; A = []
    for tuple in cursor.fetchall():
        if tuple[0] not in yearData:
            continue
        coaches = coaches + [tuple[0]]
        stats = stats + [tuple]
    stats = map(list, zip(*stats))
    for i in range(len(coaches)):
        if i % 10 == 0:
            sys.stderr.write("start row "+str(i)+" of "+str(len(coaches))+" ("+str(i*100.0/len(coaches))+"%)\n")
        A = A + [[]]
        for j in range(len(coaches)):
            entry = compareBasketballPress(stats,yearData,i,j)
            #entry = compareBasketballExtrapolate(stats,yearData,i,j)
            #entry = compareBasketballChamps(stats,i,j)
            A[i] = A[i] + [entry]
    sys.stderr.write("Matrix initialization complete (100%)\n")

    bestCoaches = [] ; rank = 1
    while True:
        bestList = []
        for c in range(len(A)):
            if sum([A[ri][c] for ri in range(len(A))]) == 0:
                bestList = bestList + [c]
        if len(bestList) > 0:
            bestCoaches = bestCoaches + [(coaches[b],rank) for b in bestList]
            rank = rank + len(bestList)
            A = [[A[ri][ci] for ci in range(len(A)) if ci not in bestList] for ri in range(len(A)) if ri not in bestList]
            coaches = [coaches[i] for i in range(len(coaches)) if i not in bestList]
        else:
            break
    for c in range(len(A[0])):
        s = 0
        for r in range(len(A)):
            s = s + A[r][c]
        if s > 0:
            for r in range(len(A)):
                A[r][c] = A[r][c] / s

    scores = [sum(row) for row in A]
    results = zip(coaches,scores)
    results.sort(key=lambda x : x[1], reverse=True)
    print "Undisputed best coaches:"
    for result in bestCoaches:
        print result
    for result in results[:RESULTS]:
        print result


conn_string = "host='localhost' dbname='coaches' user='postgres' password='postgres'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
basketball(cursor)
cursor.close()
conn.close()
