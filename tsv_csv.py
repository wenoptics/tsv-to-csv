FILE = "data/drugLibTrain_raw.tsv"
INS = 9

t = open(FILE, "rb")
wholeContent = t.read()

wholeContent = wholeContent.decode().split("@id@")


def enc(s: str):
    return s.strip().replace('\r', '\n').replace('\n', '\\n')


class Data:
    def __init__(self):
        self.idf = None
        self.urlDrugName = None
        self.rating = None
        self.effectiveness = None
        self.sideEffects = None
        self.condition = None
        self.benefitsReview = None
        self.sideEffectsReview = None
        self.commentsReview = None

    def set_item(self, k, v):
        names = ["idf", "urlDrugName", "rating", "effectiveness", "sideEffects", "condition", "benefitsReview",
                 "sideEffectsReview", "commentsReview"]
        v = enc(v)
        self.__setattr__(names[k], v)
        print("[", names[k], "] ", v)


arrData = []
for i in wholeContent:
    d = Data()
    iList = i.split('\t')
    if len(iList) == INS:
        for ii, s in enumerate(iList):
            d.set_item(ii, s)
    arrData.append(d)


def ols_csv():
    tmp = None
    for i, s in enumerate(wholeContent):
        ii = i % INS
        if ii == 0:
            arrData.append(tmp)
            tmp = Data()
            tmp.set_item(ii, s)
            print('\n\n ------ ')
        else:
            tmp.set_item(ii, s)


skipped = 0
wf = open("output.csv", "w", encoding="utf-8")

for d in arrData:
    if d is None:
        continue

    try:
        line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (d.idf, d.urlDrugName, d.rating, d.effectiveness, d.sideEffects,
                                                         d.condition, d.benefitsReview, d.sideEffectsReview,
                                                         d.commentsReview)

        wf.write(line)
    except Exception:
        skipped += 1

print('wrote {:d} lines, skipped {:d}'.format(len(arrData), skipped))
