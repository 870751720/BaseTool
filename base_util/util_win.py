import getpass
import socket
import uuid


def get_mac_address() -> str:
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e : e + 2] for e in range(0, 11, 2)])


def get_host_ip() -> str:
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


def get_pc_name() -> str:
    return getpass.getuser()
