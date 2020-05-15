from tkinter import *
#import tkinter as tk
#from ScrolledText import *
import csv
import pprint
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from difflib import SequenceMatcher



fields = ('Course Name', 'Instructor', 'Day', 'Time From', 'Time to')

def LoadData(filename1, filename2):
    lst = []
    main = {}
    with open(filename1) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        counter = 0
        for x in csv_reader:
            if counter != 0:
                lst = x
                lst1 = []

                for i in lst:
                    if i != '':
                        lst1.append(i)
                lst2 = []
                for s in lst1:
                    tup = s.split('##')
                    if len(tup) > 1:
                        tup = (tup[0], tup[1])
                    else:
                        tup = (tup[0])
                    lst2.append(tup)
                if len(lst2) != 0:
                    main[lst2[0]] = []
                    for i in range(1, len(lst2)):
                        main[lst2[0]] += [lst2[i]]
                        if len(lst2[i]) >= 2:
                            main[lst2[i]] = []

            counter += 1
    with open(filename2) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        counter = 0
        for x in csv_reader:
            if counter != 0:
                lst = x
                lst1 = []
                for i in lst:
                    if i != '':
                        lst1.append(i)
                lst2 = [(lst1[1], lst1[0]), lst[2]]
                if lst2[1] not in main[lst2[0]]:
                    lst2[1] = lst2[1].strip()
                    main[lst2[0]] += [lst2[1]]
                    main[lst2[1]] = []
            counter += 1
        return main


