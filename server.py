from socket import *

import pickle


serverPort = 11000
trusteePort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind(('',serverPort))
serverSocket.listen(1)

accumulator = 0

i = 0
#accept connections from different clients (max 9)
while(i < 9):
    connectionSocket, addr = serverSocket.accept()

    print("accepted connection from client: ",addr)

    #recieve the encrypted vote from the client
    encryptedData = connectionSocket.recv(4096)

    encryptedVote = pickle.loads(encryptedData)

    #add the vote to the accumulator that will then be sent to the trustee for decryption
    accumulator = accumulator + encryptedVote

    connectionSocket.close()

    i = i + 1


serverSocket.close()

#open a new connection between the server and the trustee
serverSocket2 = socket(AF_INET,SOCK_STREAM)
serverSocket2.connect(('127.0.0.1',trusteePort))

#send the encrypted sum
encryptedData = pickle.dumps(accumulator)
serverSocket2.send(encryptedData)

string_candidates = serverSocket2.recv(4096)

'''recieve the decrypted sum as a list where the first element represents the number votes 
   for the first candidate, i.e "Donald Trump" and so on...
'''
candidates = pickle.loads(string_candidates)

print(candidates)

#a dictionary that represents the number of votes each candidate got.
list_of_candidates = {"Donald Trump":0,"Roger Federer":0,"Britney Spears":0,"Dalai Lama":0,"Steve Jobs":0}

winner = ""
votes = 0

for candidate in list_of_candidates:
    if(len(candidates) > 0):
        list_of_candidates[candidate] = candidates.pop(0)

for candidate in list_of_candidates:
    vote = list_of_candidates.get(candidate)
    if(int(vote) >= votes):
        votes = int(vote)
        winner = candidate
    

print(votes,winner)

serverSocket2.close()



