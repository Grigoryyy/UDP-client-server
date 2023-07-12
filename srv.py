import json
import socket
import sys
import modules_for_udp.modul_udp_1
#sys.path.append('/home/lx64/PycharmProjects/Udp')  объявление пути для модуля
from modules_for_udp import modul_udp_1 # импорт модуля


BUFFER_SIZE = 4096 # значение размера буфера

"""Подготовка к открытию сокета"""
sock = socket.socket()
sock.bind(('', 19970))
sock.listen(1)

print('Sock name: {}'.format(sock.getsockname()))

while True: # сервер работает без отсановки
    conn, addr = sock.accept() # открытие сокета
    print('Connected:', addr)

    #all_data = bytearray() использовать в случае, если клиент передает 1024 а не 2048
    all_data = bytes

    while True: #
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break

        print('Recv: {}: {}'.format(len(data), data))
        all_data = data

    """Вывод значений"""

    print('All data {}: {}'.format(len(all_data), all_data))
    print(len(all_data[8:]))
    obj = all_data
    a = int.from_bytes(obj[2:4], byteorder='little')
    print(a)

    print('Close')
    conn.close()
