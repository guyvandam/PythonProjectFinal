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
        userName = data[4:12]
        pwd = data[12:20]

        s_rate, signal = wavefile.read(r'C:\PythonProject2\Songs\ClientRecording.wav')

        signal = signal.ravel()

        FFT = abs(scipy.fft(signal))

        freqs = fftpk.fftfreq(len(FFT), (1.0 / s_rate))

        maxfreq = freqs[range(len(FFT) // 2)][np.where(FFT[range(len(FFT) // 2)] == max(FFT[range(len(FFT) // 2)]))]
        print(freqs[range(len(FFT) // 2)][np.where(FFT[range(len(FFT) // 2)] == max(FFT[range(len(FFT) // 2)]))])
        ans = "max" + userName + pwd + str(int(maxfreq[0]))
        if (self.dbSocket == ""):
            print("no data base")
            return "error"
        else:
            self.dbSocket.send(ans.encode('latin-1'))
            data = self.dbSocket.recv(1024)
            data = data.decode('latin-1')

            return data

    def addSound(self, name, data):
        s_rate, signal = wavefile.read('C:\PythonProject2\Songs\ClientRecording.wav')

        signal = signal.ravel()

        FFT = abs(scipy.fft(signal))

        freqs = fftpk.fftfreq(len(FFT), (1.0 / s_rate))

        maxfreq = freqs[range(len(FFT) // 2)][np.where(FFT[range(len(FFT) // 2)] == max(FFT[range(len(FFT) // 2)]))]
        print(freqs[range(len(FFT) // 2)][np.where(FFT[range(len(FFT) // 2)] == max(FFT[range(len(FFT) // 2)]))])
        ans = "new" + data[3:19] + name + str(int(maxfreq[0]))
        if (self.dbSocket == ""):
            print("no data base")
            return "error"
        else:
            self.dbSocket.send(ans.encode('latin-1'))
            data = self.dbSocket.recv(1024)
            data = data.decode('latin-1')
            return data

    # def signup(self, info):
    #     if (self.dbSocket == ""):
    #         print("no data base")
    #         return "error"
    #     else:
    #         self.dbSocket.send(info.encode('latin-1'))
    #         data = self.dbSocket.recv(1024)
    #         data = data.decode('latin-1')
    #         print("signup data 122 " + data)
    #         return data
    #
    # def login(self, info):
    #     if (self.dbSocket == ""):
    #         print("no data base")
    #         return "error"
    #     else:
    #         self.dbSocket.send(info.encode('latin-1'))
    #         data = self.dbSocket.recv(1024)
    #         data = data.decode('latin-1')
    #         return data

    def actualWork(self):
        print("here")
        while True:
            client_data_exist = False

            rlist, wlist, xlist = select.select([self.server_socket] + self.open_client_sockets, [], [])
            '''rlist- readable  wlist-sendable  xlist-error '''

            for current_socket in rlist:

                if current_socket is self.server_socket:

                    (new_socket, address) = self.server_socket.accept()

                    self.open_client_sockets.append(new_socket)

                else:
                    # s_rate, signal = wavio.read(r'C:\Users\morgr\Desktop\\morSaved.wav')
                    client_data_exist = True
                    data = current_socket.recv(1024)
                    data = data.decode('latin-1')
                    print(str(data) + " 76")
                    print("160" + str(data[:6]))
                    # neccery but removes the client
                    if data == "":
                        self.open_client_sockets.remove(current_socket)
                        print("Connection with client closed.")

                    if str(data[:4]) == "file":
                        print("here 82")

                        with open(r'C:\PythonProject2\Songs\ClientRecording.wav', 'wb') as f:
                            print("opened")

                            while True:

                                m = current_socket.recv(1024)  # try to receive 100 bytes
                                f.write(m)
                                if not m:
                                    print("finished because no m")
                                    break
                                if "finish" in m.decode('latin-1'):
                                    print("finished in m")
                                    break

                            print(str(os.path.getsize(r'C:\PythonProject2\Songs\ClientRecording.wav')))

                            print("breaked")

                        print("finished adding file")

                        # if (os.path.exists(r'C:\Users\morgr\Desktop\morSaved.3gp')):
                        #     print("exists")
                        # else:
                        #     print("doesnt exist")
                        foundSound = self.checkMatch(data) + "\n"
                        print("ans 51: " + foundSound)
                        current_socket.send(foundSound.encode('latin-1'))
                        print("sent msg 157")

                    # elif str(data[:3]) == "new":
                    #     SoundName = data[19:]
                    #     print("here 156 " + SoundName)
                    #
                    #     with open(r'C:\PythonProject2\Songs\ClientRecording.wav', 'wb') as f:
                    #         print("opened")
                    #
                    #         while True:
                    #
                    #             m = current_socket.recv(1024)  # try to receive 100 bytes
                    #             f.write(m)
                    #             if not m:
                    #                 print("finished becouse no m")
                    #                 break
                    #             if "finish" in m.decode('latin-1'):
                    #                 print("finished in m")
                    #                 break
                    #
                    #         print(str(os.path.getsize(r'C:\PythonProject2\Songs\ClientRecording.wav')))
                    #
                    #         print("breaked")
                    #
                    #     print("finished adding file")
                    #
                    #     success = self.addSound(str(SoundName), data) + "\n"
                    #     print("ans 51: " + success)
                    #     current_socket.send(success.encode('latin-1'))
                    #     print("sent msg 157")
                    #
                    # elif (str(data[:5]) == "LogIn"):
                    #     print("in need to log in")
                    #     isSuccess = self.login(data) + "\n"
                    #     current_socket.send(isSuccess.encode('latin-1'))
                    #     # check if client exist
                    #
                    # elif (str(data[:6]) == "SignUp"):
                    #     print("in need to sign up")
                    #     print("self.signup(data)")
                    #     isSuccess = self.signup(data) + "\n"
                    #     print(isSuccess)
                    #     current_socket.send(isSuccess.encode('latin-1'))
                    #     print("succeed in send line 238")
                    #     # sign up new client
                    else:

                        print(data)
                        print("i was data")
                        self.digest((current_socket, data))

            if client_data_exist == True:
                dummyrlist, wlist, xlist = select.select([], rlist, [], 0.1)
                self.send_waiting_messages(wlist)


server = serverdb()
