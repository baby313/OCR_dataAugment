import random
chars_origin = 'ABCDEFGHJKLMNPRSTUVWXYZ0123456789'

chars_10 = 'ABCDEFGHJKLMNPRSTVWXY123456789'

chars_num = '0123456789'

wmi_home = ['LSG','LB3','LJU','LFM','LVG','LDC','LGB','LZW','LEW','LVS','LFV','LBE','LNB',
            'LBV','LS5','LS4','LVV','LGX','LSJ','LFP','LSV','LGW','LJ1','LJD','LFB','LHG']

wmi_abroad = ['SCA','SAJ','SAL','WMW','VF3','WF7','SCB','WDB','WDD','WME','WAU','JM1']            

char_num = {'0': 0, '1': 1, '2': 2,'3': 3,'4': 4,'5': 5,'6': 6,'7': 7,'8': 8,'9': 9,
            'A': 1,'B': 2,'C': 3,'D': 4,'E': 5,'F': 6,'G': 7,'H': 8,'J': 1,'K': 2,
            'L': 3,'M': 4,'N': 5,'P': 7,'R': 9,'S': 2,'T': 3,'U': 4,'V': 5,'W': 6,
            'X': 7,'Y': 8,'Z': 9}
chars_9 = '0123456789X'


def randomchar(chars):
    lenth = len(chars) - 1
    result = chars[random.randint(0,lenth)]
    return result

def line():
    m = random.random()
    if m < 0.85:
        wmi = randomchar(wmi_home)
        char1 = wmi[0]
        char2 = wmi[1]
        char3 = wmi[2]
    elif 0.85 <= m <0.95:
        wmi = randomchar(wmi_abroad)
        char1 = wmi[0]
        char2 = wmi[1]
        char3 = wmi[2]
    else:            
        char1 = randomchar(chars_origin)
        char2 = randomchar(chars_origin)
        char3 = randomchar(chars_origin)
    char4 = randomchar(chars_origin)
    char5 = randomchar(chars_origin)
    char6 = randomchar(chars_origin)
    char7 = randomchar(chars_origin)
    char8 = randomchar(chars_origin)
    char10 = randomchar(chars_10)
    char11 = randomchar(chars_origin)
    char12 = randomchar(chars_origin)
    char13 = randomchar(chars_origin)
    char14 = randomchar(chars_origin)
    char15 = randomchar(chars_num)
    char16 = randomchar(chars_num)
    char17 = randomchar(chars_num)

    char9 = chars_9[(char_num[char1]*8 + char_num[char2]*7 + char_num[char3]*6 + char_num[char4]*5 +char_num[char5]*4 + 
                     char_num[char6]*3 + char_num[char7]*2 + char_num[char8]*10 + char_num[char10]*9 + char_num[char11]*8 + 
                     char_num[char12]*7 + char_num[char13]*6 + char_num[char14]*5 + char_num[char15]*4 + char_num[char16]*3 + 
                     char_num[char17]*2 )%11]
    
    
    text = char1+char2+char3+char4+char5+char6+char7+char8+char9+char10+char11+char12+char13+char14+char15+char16+char17
    return text

if __name__ == '__main__':
    file = open('./assets/vintxt.txt','w')
    for i in range(500000):
        #try:
            text = line()
            file.write(text+'\n')
            if i%2 == 0:
                print(i)
        #except:
            #print('error')
    file.close()



        

