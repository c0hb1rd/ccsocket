import socket
import time

from CCSocketException import *

TCP_SERVER = "TCP Server"
TCP_CLIENT = "TCP Client"
UDP_SERVER = "UDP Server"
UDP_CLIENT = "UDP Client"


class CCSocket:
    def __init__(self, ip, port, timeout=None):
        self.ip = ip
        self.port = port
        self.address = (self.ip, self.port)

        self.timeout = 10 if not timeout else timeout
        self.address = (ip, port)
        self.server = None
        self.client = None

        self.flags = {
            "ip": self.ip,
            "port": self.port,
            "type": None,
            "timeout": self.timeout,
        }

    def TcpServer(self):
        if not self.server and not self.flags["type"]:
            self.flags["type"] = TCP_SERVER
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(self.address)
            self.server.settimeout(self.timeout)
            return self
        else:
            self.throwCreatedRaise()

    def UdpServer(self):
        if not self.server and not self.flags["type"]:
            self.flags["type"] = UDP_SERVER
            self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server.bind(self.address)
            self.server.settimeout(self.timeout)
            return self
        else:
            self.throwCreatedRaise()

    def TcpClient(self):
        if not self.client and not self.flags["type"]:
            self.flags["type"] = TCP_CLIENT
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.timeoutWork("self.client.connect(self.address)")
            self.client.settimeout(self.timeout)
            return self
        else:
            self.throwCreatedRaise()

    def UdpClient(self):
        if not self.client and not self.flags["type"]:
            self.flags["type"] = UDP_CLIENT
            self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.timeoutWork("self.client.connect(self.address)")
            self.client.settimeout(self.timeout)
            return self
        else:
            self.throwCreatedRaise()

    def listen(self, count):
        self.throwNoneRaise()
        self.server.listen(count)
        return self

    def send(self, context):
        self.throwNoneRaise()
        if self.isTcpOrUdp() == "TCP":
            result = self.client.send(context)
        else:
            result = self.client.sendto(context)
        return result

    def receive(self, size):
        self.throwNoneRaise()
        if self.isTcpOrUdp() == "TCP":
            result = self.client.recv(size)
        else:
            result = self.client.recvfrom(size)
        return result

    def timeoutWork(self, work):
        start = time.time()
        while True:
            try:
                eval(work)
                break
            except:
                time.sleep(0.5)
                end = time.time()
                if end - start > self.timeout:
                    self.throwTimeoutRaise()

    def __str__(self):
        return str(self.flags)

    def getType(self):
        return self.flags["type"]

    def isServerOrClient(self):
        return self.flags['type'].split(" ")[1]

    def isTcpOrUdp(self):
        return self.flags["type"].split(" ")[0]

    def throwCreatedRaise(self):
        raise AlreadyCreated(self.flags["type"])

    def throwNoneRaise(self):
        if not self.flags["type"]:
            raise NoneObject()

    def throwTimeoutRaise(self):
        raise Timeout(self.timeout)

    def quit(self):
        self.throwNoneRaise()
        flag = self.isServerOrClient()
        if flag == "Server":
            self.server.close()
        elif flag == "Client":
            self.client.close()

