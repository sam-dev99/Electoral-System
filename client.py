from socket import *
from phe import paillier
import pickle

serverName = '127.0.0.1'
port1 = 12000
port2 = 11000
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,port1))


public = clientSocket.recv(4096)

public_key = pickle.loads(public)

print("Your public key is of type: ",public_key)


clientSocket.close()

print("for more than 1 vote, separate by comma:\n")
print("0 for Donald Trump\n")
print("1 for Roger Federer\n")
print("2 for Britney Spears\n")
print("3 for Dalai lama\n")
print("4 for Steve Jobs\n")

x=input()

y = x.split(",")

if (x == ""):
    vote = 0

else:
    vote = 0
    for i in y:
        vote = vote + 10 ** int(i)

encryptedVote = public_key.encrypt(vote)

clientSocket2 = socket(AF_INET,SOCK_STREAM)
clientSocket2.connect((serverName,port2))

encryptedData = pickle.dumps(encryptedVote)

clientSocket2.send(encryptedData)





