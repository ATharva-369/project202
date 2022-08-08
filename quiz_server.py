import socket
from threading import Thread
import random

score = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8000
server.bind((ip_address,port))

server.listen()
clients = []
nicknames = []
questions = [
    "What other country, besides the US, uses the US dollar as its official currency?\na.Equador\n  b.Canada\n  c.Mexico \n d.United Kingdom",
    "The Statue of Liberty was a gift to the United States from which European country?\n a.Belgium\n b.Germany\n c.Spain\n d.France",
    "Which artist famously cut off his own ear?\n a.Vincent Van Gogh\n b.Claude Monet\n c.Salvador Dali\n d.Pablo Picasso",
     "The Mad Hatter and the Cheshire Cat are characters in which famous book?\n a.Winne-the-Pooh\n b.Charlotte's Web\n c.Charlie and the Chocolate Factory\n d.Alice In Wonderland"
]
answers = ["a","d","a","d"]

#remove question
def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def broadcast(message,connection):
    for client in clients:
        if client != connection:
            try: 
                client.send(message.encode('utf-8'))
            except :
                remove(client)    

# client thread function
def clientthread(conn,addr,nickname):
    global score
    conn.send('Welcome to trivia game!\n'.encode('utf-8'))
    conn.send('You will receieve a question that needs to be answered by choosing between a,b,c or d\n'.encode('utf-8'))
    conn.send('All the best!!\n'.encode('utf-8'))
    index , question , answer = get_random_qa(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            formattedMessage = message.split(':')[1].strip()
            if message:
                if formattedMessage == answer:
                    score += 1
                    conn.send((f"Bravo! Your score is {score} \n\n").encode('utf-8'))
                    remove_question(index)    
                    index, question , answer = get_random_qa(conn)
                else:
                    conn.send("Incorrect answer! Better luck next time\n\n".encode('utf-8'))
                    remove_question(index)    
                    index, question , answer = get_random_qa(conn)
            else : 
                remove(conn)    
                remove_nickname(nickname)
        except Exception as ar:
            print(ar)        

def remove_nickname(nickname):
    if(nickname in nicknames):
        nicknames.remove(nickname)
def remove(conn):
    if conn in clients:
        clients.remove(conn)
        
# get random question answer function
def get_random_qa(conn):
    global score
    if(len(questions) == 0):
        conn.send(f'Quiz is over! Your score is {score}'.encode('utf-8'))
        remove(conn)
    else:    
        rand_ind = random.randint(0,len(questions)-1)
        rand_ques = questions[rand_ind]
        rand_ans = answers[rand_ind]
        conn.send(rand_ques.encode('utf-8'))
        return rand_ind, rand_ques, rand_ans    

while True:
    conn,addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    clients.append(conn)
    nicknames.append(nickname)
    message = '{} joined the server!'.format(nickname)
    print(message)
    broadcast(message,conn)
    new_thread = Thread(target=clientthread, args=(conn,addr,nickname))
    new_thread.start()
