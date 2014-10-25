import csv

A = []
with open('output', 'r') as f:
    line = f.readline()
    A = map(lambda x: x.split(), line[2:-3].replace(",","").split("] ["))
    A = [[float(x) for x in y] for y in A]

with open('output.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(A)
