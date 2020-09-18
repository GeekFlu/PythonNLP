import socket
import urllib.error
import urllib.parse
import urllib.request


def make_urllib_request():
    f_handler = urllib.request.urlopen('http://data.pr4e.org/romeo.txt')
    counts = dict()
    for line in f_handler:
        words = line.decode().split()
        for word in words:
            counts[word] = counts.get(word, 0) + 1
    return counts


def sort_dictionary(dic_):
    tmb = list()
    for k, v in dic_.items():
        tmb.append((v, k))
    return sorted(tmb, reverse=True)


if __name__ == "__main__":
    my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_sock.connect(('data.pr4e.org', 80))
    cmd = 'GET http://data.pr4e.org/romeo.txt HTTP/1.0\r\n\r\n'.encode()
    my_sock.send(cmd)

    while True:
        data = my_sock.recv(512)
        if len(data) < 1:
            break
        print(data.decode(), end='')
    my_sock.close()

    dictionary_ = make_urllib_request()
    ordered_list = sort_dictionary(dictionary_)
    print(ordered_list[:5])