import os.path
import socket
import time
# 定义服务器地址和端口
SERVER_HOST = '124.222.97.94'
SERVER_PORT = 7000

def predict(filename):
    print(os.path.basename(filename).encode())
    # 连接服务器
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # 发送文件名
    client_socket.sendall(os.path.basename(filename).encode())

    time.sleep(0.1)
    # 读取并发送文件内容
    with open(filename, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.sendall(data)

    # 发送文件传输完成的标记
    client_socket.shutdown(socket.SHUT_WR)

    # 接收并打印服务器返回的结果
    response = b''
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        response += data

    # 打印服务器返回的结果
    # print(f"服务器返回的结果:\n{response}")
    response_str = response.decode('utf-8')
    # print(f"服务器返回的结果:\n{response_str}")
    result = eval(response_str)


    # 关闭连接
    client_socket.close()
    return result

if __name__ == "__main__":
    filename = 'upload/processedtest.csv'
    if os.path.exists(filename):
        result = predict(filename)
        print(result,len(result))
