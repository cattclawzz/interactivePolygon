#Import Modules
import tkinter
from math import sqrt, atan, pi

#Make the window
window = tkinter.Tk()
canWidth,canHeight = 600,400
canvas = tkinter.Canvas(window, width=  canWidth, height=canHeight, bg='light grey')
canvas.pack()

#initialize variables
points = [[150,100],[50,300],[250,300],]
pointSize = 15
colours = [['#FF0000', '#00FF00', '#0000FF', '#FFFF00'],
           ['#990000', '#009900', '#000099', '#999900']]
shades = [0 for i in points]
plusButton = []

mouse = [0,0]
mouseDown = False
holding = 500

#Functions for formulas
def shoelace(points):
    '''Find the area of the polygon using the shoelace forumula'''
    total = 0
    for i in range (len(points)):
        ip1 = (i+1)%len(points)
        total += (points[ip1][0] + points[i][0]) * (points[ip1][1] - points[i][1])
    return round(abs(total/2))

def distance(x1,y1,x2,y2):
    '''Find the distance between 2 points'''
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def slope(x1,y1,x2,y2):
    '''find the slope of a line using y2-y1/x2-x1'''
    if x2 == x1:
        return 0
    else:
        return (y2-y1) / (x2-x1)

def perimeter(points):
    '''Find the perimeter by using the distance formulma on all of the points'''
    total = 0
    for i in range(len(points)):
        ip1 = (i+1)%len(points)
        total += distance(*points[i],*points[ip1])
    return round(total)

def angle(points, i):
    '''find angle using tan x = +/- m1-m2/1+m1m2 and converting radians to degrees'''
    ip1 = (i+1)%len(points)
    im1 = (i-1)%len(points)
    m1 = slope(*points[i], *points[im1])
    m2 = slope(*points[i], *points[ip1])
    
    radians = abs(atan((m1-m2)/(1+(m1*m2))))

    return round(radians*(180/pi))

#functions for mouse detection
def dragHandler(event):
    global mouse
    mouse = [event.x,event.y]
canvas.bind("<B1-Motion>", lambda event: dragHandler(event))

def mouseHandler(event,mouseStatus):
    global mouseDown, holding, mouse, shades, points, plusButton

    mouse = [event.x,event.y]
    mouseDown = mouseStatus
    if mouseStatus:
        for i in range(len(points)):
            if (points[i][0]-pointSize <= event.x <= points[i][0]+pointSize and
                points[i][1]-pointSize <= event.y <= points[i][1]+pointSize):
                holding = i
                shades[i] = 1
                break
    elif not mouseStatus:
        holding = 500
        shades = [0 for i in points]

    if (mouseStatus and 
        mouse[0]>= plusButton[0] and mouse[0]<= plusButton[2] and
        mouse[1]>= plusButton[1] and mouse[1]<= plusButton[3]):

        points.append([abs(points[0][0] + points[len(points)-1][0]),
                      abs(points[0][1] - points[len(points)-1][1])])
        shades = [0 for i in points]

canvas.bind("<Button>", lambda event: mouseHandler(event,True))
canvas.bind("<ButtonRelease>", lambda event: mouseHandler(event,False))

#main loop
def main_loop():
    global points, holding, plusButton
    canvas.delete("all")

    canvas.create_text(500, 50, text=str('Area: '+str(shoelace(points))), fill="black", font=('Helvetica 15'))
    canvas.create_text(500, 70, text=str('Perimeter: '+str(perimeter(points))), fill="black", font=('Helvetica 15'))

    for i in range(len(points)):
        canvas.create_text(500, 90+(i*20), text= str(points[i])+'   '+str(angle(points,i))+'°',
                           fill= colours[shades[i]][i % len(colours[0])],
                           font= ('Helvetica 15'))
        
    plusButton = [485, 85+((i+1)*20), 505, 105+((i+1)*20)]
    canvas.create_rectangle(*plusButton)
    canvas.create_text(495, 95+((i+1)*20), text= '+', fill= 'black', font= ('Helvetica 15'))

    canvas.create_polygon(*points, fill='light grey', outline='black')
    
    for i in range(len(points)): #draw points of the polygon
        canvas.create_oval(
            points[i][0] - pointSize, points[i][1] - pointSize,
            points[i][0] + pointSize, points[i][1] + pointSize,
            fill=colours[shades[i]][i % len(colours[0])])

    if holding != 500:
        for i in range(2):
            points[holding][i] = mouse[i]
        
    window.after(16, main_loop)

#run the loop
main_loop()
window.mainloop()