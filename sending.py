from tkinter import Tk as graphic
from tkinter import *
from tkinter import filedialog
import socket as connected
import random
import struct
import time
import sys
import tqdm

import os


window=graphic()
window.title("File")
window.geometry("520x350")
window.resizable(False,False)

#server create
server=connected.socket(connected.AF_INET,connected.SOCK_STREAM)
server2=connected.socket(connected.AF_INET,connected.SOCK_STREAM)
server3=connected.socket(connected.AF_INET,connected.SOCK_STREAM)
#
server_send2=connected.socket(connected.AF_INET,connected.SOCK_STREAM)
server_send3=connected.socket(connected.AF_INET,connected.SOCK_STREAM)
port=1011
conn=(connected.gethostname(),port)


class graphic_process:
    def __init__(self,window):
        self.file_name=StringVar()
        self.file=Entry(window,bd=0.8,font="20",textvariable=self.file_name)  
        self.file.place(relx=0.01,rely=0.2,height=25,width=390)
        #open file:
        self.file_open=Button(window,text="Open File",font="22",bd=0.9,command=self.file_show)
        self.file_open.place(relx=.8,rely=.2,width=75,height=25)
    def window_file(self):
        self.value=filedialog.askopenfilename(initialdir="/",title="Select File",filetypes=(("All Files","*.*"),("","")))
        return self.value

    def file_show(self):
        get_value=self.window_file()
        self.file_name.set(get_value)    
    def send_close(self):
        close=Button(window,text="Close",bd=1.5,font="22",command=exit)
        close.place(relx=.6,rely=.8,width=85,height=30)
        

_graphic_class=graphic_process(window)
_graphic_class.send_close()
#file type
class file_type():
    def __init__(self):
        self.numbers=IntVar()
        self.numbers2=IntVar()
        self.png=Radiobutton(window,text="png",font="22",variable=self.numbers,value=1)
        self.png.place(relx=.1,rely=.4)
        self.jpg=Radiobutton(window,text="jpg",font="22",value=2,variable=self.numbers)
        self.jpg.place(relx=.2,rely=.4)
        self.exe=Radiobutton(window,text="exe",font="22",value=3,variable=self.numbers)
        self.exe.place(relx=.3,rely=.4)

_file_names=file_type()

def get_file():
        
    file_number=random.randint(10,1000)
    text=Text(window,fg="red",font="20")
    text.place(relx=.01,rely=.5,width=510,height=100)
    try:
        if(_file_names.numbers.get()==1):
            server.connect(conn)
            run="{}:{} Connect".format(*server.getsockname())
            packing=get_file_part(server,struct.calcsize("!I"))
            size=struct.unpack("!I",packing)[0]
            data=get_file_part(server,size)
            #
            file_png=open("Png-File\\image-"+str(file_number)+".png","wb")
            file_png.write(data)
            text.insert(INSERT,run)
            time.sleep(.1)
            text.insert(INSERT,"\nSuccess: 100%")
           
            
        elif(_file_names.numbers.get()==2):
            server2.connect(conn)
            run2="{}:{} Connect".format(*server2.getsockname())
            packing2=get_file_part(server2,struct.calcsize("!I"))
            size2=struct.unpack("!I",packing2)[0]
            data2=get_file_part(server2,size2)
            #
            file_jpg=open("Jpg-File\\image-"+str(file_number)+".jpg","wb")
            file_jpg.write(data2)
            text.insert(INSERT,run2)
            time.sleep(.1)
            text.insert(INSERT,"\nSuccess: 100%")
            
        elif(_file_names.numbers.get()==3):
            server3.connect(conn)
            run3="{}:{}\n Connect".format(*server3.getsockname())
            packing3=get_file_part(server3,struct.calcsize("!I"))
            size3=struct.unpack("!I",packing3)[0]
            data3=get_file_part(server3,size3)
            #
            get_exe=open("Exe-File\\app-"+str(file_number)+".exe","wb")
            get_exe.write(data3)
            text.insert(INSERT,run3)
            time.sleep(.1)
            text.insert(INSERT,"\nSuccess: 100%")
        else:
            text.insert(INSERT,"Erorr: System...!")
    except:
        text.insert(INSERT,"Erorr: Connect...!")
        exit()


def get_file_part(get_data,size):
    data_byte=bytearray()
    while len(data_byte)<size:
        data_all=get_data.recv(size-len(data_byte))
        data_byte.extend(data_all)
    #bytes
    return bytes(data_byte)

    
    
class file_send:
    def __init__(self):
            #send File
            self.send=Button(window,text="Send",bd=1.5,font="22",command=self.send_file)
            self.send.place(relx=.8,rely=.8,width=85,height=30)
            #get File
            self.get_file=Button(window,text="Get File",bd=1.5,font="22",command=get_file)
            self.get_file.place(relx=.4,rely=.8,width=85,height=30)
    #socket and file include
    def send_file(self):
        text=Text(window,fg="red",font="20")
        text.place(relx=.01,rely=.5,width=510,height=100)
        file_value=_graphic_class.file_name.get()
        try:
            
            server.bind(conn)
            server.listen(5)
            runed="{}:{} Send\nSuccess: 100%".format(*server.getsockname())
            (sending,ip)=server.accept()
            with open(str(file_value),"rb") as f_data:
                cor=f_data.read()
            size_data=struct.pack("!I",len(cor))
            line_data=size_data+cor
            text.insert(INSERT,runed)
            while True:
                sending.send(line_data)
                break
            
        except:
            text.insert(INSERT,"Erorr: System and Connect")
        if(file_value==""):
            text.insert(INSERT,"\nNo: File")
try:
    os.mkdir("Png-File")
    os.mkdir("Jpg-File")
    os.mkdir("Exe-File")
    file_send()
except:
    file_send()

window.mainloop()

