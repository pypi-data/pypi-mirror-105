"""
This module can be used for streaming video and audio and screenshare through ip.

Author: A.jagan kartgick
"""

__author__ = "A.Jagan karthick"
__email__ = "jagankarthick2@gmail.com"

import socket
import pyaudio
import threading
import pickle
import cv2
from PIL import ImageGrab
import numpy

class StreamingServer():
    """
    Class for the streaming server.

    Attributes
    ----------

    Private:

        __host : str
            host address of the listening server
        __port : int
            port on which the server is listening
        
    Methods
    -------

    Public:

        start_server : starts the server in a new thread
        stop_server : stops the server and closes all connections
    """
    def __init__(self, ip, port):
        self.__ip = ip
        self.__port = port
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__address = (self.__ip, self.__port)
        self.__server.bind(self.__address)
        self.__server_running = False
        self.__clients = []
        self.__buffer = 10000000
    def __start_server(self):
        self.__server.listen()
        try:
            while self.__server_running:
                connection, address = self.__server.accept()
                self.__clients.append(connection)
                loop = threading.Thread(target = self.__stream, args = [connection])
                loop.start()
        except:
            pass
    def __stream(self, root):
        try:
            while self.__server_running:
                data = root.recv(self.__buffer)
                for client in self.__clients:
                    if client != root:
                        client.sendall(data)
        except:
            for x in self.__clients:
                self.__clients.remove(x)
    def start_server(self):
        if self.__server_running:
            print(f'[WARNING] server already running on {self.__address}')
        else:
            self.__server_running = True
            loop = threading.Thread(target = self.__start_server)
            loop.start()
    def stop_server(self):
        if self.__server_running:
            for x in self.__clients:
                self.__clients.remove(x)
            self.__server_running = False
            self.__server.close()
        else:
            print('[WARNING] server is not running')

class AudiostreamClient():
    """
    Class for the audio streaming client.

    Attributes
    ----------

    Private:

        __host : str
            host address of the listening server
        __port : int
            port on which the server is listening


    Methods
    -------

    Public:

        connect_client : connects the client to the server
        close_connection : closes all the connections to the server
    """
    def __init__(self, ip, port, format = pyaudio.paInt16, channels = 2, rate = 44100):
        self.__ip = ip
        self.__port = port
        self.__format = format
        self.__channels = channels
        self.__rate = rate
        self.__chunk = 4096
        self.__audio_driver = pyaudio.PyAudio()
        self.__address = (self.__ip, self.__port)
        self.__client_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__input_stream = self.__audio_driver.open(format = self.__format, channels = self.__channels, rate = self.__rate, input = True, frames_per_buffer = self.__chunk)
        self.__output_stream = self.__audio_driver.open(format = self.__format, channels = self.__channels, rate = self.__rate, output = True, frames_per_buffer = self.__chunk)
    def __connect_client(self):
        try:
            self.__client_server.connect(self.__address)
            return True
        except:
            return False
    def __recv_client(self):
        while True:
            try:
                data = self.__client_server.recv(self.__chunk)
                self.__output_stream.write(data)
            except:
                break
    def __send_client(self):
        while True:
            try:
                data = self.__input_stream.read(self.__chunk)
                self.__client_server.sendall(data)
            except:
                break
    def connect_client(self):
        connection_status = self.__connect_client()
        if connection_status:
            thread1 = threading.Thread(target = self.__recv_client)
            thread2 = threading.Thread(target = self.__send_client)
            thread1.start()
            thread2.start()
        else:
            raise Exception(f'Server Denied Connection at {self.__address}')
    def close_connection(self):
        self.__input_stream.stop_stream()
        self.__input_stream.close()
        self.__output_stream.stop_stream()
        self.__output_stream.close()
        self.__client_server.close()

class CamerastreamClient():
    """
    Class for the streaming server.

    Attributes
    ----------

    Private:

        __host : str
            host address of the listening server
        __port : int
            port on which the server is listening


    Methods
    -------

    Public:

        connect_client : connects the client to the server
        close_connection : closes all the connections to the server
    """
    def __init__(self, ip, port, camera):
        self.__ip = ip
        self.__port = port
        self.__camera = camera
        self.__client_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__address = (self.__ip, self.__port)
        self.__started = False
        self.__camera_capture = cv2.VideoCapture(self.__camera)
    def __connect_client(self):
        try:
            self.__client_server.connect(self.__address)
            return True
        except:
            return False
    def __send(self):
        while self.__started:
            try:
                frames = self.__camera_capture.read()
                data = pickle.dumps(frames)
                self.__client_server.sendall(data)
            except:
                break
    def __recv(self):
        while self.__started:
            try:
                print('start')
                data = self.__client_server.recv(10000000)
                print(data)
                data = pickle.loads(data)
                cv2.imshow('recieving', data)
            except:
                break
    def connect_client(self):
        started_status = self.__connect_client()
        self.__started = True
        if started_status:
            thread1 = threading.Thread(target = self.__recv)
            thread2 = threading.Thread(target = self.__send)
            thread1.start()
            thread2.start()
        else:
            raise Exception(f'Server Denied Connection at {self.__address}')
    def close_connection(self):
        if self.__started:
            self.__started = False
        else:
            raise Exception('client already not running')

class Screenshareclient():
    """
    Class for the streaming server.

    Attributes
    ----------

    Private:

        __host : str
            host address of the listening server
        __port : int
            port on which the server is listening
        __quit_key : chr
            key that has to be pressed to close connection


    Methods
    -------

    Public:

        connect_client : connects the client to the server
        close_connection : closes all the connections to the server
    """
    def __init__(self, ip, port, quit_key = 'q'):
        self.__ip = ip
        self.__port = port
        self.__quit_key = str(quit_key)
        self.__client_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__address = (self.__ip, self.__port)
        self.__running = False
        self.__buffer = 10000000
        self.__window_title = "streaming from {}".format(self.__address)
    def __connect_client(self):
        try:
            self.__client_server.connect(self.__address)
            return True
        except:
            return False
    def __send(self):
        try:
            while self.__running:
                img = ImageGrab.grab()
                array = numpy.array(img)
                pickled_data = pickle.dumps(array)
                self.__client_server.sendall(pickled_data)
        except:
            self.__running = False
    def __recv(self):
        try:
            while self.__running:
                data = self.__client_server.recv(self.__buffer)
                if data != b'end':
                    try:
                        data = pickle.loads(data)
                        data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
                        cv2.imshow(self.__window_title, data)
                        if cv2.waitKey(1) == ord(self.__quit_key):
                            self.__running = False
                            self.__client_server.send(b'end')
                            break
                    except pickle.UnpicklingError as e:
                        pass
                else:
                    self.__running = False
                    self.__client_server.close()
                    cv2.destroyAllWindows()
        except:
            self.__running = False
    def __start_stream(self):
        loop1 = threading.Thread(target = self.__recv)
        loop2 = threading.Thread(target = self.__send)
        loop1.start()
        loop2.start()
    def connect_client(self):
        connect_status = self.__connect_client()
        if connect_status:
            self.__running = True
            loop = threading.Thread(target = self.__start_stream)
            loop.start()
        else:
            raise Exception(f"[ERROR] Unable to connect to the server at {self.__address}")
    def close_connection(self):
        if self.__running:
            self.__running = False
            self.__client_server.close()
            cv2.destroyAllWindows()
