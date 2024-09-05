from machine import Pin
from machine import UART
import time
import re

#####################   Справочная информация   #########################
#
# ЗАДАНО (пользователем)
# FiO2 - 5000
# T - 5100
# Длит - 5200
#
# ПРИНЯТО (с датчиков)
# FiO2 - 5300
# T - 5400
# Vti - 5500
# HR - 5600
# SpO2 - 5700
#
#########################################################################

uart = UART(1, baudrate=115200, tx=17, rx=16)

commandFiO2 = [0x5A, 0xA5, 0x05, 0x82, 0x53, 0x00, 0x00, 0x19] #конец строки - какие данные
commandT = [0x5A, 0xA5, 0x05, 0x82, 0x54, 0x00, 0x00, 0x21] #конец строки - какие данные
commandVti = [0x5A, 0xA5, 0x05, 0x82, 0x55, 0x00, 0x03, 0xB1] #конец строки - какие данные
commandHR = [0x5A, 0xA5, 0x05, 0x82, 0x56, 0x00, 0x00, 0x46] #конец строки - какие данные
commandSpO2 = [0x5A, 0xA5, 0x05, 0x82, 0x57, 0x00, 0x00, 0x63] #конец строки - какие данные

commandMinute1 = [0x5A, 0xA5, 0x05, 0x82, 0x61, 0x00, 0x00, 0x00] #конец строки - какие данные
commandMinute2 = [0x5A, 0xA5, 0x05, 0x82, 0x62, 0x00, 0x00, 0x00] #конец строки - какие данные

FiO2 = 0
T = 0
Time = 0

dictGetValues = {"5000" : FiO2, "5100" : T, "5200" : Time}

def send_data(data):
    print("send_data = " + str(data))
    uart.write(data)
    #print(f"Sent data: {data}")

def receive_data():
    if uart.any():
        data = uart.read()
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Received data: {data.hex()}")
        return data
    else:
        #print("No data received")
        return None


while True:
    receiveData = receive_data()
       
    if receiveData != None:
        #print("receiveData   ")
        #print(receiveData)
        #text2 = str(receiveData).split("\\x") не удобный вывод
        #print("text2   ")
        #print(text2)
        
        n = 2
        text = [receiveData.hex()[i:i+n] for i in range(0, len(receiveData.hex()), n)]
        print("text   ")
        print(text)
        
        #здесь разбираем text - с какого адреса пришли значения ( 4 и 5 )- какая переменная
        # 8 - само значение в 16ричном формате
        #if str(text[4])+str(text[5]) == "5000": #сделать без if через список, структуру...
        print("text[7] === " + text[7])
        print("text[8] === " + text[8]) #проверить
        key = str(text[4])+str(text[5])        
        dictGetValues[key] = str(text[7]) + str(text[8]) #словарь должен содержать ВСЕ адреса, с которых мы можем что-то принять НО пока всё равно нет соответствия переменным...
        print(" dictGetValues[key] === " + key)
        print(" dictGetValues[key] === " + str(int(dictGetValues[key], 16)))
        
        if key=="5200":
            print("Начали!")
            reverseTimer = dictGetValues["5200"]
            print("reverseTimer ========= " + reverseTimer)
            print("Минут всего   " + str(int(reverseTimer, 16)))
            print("Секунд всего   " + str(int(reverseTimer,16)*60))
            test = str(int(reverseTimer,16))
            if len(test)==2 :
                print("до изменения commandMinute1    " + str(commandMinute1))
                commandMinute1[7] = int(test[0])
                print("после изменения commandMinute2    " + str(commandMinute1))
                send_data(bytes(commandMinute1))
                print("до изменения commandMinute2    " + str(commandMinute2))
                commandMinute2[7] = int(test[1])
                print("после изменения commandMinute2    " + str(commandMinute2))
                send_data(bytes(commandMinute2))
    
    #time.sleep(5)
    #print("commandHR") 
    #print(commandHR)
    #send_data(bytes(commandHR)) #передать список !!!
    time.sleep(1)
    
    #print("commandVti") 
    #print(commandVti)
    #send_data(bytes(commandVti)) #передать список !!!
    #time.sleep(1)
    
    #print("commandSpO2") 
    #print(commandSpO2)
    #send_data(bytes(commandSpO2)) #передать список !!!
    #time.sleep(1)
    
    #print("commandFiO2") 
    #print(commandFiO2)
    #send_data(bytes(commandFiO2)) #передать список !!!
    #time.sleep(1)
    
    #print("commandT") 
    #print(commandT)
    #send_data(bytes(commandT)) #передать список !!!
    #time.sleep(1)
    
    
    
    
        
