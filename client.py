import socket
from threading import Thread
import random
from tkinter import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8000
server.connect((ip_address,port))

print("Connected with the server...")

class GUI:

    self.clients = []
    self.nicknames = []
    self.questions = [
        "What other country, besides the US, uses the US dollar as its official currency?\na.Equador\n  b.Canada\n  c.Mexico \n d.United Kingdom",
        "The Statue of Liberty was a gift to the United States from which European country?\n a.Belgium\n b.Germany\n c.Spain\n d.France",
        "Which artist famously cut off his own ear?\n a.Vincent Van Gogh\n b.Claude Monet\n c.Salvador Dali\n d.Pablo Picasso",
        "The Mad Hatter and the Cheshire Cat are characters in which famous book?\n a.Winne-the-Pooh\n b.Charlotte's Web\n c.Charlie and the Chocolate Factory\n d.Alice In Wonderland"
                    ]
    self.answers = ["a","d","a","d"]   
    self.score = 0

    def __init__(self):
        self.window = Tk()
        self.window.withdraw()
        self.login = Toplevel()
        self.login.title('Login')
        self.login.resizable(width = False, height = False)
        self.login.configure(width = 400, height = 300)
        self.pls = Label(self.login,text="Please login to continue",justify = CENTER, font = 'Helvetica 14 bold')
        self.pls.place(relheight = 0.15, relx = 0.2, rely = 0.07)
        self.labelName = Label(self.login, text = 'Name', font = 'Helvetica 12')
        self.labelName.place(relheight = 0.2, relx = 0.1, rely = 0.2)
        self.entryName = Entry(self.login, font = 'Helvetica 14')
        self.entryName.place(relwidth=0.4, relheight = 0.12 , relx = 0.35, rely = 0.2)
        self.entryName.focus()
        self.loginButton = Button(self.login, text="Login", font = 'Helvetica 12', command= lambda : self.goahead(self.entryName.get()))
        self.loginButton.place(relx = 0.4, rely = 0.55)
        self.window.mainloop()


    # client thread function
    def clientthread(self,conn,addr,nickname):
        global score
        conn.send('Welcome to trivia game!\n'.encode('utf-8'))
        conn.send('You will receieve a question that needs to be answered by choosing between a,b,c or d\n'.encode('utf-8'))
        conn.send('All the best!!\n'.encode('utf-8'))
        self.index , self.question , self.answer = self.get_random_qa(conn)
        while True:
            try:
                self.message = conn.recv(2048).decode('utf-8')
                self.formattedMessage = message.split(':')[1].strip()
                if self.message:
                    if self.formattedMessage == answer:
                        score += 1
                        conn.send((f"Bravo! Your score is {score} \n\n").encode('utf-8'))
                        self.remove_question(index)    
                        self.index, self.question , self.answer = self.get_random_qa(conn)
                    else:
                        conn.send("Incorrect answer! Better luck next time\n\n".encode('utf-8'))
                        self.remove_question(index)    
                        self.index, self.question , self.answer = self.get_random_qa(conn)
                else : 
                    self.remove(conn)    
                    self.remove_nickname(nickname)
            except Exception as ar:
                print(ar)      


    # get random question answer function
    def get_random_qa(self,conn):
        global score
        if(len(self.questions) == 0):
            conn.send(f'Quiz is over! Your score is {score}'.encode('utf-8'))
            self.remove(conn)
        else:    
            self.rand_ind = random.randint(0,len(questions)-1)
            self.rand_ques = questions[rand_ind]
            self.rand_ans = answers[rand_ind]
            conn.send(rand_ques.encode('utf-8'))
            return self.rand_ind, self.rand_ques, self.rand_ans    
    
    def remove_nickname(self,nickname):
        if(nickname in self.nicknames):
            self.nicknames.remove(nickname)

    def remove(conn):
        if conn in self.clients:
            self.clients.remove(conn)         

    def goahead(self,name):
        self.login.destroy()
        self.name = name
        rcv = Thread(target = self.receive)
        rcv.start()    


    def receive(self): 
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    server.send(self.name.encode('utf-8'))
                else:
                    print(message)
            except:
                print("An error occured!")
                server.close()
                break

    def write(self):
        while True:
            message = '{}: {}'.format(self.name, input(''))
            client.send(message.encode('utf-8'))    

    def remove_question(index):
        self.questions.pop(index)
        self.answers.pop(index)

    def broadcast(message,connection):
        for client in self.clients:
            if client != connection:
                try: 
                    client.send(message.encode('utf-8'))
                except :
                    self.remove(client)             

g = GUI()