import socket, getpass

def connect(ip, port):
    sock = socket.socket()
    sock.settimeout(1)
    print("Происходит подключение к серверу")

    try:
        sock.connect((ip, port))
    except ConnectionRefusedError as err:
        print(err)
        return False
    except TypeError:
        return False
    print("Соединение установлено")

    while True:
        try:
            data = sock.recv(1024)
        except socket.timeout:
            break

    print("Сообщение получено")
    print(data.decode())

    while True:
        msg = input("Введите сообщение на сервер: ")
        print("\nОтправка информации...")
        sock.send(msg.encode())
        if msg == "Выход":
            break
        try:
            data = sock.recv(1024)
        except socket.timeout:
            continue
        print("Сообщение получено")
        print(data.decode())

    sock.close()
    return True

ip = getpass.getpass(prompt = "Напишите ip адрес: ")
if ip == "":
    ip = "127.0.0.1"
port = getpass.getpass(prompt = "Напишите порт: ")
if port == "":
    port = 12345
else:
    try:
        port = int(port)
    except:
        print("Неверный порт")

logical = False
connCount = 0
while not logical and connCount<5:
    logical = connect(ip, port)
    if not logical:
        connCount += 1
    else:
        connCount=0
if connCount==5:
    print("Сервер закрыт. Попытки подключиться закончились.")