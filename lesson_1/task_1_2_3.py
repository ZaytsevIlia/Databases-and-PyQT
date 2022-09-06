import platform
from ipaddress import ip_address
from tabulate import tabulate
from subprocess import Popen, PIPE
import threading

result = {'Узел доступен': '', 'Узел недоступен': ''}


def ping(ip, result, get_list):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '1', str(ip)]
    reply = Popen(args, stdout=PIPE)

    if reply.wait() == 0:
        result['Узел доступен'] += f'{ip}\n'
    else:
        result['Узел недоступен'] += f'{ip}\n'
    return result


def host_ping(ip_dict, get_list=False):
    threads = []
    for ip in ip_dict:
        thread = threading.Thread(target=ping, args=(ip, result, get_list))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return result


def create_ip_dict():
    ip_dict = []
    ip_addr = input('Введите ip адрес: ')
    try:
        ipv4 = ip_address(ip_addr)
    except ValueError:
        raise Exception('Некорректный ip адрес')
    last_part_ip = int(ip_addr.split('.')[3])
    num_ip = int(input('Введите количество ip: '))
    while True:
        if last_part_ip + num_ip > 256:
            print('Максимальное число хостов не должно превышать 256.')
            num_ip = int(input('Введите количество ip: '))
        else:
            break
    for i in range(num_ip):
        ip_dict.append(str(ipv4 + i))
    return ip_dict


if __name__ == '__main__':
    """
    Для решения первой задачи
    """
    # my_dict = ['192.168.8.1', '8.8.8.8', 'yandex.ru', 'google.com',
    #            '0.0.0.1', '0.0.0.2', '0.0.0.3', '0.0.0.4', '0.0.0.5',
    #            '0.0.0.6', '0.0.0.7', '0.0.0.8', '0.0.0.9', '0.0.1.0']
    # host_ping(my_dict)
    # print(tabulate([result], headers='keys', tablefmt='grid'))
    """
    Для решения второй и третьей задачи
    """
    host_ping(create_ip_dict())
    print(tabulate([result], headers='keys', tablefmt='grid'))
