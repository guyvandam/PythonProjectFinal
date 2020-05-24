import os.path
import select
import socket

import numpy as np
import scipy
import scipy.fftpack as fftpk
import scipy.io.wavfile as wavefile


class serverdb():
    def __init__(self):
        self.server_socket = socket.socket()

        # self.server_socket.bind(("10.0.0.6", 8888))
        self.server_socket.bind(("0.0.0.0", 8888))
        # self.server_socket.bind(("192.168.43.174", 8888))

        self.server_socket.listen(5)

        self.open_client_sockets = []
        self.messages_to_send = []
        self.dbSocket = ""

        self.actualWork()

    def send_waiting_messages(self, wlist):

        for current_socket in wlist:
            for message in self.messages_to_send:
                (client_socket, data) = message
                print("line 26: data is" + data)
                print("line 27: data[0]==1" + str(data[0] == str(1)))
                data = message[1].encode('latin-1')
                print("sent:" + data.decode('latin-1'))
                if data[0] == str(1):
                    print("sent to db" + data)
                    self.dbSocket.send(data)
                else:
                    client_socket.send("i got from you".encode('latin-1') + data);
                print("sent")
                self.messages_to_send.remove(message)

    def digest(self, info):

        (current_socket, data) = info
        print("data 41:" + str(data))
        if data == "IMDATABASE":
            self.dbSocket = current_socket
            print("data base connected")
        elif data == "":
            print("no data")
        elif data[0] == 1:
            print("trying to send to db")
            self.messages_to_send.append((self.dbSocket, data))

        else:
            self.messages_to_send.append(info)
            print(data)

    def checkMatch(self, data):
        ans = "max"
        if self.dbSocket == "":
            print("'dbsocket' is an empty string.")
            return "db socket was empty"
        else:
            print("===== IN THE 'ELSE' OF 'CHECKMATCH' =====")
            self.dbSocket.send(ans.encode('latin-1'))
            data = self.dbSocket.recv(1024)
            data = data.decode('latin-1')

            return data

    def sreachInDatabase(self):
        return "'searchInDatabase' is still empty"

    def updateTheWavFile(self, current_socket):
        print("ENTERED updateTheWavFile")

        with open(r'C:\PythonProject2\Songs\ClientRecording.wav', 'wb') as f:
            print("opened the ClientRecording file...")

            while True:

                m = current_socket.recv(1024)  # try to receive 100 bytes
                f.write(m)
                if not m:
                    print("finished m was empty")
                    break
                if "finish" in m.decode('latin-1'):
                    print("'finish' was in the data../finished in m")
                    break

            print("size of the new file ",
                  str(os.path.getsize(r'C:\PythonProject2\Songs\ClientRecording.wav')))

        print("finished adding the file, now searching the database")
        answer = self.searchInDatabase()
        print("finished searching the database")
        current_socket.send(answer.encode('latin-1'))
        print("sent the message")
        print("EXITING updateTheWavFile")

    def actualWork(self):
        print("server is up...")
        while True:
            client_data_exist = False

            rlist, wlist, xlist = select.select([self.server_socket] + self.open_client_sockets, [], [])
            '''rlist- readable  wlist-sendable  xlist-error '''

            for current_socket in rlist:

                if current_socket is self.server_socket:

                    (new_socket, address) = self.server_socket.accept()

                    self.open_client_sockets.append(new_socket)

                else:
                    client_data_exist = True
                    data = current_socket.recv(1024)
                    data = data.decode('latin-1')
                    print("data: ", str(data))
                    # neccery but removes the client
                    if data == "":
                        self.open_client_sockets.remove(current_socket)
                        print("Connection with client closed.")

                    elif str(data[:4]) == "file":
                        self.updateTheWavFile(current_socket)
                        # print("data started with 'file'")
                        #
                        # with open(r'C:\PythonProject2\Songs\ClientRecording.wav', 'wb') as f:
                        #     print("opened the ClientRecording file...")
                        #
                        #     while True:
                        #
                        #         m = current_socket.recv(1024)  # try to receive 100 bytes
                        #         f.write(m)
                        #         if not m:
                        #             print("finished m was empty")
                        #             break
                        #         if "finish" in m.decode('latin-1'):
                        #             print("'finish' was in the data../finished in m")
                        #             break
                        #
                        #     print("size of the new file ",
                        #           str(os.path.getsize(r'C:\PythonProject2\Songs\ClientRecording.wav')))
                        #
                        # print("finished adding the file")
                        # answer = self.searchInDatabase()
                        # print("finished with 'checkMatch")
                        # current_socket.send(answer.encode('latin-1'))
                        # print("sent the message")
                    else:
                        print("=====NEEDED DIGEST=====")
                        print("data: ", data)
                        self.digest((current_socket, data))

            if client_data_exist:
                dummyrlist, wlist, xlist = select.select([], rlist, [], 0.1)
                self.send_waiting_messages(wlist)


server = serverdb()
