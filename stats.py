import src.localgameforstat as localgameforstat
cptB = 0
cptW = 0
cptD = 0
nbtest = 100

for i in range(0, nbtest):
    res = localgameforstat.localgame()
    if res == "WHITE":
        cptW +=1
    if res == "BLACK":
        cptB +=1
    if res == "DEUCE":
        cptD +=1
print("Pourcentage de victoire : ",cptB/nbtest)