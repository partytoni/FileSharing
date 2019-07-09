import time
from tkinter import *
from tkinter.filedialog import askopenfilename
import socket
import os
import math
import threading
import base64
#client method to send the file

CONSTANT = 1024*8
SEND_SEMAPHORE=threading.Semaphore()
LISTEN_SEMAPHORE=threading.Semaphore()
listen_t = None
send_t = None

DEBUG=True

def send_thread():
    ret = SEND_SEMAPHORE.acquire(timeout=1)
    if (ret==False):
        print("Send already in progress.")
        return

    pathname=filename_client_label.cget("text")
    try:
        f = open(pathname, "rb")
    except:
        SEND_SEMAPHORE.release()
        return
    size = os.path.getsize(pathname)

    #filename has only the name of the file, while pathname has full path /Volumes/...


    #byte contains each read of CONSTANT bytes
    byte = f.read(CONSTANT)

    host = ip_client_text.get()
    port = int(port_client_text.get())

    if (DEBUG):
        port = 4000
        host = '127.0.0.1'

    send_client_percentage_label.config(text="0%")

    percentage = 0
    times = 0

    mySocket = socket.socket()
    try:
        mySocket.connect((host, port))
        mySocket.send((filename_client_label.cget("text").split("/")[-1]).encode())
        mySocket.close()
    except:
        SEND_SEMAPHORE.release()
        return

    

    mySocket = socket.socket()
    try:
        mySocket.connect((host, port))
        while byte:
        mySocket.send(byte)
        times += 1
        current_percentage = math.floor(((times*CONSTANT)/size)*100)
        if current_percentage > percentage:
            send_client_percentage_label.config(text=str(percentage)+"%")
            percentage += 1

        #reads next sequence of bytes
        byte = f.read(CONSTANT)

        send_client_percentage_label.config(text="Done.")
        #close the socket when you are done
        mySocket.close()
        SEND_SMAPHORE.release()
    except:
        mySocket.close()
        SEND_SEMAPHORE.release()
        return


    

def send():
    send_t = threading.Thread(target=send_thread)
    send_t.start()

def listen_thread():
    ret = LISTEN_SEMAPHORE.acquire(timeout=1)
    if (ret == False):
        print("Listen already in progress.")
        return

    listening_server_label.config(text="Listening")
    host="127.0.0.1"
    port = int(port_server_text.get())

    if (DEBUG):
        port=4000

    mySocket = socket.socket()
    mySocket.bind((host, port))

    #first connection sends file name
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    data = conn.recv(1024)
    filename = data.decode()
    print("The file name is ",filename)
    conn.close()

    #second connection receives the file. I know, it sucks, but it works.
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    listening_server_label.config(text="Receiving")

    if (os.path.isfile(filename)):
        #TODO show dialog
    f = open(filename, "wb")
    while True:
        data = conn.recv(CONSTANT)
        if not data:
            break
        f.write(data)

    listening_server_label.config(text="Done")

    conn.close()
    LISTEN_SEMAPHORE.release()


def listen():
    if (LISTEN_SEMAPHORE._value==1):
        listen_t = threading.Thread(target=listen_thread)
        listen_t.start()

def choose():
    filename = askopenfilename()
    filename_client_label.config(text=filename)
    

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

#root definition
root = Tk()
client_or_server_var = IntVar()

#server definitions of elements
server_frame = Frame(root)
ip_server_label = Label(server_frame, text="Your IP address is "+IPAddr)
port_server_label = Label(server_frame, text="Port: ")
port_server_text = Entry(server_frame, highlightbackground="grey")
filename_server_label = Label(server_frame, text="Filename: ")
filename_server_text = Entry(server_frame, highlightbackground="grey")
listen_server_button = Button(server_frame, text="Listen", command=listen)
listening_server_label = Label(server_frame, text="")

#client definition of elements
client_frame = Frame(root)
ip_client_label = Label(client_frame, text="Server's IP address: ")
ip_client_text = Entry(client_frame, highlightbackground="grey")
port_client_label = Label(client_frame, text="Port: ")
port_client_text = Entry(client_frame, highlightbackground="grey")
send_client_button = Button(client_frame, text="Send", command=send)
send_client_percentage_label = Label(client_frame, text="")
filename_client_label = Label(client_frame, text = "No selected file.")
choose_file_client_button = Button(client_frame, text="Choose file", command=choose)

#server packing
ip_server_label.grid(row=0, column=0, columnspan=2)
port_server_label.grid(row=1, column=0)
port_server_text.grid(row=1, column=1)
listen_server_button.grid(row=2,column=0)
listening_server_label.grid(row=2, column=1)


#client packing
ip_client_label.grid(row=0, column=0)
ip_client_text.grid(row=0, column=1)
port_client_label.grid(row=1, column=0)
port_client_text.grid(row=1, column=1)
filename_client_label.grid(row=2,column=0)
choose_file_client_button.grid(row=2,column=1)
send_client_percentage_label.grid(row=3, column=0)
send_client_button.grid(row=3,column=1)




# 0 is for the server, 1 for the client 
def client_or_server_func():
    value = client_or_server_var.get()

    # server
    if value == 0:
        client_frame.pack_forget()
        server_frame.pack()

    else:
        server_frame.pack_forget()
        client_frame.pack()


def main():
    client_or_server_frame = Frame(root)
    client_or_server_label = Label(
        client_or_server_frame, text="Choose client to send the file or server to receive it.")
    client_radio = Radiobutton(client_or_server_frame, text="client",
                               variable=client_or_server_var, value=1, command=client_or_server_func)
    server_radio = Radiobutton(client_or_server_frame, text="server",
                               variable=client_or_server_var, value=0, command=client_or_server_func)

    client_or_server_label.pack(side=LEFT)
    client_radio.pack(side=LEFT)
    server_radio.pack(side=LEFT)
    client_or_server_frame.pack()
    client_or_server_func()
    root.mainloop()


if __name__ == '__main__':
    main()



'''
HOW TO KILL A THREAD

def do_work(id, stop):
    print("I am thread", id)
    while True:
        print("I am thread {} doing something".format(id))
        if stop():
            print("  Exiting loop.")
            break
    print("Thread {}, signing off".format(id))


def main():
    stop_threads = False
    workers = []
    for id in range(0, 3):
        tmp = threading.Thread(target=do_work, args=(id, lambda: stop_threads))
        workers.append(tmp)
        tmp.start()
    time.sleep(3)
    print('main: done sleeping; time to stop the threads.')
    stop_threads = True
    for worker in workers:
        worker.join()
    print('Finis.')
'''
