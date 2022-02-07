from tkinter import Entry, Button, Tk, StringVar, Frame, N, S, E, W, NE,END
import Calculator
def add_display(string):
    global eText
    global display
    if eText.get() == "0":
        eText.set(string)
    else:
        newvalue= eText.get()+string
        eText.set(newvalue)
    display.xview(END)
def equals_Key():
    global eText
    global display
    tokens= Calculator.get_token(eText.get())
    rpn= Calculator.get_rpn(tokens)
    result= Calculator.operate_expression(rpn)
    
    eText.set(str(result).rstrip('0').rstrip('.'))
    display.xview(END)
    
class Application(Frame):
    def __init__(self, parent, *args, **kwargs):
        global eText
        global display
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
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
        eText = StringVar(value="0")
        display= Entry(mainframe,textvariable=eText, font=("Verdana", 30, ), bd = 10, 
                      state='readonly',
                      cursor="arrow",
                      justify="right" 
        )
        display.grid(row=0, column=0,columnspan=4, sticky=(W, E))     
   
        # Buttons
        fontsize= 15
        width=2
        bd= 3  
        sticky=E+W+N+S   
        font=("Verdana", fontsize, )
        
        # row 4
        Button(mainframe, text="/", command=lambda: add_display("/"), font=font, bd=bd,width=width).grid(row=1, column=3,sticky=sticky)
        Button(mainframe, text="9", command=lambda: add_display("9"), font=font, bd=bd, width=width).grid(row=1, column=2,sticky=sticky)
        Button(mainframe, text="8", command=lambda: add_display("8"), font=font, bd=bd, width=width).grid(row=1, column=1,sticky=sticky)
        Button(mainframe, text="7", command=lambda: add_display("7"), font=font, bd=bd, width=width).grid(row=1, column=0,sticky=sticky)
        # row 3
        Button(mainframe, text="*", command=lambda: add_display("*"), font=font, bd=bd, width=width).grid(row=2, column=3,sticky=sticky)
        Button(mainframe, text="6", command=lambda: add_display("6"), font=font, bd=bd, width=width).grid(row=2, column=2,sticky=sticky)
        Button(mainframe, text="5", command=lambda: add_display("5"), font=font, bd=bd, width=width).grid(row=2, column=1,sticky=sticky)
        Button(mainframe, text="4", command=lambda: add_display("4"), font=font, bd=bd, width=width).grid(row=2, column=0,sticky=sticky)
        # row 2
        Button(mainframe, text="-", command=lambda: add_display("-"), font=font, bd=bd, width=width).grid(row=3, column=3,sticky=sticky)
        Button(mainframe, text="3", command=lambda: add_display("3"), font=font, bd=bd, width=width).grid(row=3, column=2,sticky=sticky)
        Button(mainframe, text="2", command=lambda: add_display("2"), font=font, bd=bd, width=width).grid(row=3, column=1,sticky=sticky)
        Button(mainframe, text="1", command=lambda: add_display("1"), font=font, bd=bd, width=width).grid(row=3, column=0,sticky=sticky)
        # row 1
        Button(mainframe, text="+", command=lambda: add_display("+"), font=font, bd=bd, width=width).grid(row=4, column=3,sticky=sticky)
        Button(mainframe, text="=", command=equals_Key, font=font, bd=bd, width=width).grid(row=4, column=2,sticky=sticky)
        Button(mainframe, text=".", command=lambda: add_display("."), font=font, bd=bd, width=width).grid(row=4, column=1,sticky=sticky)
        Button(mainframe, text="0", command=lambda: add_display("0"), font=font, bd=bd, width=width).grid(row=4, column=0,sticky=sticky)

if __name__ == "__main__":
    root = Tk()
    Application(root).grid()
    root.mainloop()  
    









