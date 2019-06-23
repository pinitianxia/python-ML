import operator

def getdata():
    mushDatSet = [line.split() for line in open("mushroom.dat").readlines()]
    return mushDatSet

def createc1(data):
    c1 = []
    aa = set()
    bb = []
    for transaction in data:
        for item in transaction:
            if item not in c1:
                c1.append(item)
    c1.sort()
    for i in c1:
        aa.add(i)
        bb.append(frozenset(aa))
        aa.remove(i)
    return bb

def scanD(ck, d, minsuport):
    ssCnt = {}
    for item in d:
        for can in ck:
            if can.issubset(item):
                if can in ssCnt.keys():
                    ssCnt[can] += 1
                else:
                    ssCnt[can] = 1
    relist = []
    supportdata = {}
    for key in ssCnt:
        support = ssCnt[key] / int(len(d))
        if support >= minsuport:
            supportdata[key] = support
            relist.append(key)
    return relist, supportdata

def aprioriGen(Lk, k):
    relist = []
    for i in range(len(Lk)):
        for j in range(i + 1, len(Lk)):
            l1 = list(Lk[i])[:k - 2]
            l2 = list(Lk[j])[:k - 2]
            if operator.eq(l1, l2):
                relist.append(Lk[i] | Lk[j])
    return relist

def apriori(data, minsupport):
    c1 = createc1(data)
    d = list(map(set, data))
    l1, supportdata = scanD(c1, d, minsupport)
    L = [l1]
    k = 2
    while (len(L[k - 2]) > 0):
        ck = aprioriGen(L[k - 2], k)
        lk, supk = scanD(ck, d, minsupport)
        supportdata.update(supk)
        L.append(lk)
        k += 1
    return L, supportdata, k - 1

def getRules(L, supportData, minConf):
    rulelist = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            freqSet2 = list(freqSet)
            H1 = []
            ff = set()
            for item in freqSet2:
                ff.add(item)
                H1.append(frozenset(ff))
                ff.clear()
            rulesFromConseq(freqSet, H1, supportData, rulelist, minConf)
    return rulelist

def calcConf(freqSet, H, supportData, brl, minConf):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf > minConf:
            print(freqSet - conseq, "--->", conseq, "conf:", conf)
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append((conseq))
    return prunedH

def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    while (len(freqSet) > m):
        H = calcConf(freqSet, H, supportData, brl, minConf)
        if (len(H) > 1):
            H = aprioriGen(H, m + 1)
            m += 1
        else:
            break

if __name__ == '__main__':
    L, supportdata, k = apriori(getdata(), 0.6)
    print("频繁{}项集：{}".format(2, L[1]))
    rules = getRules(L, supportdata, 0.7)