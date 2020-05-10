import math
import itertools as itools

class Skytale():
    def Encrypt(self, value, key, fillwhitespace = True):
        if(len(value)<= key):
            return value
        _value = value
        if fillwhitespace and ((len(value) % key) != 0):
            for i in range(key - (len(value)%key)):
                _value+= ' '

        return Skytale.Decrypt1(self, _value, math.ceil(len(value) / key))
    
    def Decrypt(self, value, key):
        if(len(value)<= key):
            return value
        if(len(value) % key == 0):
            return Skytale.Decrypt1(self, value, key)
        else:
            return Skytale.Decrypt2(self, value, key)
            
    def Decrypt1(self, value, key):
        return ''.join([value[i::key] for i in range(key)])

    def Decrypt2(self, value, key):
        dif = key - (len(value) % key)
        length = len(value) - (dif * (key - 1))

        result1 = [value[i:length:key] for i in range(key)]
        result2 = [value[length + i::key-1] for i in range(key-1)]

        return ''.join([a+b for a,b in itools.zip_longest(result1,result2, fillvalue='')])



def main():
    f = open("source_scytale.txt", "r", encoding="utf-8")
    source_scytale = f.read()
    f.close()


    f = open("encrypted_scytale.txt", "r", encoding="utf-8")
    encrypted_scytale = f.read()
    f.close()

    c = Skytale()

    encrypted = c.Encrypt(source_scytale, 93, False)
    d = c.Decrypt(encrypted,93)
    decrypted = c.Decrypt(encrypted_scytale, 93)

    if(source_scytale != decrypted or encrypted_scytale != encrypted):
        print("Check files failed.")
    else:
        print("Check files succedded.")



if __name__ == "__main__":
    main()