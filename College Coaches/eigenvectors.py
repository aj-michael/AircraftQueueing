import numpy
import csv
import psycopg2
import sys

# returns 1.0 if i is definitely better than j
def compareCoaches(coachList,stats,i,j):
    #name, start, end, school, years, games, wins, losses, ties, pct, bowls, bowlwins, bowllosses, bowlties = stats
    name, startyear, endyear, lastschool, years, games, wins, losses, pct, confchamps, conftournchamps, ncaaapp, final4, ncaachamp = stats
    

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

def sqlApproach(cursor):
    query = "select * from basketball;"
    cursor.execute(query)
    coaches = []
    stats = []
    A = []
    for tuple in cursor.fetchall():
        name = tuple[0]
        coaches = coaches + [name]
        stats = stats + [tuple]
    stats = map(list, zip(*stats))
    for i in range(len(coaches)):
        if i % 10 == 0:
            sys.stderr.write("starting row "+str(i)+" of "+str(len(coaches))+" ("+str(i*100.0/len(coaches))+"%)\n")
        A = A + [[]]
        for j in range(len(coaches)):
            entry = compareCoaches(coaches,stats,i,j)
            A[i] = A[i] + [entry]
    sys.stderr.write("Matrix initialization complete (100%)\n")

    coachesByYear = []
    query = "select * from footballbyyear;"
    cursor.execute(query)
    for tuple in cursor.fetchall():
        coachesByYear = coachesByYear + [tuple]


    # Note to self, not account for ties in zero rows
    bestCoaches = []
    rank = 1
    while True:
        c = 0
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

    for row in A:
        for cell in row:
            if cell > 0:
                cell = 0
            else:
                cell = 1.0


    # normalize the columns
    for c in range(len(A[0])):
        s = 0
        for r in range(len(A)):
            s = s + A[r][c]
        if s > 0:
            for r in range(len(A)):
                A[r][c] = A[r][c] / s






 
    evalues, evectors = numpy.linalg.eig(A)
    evalues = map(abs,evalues.tolist())
    index = evalues.index(max(evalues))
    print "index was " + str(index)
    scores = map(abs, evectors[index].tolist())
    scores = [sum(row) for row in A]
    results = zip(coaches,scores)
    results.sort(key=lambda x : x[1], reverse=True)

    print "evalues"
    print "\n".join([str(e) for e in evalues])
    print "evector"
    print "\n".join([str(s) for s in scores])
    print "coaches"
    print "\n".join(coaches) 

    print "Undisputed best coaches:"
    for result in bestCoaches:
        print result
    print "Next best coaches:"
    for result in results[:50]:
        print result

    #print A[11]
    #print compareCoaches(coaches,stats,2,11)
            


conn_string = "host='localhost' dbname='coaches' user='postgres' password='postgres'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

sqlApproach(cursor)
        
cursor.close()
conn.close()        