def teachers(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        teachers = {}
        counter = 0
        for x in csv_reader:
            if counter != 0:
                lst1 = []
                for i in x:
                    i = i.strip()
                    lst1.append(i)

                lst = x
                teachers[lst1[0]] = lst1[1:]
            counter += 1

        ##        pprint.pprint(teachers)
        return teachers


def bfs(G, node):
    q = [node]
    lst = []
    while not is_empty(q):
        a = dequeue(q)
        if a not in lst:
            lst.append(a)
            for tup in G[a]:
                enqueue(q, tup)
    return lst


def mf(course, teacher, day, time1, time2, G, teachd,root):
    if course == 'None':
        course = None
    if teacher == 'None':
        teacher = None
    if day == 'None':
        day = None
    if time1 == 'None':
        time1 = None
    if time2 == 'None':
        time2 = None
    if course!=None:
        max=0
        maxkey=""
        for key in G:
            if G[key]!=[]:
                if len(key)==2:
                    m = SequenceMatcher(None, course.lower(), key[0].lower())
                    k = m.ratio()
                    if k>max:
                        max=k
                        maxkey=key[0]
                else:
                    m = SequenceMatcher(None, course.lower(), key.lower())
                    k = m.ratio()
                    if k>max:
                        max=k
                        maxkey=key
        #print(max)
        course = maxkey
        #print(course)
    if teacher!=None:
        max=0
        maxkey=""
        for key in G:
            #k=fuzz.ratio(teacher,key)
            m = SequenceMatcher(None, teacher.lower(), key.lower())
            k = m.ratio()
            if k>max:
                max=k
                maxkey=key
        teacher = maxkey
        max = 0
        maxkey = ''
        for keys in teachd:
            #k = fuzz.ratio(teacher,keys)
            m = SequenceMatcher(None, teacher.lower(), keys.lower())
            k = m.ratio()
            if k>max:
                max=k
                maxkey = keys
        teacher1 = maxkey
        #print(teacher)
    dayss= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    if day!=None:
        max = 0
        maxkey = ''
        for da in dayss:
            k = fuzz.ratio(day, da)
            if k > max:
                max = k
                maxkey = da
        day = maxkey


    # print(course,teacher,day,time1,time2)
    if teacher != None:
        T = [teacher]
    elif course != None:
        tup = coursetup(course, G)
        T = bfs(G, tup)

    else:
        print('Please specify either a teacher or course(or both)')

    if day != None:
        final = []
        for t in T:
            if day == 'Monday':
                if teachd[t][4] != '-':
                    final.append([t, teachd[t][4]])
            elif day == 'Tuesday':
                if teachd[t][5] != '-':
                    final.append([t, teachd[t][5]])
            elif day == 'Wednesday':
                if teachd[t][6] != '-':
                    final.append([t, teachd[t][6]])
            elif day == 'Thursday':
                if teachd[t][7] != '-':
                    final.append([t, teachd[t][7]])
            elif day == 'Friday':
                if teachd[t][8] != '-':
                    final.append([t, teachd[t][8]])
            elif day == 'Saturday':
                if teachd[t][9] != '-':
                    final.append([t, teachd[t][9]])

        if time1 != None:

            result = []
            for f in final:
                officH = f[1]
                time = time_comparison(officH, time1, time2)
                if time:
                    result.append(f[0])

            final = result

    elif time1 != None:
        final = []
        for t in T:
            info = teachd[t]
            l = []
            for i in range(4, 10):
                if teachd[t][i] != '-':
                    time = time_comparison(teachd[t][i], time1, time2)
                    if time:
                        if i == 4:
                            l.append('Monday')
                        elif i == 5:
                            l.append('Tuesday')
                        elif i == 6:
                            l.append('Wednesday')
                        elif i == 7:
                            l.append('Thursday')
                        elif i == 8:
                            l.append('Friday')
                        elif i == 9:
                            l.append('Saturday')
            if l != []:
                l.append(t)
                final.append(l)

    else:
        final = T

    if final == []:
        print('Sorry, no one is available at this time.')

    s = ''
    yep =[]
    for something in final:
        if type(something) == str:

            s = something + '\n'
            info = teachd[something]
            s += info[0] + '\n' + 'Faculty Pod: ' + info[1] + ', Pod No.: ' + info[2] + '\n' + 'Email: ' + info[
                3] + '\n' + 'Office Hours: ' + '\n'

            if day == None and time1 == None:
                if info[4] != '-':
                    s += 'Monday: ' + info[4] + '\n'
                if info[5] != '-':
                    s += 'Tuesday: ' + info[5] + '\n'
                if info[6] != '-':
                    s += 'Wednesday: ' + info[6] + '\n'
                if info[7] != '-':
                    s += 'Thursday: ' + info[7] + '\n'
                if info[8] != '-':
                    s += 'Friday: ' + info[8] + '\n'
                if info[9] != '-':
                    s += 'Saturday: ' + info[9] + '\n'
            elif day != None:
                i = day
                print(i)

                if i == 'Monday':
                    s += i + ': ' + info[4] + '\n'
                elif i == 'Tuesday':
                    s += i + ': ' + info[5] + '\n'
                elif i == 'Wednesday':
                    s += i + ': ' + info[6] + '\n'
                elif i == 'Thursday':
                    s += i + ': ' + info[7] + '\n'
                elif i == 'Friday':
                    s += i + ': ' + info[8] + '\n'
                elif i == 'Saturday':
                    s += i + ': ' + info[9] + '\n'
            s += '\n'
            yep.append(s)
        else:
            if time1 == None:
                s = something[0] + '\n'
                info = teachd[something[0]]
                s += info[0] + '\n' + 'Faculty Pod: ' + info[1] + ', Pod No.: ' + info[2] + '\n' + 'Email: ' + info[
                    3] + '\n' + 'Office Hours: ' + '\n'
                s += day + ': ' + something[1] + '\n' + '\n'
            elif day == None:
                s = something[-1] + '\n'
                info = teachd[something[-1]]
                s += info[0] + '\n' + 'Faculty Pod: ' + info[1] + ', Pod No.: ' + info[2] + '\n' + 'Email: ' + info[
                    3] + '\n' + 'Office Hours: ' + '\n'
                for d in range(len(something) - 1):
                    i = something[d]
                    if i == 'Monday':
                        s += i + ': ' + info[4] + '\n'
                    elif i == 'Tuesday':
                        s += i + ': ' + info[5] + '\n'
                    elif i == 'Wednesday':
                        s += i + ': ' + info[6] + '\n'
                    elif i == 'Thursday':
                        s += i + ': ' + info[7] + '\n'
                    elif i == 'Friday':
                        s += i + ': ' + info[8] + '\n'
                    elif i == 'Saturday':
                        s += i + ': ' + info[9] + '\n'
                yep.append(s)
                s += '\n'
    if s == '':
        print('Sorry, no one is available at this time.')
    print(yep)
    print(s)
    printsome(yep,root)
#root = Tk()
def printsome(yep,root):
    #root = Tkinter.Tk(className=" Another way to create a Scrollable text area")
    #textPad = ScrolledText(root, width=50, height=40)
    #textPad.pack()
    #scrollbar = Scrollbar(root)
    #scrollbar.pack(side=RIGHT, fill=Y)
    # scrollbar = Scrollbar(txtWin)
    # scrollbar.pack(side=RIGHT, fill=Y)
    #
    # area = Text(txtWin, yscrollcommand=scrollbar.set, background='black', foreground='green’, insertbackground = 'yellow', insertwidth = 5, selectbackground = 'red' )
    # area.pack(expand=True, fill='both')
    #
    # scrollbar.config(command=area.yview)
    #mylist = Listbox(root, yscrollcommand=scrollbar.set)
    # for line in range(100):
    #    mylist.insert(END, "This is line number " + str(line))

   # mylist.pack(side=BOTTOM, fill=BOTH)
    #scrollbar.config(command=mylist.xview)

    for sm in yep:
        label = Label(root, text=str(sm))
        #mylist.insert(END, str(sm))

        label.pack()
    # this creates x as a new label to the GUI
        #mylist.pack(side=BOTTOM, fill=X)

        #scrollbar.config(command=mylist.xview)

 #       label.pack()
    root.attributes('-fullscreen', True)
def qexit():
    root.destroy()
def enqueue(lst, item):
    lst.append(item)


def dequeue(lst):
    return lst.pop(0)


def is_empty(stack):
    if len(stack) == 0:
        return True
    else:
        return False


def coursetup(course, G):
    for key in G:
        if len(key) == 2:
            if key[0] == course or key[1] == course:
                return key
    return course


def bfs(G, node):
    q = [node]
    lst = []
    while not is_empty(q):
        a = dequeue(q)
        if a not in lst:
            if G[a] == []:
                lst.append(a)
            for tup in G[a]:
                enqueue(q, tup)
    return lst


def time_comparison(officeH, inp, inp2):
    officeH = officeH.split(" - ")
    officeH[0] = officeH[0].split(':')
    officeH[0][1] = officeH[0][1].split()
    t = officeH[0][1][1]
    officeH[0] = officeH[0][0] + '.' + officeH[0][1][0]
    officeH[0] = float(officeH[0])
    if t == "PM" and officeH[0] < 12:
        officeH[0] += 12
    officeH[1] = officeH[1].split(':')
    officeH[1][1] = officeH[1][1].split()
    to = officeH[1][1][1]
    officeH[1] = officeH[1][0] + '.' + officeH[1][1][0]
    officeH[1] = float(officeH[1])
    if to == "PM" and officeH[1] < 12:
        officeH[1] += 12
    inp = inp.split(':')
    inp[1] = inp[1].split()
    t = inp[1][1]
    inp = inp[0] + '.' + inp[1][0]
    inp = float(inp)
    if t == "PM" and inp < 12:
        inp += 12
    inp2 = inp2.split(':')
    inp2[1] = inp2[1].split()
    to = inp2[1][1]
    inp2 = inp2[0] + '.' + inp2[1][0]
    inp2 = float(inp2)
    if to == "PM" and inp2 < 12:
        inp2 += 12
    if abs(inp - inp2) >= abs(officeH[0] - officeH[1]):
        if officeH[0] >= inp and officeH[0] <= inp2:
            return True
        elif inp <= officeH[1] <= inp2:
            return True
    elif abs(inp - inp2) < abs(officeH[0] - officeH[1]):
        if officeH[0] <= inp <= officeH[1]:
            return True
        elif officeH[0] <= inp2 <= officeH[1]:
            return True
    return False


def trial(entries,root):
    course = entries['Course Name'].get()
    teacher = entries['Instructor'].get()
    day = entries['Day'].get()
    time1 = entries['Time From'].get()
    time2 = entries['Time to'].get()

    print(course)
    print(teacher)

    filename = 'FINALL.csv'
    filename2 = 'DSA Project Teacherss.csv'
    filename3 = 'broo.csv'

    G = LoadData(filename, filename3)
    print(G["CS"])
def reset():
    # labelYourBMI2 = Button(topFrame, text="")
    #Course Name.set("None")
    #.set('None')
    #Weight.set('None')
    return

    teachd = teachers(filename2)
    ##    print(teach)
    ##    mf(None,'Muhammad Haris',None, '2:30 PM','3:00 PM',m,teachd)
    mf(course, teacher, day, time1, time2, G, teachd,root)


def makeform(root, fields):
    entries = {}
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=22, text=field + ": ", anchor='w')
        ent = Entry(row)
        ent.insert(0, "None")
        row.pack(side=TOP, fill=X, padx=5, pady=5)

        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries[field] = ent
    return entries


if __name__ == '__main__':
    root = Tk()
    ents = makeform(root, fields)

    b1 = Button(root, text='Search',
                command=(lambda e=ents: trial(e,root)))
    b1.pack(side=LEFT, padx=5, pady=5)
    #b1.pack_forget()
    root.title('Academic Help Portal')
    b2= Button(root, text='Exit',command = qexit)
                #command=(lambda e=ents: trial(e, root)))
    b2.pack(side=LEFT, padx=5, pady=5)
    #root.attributes('-fullscreen', True)


    #topFrame = Frame(root)
    #topFrame.pack()
    #ButtonReset = Button(topFrame, text="Reset", command=reset)
    #ButtonReset.pack()
    #root = tk.Tk()

    #label = tk.Label()
    #label.grid()


    # def write():
    #     label.config(text="Blah" * 6)
    #
    #
    # def clear():
    #     label.config(text="")


    #tk.Button(text="write", command=write).grid()
    #tk.Button(text="clear", command=clear).grid()

    root.mainloop()
