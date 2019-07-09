from tkinter import *
from tkinter.filedialog import askopenfilename
import socket
import os
import math
import threading

#client method to send the file

CONSTANT = 1024*8
SEND_SEMAPHORE=threading.Semaphore()
LISTEN_SEMAPHORE=threading.Semaphore()
listen_t = None
send_t = None

def send_thread():
    ret = SEND_SEMAPHORE.acquire(timeout=1)
    if (ret==False):
        print("Send already in progress.")
        return

    filename=filename_client_label.cget("text")
    f = open(filename, "rb")
    size = os.path.getsize(filename)

    #byte contains each read of CONSTANT bytes
    byte = f.read(CONSTANT)

    host = ip_client_text.get()
    port = int(port_client_text.get())


    send_client_percentage_label.config(text="0%")

    percentage = 0
    times = 0

    mySocket = socket.socket()
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
    SEND_SEMAPHORE.release()

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

    mySocket = socket.socket()
    mySocket.bind((host, port))

    mySocket.listen(1)
    conn, addr = mySocket.accept()
    listening_server_label.config(text="Receiving")

    f = open("server.mp4", "wb")
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
send_client_button.grid(row=3,column=0,columnspan=2)
send_client_percentage_label.grid(row=3, column=1)




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
