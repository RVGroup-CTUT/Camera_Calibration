import cv2
import numpy as np
import serial
from time import sleep
import serial.tools.list_ports
from tkinter import *
from PIL import ImageTk, Image

#def get_ports():
    #ports = serial.tools.list_ports.comports()
    #return ports
#def findArduino(portsFound):
    #commPort = 'None'
    #numConnection = len(portsFound)
    #for i in range(0, numConnection):
        #port = foundPorts[i]
        #strPort = str(port)
        #if ' ' in strPort:
            #splitPort = strPort.split(' ')
            #commPort = (splitPort[0])
    #return commPort
#foundPorts = get_ports()
#connectPort = findArduino(foundPorts)
#aa = serial.Serial(connectPort, 115200)

# aa = serial.Serial('COM4', 115200)
cap = img = obj = grabResult = frame = []
nObj = 0
Px = Py = Or = 0.0
s = 0
h = 1

cap = cv2.VideoCapture(0)
#Tạo cửa sổ laàm việc
root1 = Tk()
root1.title("LUẬN VĂN TỐT NGHIỆP")
root1.geometry('1300x770')
root1.config(bg="white")
# Thêm logo Trường
logo = cv2.imread('Logo ctuet.png')
logo = cv2.resize(logo, (200, 200))
logo = cv2.cvtColor(logo, cv2.COLOR_BGR2RGB)
img = Image.fromarray(logo)
img = ImageTk.PhotoImage(image=img)
imglabel = Label(root1, image=img)
imglabel.place(x=0, y=0)
# Thêm logo Khoa KTCK
logo1 = cv2.imread('Logo_khoa ktck.jpg')
logo1 = cv2.resize(logo1, (195, 195))
logo1 = cv2.cvtColor(logo1, cv2.COLOR_BGR2RGB)
img1 = Image.fromarray(logo1)
img1 = ImageTk.PhotoImage(image=img1)
img1label = Label(root1, image=img1)
img1label.place(x=1095, y=0)
# Thêm các label
tentruong = Label(root1, text="TRƯỜNG ĐẠI HỌC KỸ THUẬT - CÔNG NGHỆ CẦN THƠ", bg='white', font=('Time 25 bold'))
tentruong.pack(side=TOP)
a = Label(root1, text="      ", bg='white', font=('Time 5 bold'))
a.pack(side=TOP)
khoa = Label(root1, text="KHOA KỸ THUẬT CƠ KHÍ", bg='white', font=('Time 25 bold'))
khoa.pack(side=TOP)
b = Label(root1, text="      ", bg='white', font=('Time 5 bold'))
b.pack(side=TOP)
hocphan = Label(root1, text="LUẬN VĂN TỐT NGHIỆP ĐẠI HỌC", bg='white', font=('Time 20 bold'))
hocphan.pack(side=TOP)
c = Label(root1, text="    ", bg='white', font=('Time 28 bold'))
c.pack(side=TOP)
detai = Label(root1, text="XÂY DỰNG VÀ ĐIỀU KHIỂN", bg='white', fg='red', font=('Time 30 bold'))
detai.pack(side=TOP)
detai = Label(root1, text="MÔ HÌNH ROBOT SONG SONG DELTA", bg='white', fg='red', font=('Time 30 bold'))
detai.pack(side=TOP)
detai = Label(root1, text="PHÂN LOẠI SẢN PHẨM DỰA TRÊN XỬ LÝ ẢNH", bg='white', fg='red', font=('Time 30 bold'))
detai.pack(side=TOP)
toado = Label(root1, text="TỌA ĐỘ", bg='white', fg='blue', font=('Time 18 bold'))
toado.place(x=690, y=420)
toadox = Label(root1, text="X", bg='yellow', fg='black', width=5, height=1, font=('Time 20 bold'))
toadox.place(x=630, y=470)
toadoy = Label(root1, text="Y", bg='yellow', fg='black', width=5, height=1, font=('Time 20 bold'))
toadoy.place(x=750, y=470)
x = Label(root1, text=0, width=5, height=1, bg='white', fg='black', font=('Time 20 bold'))
x.place(x=630, y=520)
y = Label(root1, text=0, width=5, height=1, bg='white', fg='black', font=('Time 20 bold'))
y.place(x=750, y=520)
mausac = Label(root1, text="LOẠI SẢN PHẨM", bg='white', fg='blue', font=('Time 18 bold'))
mausac.place(x=640, y=565)
disc = Label(root1, text='', bg='white', fg='black', font=('Time 18 bold'), width=30,anchor='center')
disc.place(x=510, y=610)
svth = Label(root1, text="SINH VIÊN THỰC HIỆN", width=20, height=1, bg='white', fg='blue', font=('Time 18 bold'))
svth.place(x=950, y=435)
ten = Label(root1, text="Lâm Tuấn Lực", width=14, height=1, bg='white', font=('Time 14 bold'))
ten.place(x=1015, y=470)
mssv = Label(root1, text="1800001", width=18, height=1, bg='white', font=('Time 14 bold'))
mssv.place(x=990, y=505)
cbhd = Label(root1, text="GIẢNG VIÊN HƯỚNG DẪN", width=20, height=1, bg='white', fg='blue', font=('Time 18 bold'))
cbhd.place(x=950, y=565)
cbhd1 = Label(root1, text="ThS. Huỳnh Minh Vũ", width=20, height=1, bg='white', font=('Time 14 bold'))
cbhd1.place(x=975, y=605)

