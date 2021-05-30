# coding: utf-8
# wsgi的简单实现：
#   1.创建一个套接字，并与本机的某个端口绑定，
#   2.监听该端口
#   3.接受请求，创建发送端口
#   4.发送HTTP响应报文序列化后的字节流

import socket

count = 0

## 两个空行代表HTTP报文结束
EOL1 = b'\n\n'
EOL2 = b'\n\r\n'



def handle_connection(conn, addr):
    global count
    print(f"conn is {conn},\naddr is {addr}")
    request = b''
    while EOL1 not in request and EOL2 not in request:
        request += conn.recv(1024)
        # print(request)
    body = '''Hello, world！<h1> from the5fire 《DJango企业开发实战》</h1>''' + str(count)
    response_params =[
        'HTTP/1.0 200 OK',
        'Date: Sun, 27 may 2018 01:01:01 GMT',
        'Content-Type: text/html; charset=utf-8',
        'Content-Length: {}\r\n'.format(len(body.encode())),
        body,
    ]
    response = '\r\n'.join(response_params)
    conn.send(response.encode())
    conn.close()

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('127.0.0.1',8000))
    serversocket.listen(5)
    print('http://127.0.0.1:8000')

    try:
        while True:
            # 接受和发送报文使用不断的套接字和端口。
            global count
            conn, addr = serversocket.accept()
            count += 1
            handle_connection(conn, addr)
    finally:
        serversocket.close()
    

if __name__=='__main__':
    main()