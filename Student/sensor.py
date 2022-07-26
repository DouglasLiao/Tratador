import serial

def getsensordata():
    #print("------Reading collection starts now------")
    sr = serial.Serial("COM4",9600)
    st = list(str(sr.readline(),'utf-8'))
    sr.close() 
    #print("------Reading collection ends successfully------")
    return int(str(''.join(st[:])))