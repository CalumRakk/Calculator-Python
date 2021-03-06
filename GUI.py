from tkinter import Entry, Button, Tk, StringVar, Frame, N, S, E, W, NE,END
from tkinter.font import BOLD   
import Calculator
from Calculator import isSign, isOperator

def isDisplayConcatenable(key,displayText):
    
    # Si el último digito de display es un digito o es igual a cero, key tiene que ser un digito, operador o punto.
    # Si el último digito de display es un un punto, key tiene que ser un digito.
    # Si el último digito de display es un operador, key tiene que ser un digito.
    lastDigit= displayText[-1]
    if lastDigit.isdigit() or lastDigit=="0":
        if key.isdigit():
            return True
        elif key==".":
            return True
        elif isOperator(key):
            return True        
    elif lastDigit==".":
        if key.isdigit():
            return True
    elif isOperator(lastDigit) and not isSign(lastDigit):
        if key.isdigit():
            return True
        if isSign(key):
            return True
    elif isSign(lastDigit):
        if key.isdigit():
            return True

    return False
def isDisplayReplaceable(key,displayText):
    if displayText == "0":
        if key.isdigit() or isSign(key):
            return True
    elif displayText=="Result too large":
        return True
    return False
def send_key(key,target):
    display,entryVar= target
    displayText=entryVar.get()
    
    if isDisplayReplaceable(key,displayText):
        entryVar.set(key)  
    elif isDisplayConcatenable(key,displayText):
        entryVar.set(displayText + key)
          
   
    display.xview(END)    
def displayWarning(target):
    display,entryVar= target
    root.after(100)
    display.configure(foreground="black")
def equals_key(target):
    display, entryVar= target
    
    displayText= entryVar.get()
    lastDigit= displayText[-1]
    if lastDigit.isdigit():
        try:
            result= Calculator.operate_expression(displayText)
            
            entryVar.set(result)
            display.xview(END)
        except:
            display.configure(foreground="red")
            root.after(1, lambda: displayWarning(target))  
    else:
        display.configure(foreground="red")
        root.after(1, lambda: displayWarning(target))   
def ac_key(target):
    display, entryVar= target
    entryVar.set("0")
    display.xview(END)
class Application(Frame):
    def __init__(self, parent):        
        self.parent = parent
        Frame.__init__(self, parent)
        self.parent.maxsize(400, 550)
        self.parent.minsize(290, 500)
        
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        
        
        mainframe = Frame(self.parent)
        mainframe.columnconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=1)
        mainframe.columnconfigure(2, weight=1)
        mainframe.columnconfigure(3, weight=1) 
        
        mainframe.rowconfigure(0, weight=2)
        mainframe.rowconfigure(1, weight=2)
        mainframe.rowconfigure(2, weight=2)
        mainframe.rowconfigure(3, weight=2) 
        mainframe.rowconfigure(4, weight=2) 
        mainframe.rowconfigure(5, weight=2)         
        
        mainframe.grid(column=0, row=0,columnspan=3, rowspan=3, sticky=(N, W, E, S), padx=10,pady=15 )
        
        # Display and row 0
        entryVar= StringVar(value="0")
        display= Entry(mainframe,textvariable=entryVar, font=("Verdana", 22, ), bd = 3,
                      state='readonly',
                      cursor="arrow",
                      justify="right",

        )
        display.grid(row=0, column=0,columnspan=4, sticky=(W, E),ipady=3)     
        target= (display, entryVar)


        # Buttons
        fontsize= 14
        width=2
        bd= 0
        fgDigits="#00A3F5"
        fgAC= "#E8AF21"
        fgOperators="#AD63FF"
        sticky=E+W+N+S   
        font=("Verdana", fontsize,)    
        
        row=1
        Button(mainframe, text="AC", command=lambda: ac_key(target),fg=fgAC,font=font, bd=bd, width=width).grid(row=row, column=0,sticky=sticky, columnspan=2)
        Button(mainframe, text="%", command=lambda: send_key("%",target),fg=fgOperators, font=font, bd=bd,width=width).grid(row=row, column=2,sticky=sticky)
        Button(mainframe, text="^", command=lambda: send_key("^",target),fg=fgOperators, font=font, bd=bd, width=width).grid(row=row, column=3,sticky=sticky)
        row=2
        Button(mainframe, text="/", command=lambda: send_key("/",target),fg=fgOperators, font=font, bd=bd,width=width).grid(row=row, column=3,sticky=sticky)
        Button(mainframe, text="9", command=lambda: send_key("9",target),fg=fgDigits, font=font, bd=bd, width=width).grid(row=row, column=2,sticky=sticky)
        Button(mainframe, text="8", command=lambda: send_key("8",target),fg=fgDigits, font=font, bd=bd, width=width).grid(row=row, column=1,sticky=sticky)
        Button(mainframe, text="7", command=lambda: send_key("7",target),fg=fgDigits, font=font, bd=bd, width=width).grid(row=row, column=0,sticky=sticky)
        row=3
        Button(mainframe, text="*", command=lambda: send_key("*",target),fg=fgOperators, font=font, bd=bd, width=width).grid(row=row, column=3,sticky=sticky)
        Button(mainframe, text="6", command=lambda: send_key("6",target),fg=fgDigits, font=font, bd=bd, width=width).grid(row=row, column=2,sticky=sticky)
        Button(mainframe, text="5", command=lambda: send_key("5",target),fg=fgDigits, font=font, bd=bd, width=width).grid(row=row, column=1,sticky=sticky)
        Button(mainframe, text="4", command=lambda: send_key("4",target),fg=fgDigits, font=font, bd=bd, width=width).grid(row=row, column=0,sticky=sticky)
        row=4
        Button(mainframe, text="-", command=lambda: send_key("-",target),fg=fgOperators, font=font, bd=bd, width=width).grid(row=row, column=3,sticky=sticky)
        Button(mainframe, text="3", command=lambda: send_key("3",target),fg=fgDigits, font=font, bd=bd, width=width).grid(row=row, column=2,sticky=sticky)
        Button(mainframe, text="2", command=lambda: send_key("2",target),fg=fgDigits, font=font, bd=bd, width=width).grid(row=row, column=1,sticky=sticky)
        Button(mainframe, text="1", command=lambda: send_key("1",target),fg=fgDigits, font=font, bd=bd, width=width).grid(row=row, column=0,sticky=sticky)
        row=5
        Button(mainframe, text="+", command=lambda: send_key("+",target),fg=fgOperators, font=font, bd=bd, width=width).grid(row=row, column=3,sticky=sticky)
        Button(mainframe, text="=", command=lambda: equals_key(target),fg=fgOperators, font=font, bd=bd, width=width).grid(row=row, column=2,sticky=sticky)
        Button(mainframe, text=".", command=lambda: send_key(".",target),fg=fgDigits, font=font, bd=bd, width=width).grid(row=row, column=1,sticky=sticky)
        Button(mainframe, text="0", command=lambda: send_key("0",target),fg=fgDigits, font=font, bd=bd, width=width).grid(row=row, column=0,sticky=sticky)

if __name__ == "__main__":
    root = Tk()
    root.title("Calculator")
    Application(root).grid(padx=10,pady=15)
    root.mainloop()  
    
