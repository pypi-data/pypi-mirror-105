import socket
import threading
import socketserver
import time
import os


class RequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        #print(self, *args, **kwargs)
        #print("Got connection from {}".format( self.client_address[0]) )
        super().__init__(*args, **kwargs)
        self.request.settimeout(1)

        #socketserver.BaseRequestHandler.__init__(self, *args, **kwargs)

    def handle(self):
        while True:
            data = str(self.request.recv(1024), 'ascii')
            cur_thread = threading.current_thread()
            print("{} received {} from {}".format(cur_thread.name, data, self.client_address) )
            if data == "":
                return

        #when this methods returns, the connection to the client closes

    def setup(self):
        print("Got new connection from {}".format( self.client_address) )
        self.server.handlers.append(self)

    def finish(self):
        print("Connection from {} lost".format( self.client_address) )
        self.server.handlers.remove(self)


class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def init(self):
        """
        __init__ should not be overriden
        """
        self.handlers = []

    def close(self):
        for handler in self.handlers:
            handler.request.shutdown(socket.SHUT_RDWR)
            handler.request.close()
        self.shutdown()
        print("Server shut down")


class DummyRobot(object):
    def __init__(self, host="localhost", port=30003, sample_time=1/125.0):
        self.host = host
        self.port = port
        self.sample_time = sample_time

        self.server = Server((self.host, self.port), RequestHandler)
        self.publish_packets = False

    def run(self):
        self.server.init()

        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        self.publish_packets = True
        publisher_thread = threading.Thread(target=self._package_publisher)
        publisher_thread.daemon = True
        publisher_thread.start()

    def _package_publisher(self):
        with open(os.path.join(os.path.dirname(__file__), "packet.bin"), "rb") as f:
            packet = f.read()
            f.close()
            while self.publish_packets:
                time.sleep(self.sample_time)
                for handler in self.server.handlers:
                    handler.request.sendall(packet)
        print("Publisher stopped.")

    def close(self):
        print("Shutting down robot")
        self.publish_packets = False
        time.sleep(1)
        self.server.close()
