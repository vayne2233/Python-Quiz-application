from tkinter import *
from tkinter.scrolledtext import *
from tkinter.messagebox import *
from tkinter.ttk import *
from json import *
from random import *


class basedeck():
    def __init__(self, master):
        self.window = master
        self.window.config()
        self.window.title('Quiz')
        self.window.geometry("400x400")
        self.window.resizable(0, 0)

        initface(self.window)


class initface():
    def __init__(self, master):
        self.master = master
        self.master.config(bg="white")
        self.initface = Frame(self.master)
        self.initface.pack(pady=100)
        start = Button(self.initface, text='start', command=self.started)
        start.pack(side='bottom', ipadx=40, ipady=20)
        edit = Button(self.initface, text='Edit', command=self.edited)
        edit.pack(side='top', ipadx=40, ipady=20)

    def started(self):
        self.initface.destroy()
        env(self.master)

    def edited(self):
        self.initface.destroy()
        editface(self.master)


class editface():
    def __init__(self, master):
        self.master = master
        self.master.config(bg="white")
        self.editface = Frame(self.master)
        self.editface.pack(pady=100)
        lbl1 = Label(self.editface, text="English")
        lbl1.pack()
        self.ent = Entry(self.editface, width=10)
        self.ent.pack()
        lbl2 = Label(self.editface, text="Chinese")
        lbl2.pack()
        self.ent2 = Entry(self.editface, width=10)
        self.ent2.pack()
        add = Button(self.editface, text="Add", width=10, command=self.Add)
        add.pack()
        openfile = Button(self.editface, text="Open File",
                          width=10, command=self.Open)
        openfile.pack(pady=10)
        back = Button(self.editface, text='Back',
                      width=10, command=self.change)
        back.pack()

    def change(self):
        self.editface.destroy()
        initface(self.master)

    def Add(self):
        english = self.ent.get()
        chinese = self.ent2.get()

        add = {
            english: chinese
        }

        with open('question.json', 'r+') as file:
            dct = load(file)
            dct.update(add)
            file.seek(0)
            dump(dct, file, indent=4)

    def Open(self):
        self.editface.destroy()
        File(self.master)


class File():
    def __init__(self, master):
        self.root = master
        self.root.config(bg='white')
        self.File = Frame(self.root)
        self.File.pack()

        with open('question.json', 'r+') as file:
            dct = load(file)

        comment = Label(
            self.File, text='How to use: "English": "chinese". Use comma to sperate two words').pack()
        self.text = ScrolledText(self.File)
        self.text.insert(INSERT, dct)

        save = Button(self.File, text='Save', command=self.change)
        back = Button(self.File, text='Back', command=self.back)
        self.text.pack()
        save.pack()
        back.pack()

    def change(self):
        txt = dict(eval(self.text.get('1.0', END)))
        with open('question.json', 'w') as file:
            dump(txt, file, indent=4)

    def back(self):
        self.File.destroy()
        editface(self.root)


class env():
    def __init__(self, master):
        self.window = master
        self.window.config(bg="white")
        self.env = Frame(self.window)
        self.env.pack(pady=100)

        env.__init__.check = BooleanVar()
        env.__init__.check2 = BooleanVar()

        env.__init__.check.set(False)
        env.__init__.check2.set(False)

        c_e = Checkbutton(self.env, text="中翻英", variable=env.__init__.check)
        c_e.pack()
        e_c = Checkbutton(self.env, text="英翻中", variable=env.__init__.check2)
        e_c.pack()

        submit = Button(self.env, text="SUBMIT", command=self.start)
        submit.pack()

        back = Button(self.env, text="Back", command=self.change)
        back.pack()
        back.focus()

    def change(self):
        self.env.destroy()
        initface(self.window)

    def start(self):
        with open('question.json', 'r') as file:
            data = load(file)

        if len(data) < 10:
            showwarning("Warning", "Your data aren't enough")
            self.start.destroy()
            editface(self.window)
        else:
            self.env.destroy()
            start(self.window)


