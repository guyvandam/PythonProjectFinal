import ImportsFile
import socket
import select
from DatabaseItems.FingerprintDatabase import FingerprintDatabase
from DatabaseItems.Recording import Recording


class DatabaseServer:
    def __init__(self, port):
        self.serverSocket = socket.socket()
        self.serverSocket.bind(("0.0.0.0", port))

        self.fingerprintDatabase = FingerprintDatabase()

        self.serverSocket.listen(5)

        self.openClientSockets = []
        self.messagesToSend = []

        self.recordingPath = r'C:\PythonProject2\Recordings\clientRecording.wav'

    """
    function name: sendWaitingMessages.
    input: wlist - a list of writeable socket.
    output: N/A
    operation: loops through the input list and sends the messages in the 'messagesToSend' list if the socket is 
    writable
    """

    def sendWaitingMessages(self, wlist):

        for message in self.messagesToSend:
            (client_socket, data) = message
            if client_socket in wlist:
                print("data is" + data)
                data = data.encode('latin-1')
                client_socket.send(data);
                print("sent message")
                self.messagesToSend.remove(message)

    """
    function name: updateTheWavFile.
    input: currentSocket, the current socket that needs attention.
    output: the result of the search.
    operation: updates the 'clientRecording.wav' file, and searches the database to find the information about the 
    recording. 
    """

    def updateTheWavFile(self, currentSocket):

        with open(self.recordingPath, 'wb') as f:
            while True:

                m = currentSocket.recv(1024)  # try to receive 100 bytes
                f.write(m)
                if not m:
                    print("finished because m is empty")
                    break
                if "finish" in m.decode('latin-1'):
                    break

        searchResult = self.searchInDatabase() + "\n"
        currentSocket.send(searchResult.encode('latin-1'))

    """
    function name: run.
    input: N/A
    output: N/A
    operation: runs the server, channels the clients.
    """

    def run(self):
        print("server is up")
        while True:
            client_data_exist = False

            rlist, wlist, xlist = select.select([self.serverSocket] + self.openClientSockets, [], [])

            for current_socket in rlist:

                if current_socket is self.serverSocket:

                    (new_socket, address) = self.serverSocket.accept()

                    self.openClientSockets.append(new_socket)

                else:
                    client_data_exist = True
                    data = current_socket.recv(1024)
                    data = data.decode('latin-1')

                    if data == "":
                        self.openClientSockets.remove(current_socket)
                    elif str(data[:4]) == "file":
                        self.updateTheWavFile(current_socket)
            if client_data_exist:
                dummyrlist, wlist, xlist = select.select([], rlist, [], 0.1)
                self.sendWaitingMessages(wlist)

    """
    function name: showCollection.
    input: N/A
    output: N/A
    operation: prints the MongoDB collection, our database.
    """

    def showCollection(self):
        self.fingerprintDatabase.showCollection()

    """
    function name: searchInDatabase.
    input: N/A
    output: the result of the search in the database.
    operation: calls the 'searchInDatabase' function of the FingerprintDatabase object with a recording associated 
    with the 'clientRecording.wav' file"""

    def searchInDatabase(self):
        r = Recording(self.recordingPath)
        r.initializeAll()
        return self.fingerprintDatabase.searchInDatabase(r)


if __name__ == '__main__':
    port = 8888
    server = DatabaseServer(port)
    server.run()
