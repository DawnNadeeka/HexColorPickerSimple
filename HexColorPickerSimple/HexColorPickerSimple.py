'''Imports and Variables'''
import math, random
from tkinter import *

#colors for the GUI
colorLight = "#230D2B"
colorDark = "#792E60"
accentLight = "#C159A6"
accentMid = "#AB387D"
accentDark = "#5D1E53"

characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
mode = "RGB"

#starting colors (I would start with #FF0000, but if two variables start 
# at the same value it links their sliders for some reason)
R = random.randint(0, 255)
G = random.randint(0, 255)
B = random.randint(0, 255)

#These are set to 0 because they'll be updated to the random values right away
H = 0
S = 1
V = 2

'''Functions'''
def updateCircle(): #changes the circle color
    pen.itemconfig(circle, fill=hexCode)

def hexUpdate(x=1, y=2, z=3): #x, y, and z are useless variables to avoid an error I can't fix
    global hexCode
    global R
    global G
    global B
    global H
    global S
    global V
    correctCode = True
    if len(hexBox.get()) > 0 and len(hexBox.get()) == 7: #checks to make sure the code entered is a real code
        for i in range(len(hexBox.get())):
            testingHex = hexBox.get()[i].upper()
            if i == 0:
                if  testingHex != "#":
                    correctCode = False
            elif not testingHex in characters:
                correctCode = False
        if correctCode:
            hexCode = ""
            for i in hexBox.get():
                hexCode += i.upper()
                hexBox.delete(0, END)
                hexBox.insert(0, hexCode)

        #calculates RGB
        R = (characters.index(hexCode[1]) * 16) + characters.index(hexCode[2])
        G = (characters.index(hexCode[3]) * 16) + characters.index(hexCode[4])
        B = (characters.index(hexCode[5]) * 16) + characters.index(hexCode[6])
        #calculates HSV
        RGBList = [(R / 255.0), (G / 255.0), (B / 255.0)]
        cMax = max(RGBList)
        cMin = min(RGBList)
        delta = cMax - cMin

        if delta == 0:
            H = 0
        elif cMax == RGBList[0]:
            H = ((RGBList[1] - RGBList[2]) / delta)
            if RGBList[1] < RGBList[2]:
                H += 6
            H *= 60
        elif cMax == RGBList[1]:
            H = 60 * (((RGBList[2] - RGBList[0]) / delta) + 2)
        elif cMax == RGBList[2]:
            H = 60 * (((RGBList[0] - RGBList[1]) / delta) + 4)
        
        if cMax == 0:
            S = 0
        else:
            S = (delta / cMax) * 100
        V = cMax * 100

        if mode == "RGB": #sets the right sliders
            sliderR.set(R)
            sliderG.set(G)
            sliderB.set(B)
        else:
            sliderH.set(H)
            sliderS.set(S)
            sliderV.set(V)
        updateCircle()

def RGBUpdate(x, random = False): #same as above, x is useless
    global hexCode
    global R
    global G
    global B

    if random == False:
        R = sliderR.get()
        G = sliderG.get()
        B = sliderB.get()

    #Calculates the hex code based off of RGB
    hexCode = "#" + (characters[math.floor(R / 16)]) + (characters[int(((R / 16) - math.floor(R / 16)) * 16)]) + (characters[math.floor(G / 16)]) + (characters[int(((G / 16) - math.floor(G / 16)) * 16)]) + (characters[math.floor(B / 16)]) + (characters[int(((B / 16) - math.floor(B / 16)) * 16)])
    hexBox.delete(0, END)
    hexBox.insert(0, hexCode)
    updateCircle()

