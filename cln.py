import socket
import time
import json
import sys
import glob
sys.path.append('/home/') # объявление относительного пути для модуля
# sys.path.append('/home/lx64/PycharmProjects/Udp') абсолютный путь
from modules_for_udp import modul_udp_1 # импорт модуля


sock = socket.socket() # бинд сокета
sock.connect(('localhost', 19970)) # обозначение подключения
list_struct = [] # здесь будут лежать данные из структур
#for filename in glob.glob("/home/lx64/PycharmProjects/Udp/UDP_work/struct_json/*.json"): # для возможности просмотра и выбора из списка структур (абсолютный путь)
for filename in glob.glob("/home/struct_json/*.json"): # относительный путь
    pop_list = '/'.join(filename.split('/')[-1:])
    list_struct.append(pop_list)
for i, structs in enumerate(list_struct):
    print(i, structs)

input_structs = input('Введите структуру для проверки, выше список доступных: ')


f = open(modul_udp_1.open_file(input_structs)) # открытие выбранного файла
data = json.load(f)
frame = modul_udp_1.create_frame(data) # получение данных из структуры
print(frame)
print('Send:', frame)


with open('/home/data.bin', 'wb') as file: # открытие бинарного файла и запись значений
    file.truncate(1500) # назначение размера файла
    for i in range(len(frame)):
        try:
            write_data = int.to_bytes(frame[i], length=2, byteorder='little')
        except OverflowError:
            write_data = int.to_bytes(frame[i], length=4, byteorder='little')
        file.write(write_data)

#with open('/home/lx64/data.bin', 'rb') as file2: отправка на сервер (абсолютный путь)
with open('/home/data.bin', 'rb') as file2 #относительный путь
    l = file2.read(1500)
    while (l):
        '''отправляем строку на сервер'''
        sock.send(l)
        l = file2.read(1500)

print('Close') # закрыть соединение
sock.close()
