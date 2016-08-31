#creates a json for D3 to visualze n degrees of kevin bacon
import sqlite3
import json

depth = 3

db = sqlite3.connect('imdb_data')

soaps = ["One Life to Live", "General Hospital", "The Guiding Light", "Search for Tomorrow", "As the World Turns", "All My Children", "Days of Our Lives", 'The Bold and the Beautiful', "Another World", "Grand Theft Auto V"  ]

cursor = db.cursor()
nodes = {}
egdes = []

a = 1
m = 0
e = 0

def runBacon(id, actor, depth):
    if depth <=0:
        return
    global  a,m,e

    if(actor):
        cursor.execute(
        """Select distinct title, M.idmovies
            From movies as M join acted_in as AI on AI.idmovies = M.idmovies
            where idactors = """ + str(id) + """ and (AI.character Not Like "%Himself%" and AI.character NOT LIKE "%Herself%" And AI.character is not null) and  AI.idseries is null""")
        allrows = cursor.fetchall()
        if (depth - 1) >= 0:
            for row in allrows:
                if(row[1]) not in nodes and row[0] not in soaps:
                    m = m +1
                    print(str(m) + " movies")
                    nodes[str(row[1])] = [row[0], " movie"]
                    runBacon(row[1], False, depth)
    else:
        cursor.execute(
        """Select distinct A.idactors, fname, lname
            From actors as A join acted_in as AI on AI.idactors = A.idactors
            where AI.idmovies = """ + str(id))
        allrows = cursor.fetchall()
        for row in allrows:
            if(depth -1)>= 0 or str(row[0]) in nodes:
                e = e +1
                print (str(e) +" edges")
                egdes.append({"source": str(id), "target": str(row[0])})
        for row in allrows:
            if str(row[0]) not in nodes:
                a = a +1
                print(str(a) + " actors")
                nodes[str(row[0])] = [str(row[1]) + " " +str(row[2]), "person"]
                runBacon(row[0], True, depth -1)


print("started")
nodes["1443046"] = ["Kevin Bacon", "bacon"]

runBacon(1443046, True, depth)
nodeArray = []

for node in nodes:
     nodeArray.append({'id' : node, 'name': nodes[node][0], "type": nodes[node][1]})

jsonFileName = "graph" + str(depth) + ".json 

graph = {"nodes": nodeArray, "links":egdes}
f = open('filename', 'w')
f.write(json.dumps(graph))

print("complete")
db.close()
