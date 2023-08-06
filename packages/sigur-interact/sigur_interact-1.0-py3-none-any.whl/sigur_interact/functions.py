from socket import socket


def get_connection(ip, port):
    try:
        sock = socket()
        sock.connect((ip, port))
        return sock
    except ConnectionRefusedError:
        pass

def new_event_react(data, external_event_func, *args, **kwargs):
    """ Реакция на новое событие по подписке """
    if external_event_func:         # Если задана функция внешнего модуля,
        external_event_func(data)   # вызвать его и передать ему событие
