def ENCRYPTION(i,key):
    key=key%12
    if key==6 or key==0:
        key+=1
    Key=[[key+1,key],[key,key+1]]
    # print(Key)
    if len(i)%2!=0:
        i=i+" "
    i=list(i)

    res = []
    for ele in i:
        res.extend(ord(num)-97 for num in ele)
    
    data=[]
    for i in res:
        if i==-65:
            res[res.index(i)]=27
    data.extend(zip(res[::2],res[1::2]))


    def multiply(Text,Key,i):
        for j in range(len(Key[0])):
            for k in range(len(Key)):
                encrypted_Text[i][j] += Text[0][k] * Key[k][j]
            encrypted_Text[i][j]%=29
        return encrypted_Text

    def encryption(Text,Key):
        # print(t,k)
        for i in range (len(Text)):
            encrypted_Text=multiply([Text[i]],Key,i)
        return encrypted_Text

    Text=data
    encrypted_Text=[]
    for i in range(len(data)):
        encrypted_Text.append([0,0])

    encrypted_Text=encryption(Text,Key)

    singleList = [element for innerList in encrypted_Text for element in innerList]
    cipher_text=""
    for val in singleList:
        cipher_text=cipher_text+chr(val+97)

    return cipher_text





def DECRYPTION(cipher_text,key):
    key=key%12
    if key==6 or key==0:
        key+=1
    Key=[[key+1,key],[key,key+1]]
    cipher_text=list(cipher_text)

    res = []
    for ele in cipher_text:
        res.extend(ord(num)-97 for num in ele)
    
    cipher_data=[]

    cipher_data.extend(zip(res[::2],res[1::2]))

    def inverse(Key):
        inv[0][1]=-Key[0][1]
        inv[1][0]=-Key[1][0]
        inv[0][0]=Key[1][1]
        inv[1][1]=Key[0][0]
        return inv

    def EEA(det) :
        if(det>29):
            x=det
            y=29
        else:
            x=29
            y=det
        t0=0
        t1=1
        r=x%y
        while r!=0:
            q=x//y
            r=x%y

            t=t0-t1*q
            t0=t1
            t1=t
            x=y
            y=r

        return t0

    inv=[[0,0],[0,0]]
    inv=inverse(Key)

    det=Key[0][0]*Key[1][1]-Key[0][1]*Key[1][0]
    no=EEA(det)

    for i in range(len(inv)):
        for j in range(len(inv[0])):
            inv[i][j]=inv[i][j]%29
            inv[i][j]*=no
            inv[i][j]=inv[i][j]%29

    def demultiply(Text,Key,i):
        for j in range(len(Key[0])):
            for k in range(len(Key)):
                decrypted_text[i][j] += Text[0][k] * Key[k][j]
            decrypted_text[i][j]%=29
        return decrypted_text

    def decryption(cipher_text,inv):
        for i in range (len(cipher_text)):
            decrypted_text=demultiply([cipher_text[i]],inv,i)
        return decrypted_text

    decrypted_text=[]
    for i in range(len(cipher_data)):
        decrypted_text.append([0,0])
    decrypted_text=decryption(cipher_data,inv)

    flatList = [element for innerList in decrypted_text for element in innerList]
    plain_text=""
    for i in flatList:
        if i==27:
            flatList[flatList.index(i)]=-65
    
    for val in flatList:
        plain_text=plain_text+chr(val+97)
    return plain_text