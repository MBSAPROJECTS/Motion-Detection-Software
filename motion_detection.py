# created by m.b.sai aditya (student at nitk surathkal)
from tkinter import Button,Label,Tk,mainloop
from tkinter import messagebox,filedialog  
from ctypes import windll
from tkinter.constants import LEFT
import win32gui
from cv2 import imshow,resize,cvtColor,dilate,absdiff,GaussianBlur,threshold,findContours,boundingRect,contourArea,rectangle,waitKey,VideoCapture,destroyAllWindows,COLOR_BGR2GRAY,THRESH_BINARY,RETR_TREE,CHAIN_APPROX_SIMPLE
user32 = windll.user32

def MotionDetect(input):
    def windowEnumerationHandler(hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    cap=VideoCapture(input)
    ret,frame1=cap.read()
    ret,frame2=cap.read()
    top_windows = []
    while cap.isOpened():
        frame=frame1
        frame = resize(frame, (500, 500))
        imshow("Original Video",frame)
        diff=absdiff(frame1,frame2)
        gray=cvtColor(diff,COLOR_BGR2GRAY)
        blur=GaussianBlur(gray,(5,5),0)
        _,thresh=threshold(blur,20,255,THRESH_BINARY)
        dilated=dilate(thresh,None,iterations=3)
        contours,_=findContours(dilated,RETR_TREE,CHAIN_APPROX_SIMPLE)
        for contour in contours:
            (x,y,w,h)=boundingRect(contour)
            if(contourArea(contour)<2000): # 2000 metre square 
                continue
            rectangle(frame1,(x,y),(x+w,y+h),(0,25,45),3)
        frame1 = resize(frame1, (500, 500))
        frame__=frame1
        imshow("Motion Detection",frame1)
        frame1=frame2
        _,frame2=cap.read()
        key = waitKey(10)
        if key == ord('q') or key == ord('Q'):
            MsgBox = messagebox.askquestion ('Exit Application','Are you sure you want to close the Videos',icon = 'warning')
            if MsgBox=='yes':
                break
            else:
                win32gui.EnumWindows(windowEnumerationHandler, top_windows)
                for i in top_windows:
                    if 'Original Video' in i[1]:
                        win32gui.ShowWindow(i[0],5)
                        win32gui.SetForegroundWindow(i[0])
                pass   
        if key == ord('p') or key == ord('P'):
            def windowEnumerationHandler(hwnd, top_windows):
                top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
            messagebox.showinfo("Paused", "Click OK & then click on any button to unpause!!")
            # top_windows = []
            win32gui.EnumWindows(windowEnumerationHandler, top_windows)
            for i in top_windows:
                if 'Original Video' in i[1]:
                    win32gui.ShowWindow(i[0],5)
                    win32gui.SetForegroundWindow(i[0])
            waitKey(-1)
        if _==False:
            messagebox.showinfo("COMPLETED", "Video Completed!!!Choose Another!")
            break
    destroyAllWindows()
    cap.release()
base = Tk()
base.title('Motion Detection Software')
base.configure(bg='#A8FFA8')
width = str(int((user32.GetSystemMetrics(0))/2.7));
height = str(int((user32.GetSystemMetrics(1))/5));
base.geometry(width+'x150+0+0')
# img = Image.open("capture.PNG") 
# img = img.resize((150, 50),Image.ANTIALIAS)
# loadImage =  ImageTk.PhotoImage(img)
def video_file_opener():
    input = filedialog.askopenfile(initialdir="/",mode ='r',filetypes =[('Python Files', '*.mp4')],title='Choose a Video File ')
    if input is not None:
       name=input.name
       name.replace("/","\\")
       MotionDetect(name)
x = Button(base, text ='MOTION DETECTION', command = lambda:video_file_opener(),bg='#30ff60',fg='black')
x.config(font=("HELVETICA BOLD",16))
x.place(x=150,y=(user32.GetSystemMetrics(1)/10))
label = Label(base, text = "Some Important Intructions:-\n1.Use 'p' button on your keyboard to pause the video & then press any key to upause the video\n2.Use 'q' button on your keyboard to close the video windows\n3.Only Choose .mp4 Videos!!!", fg = "black",justify=LEFT,bg='#A8FFA8')  
label.config(font=("Courier bold",10))
label.place(x=10,y=(user32.GetSystemMetrics(1)/100))
base.resizable(False, False)
mainloop()