def HSVUpdate(x, random=False): #same as above, x is useless
    global hexCode
    global H
    global S
    global V
    global R
    global G
    global B

    #calculates HSV from RGB (there is no way to go straight to Hex that I could find)
    if random == False:
        H = sliderH.get()
        S = sliderS.get()
        V = sliderV.get()
    C = ((V / 100) * (S / 100))
    HPrime = H / 60
    m = (V / 100) - C
    X = C * (1 - abs(math.fmod(HPrime, 2) - 1))
    if HPrime <= 1:
        RGBList = [C, X, 0]
    elif HPrime <= 2:
        RGBList = [X, C, 0]
    elif HPrime <= 3:
        RGBList = [0, C, X]
    elif HPrime <= 4:
        RGBList = [0, X, C]
    elif HPrime <= 5:
        RGBList = [X, 0, C]
    elif HPrime <= 6:
        RGBList = [C, 0, X]
    R = (RGBList[0] + m) * 255
    G = (RGBList[1] + m) * 255
    B = (RGBList[2] + m) * 255

    hexCode = "#" + (characters[math.floor(R / 16)]) + (characters[int(((R / 16) - math.floor(R / 16)) * 16)]) + (characters[math.floor(G / 16)]) + (characters[int(((G / 16) - math.floor(G / 16)) * 16)]) + (characters[math.floor(B / 16)]) + (characters[int(((B / 16) - math.floor(B / 16)) * 16)])
    hexBox.delete(0, END)
    hexBox.insert(0, hexCode)
    updateCircle()

def swapModes(): #alters between the two modes: RGB, and HSV
    global mode
    if mode == "RGB":
        mode = "HSV"
        modeButton["text"] = "RGB"
        sliderR.place_forget()
        sliderG.place_forget()
        sliderB.place_forget()

        sliderH.place(x=50, y=75)
        sliderS.place(x=50, y=125)
        sliderV.place(x=50, y=175)
        sliderH.set(H)
        sliderS.set(S)
        sliderV.set(V)

        labelTop["text"] = "H"
        labelMid["text"] = "S"
        labelBottom["text"] = "V"
    else:
        mode = "RGB"
        modeButton["text"] = "HSV"
        sliderH.place_forget()
        sliderS.place_forget()
        sliderV.place_forget()

        sliderR.place(x=50, y=75)
        sliderG.place(x=50, y=125)
        sliderB.place(x=50, y=175)
        sliderR.set(R)
        sliderG.set(G)
        sliderB.set(B)

        labelTop["text"] = "R"
        labelMid["text"] = "G"
        labelBottom["text"] = "B"

def randomColor():
    global R
    global G
    global B
    global H
    global S
    global V
    global hexCode
    if mode == "RGB":
        R = random.randint(0, 255)
        G = random.randint(0, 255)
        B = random.randint(0, 255)
        RGBUpdate(0, True)
        updateCircle()
        sliderR.set(R)
        sliderG.set(G)
        sliderB.set(B)
    else:
        H = random.randint(0, 360)
        S = random.randint(0, 100)
        V = random.randint(0, 100)
        HSVUpdate(0, True)
        sliderH.set(H)
        sliderS.set(S)
        sliderV.set(V)
    hexBox.delete(0, END)
    hexBox.insert(0, hexCode)

'''code'''
#create canvas
master = Tk() #create new window or "canvas" called "master"
master.title("Hex Color Picker") #window title
master.configure(bg = colorLight, bd=10)
master.resizable(False, False) #disables resize screen
pen = Canvas(master, width=480, height=330, bg=colorLight, highlightbackground=colorLight)
pen.pack()

#buttons
modeButton = Button(master, command=swapModes, text="HSV", font=("KBCloudyDay", 12), bd=0, bg=accentMid, padx=10, pady=10, fg=accentDark, activebackground=accentDark, activeforeground=accentMid, width=5)
modeButton.place(x=65, y=285)
randomButton = Button(master, command=randomColor, text="Random", font=("KBCloudyDay", 12), bd=0, bg=accentMid, padx=10, pady=10, fg=accentDark, activebackground=accentDark, activeforeground=accentMid, width=5)
randomButton.place(x=155, y=285)
quitButton = Button(master, command=master.destroy, text="Quit", font=("KBCloudyDay", 8), bd=0, bg=accentMid, padx=10, pady=10, fg=accentDark, activebackground=accentDark, activeforeground=accentMid, width=5)
quitButton.place(x=343, y=290)

