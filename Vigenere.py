from operator import itemgetter
import string
import numpy as np

def addKeyValue (textNum:int, keyNum:int):
    numOut=0
    numOut=textNum+keyNum
    if ((chr(textNum).isupper()) and(numOut>90)) or (chr(textNum).islower() and(numOut>122)):
        numOut-=26
    return numOut
    
def encrVigenere (text:str, key:str):
    textlist=[ord(char) for char in text]
    textlist=list(filter(lambda x: chr(x).isupper() or chr(x).islower() , textlist))
    keylist=[ord(char.lower())%97 for char in key]
    list_int=[]
    index=0
    for element in textlist:
        list_int.append(chr(addKeyValue(element,keylist[index])))
        index+=1
        index%=len(key)
    return(''.join(list_int))

def subKeyValue (textNum:int, keyNum:int):
    numOut=0
    numOut=textNum-keyNum
    if ((chr(textNum).isupper()) and(numOut<65)) or (chr(textNum).islower() and(numOut<97)):
        numOut+=26
    return numOut

def decrVigenere(text:str, key:str):   
    textlist=[ord(char) for char in text]
    keylist=[ord(char.lower())%97 for char in key]
    listInt=[]
    index=0
    for element in textlist:
        listInt.append(chr(subKeyValue(element,keylist[index])))
        index+=1
        index%=len(key)
    return(''.join(listInt))

def calcCoincidenceIndex(text:str):
    tmp=0
    textTmp=text.lower()
    alphabetList=list(string.ascii_lowercase)
    for char in alphabetList:
        tmp+=(textTmp.count(char)*(textTmp.count(char)-1))
    tmp=tmp/(len(text)*(len(text)-1))
    return (tmp)

def stringSeperator(text:str,keysize:int):
    length=len(text)
    splittedtext=[text[i:i+keysize] for i in range(0, length, keysize)]
    return splittedtext


def getHighestCoincidence(text:str,maxlengthKey:int):
    coinList=[]
    textTmp=text.lower()
    for i in range(1,maxlengthKey+1):
        tempList=stringSeperator(textTmp,i)
        rawList=[]
        for j in range(0,i):
            rawList.append("")
        for item in tempList:
            for k in range(0,len(item)): 
                rawList[k]+=item[k]
        coinList.append((calcCoincidenceIndex(rawList[k]),i))
        coinList.sort(key=itemgetter(0), reverse=True)
    print('Highest coincidence is reached with {} chars: {}'.format((coinList[0][1]),(coinList[0][0])))
    estimatedLength=coinList[0][1]
    return estimatedLength, stringSeperator(text,estimatedLength)
        
def getKey(seperatedList:list, estimatedlength:int):
    rawList=[]
    keystring=""
    for i in range(0,estimatedlength):
            rawList.append("")
    for item in seperatedList:
        for j in range(0,len(item)):
            rawList[j]+=item[j]
    for element in rawList:
        keystring+=getKeychar(element)
    return keystring   

def getKeychar(text:str):
    qtt=np.zeros((26))
    for i in text:
        place=ord(i)-97
        if(place>-1 and place<27):
            qtt[place]+=1
    key=chr(np.argmax(qtt)+97-4)
    return key

if __name__ == "__main__":
    with open('source_vigenere.txt', 'r',encoding='utf-8') as file:
        content1 = file.read()

    with open('encrypted_vigenere.txt', 'r',encoding='utf-8') as file:
        content2 = file.read()
        
    encrypted=encrVigenere(content1,"avecaesar")
    decrypted=decrVigenere(content2,"avecaesar")

    estimatedLength,helperlist=getHighestCoincidence(content2,10)
    keystring=getKey(helperlist,estimatedLength)

    print("Keyword:",keystring)
    print(encrypted)
    print(decrypted)  