hinhanh = Label(root1, text="CAMERA", width=25, height=1, bg='white', fg='dark orange', font=('Time 22 bold'))
hinhanh.place(x=60, y=420)
canvas = Canvas(root1, width=480, height=226, bg="white")
canvas.place(x=50, y=488)

def image():
    global cap, img12,  image2, frame1, image2, canvas, image, root1,frame01,frame123
    ret, img12 = cap.read()
    img12 = cv2.resize(img12, (480, 490))
    frame123 = img12[148:374, 0:480]
    frame01 = img12[142:370, 0:190] #[142:380, 0:190]
    cv2.imshow('123', frame01)
    frame1 = cv2.cvtColor(frame123, cv2.COLOR_BGR2RGB)
    image2 = ImageTk.PhotoImage(image=Image.fromarray(frame1))
    canvas.create_image(0, 0, image=image2, anchor=NW)
    root1.after(15, image)
def imgProccessing():
    global nObj, obj, frame01, Objects, x, y,root1,img
    Objects = []
    min_area = 7000
    max_area = 100000
    image = cv2.cvtColor(frame01, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([0, 90, 142])
    upper_hsv = np.array([255, 255, 255])
    mask_hsv = cv2.inRange(image, lower_hsv, upper_hsv)
    contours, hierachy = cv2.findContours(mask_hsv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        find_obj = len(approx)
        print(find_obj)
        if find_obj == 4:
            ob = 2
        elif find_obj == 3:
            ob = 1
        else:
            ob = 0
        area = cv2.contourArea(contour)
        if (area > min_area) & (area < max_area):
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            Objects.append([cX, cY, ob])
    nObj = len(Objects)
    if nObj:
        def X(elem):
            return elem[1]
        Objects.sort(key=X, reverse=True)
        def X(elem):
            return elem[0]
        Objects.sort(key=X, reverse=True)
        obj = Objects[0]

def convertCoordinates():
    global obj, Px, Py, Ob
    k = 0.36
    osX = -100
    osY = 25
    Px = obj[1] * k + osX
    Py = obj[0] * k + osY
    Ob = obj[2]

def sendData():
    global Px, Py, Pz, Ob, x, y, disc
    Pz = -293
    Tx = 'o' + ' ' + str(int(Px)) + ' ' + str(int(Py)) + ' ' + str(int(Pz)) + ' ' + str(int(Ob)) + '\r'
    Tx = Tx.encode()
    print(Tx)
    #aa.write(Tx)
    #aa.flush()
    if Ob == 0:
        text_c = 'HÌNH TRÒN'
    elif Ob == 1:
        text_c = 'HÌNH TAM GIÁC'
    elif Ob == 2:
        text_c = 'HÌNH VUÔNG'
    disc.config(text=text_c)
    x.config(text=int(Px))
    y.config(text=int(Py))
def ad():
    global s, h, nObj, ad, root1
    if s:
        imgProccessing()
        if nObj:
            convertCoordinates()
            sendData()
            s = 0
            h = 0
        else:
            s = 1
            if ~h:
                #aa.write(b'h\r')
                h = 1
            sleep(0.001)
    root1.after(15, ad)
#def receiverData():
 #   global s,root1,receiverData
  #  if (aa.in_waiting > 0):
   #     Rx = aa.readline()
    #    Rx = Rx.decode()
     #   Rx = Rx.rstrip()
      #  if Rx == 's1': s = 1
   # root1.after(15, receiverData)
try:
    #receiverData()
    image()
    imgProccessing()
    ad()
except KeyboardInterrupt:
    cap.release()
    cv2.destroyAllWindows()
    #aa.close()
root1.mainloop()