class start():
    def __init__(self, master):
        self.master = master
        self.master.config(bg="white")
        self.start = Frame(self.master)
        self.start.pack(pady=100)

        if env.__init__.check.get() == True and env.__init__.check2.get() == True:
            self.mode = 1
        elif env.__init__.check.get() == True and env.__init__.check2.get() == False:
            self.mode = 2
        elif env.__init__.check.get() == False and env.__init__.check2.get() == True:
            self.mode = 3
        elif env.__init__.check.get() == False and env.__init__.check2.get() == False:
            showwarning('Warning', 'Choose your mode')
            self.start.destroy()
            env(self.master)
            
        with open('question.json', 'r+') as file:
            self.data = load(file)

        self.englishs = list(self.data.keys())
        self.chineses = list(self.data.values())

        self.database = self.englishs.copy()
        self.database_chinese = self.chineses.copy()

        self.qn = 1
        self.ques()
        self.select = StringVar()
        self.opts = self.radiobtns()
        self.display_opts()

    def ques(self):
        self.question = Label(self.start, text='', font=('times', 20))
        self.question.pack()

        self.show = Label(self.start, text='', font=('times', 15))
        self.show.pack()

    def radiobtns(self):
        val = 0
        option_list = []
        while len(option_list) < 4:
            option = Radiobutton(self.start, text='', value=0,
                                 variable=self.select, command=self.check, state=NORMAL)

            option.pack()
            option_list.append(option)

            val += 1

        return option_list

    def display_opts(self):
        option_list = []

        if self.mode == 2:
            chinese_question = choice(self.chineses)
            idx = self.chineses.index(chinese_question)
            self.answer = self.englishs[idx]
            option_list.append(self.answer)

            while len(option_list) < 4:
                shuffle(self.database)
                if self.database[0] not in option_list and self.data[self.database[0]] not in option_list:
                    option_list.append(self.database[0])

            shuffle(option_list)
            self.question['text'] = chinese_question

        elif self.mode == 3:
            english_question = choice(self.englishs)
            self.answer = self.data[english_question]

            option_list.append(self.answer)

            while len(option_list) < 4:
                shuffle(self.database_chinese)
                if self.database_chinese[0] not in option_list:
                    option_list.append(self.database_chinese[0])

            shuffle(option_list)
            self.question['text'] = english_question

        elif self.mode == 1:
            choose = choice([1, 2])
            if choose == 1:
                chinese_question = choice(self.chineses)
                idx = self.chineses.index(chinese_question)
                self.answer = self.englishs[idx]
                option_list.append(self.answer)

                while len(option_list) < 4:
                    shuffle(self.database)
                    if self.database[0] not in option_list:
                        option_list.append(self.database[0])

                shuffle(option_list)
                self.question['text'] = chinese_question
            else:
                english_question = choice(self.englishs)
                self.answer = self.data[english_question]

                option_list.append(self.answer)

                while len(option_list) < 4:
                    shuffle(self.database_chinese)
                    if self.database_chinese[0] not in option_list:
                        option_list.append(self.database_chinese[0])

                shuffle(option_list)
                self.question['text'] = english_question

        self.show.config(text='')
        self.select.set(0)

        for i in range(4):
            for j in ['text', 'value']:
                self.opts[i]['state'] = NORMAL
                self.opts[i][j] = option_list[i]

    def check(self):
        for i in range(4):
            self.opts[i]['state'] = DISABLED
        if str(self.select.get()) != str(self.answer):
            self.show.config(text=self.answer)
        else:
            self.show.config(text="Bingo")

        times = 10 if self.qn < 100 else self.qn % 100
        if self.qn == times:
            self.start.after(1500, self.done)
        else:
            self.qn += 1
            self.start.after(1500, self.display_opts)

    def done(self):
        showinfo("Good", "That's the end of the quiz!!!")
        self.start.destroy()
        env(self.master)


if __name__ == "__main__":
    window = Tk()
    basedeck(window)
    window.mainloop()
