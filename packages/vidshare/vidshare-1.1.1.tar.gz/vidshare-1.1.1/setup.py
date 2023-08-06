from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.1.1'
DESCRIPTION = 'Streaming video and audio and screenshare data via networks'
LONG_DESCRIPTION = """this is a package that is used to stream camera, audio, screenshare data via network

examples:-

    server.py
        from vidshare import StreamingServer
        import threading

        server = StreamingServer("localhost", 5000) #set your ip and port on server

        thread = threading.Thread(target = server.start_server) #thread to start server
        thread.start() #start the thread

        while True:
            input_ = input('Enter Quit To Exit : ')
            if input_ == 'quit' or input_ == 'exit':
                server.stop_server() #to stop the server
                break
    
    audio client example:-
    client1.py
        from vidshare import AudiostreamClient
        import threading

        server = AudiostreamClient("localhost", 8000) #ip and port to connect to the server

        thread = threading.Thread(target = server.connect_client) #thread to connect to the server
        thread.start() #start the thread

        while True:
            input_ = input('Enter Quit To Exit : ')
            if input_ == 'quit' or input_ == 'exit':
                server.close_connection() #to close the connection to the server
                break
    
    client2.py
        from vidshare import AudiostreamClient
        import threading

        server = AudiostreamClient("localhost", 8000) #ip and port to connect to the server

        thread = threading.Thread(target = server.connect_client) #thread to connect to the server
        thread.start() #start the thread

        while True:
            input_ = input('Enter Quit To Exit : ')
            if input_ == 'quit' or input_ == 'exit':
                server.close_connection() #to close the connection with the server
                break
    
    screenshare streaming example:-
    
    client1.py
        from vidshare import Screenshareclient
        import threading

        server = Screenshareclient("localhost", 8000, quit_key = "q") #ip and port to connect to the server and quit_key which is used to quit the cv2 window

        thread = threading.Thread(target = server.connect_client) #thread to connect to the server
        thread.start() #start the thread

        while True:
            input_ = input('Enter Quit To Exit : ')
            if input_ == 'quit' or input_ == 'exit':
                server.close_connection() #to close the connection to the server
                break
    
    client2.py
        from vidshare import Screenshareclient
        import threading

        server = Screenshareclient("localhost", 8000, quit_key = "q") #ip and port to connect to the server and quit_key which is used to quit the cv2 window

        thread = threading.Thread(target = server.connect_client) #thread to connect to the server
        thread.start() #start the thread

        while True:
            input_ = input('Enter Quit To Exit : ')
            if input_ == 'quit' or input_ == 'exit':
                server.close_connection() #to close the connection to the server
                break
    
    camera client example:-

    client1.py
        from vidshare import CamerastreamClient
        import threading

        server = CamerastreamClient("localhost", 8000, camera = 0) #ip and port to connect to the server and camera to define camera number default is 0

        thread = threading.Thread(target = server.connect_client) #thread to connect to the server
        thread.start() #start the thread

        while True:
            input_ = input('Enter Quit To Exit : ')
            if input_ == 'quit' or input_ == 'exit':
                server.close_connection() #to close the connection to the server
                break
    
    client2.py
        from vidshare import CamerastreamClient
        import threading

        server = CamerastreamClient("localhost", 8000, camera = 0) #ip and port to connect to the server and camera to define camera number default is 0

        thread = threading.Thread(target = server.connect_client) #thread to connect to the server
        thread.start() #start the thread

        while True:
            input_ = input('Enter Quit To Exit : ')
            if input_ == 'quit' or input_ == 'exit':
                server.close_connection() #to close the connection to the server
                break
"""

# Setting up
setup(
    name="vidshare",
    version=VERSION,
    author="A.Jagan karthick",
    author_email="<jagankarthick2@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description = LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'Pillow', 'pyaudio', 'numpy'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)