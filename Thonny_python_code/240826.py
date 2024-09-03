from machine import Pin
from machine import UART
import time
import re

uart = UART(1, baudrate=115200, tx=17, rx=16)

commandFiO2 = [0x5A, 0xA5, 0x05, 0x82, 0x53, 0x00, 0x00, 0x19] #конец строки - какие данные
commandT = [0x5A, 0xA5, 0x05, 0x82, 0x54, 0x00, 0x00, 0x21] #конец строки - какие данные
commandVti = [0x5A, 0xA5, 0x05, 0x82, 0x55, 0x00, 0x03, 0xB1] #конец строки - какие данные
commandHR = [0x5A, 0xA5, 0x05, 0x82, 0x56, 0x00, 0x00, 0x46] #конец строки - какие данные
commandSpO2 = [0x5A, 0xA5, 0x05, 0x82, 0x57, 0x00, 0x00, 0x63] #конец строки - какие данные

def send_data(data):    
    uart.write(data)
    print(f"Sent data: {data}")

def receive_data():
    if uart.any():
        data = uart.read()
        print(f"Received data: {data.hex()}")
        return data
    else:
        print("No data received")
        return None


while True:
    receiveData = receive_data()
       
    if receiveData != None:
        print("receiveData   ")
        print(receiveData)
        #text2 = str(receiveData).split("\\x") не удобный вывод
        #print("text2   ")
        #print(text2)
        
        n = 2
        text = [receiveData.hex()[i:i+n] for i in range(0, len(receiveData.hex()), n)]
        print("text   ")
        print(text)
    
    time.sleep(5)
    print("commandHR") 
    print(commandHR)
    send_data(bytes(commandHR)) #передать список !!!
    time.sleep(1)
    
    print("commandVti") 
    print(commandVti)
    send_data(bytes(commandVti)) #передать список !!!
    time.sleep(1)
    
    print("commandSpO2") 
    print(commandSpO2)
    send_data(bytes(commandSpO2)) #передать список !!!
    time.sleep(1)
    
    print("commandFiO2") 
    print(commandFiO2)
    send_data(bytes(commandFiO2)) #передать список !!!
    time.sleep(1)
    
    print("commandT") 
    print(commandT)
    send_data(bytes(commandT)) #передать список !!!
    time.sleep(1)
    
    
    
    
        
