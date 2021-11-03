import random, socket, sys

sock = socket.socket()
portnumber = 12345

while True:
    try:
        sock.bind(('127.0.0.1', portnumber))
        print("Подключение к {}".format(portnumber))
        break
    except OSError as oserr:
        print("Порт {} не доступен".format(portnumber))
        portnumber = random.randint(1024, 65535)

sock.listen(0)
print("В процессе работы...")

def listening(sock):
    conn, addr = sock.accept()
    print("Клиент {} подключился".format(addr))

    with open("clients.txt", 'a+') as clients:
        clients.seek(0, 0)
        for line in clients:
            if addr[0] in line:
                conn.send(('Привет ' + line.replace(addr[0], '')).encode())
                break
        else:
            conn.send("Введите Ваше имя: ".encode())
            username = conn.recv(1024).decode()
            clients.write('\n' + username + addr[0])

    ret = False
    msg = ""

    while True:
        print("Информация от клиента: ")

        try:
            data = conn.recv(1024)
        except (ConnectionResetError, ConnectionAbortedError) as err:
            print(err, addr)
            return

        msg = data.decode()
        print(msg)

        if msg == "Выход":
            ret = True
            break
        if not data:
            break

        conn.send(data)
        print("Отправка данных клиенту...")
    conn.close()
    print("Клиент {} отключился".format(addr))
    return ret


ret = False
while not ret:
    ret = listening(sock)
print("Остановка сервера")