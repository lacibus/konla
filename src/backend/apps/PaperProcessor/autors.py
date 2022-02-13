import spacy
import pickle

class AuthorParser():
    def __init__(self,doc):
        self.doc=doc
        self.names=[]


    def getConsecutiveNames(self):
        counter=0
        for i in self.doc.ents:
            if i.label_=="PERSON":
                self.names.append(i.text)
            else:
                if counter >2:
                    break
                counter+=1

    def run(self):
        self.getConsecutiveNames()
        return self.names


def test():
    doc=pickle.load(open("doc.pkl","rb"))
    ap=AuthorParser(doc)
    ap.getConsecutiveNames()
    tokens=[i for i in ap.doc]
    refs=[i for i in ap.doc.ents if i.label_=="WORK_OF_ART"]
    pass


test()