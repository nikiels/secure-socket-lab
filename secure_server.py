import socket
import ssl

HOST = 'localhost'
PORT = 8443
CERT_FILE = 'cert.pem'
KEY_FILE = 'key.pem'

def secure_server():
    # Создаем SSL-контекст для сервера
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # Загружаем нашу пару: сертификат и приватный ключ
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    # Создаем стандартный TCP сокет
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        print(f"Сервер слушает на {HOST}:{PORT} (SSL/TLS)...")
        
        # Ожидаем входящее соединение
        conn, addr = sock.accept()
        print(f"Клиент {addr} подключился (незащищенный сокет).")

        # Оборачиваем сокет в SSL
        try:
            with context.wrap_socket(conn, server_side=True) as secure_conn:
                print(f"SSL-соединение установлено. Шифр: {secure_conn.cipher()}")
                
                # Получаем данные и отправляем обратно (эхо)
                data = secure_conn.recv(1024)
                print(f"Получено зашифрованное сообщение: {data.decode()}")
                
                secure_conn.sendall(data)
                print("Отправлено эхо по зашифрованному каналу.")

        except ssl.SSLError as e:
            print(f"Ошибка SSL: {e}")
        finally:
            print("Соединение закрыто.")


if __name__ == "__main__":
    secure_server()