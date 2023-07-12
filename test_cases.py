import time
import platform
import time
import json
import os
import sys
import subprocess


"""
Тесты рассчитаны исключительно на дистрибутив AstraLinux 1.6 3-го уровня защищенности "Смоленск", 
поскольку для корректной работы необходимы некоторые библиотеки, указанные в тестах 
и на других дистрибутивов большинство тестов не нужны 
"""

def color_text(text, color): # функция для окрашивания текста в консоли
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m'
    }
    if color not in colors:
        raise ValueError('Unsupported color')
    colored_text = colors[color] + text + '\033[0m'
    return colored_text


def progress_bar(iteration, total, prefix='', suffix='', length=50, fill='#'): # функция для отображения процесса выполнения в консоли
    precent = "{:.1f}".format(100*(iteration/float(total)))
    filled_length = int(length*iteration//total)
    bar = fill*filled_length + '-'*(length-filled_length)
    print('\r{} |{}| {}% {}'.format(prefix, bar, precent, suffix), end='\r')
    if iteration == total:
        print()


def progress(): # более легкий вариант отображения прогресса (в дальнейшем используется именно он)
    total = 100
    for i in range(total+1):
        progress_bar(i, total, prefix='Process', suffix='Complete', length=50, fill="#")
        time.sleep(0.007)
        
 
def test_users(): # тест на пользователя, который будет запускать скрипт UDP сервера-клиента
    count = 0
    print('test users')
    progress()
    with open('/etc/passwd', 'r') as pas_res:
        result = pas_res.readlines()
        for i in result:
            if i == 'sadm:x:1000:1000:,,,:/home/sadm:/bin/bash\n':
                mes = "OK"
                count += 1
                return color_text(mes, 'green')
        if count != 1:
            mess = "ERROR! Not user sadm!"
            return color_text(mess, 'red')
            

def test_groups(): # тест на группу пользователя, который запускает скрипт UDP сервера-клиента
    count = 0
    print('test groups')
    progress()
    with open('/etc/group', 'r') as pas_res:
        result = pas_res.readlines()
        for i in result:
            if i == 'sadm:x:1000:\n':
                count += 1
                mes = "OK"
                return color_text(mes, 'green')
        if count != 1:
            mes = "ERROR! Not group user!"
            return color_text(mes, 'red')


def test_platform(): # тест на платформу, в которой должны запускаться программы
    count = 0
    print('test platform')
    progress()
    pfm = platform.system()
    if pfm == 'Linux':
        count += 1
        mes = "OK"
        return color_text(mes, 'green')
    else:
        mes = "ERROR! platform not Linux"
        return color_text(mes, 'red')


def test_hostname(): # тест на имя машины, для эмулирования работы должен быть host1
    print('test hostname')
    progress()
    with open('/etc/hostname', 'r') as res_host:
        host = res_host.read()
    if host == 'host1':
        mes = "OK"
        return color_text(mes, 'green')
    else:
        mes = "ERROR! hostname not host1!"
        return color_text(mes, 'red')


def test_localhost(): # дополнительный тест на имя в сети, интернета быть не должно
    print('test localhost')
    progress()
    with open('/etc/hosts', 'r') as file:
        read_lh = file.readlines()
    if read_lh[0] == '127.0.0.1     localhost\n':
        mes = "OK"
        return color_text(mes, 'green')
    else:
        mes = 'ERROR! encorrect name host!'
        return color_text(mes, 'red')
        

def test_update(): # тест на актуальное обновление AstraLinux 1.6
    print('test update')
    progress()
    with open('/etc/astra_update_version', 'r') as file:
        read_up = file.readlines()
    if read_up[0] == 'Update 10\n':
        mes = "OK"
        return color_text(mes, 'green')
    elif read_up[0] == 'Update 12\n':
        mes = "WARNING! Astra update 12, possible incorrect work!"
        return color_text(mes, 'yellow')
    else:
        mes = 'ERROR! encorrect name host!'
        return color_text(mes, 'red')
     
     
def test_systemctl_PostgreSQL(): # тестирование статуса базы данных
    print("test systemctl PostgreSQL")
    progress()
    cmd = "systemctl is-active postgresql"
    result = os.popen(cmd).read().strip()
    if result == "active":
        mes = "OK"
        return color_text(mes, 'green')
    else:
        mes = "ERROR! Systemctl PostgreSQL don`t working!"
        return color_text(mes, 'red')


def test_libvulkan1(): # тест на наличие сервиса libvulkan1
    print("test libvulkan1")
    progress()
    result = subprocess.run(['dpkg', '-l', 'libvulkan1'], stdout=subprocess.PIPE)
    if "libvulkan1" in result.stdout.decode('utf-8'):
        mes = "OK"
        return color_text(mes, 'green')
    else:
        mes = "ERROR! libvulkan1 don`t installing!"
        return color_text(mes, 'red')
    
def test_libev4(): # тест на наличие сервиса libev4
    print("test libev4")
    progress()
    result = subprocess.run(['dpkg', '-l', 'libev4'], stdout=subprocess.PIPE)
    if "libvulkan1" in result.stdout.decode('utf-8'):
        mes = "OK"
        return color_text(mes, 'green')
    else:
        mes = "ERROR! libev4 don`t installing!"
        return color_text(mes, 'red')


with open('/home/tests/config.json', 'r') as file: # чтение заранее проставленных меток в тестах (1 - проводить проверку, 0 и др. - не проводить)
    conf = json.load(file)
try: # проверка, исходя из того, какие тесты выбраны, с игнорированием ошибок для предотвращения аварийного завершения тестов
    if conf["test_users"] == 1:
        print(test_users())
    if conf["test_groups"] == 1:
        print(test_groups())
    if conf["test_platform"] == 1:    
        print(test_platform())
    if conf["test_hostname"] == 1:    
        print(test_hostname())
    if conf["test_localhost"] == 1:            
        print(test_localhost())
    if conf["test_update"] == 1:
        print(test_update())
    if conf["test_systemctl_PostgreSQL"] == 1:
        print(test_systemctl_PostgreSQL())
    if conf["test_libvulkan1"] == 1:
        print(test_libvulkan1())        
except TypeError:
    pass