#labels/text in window
canvasTitle = Label(master, text="Hex Color Picker", font=("KBCloudyDay", 18), fg=colorDark, bg=colorLight)
canvasTitle.place(x=5) #pack has to be separate for some reason; else will break
version = Label(master, text="v.1.0 Feb. 2021", font=("KBCloudyDay", 8), anchor="center", fg=colorDark, bg=colorLight) #Version and date updated
version.place(x=225, y=10)
author = Label(master, text="By Raya Ronaghy", font=("KBCloudyDay", 10), anchor="center", fg=colorDark, bg=colorLight) #Author name
author.place(x=20, y=30)

hexText = Label(master, text="Hex code:", font=("KBCloudyDay", 12), anchor="center", fg=colorDark, bg=colorLight) #displays how many cells are on the board
hexText.place(x=20, y=235)

labelTop = Label(master, text="R", font=("KBCloudyDay", 14), anchor="center", fg=colorDark, bg=colorLight)
labelTop.place(x=20, y=85)
labelMid = Label(master, text="G", font=("KBCloudyDay", 14), anchor="center", fg=colorDark, bg=colorLight)
labelMid.place(x=20, y=135)
labelBottom = Label(master, text="B", font=("KBCloudyDay", 14), anchor="center", fg=colorDark, bg=colorLight)
labelBottom.place(x=20, y=185)

#Creates circle
circle = pen.create_oval(275, 50, 475, 250, fill="#000000", outline="#FFFFFF", width=3) #draws center circle

#RGB sliders
sliderR = Scale(master, variable=R, font=("KBCloudyDay", 12), length = 200, command=RGBUpdate, from_=0, to=255, orient=HORIZONTAL, bg=accentMid, fg=accentDark, bd=0, activebackground=accentLight, troughcolor=accentDark)
sliderR.place(x=50, y=75)
sliderG = Scale(master, variable=G, font=("KBCloudyDay", 12), length = 200, command=RGBUpdate, from_=0, to=255, orient=HORIZONTAL, bg=accentMid, fg=accentDark, bd=0, activebackground=accentLight, troughcolor=accentDark)
sliderG.place(x=50, y=125)
sliderB = Scale(master, variable=B, font=("KBCloudyDay", 12), length = 200, command=RGBUpdate, from_=0, to=255, orient=HORIZONTAL, bg=accentMid, fg=accentDark, bd=0, activebackground=accentLight, troughcolor=accentDark)
sliderB.place(x=50, y=175)
sliderR.set(R)
sliderG.set(G)
sliderB.set(B)

#HSV sliders
sliderH = Scale(master, variable=H, font=("KBCloudyDay", 12), length = 200, command=HSVUpdate, from_=0, to=360, orient=HORIZONTAL, bg=accentMid, fg=accentDark, bd=0, activebackground=accentLight, troughcolor=accentDark)
sliderS = Scale(master, variable=S, font=("KBCloudyDay", 12), length = 200, command=HSVUpdate, from_=0, to=100, orient=HORIZONTAL, bg=accentMid, fg=accentDark, bd=0, activebackground=accentLight, troughcolor=accentDark)
sliderV = Scale(master, variable=V, font=("KBCloudyDay", 12), length = 200, command=HSVUpdate, from_=0, to=100, orient=HORIZONTAL, bg=accentMid, fg=accentDark, bd=0, activebackground=accentLight, troughcolor=accentDark)

#Hex box
tracer = StringVar()
tracer.trace_add("write", hexUpdate)
hexBox = Entry(master, width=10, font=("KBCloudyDay", 12), bd=0, bg=accentMid, fg=accentDark, textvariable=tracer)
hexBox.place(x=110, y=237)

RGBUpdate(0)
updateCircle()
hexBox.insert(0, hexCode)

mainloop() #is used for Tkinter