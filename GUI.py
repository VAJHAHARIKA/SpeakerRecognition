from tkinter import *
import sys
sys.path.append("D:/Projects/Internship/finaltest.py")

class App(Frame):
    def run_script(self):
        sys.stdout = self
        ## sys.stderr = self
        try:
            del(sys.modules["finaltest"])
        except:
            pass
        import finaltest
        test_script.play()
        sys.stdout = sys.__stdout__
        ## sys.stderr = __stderr__
        exit(0)

    def build_widgets(self):
        self.text1 = Text(self)
        self.text1.pack(side=TOP)
        self.button = Button(self)
        self.button["text"] = "Run for attendance"
        self.button["command"] = self.run_script
        self.button.pack(side=TOP)

    def write(self, txt):
        self.text1.insert(INSERT, txt)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.build_widgets()
   

root = Tk()
app = App(master = root)
app.mainloop()
exit(0)
