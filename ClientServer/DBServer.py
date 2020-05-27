import ImportsFile
import socket
import select
from DatabaseItems.FingerprintDatabase import FingerprintDatabase
from DatabaseItems.Recording import Recording


class DatabaseServer:
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(("0.0.0.0", 8888))

        self.fingerprintDatabase = FingerprintDatabase()

        self.server_socket.listen(5)

        self.open_client_sockets = []
        self.messages_to_send = []

        self.recordingPath = r'C:\PythonProject2\Recordings\clientRecording.wav'

    def send_waiting_messages(self, wlist):

        for message in self.messages_to_send:
            (client_socket, data) = message
            if client_socket in wlist:
                print("data is" + data)
                data = data.encode('latin-1')
                client_socket.send(data);
                print("sent message")
                self.messages_to_send.remove(message)

    def updateTheWavFile(self, current_socket):

        with open(self.recordingPath, 'wb') as f:
            while True:

                m = current_socket.recv(1024)  # try to receive 100 bytes
                f.write(m)
                if not m:
                    print("finished because m is empty")
                    break
                if "finish" in m.decode('latin-1'):
                    print("finished successfully")
                    break

        searchResult = self.searchInDatabase() + "\n"
        current_socket.send(searchResult.encode('latin-1'))
        print("message sent")

    def run(self):
        print("server is up")
        while True:
            client_data_exist = False

            rlist, wlist, xlist = select.select([self.server_socket] + self.open_client_sockets, [], [])

            for current_socket in rlist:

                if current_socket is self.server_socket:

                    (new_socket, address) = self.server_socket.accept()

                    self.open_client_sockets.append(new_socket)

                else:
                    client_data_exist = True
                    data = current_socket.recv(1024)
                    data = data.decode('latin-1')

                    if data == "":
                        self.open_client_sockets.remove(current_socket)
                        print("Connection with client closed.")
                    elif str(data[:4]) == "file":
                        self.updateTheWavFile(current_socket)
            if client_data_exist:
                dummyrlist, wlist, xlist = select.select([], rlist, [], 0.1)
                self.send_waiting_messages(wlist)

    def showCollection(self):
        self.fingerprintDatabase.showCollection()

    def searchInDatabase(self):
        r = Recording(self.recordingPath)
        r.initializeAll()
        return self.fingerprintDatabase.searchInDatabase(r)


if __name__ == '__main__':
    server = DatabaseServer()
    server.showCollection()
    server.run()
