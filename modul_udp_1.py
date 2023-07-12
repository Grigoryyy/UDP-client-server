import json


"""Модуль, который достает данные (числа) из структур(вида .json)"""

def open_file(struct_select: str = 'transfer_protocol.json'): # отдельная функция, открывающая файл .json, для более удобного выбора структур
   # path_struct = '/home/lx64/PycharmProjects/Udp/UDP_work/struct_json/' абсолютный путь
    path_struct = 'home/struct_json/' # относительный
    return path_struct + struct_select


f = open(open_file()) # открытик файла
data = json.load(f)
row_frame = [] # помещение структуры в список


def create_frame(data_d): # алгоритм, получающий данные из структуры
    if str(type(data_d)) == "<class 'dict'>":
        for value in list(data_d.values()):
            if str(type(value)) == "<class 'dict'>":
                create_frame(value)
            elif str(type(value)) == "<class 'list'>":
                create_frame(value)
            else:
                row_frame.append(value)
    else:
        for value2 in list(data_d):
            if str(type(value2)) == "<class 'dict'>":
                create_frame(value2)
            elif str(type(value2)) == "<class 'list'>":
                create_frame(value2)
            else:
                row_frame.append(value2)
    return row_frame


def answer_for_server(obj=bytes): # ответы для сервера
   #  with open('/home/lx64/PycharmProjects/Udp/UDP_work/struct_json/code_result.json', 'r') as file:  абсолютный путь
    with open('/home/code_result.json', 'r') as file: # относительный
        code = json.load(file)

