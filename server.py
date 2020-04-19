import socket
from thread import *
import random
import sys
import time
import select


PORT = 1234
IP = "127.0.0.1"


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((IP, PORT))
s.listen(100)

sent_questions = []
client_list = []
buzzer = [0, 0, 0]
client = ["client_socket_address", "index_in_client_list"]
score_counter = []

question_list = []

for i in range(100):
    question_list.append(str(i))

answers = []
for i in range(100):
    answers.append(str(i))

def show_all_clients(msg):
    for clnt in client_list:
        try:
            clnt.send(msg)
        except:
            clnt.close()
            client_list.remove(clnt)

def check_in_list(k):
    for i in range(len(sent_questions)):
        if(k == sent_questions[i]):
            return 0
    return 1

def send_question(conn):
    k = random.randint(0,10000)%len(question_list)
    while(check_in_list(k) != 1):
        k = random.randint(0,10000)%len(question_list)
    buzzer[1] = k
    sent_questions.append(k)
    for clnt in client_list:
        clnt.send(question_list[k])








def stop():
    show_all_clients("Quiz is finished\n")
    #i = score_counter.index(max(score_counter))
    #show_all_clients("Player " + str(i+1) + "wins!!Their score is " + str(score_counter[i]) + "Points ")
    s.close()
    sys.exit()


def main_fun(conn, addr):
    i = 0
    conn.send("The ultimate quiz of all time is finally here!!!!\nThe moment you've all been waiting for\nRules:For each question if you know the answer press the buzzer You have 10 secs to press the buzzer..Do that by pressing any key on the key board and then pressing enter...and then enter the answer..In our case the answer is the question itself...You will be given 10 secs to answer\nThe first person to press the buzzer get to answer....\n")
    no_of_question = 0
    while True:
        flag10 = 0

        start_time1 = time.time()
        msg = conn.recv(2048)
        while(time.time() - start_time1 < 10):
            if(msg):

                if buzzer[0] == 0:
                    
                    client[0] = conn
                    i = 0
                    while(conn!=client_list[i]):
                        i+=1
                        if(i == len(client_list)):
                            break
                    '''while i < len(client_list):
                        if client_list[i] == client[0]:
                            break
                        i+=1'''
                    client[1] = int(i)
                    conn.send("Buzzed\n")
                    buzzer[0] = 1
                    flag10 = 1
                    break

                elif( conn!=client[0]):

                    
                    conn.send("Player " + str(client[1]+1) + " has pressed the buzzer first")
                    
                    flag10 = 1
                    break

                elif buzzer[0] == 1 and conn == client[0]:
                    print msg
                    
                    check_answer(conn, i, msg, no_of_question)
                    flag10 = 1
                    break




            else:
                msg = conn.recv(2048)

        if(flag10 == 0):
            if(buzzer[0] == 0):
                show_all_clients("Time limit to buzz over\n")
                send_question(conn)
            elif(buzzer[0] == 1 and conn == client[0]):
                show_all_clients("Time limit to ans over\n")
                buzzer[0] = 0
                send_question(conn)
            else:
                conn.send("Player " + str(client[1]+1) + " has pressed the buzzer first")








def check_answer(conn, i, msg, no_of_question):
    if((len(answers[buzzer[1]]) == 1 and msg[0] == answers[buzzer[1]][0]) or (len(answers[buzzer[1]]) == 2 and msg[1] == answers[buzzer[1]][1] and msg[0] == answers[buzzer[1]][0])):
        show_all_clients("Player " + str(client[1]+1) + "'s score has increased by 1\n")
        score_counter[i]+=1
        if(score_counter[i]>=5):
            show_all_clients("Player " + str(client[1]+1) + " WINS!!!")
            stop()
            sys.exit()
    else:
        show_all_clients("Player " + str(client[1]+1) + " loses a point\n")
        score_counter[i] = float(score_counter[i])
        score_counter[i]-=(0.5)
        
    buzzer[0] = 0
    no_of_question += 1
    if(no_of_question == 50 ):
        show_all_clients("Its a draw!!!\n")
        s.close()
        sys.exit()


    if(len(question_list)!= 0):
        answers.pop(buzzer[1])
        question_list.pop(buzzer[1])
    else:
        stop()
    send_question(conn)



while True:
    conn, address = s.accept()
    score_counter.append(0)
    client_list.append(conn)
    print address[0] + " connected"
    start_new_thread(main_fun, (conn, address))
    if(len(client_list) == 3):
        send_question(conn)

conn.close()
s.close()
