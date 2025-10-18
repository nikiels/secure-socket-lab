import socket
import ssl

HOST = 'localhost'
PORT = 8443
CERT_FILE = 'cert.pem'

def secure_client():
    # Создаем SSL-контекст для клиента
    # PROTOCOL_TLS_CLIENT обеспечивает хорошие настройки безопасности
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    
    # Загружаем сертификат сервера, чтобы мы могли проверить его подлинность
    context.load_verify_locations(CERT_FILE)
    
    # Создаем обычный сокет
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Оборачиваем его в SSL-контекст
        # server_hostname важен для проверки того, что мы подключились к нужному серверу
        with context.wrap_socket(sock, server_hostname=HOST) as secure_sock:
            try:
                secure_sock.connect((HOST, PORT))
                print(f"SSL-соединение с сервером {HOST}:{PORT} установлено.")
                
                message = "Это секретное сообщение!"
                secure_sock.sendall(message.encode())
                print(f"Отправлено: {message}")
                
                data = secure_sock.recv(1024)
                print(f"Получено эхо: {data.decode()}")

            except ssl.SSLCertVerificationError as e:
                print(f"Ошибка проверки сертификата: {e}")
            except ConnectionRefusedError:
                print("Не удалось подключиться. Убедитесь, что сервер запущен.")

if __name__ == "__main__":
    secure_client()
