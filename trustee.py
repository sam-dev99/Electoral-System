from socket import *
from phe import paillier
import pickle


public_key, private_key = paillier.generate_paillier_keypair()

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('127.0.0.1',serverPort))
serverSocket.listen()

print("the public key is : ",public_key)



i = 0

#accept 9 connections from 9 different voters
while(i < 9):
    conn, addr = serverSocket.accept()

    #sending the public key to the client as a byte_string stream instead of an object.
    data_string = pickle.dumps(public_key)

    conn.send(data_string)

    conn.close()

    i = i + 1

#accept from server a TCP connection
j = 0
while(j < 1):
    conn, addr = serverSocket.accept()

    #recieve the encrypted sum of votes from the server
    encryptedData = conn.recv(4096)

    encryptedSum = pickle.loads(encryptedData)

    decryptedSum = private_key.decrypt(encryptedSum)

    sumLen = len(str(decryptedSum))

    decryptedSum_string = str(decryptedSum)
    candidates = []

    for i in range(sumLen):
        candidateVote = decryptedSum_string[-1]
        candidates.append(candidateVote)

        decryptedSum_string = decryptedSum_string[:(sumLen-1)]
        sumLen = sumLen - 1

        print(decryptedSum_string)

    print(candidates)


    string_candidates = pickle.dumps(candidates)
    conn.send(string_candidates)

    conn.close()

    j = j + 1



serverSocket.close()





