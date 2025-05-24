import socket

HOST = 'localhost'
PORT = 9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Подключен клиент: {addr}")
            data = conn.recv(1024)
            if not data:
                break
            print("Получено:", data.decode('utf-8'))