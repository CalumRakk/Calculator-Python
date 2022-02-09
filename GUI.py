from tkinter import Entry, Button, Tk, StringVar, Frame, N, S, E, W, NE,END, DISABLED
import Calculator

def isDisplayConcatenable(key,displayText):
    # Si display vale 0, key tiene que ser un operador o un punto.
    # Si el último digito de display es un digito, key tiene que ser un digito, punto o operador.
    # Si el último digito de display es un operador, key tiene que ser un digito.
    # si el último digito de display es un punto, key tiene que ser un digito.
    # Si el último digito de display es un operador, key tiene que ser un digito.
    # Si el último digito de display es un operador, key tiene que ser un signo positivo o negativo y display diferente de + o -.
    if displayText=="0":
        if Calculator.isOperator(key) or key==".":
            return True
    elif displayText[-1].isdigit() and (key.isdigit() or key=="." or Calculator.isOperator(key)):
        return True
    elif displayText[-1] == "." and key.isdigit():
        return True
    elif Calculator.isOperator(displayText[-1]) and key.isdigit():        
        return True
    elif Calculator.isOperator(displayText[-1]) and (key in ["+","-"] and not displayText[-1] in ["+","-"]):
        return True
    return False
def isDisplayReplaceable(key,displayText):
    # Si display vale 0, key tiene que ser un operador o un punto.
    if displayText == "0" and key.isdigit():
        return True
    return False
def send_key(key,target):
    display,entryVar= target
    displayText=entryVar.get()
    
    if isDisplayConcatenable(key,displayText):
        entryVar.set(displayText + key)
    elif isDisplayReplaceable(key,displayText):
        entryVar.set(key)        
   
    display.xview(END)    
def displayWarning(target):
    display,entryVar= target
    root.after(100)
    display.configure(foreground="black")
def equals_key(target):
    display, entryVar= target
    
    displayText= entryVar.get()
    if Calculator.isExpression(displayText) and not Calculator.isOperator(displayText[-1]):
        tokens= Calculator.parser(displayText)
        rpn= Calculator.get_rpn(tokens)
        result= Calculator.operate_expression(rpn)
        
        entryVar.set(result)
        display.xview(END)
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
        self.parent.maxsize(500, 450)
        self.parent.minsize(300, 300)
        
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        
        
        mainframe = Frame(self.parent)
        mainframe.columnconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=1)
        mainframe.columnconfigure(2, weight=1)
        mainframe.columnconfigure(3, weight=1) 
        
        mainframe.rowconfigure(0, weight=1)
        mainframe.rowconfigure(1, weight=2)
        mainframe.rowconfigure(2, weight=2)
        mainframe.rowconfigure(3, weight=2) 
        mainframe.rowconfigure(4, weight=2)          
        
        mainframe.grid(column=0, row=0,columnspan=3, rowspan=3, sticky=(N, W, E, S), padx=10, pady=10 )
        
        # Display
        entryVar= StringVar(value="0")
        display= Entry(mainframe,textvariable=entryVar, font=("Verdana", 30, ), bd = 10, 
                      state='readonly',
                      cursor="arrow",
                      justify="right" 
        )
        display.grid(row=0, column=0,columnspan=4, sticky=(W, E))     
        target= (display, entryVar)

        # Buttons
        fontsize= 15
        width=2
        bd= 3  
        sticky=E+W+N+S   
        font=("Verdana", fontsize, )
        # row 4
        row=1

        Button(mainframe, text="AC", command=lambda: ac_key(target), font=font, bd=bd, width=width).grid(row=row, column=0,sticky=sticky, columnspan=2)
        Button(mainframe, text="%", command=lambda: send_key("%",target), font=font, bd=bd,width=width).grid(row=row, column=2,sticky=sticky)
        Button(mainframe, text="^", command=lambda: send_key("^",target), font=font, bd=bd, width=width).grid(row=row, column=3,sticky=sticky)
        # row 3
        row=2
        Button(mainframe, text="/", command=lambda: send_key("/",target), font=font, bd=bd,width=width).grid(row=row, column=3,sticky=sticky)
        Button(mainframe, text="9", command=lambda: send_key("9",target), font=font, bd=bd, width=width).grid(row=row, column=2,sticky=sticky)
        Button(mainframe, text="8", command=lambda: send_key("8",target), font=font, bd=bd, width=width).grid(row=row, column=1,sticky=sticky)
        Button(mainframe, text="7", command=lambda: send_key("7",target), font=font, bd=bd, width=width).grid(row=row, column=0,sticky=sticky)
        # row 2
        row=3
        Button(mainframe, text="*", command=lambda: send_key("*",target), font=font, bd=bd, width=width).grid(row=row, column=3,sticky=sticky)
        Button(mainframe, text="6", command=lambda: send_key("6",target), font=font, bd=bd, width=width).grid(row=row, column=2,sticky=sticky)
        Button(mainframe, text="5", command=lambda: send_key("5",target), font=font, bd=bd, width=width).grid(row=row, column=1,sticky=sticky)
        Button(mainframe, text="4", command=lambda: send_key("4",target), font=font, bd=bd, width=width).grid(row=row, column=0,sticky=sticky)
        # row 1
        row=4
        Button(mainframe, text="-", command=lambda: send_key("-",target), font=font, bd=bd, width=width).grid(row=row, column=3,sticky=sticky)
        Button(mainframe, text="3", command=lambda: send_key("3",target), font=font, bd=bd, width=width).grid(row=row, column=2,sticky=sticky)
        Button(mainframe, text="2", command=lambda: send_key("2",target), font=font, bd=bd, width=width).grid(row=row, column=1,sticky=sticky)
        Button(mainframe, text="1", command=lambda: send_key("1",target), font=font, bd=bd, width=width).grid(row=row, column=0,sticky=sticky)
        # row 0
        row=5
        Button(mainframe, text="+", command=lambda: send_key("+",target), font=font, bd=bd, width=width).grid(row=row, column=3,sticky=sticky)
        Button(mainframe, text="=", command=lambda: equals_key(target), font=font, bd=bd, width=width).grid(row=row, column=2,sticky=sticky)
        Button(mainframe, text=".", command=lambda: send_key(".",target), font=font, bd=bd, width=width).grid(row=row, column=1,sticky=sticky)
        Button(mainframe, text="0", command=lambda: send_key("0",target), font=font, bd=bd, width=width).grid(row=row, column=0,sticky=sticky)

if __name__ == "__main__":
    root = Tk()
    Application(root).grid()
    root.mainloop()  
    









