from tkinter import *
import time
import sys
import random
#(c)Matt-C-Games 2014
tk=Tk()
canvas=Canvas(tk,width=960,height=600,highlightthickness=0,bd=0,bg='lightblue')
canvas.pack()
tk.title('Westie Run')
tk.wm_attributes('-topmost',1)
class Log:
    def __init__ (self,canvas):
        self.canvas=canvas
        self.logs=self.canvas.create_oval(910,350,960,400,fill='brown')
        self.circle=self.canvas.create_oval(920,360,950,390,fill='brown')
        self.line=self.canvas.create_line(920,360,950,390,fill='black')
        self.grass=self.canvas.create_polygon(0,400,960,400,960,600,0,600,fill='green')
    def draw(self):
        self.canvas.move(self.logs,-4,0)
        self.canvas.move(self.circle,-4,0)
        self.canvas.move(self.line,-4,0)
        self.logspos=self.canvas.coords(self.logs)
        self.circlepos=self.canvas.coords(self.circle)
        self.linepos=self.canvas.coords(self.line)
        tk.update()
        if self.logspos[2]<=0:
           self.canvas.delete(self.logs)
           self.canvas.delete(self.circle)
           self.canvas.delete(self.line)
           self.logs=self.canvas.create_oval(910,350,960,400,fill='brown')
           self.circle=self.canvas.create_oval(920,360,950,390,fill='brown')
           self.line=self.canvas.create_line(920,360,950,390,fill='black')
           tk.update()
class Westie:
    def __init__ (self,canvas,log):
        self.canvas=canvas
        self.log=log
        self.westie=self.canvas.create_oval(0,0,100,30,fill='white')
        self.leg1=self.canvas.create_line(10,25,10,50,fill='white')
        self.leg2=self.canvas.create_line(80,25,80,50,fill='white')
        self.head=self.canvas.create_oval(70,-30,110,5,fill='white')
        self.tail=self.canvas.create_line(-30,10,0,10,fill='white')
        self.canvas.move(self.leg1,100,350)
        self.canvas.move(self.leg2,100,350)
        self.canvas.move(self.head,100,350)
        self.canvas.move(self.tail,100,350)
        self.canvas.move(self.westie,100,350)
        self.y=0
        self.started=False
        tk.update()
        self.canvas.bind_all('<KeyPress-Up>',self.fly)
        self.canvas.bind_all('<KeyPress-Down>',self.land)
        self.canvas.bind_all('<Button-1>',self.start)
        self.canvas.bind_all('<KeyPress-f>',self.pause)
        self.westiepos=self.canvas.coords(self.westie)
        self.flyplane=canvas.create_rectangle(960,190,980,210,fill='red')
        self.plane=self.canvas.coords(self.flyplane)
        self.instructions=self.canvas.create_text(0,0,anchor=NW,text='How to play:\nUse the up and down arrow keys to move the dog.\nAvoid logs and flying debris.\nClick to begin.\nPress "f" to pause.\nTry to get the highest score possible!',font=('Times',30),fill='red',state='normal')
        self.text=self.canvas.create_text(480,300,text='Paused\nClick to Play',font=('Times',30),fill='orange',state='hidden')
        self.t1=0
        self.tq=0
        self.score=0
        self.scoreboard=canvas.create_text(930,0,anchor=N,text=self.score,font=('Times',30),fill='orange')
    def pause(self,evt):
        if self.started==True:
            self.canvas.itemconfig(self.text,state='normal')
            self.started=False
            self.tq+=time.time()-self.t1
    def start(self,evt):
        self.started=True
        self.canvas.itemconfig(self.instructions,state='hidden')
        self.canvas.itemconfig(self.text,state='hidden')
        self.t1=time.time()
    def fly(self,evt):
        self.y=-1
    def land(self,evt):
        self.y=1
    def draw(self):
        self.difference=time.time()-self.t1
        self.score=int(self.difference+self.tq)
        self.canvas.itemconfig(self.scoreboard,text=self.score)
        self.canvas.move(self.leg1,0,self.y)
        self.canvas.move(self.leg2,0,self.y)
        self.canvas.move(self.head,0,self.y)
        self.canvas.move(self.tail,0,self.y)
        self.canvas.move(self.westie,0,self.y)
        self.legpos=self.canvas.coords(self.leg1)
        if self.legpos[3]>400:
            self.y=0
            self.canvas.move(self.leg1,0,400-self.legpos[3])
            self.canvas.move(self.leg2,0,400-self.legpos[3])
            self.canvas.move(self.head,0,400-self.legpos[3])
            self.canvas.move(self.tail,0,400-self.legpos[3])
            self.canvas.move(self.westie,0,400-self.legpos[3])
        self.headpos=self.canvas.coords(self.head)
        if self.headpos[1]<=150:
            self.canvas.move(self.leg1,0,150-self.headpos[1])
            self.canvas.move(self.leg2,0,150-self.headpos[1])
            self.canvas.move(self.head,0,150-self.headpos[1])
            self.canvas.move(self.tail,0,150-self.headpos[1])
            self.canvas.move(self.westie,0,150-self.headpos[1])
            self.y=1
        self.westiepos=self.canvas.coords(self.westie)
        if self.westiepos[2]>=self.log.logspos[0]and self.legpos[3]>=self.log.logspos[1]and self.westiepos[0]<=self.log.logspos[0]:
            canvas.create_text(480,300,anchor=CENTER,text='Ouch. That hurt!',font=('Times',30),fill='red')
            canvas.create_text(480,400,anchor=CENTER,text='Score: %s pts'%(self.score),font=('Times',30),fill='red')
            tk.update()
            time.sleep(3)
            sys.exit('Score: %s pts'%(self.score))
        self.plane=self.canvas.coords(self.flyplane)
        self.canvas.move(self.flyplane,-5,0)
        if self.plane[2]<0:
            self.flyplane=canvas.create_rectangle(960,150,980,170,fill='red')
        if self.headpos[2]>=self.plane[0]and self.headpos[1]<=self.plane[3]and self.headpos[0]<=self.plane[2]or self.westiepos[2]>=self.plane[0]and self.westiepos[1]<=self.plane[3]and self.westiepos[0]<=self.plane[2]:
            canvas.create_text(480,300,anchor=CENTER,text='Ouch. That hurt!',font=('Times',30),fill='red')
            canvas.create_text(480,400,anchor=CENTER,text='Score: %s pts'%(self.score),font=('Times',30),fill='red')
            tk.update()
            time.sleep(3)
            sys.exit('Score: %s pts'%(self.score))

log=Log(canvas)
westie=Westie(canvas,log) 
while 1:
    if westie.started==True:
        log.draw()
        westie.draw()
    time.sleep(0.003)
    tk.update_idletasks()
    tk.update()

