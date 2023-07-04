#from tkinter import *

#root = Tk()
#root.mainloop()

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import time
import threading
import math
import itertools
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import random
from mpl_toolkits.mplot3d import Axes3D

def click_btn_1a():
    button_1a['text'] = 'クリックしました'

def click_btn_1b():
    button_1b['text'] = 'クリックしました'

def click_btn_1c():
    button_1c['text'] = 'クリックしました'

def click_btn_1d():
    button_1d['text'] = 'クリックしました'

def click_btn_2a():
    button_2a['text'] = 'クリックしました'

def click_btn_2b():
    button_2b['text'] = 'クリックしました'

def click_btn_3():
    button_3['text'] = 'クリックしました'

def _redraw(_, x, y):
    #ax1 = fig.add_subplot(111)
    """グラフを再描画するための関数"""
    # 現在のグラフを消去する
    #plt.cla()
    ax1.cla()
    # 折れ線グラフを再描画する
    #plt.ylim(-1.2, 1.2)
    #plt.ylim(0, 100)
    ax1.set_ylim(0, 100)
    #plt.title('2D VIEW (X-Y)')
    ax1.set_title('2D VIEW (X-Y)')
    #plt.xlabel('x')
    ax1.set_xlabel('x')
    #plt.ylabel('y')
    ax1.set_ylabel('y')
    #plt.scatter(x, y)
    ax1.scatter(x, y)
    #plt.plot(x, y)

def _redrawb(_, xb, yb, zb):
    #ax2 = figb.add_subplot(111)
    """グラフを再描画するための関数"""
    # 現在のグラフを消去する
    #plt.cla()
    ax2.cla()
    # 折れ線グラフを再描画する
    #plt.ylim(-1.2, 1.2)
    ax2.set_xlim(0, 100)
    #plt.ylim(0, 100)
    ax2.set_ylim(0, 100)
    ax2.set_zlim(0, 10)
    #plt.title('3D VIEW')
    ax2.set_title('3D VIEW')
    #plt.xlabel('x')
    ax2.set_xlabel('x')
    #plt.ylabel('y')
    ax2.set_ylabel('y')
    ax2.set_zlabel('z')
    #plt.scatter(xb, yb)
    ax2.scatter(xb, yb, zb)
    #plt.plot(x, y)

def _update():
    """データを一定間隔で追加するスレッドの処理"""
    i = 100
    list = [random.randint(0, 100) for _ in range(100)]
    #for frame in itertools.count(0, 0.1):
    for frame in itertools.cycle(list):    
        x.pop(0)
        x.append(i)
        i += 1

        y.pop(0)
        #y.append(math.sin(frame))
        y.append(frame)
        # データを追加する間隔 (100ms)
        time.sleep(0.2)

def _updateb():
    """データを一定間隔で追加するスレッドの処理"""
    ib = 100
    lista = [random.randint(0, 100) for _ in range(100)]
    listb = [random.randint(0, 100) for _ in range(100)]
    listc = [random.randint(0, 10)  for _ in range(100)]
    #for frame in itertools.count(0, 0.1):
    #for framea, frameb, framec in itertools.cycle(lista, listb, listc):    
    #    xb.pop(0)
    #    #xb.append(ib)
    #    #ib += 1
    #    yb.append(framea)

    #    yb.pop(0)
    #    #y.append(math.sin(frame))
    #    yb.append(frameb)

    #    zb.pop(0)
    #    zb.append(framec)

    #    # データを追加する間隔 (100ms)
    #    time.sleep(0.5)

    for framea in itertools.cycle(lista):
        xb.pop(0)
        xb.append(framea)

        for frameb in itertools.cycle(listb):
            yb.pop(0)
            yb.append(frameb)

            for framec in itertools.cycle(listc):
                zb.pop(0)
                zb.append(framec)

                # データを追加する間隔 (100ms)
                time.sleep(0.2)

def _init():
    """データを一定間隔で追加するためのスレッドを起動する"""
    t = threading.Thread(target=_update)
    t.daemon = True
    t.start()

def _initb():
    """データを一定間隔で追加するためのスレッドを起動する"""
    tb = threading.Thread(target=_updateb)
    tb.daemon = True
    tb.start()

if __name__ == '__main__':

    # 描画領域
    fig  = plt.figure(figsize=(6,4), dpi=72)
    figb = plt.figure(figsize=(6,4), dpi=72)

    ax1 = fig.add_subplot(111)
    ax2 = figb.add_subplot(111, projection='3d')

    # 描画するデータ (最初は空)
    x  = [j for j in range(100)]
    #xb = [0.0] *100
    xb = [random.randint(0, 100) for _ in range(100)]
    #x = [0.0] *100
    #y = [0.0] *100
    y  = [random.randint(0, 100) for _ in range(100)]
    #yb = [0.0] *100
    yb = [random.randint(0, 100) for _ in range(100)]

    #zb = [0.0] *100
    zb = [random.randint(0, 10) for _ in range(100)]

    params = {
        'fig': fig,
        'func': _redraw,  # グラフを更新する関数
        'init_func': _init,  # グラフ初期化用の関数 (今回はデータ更新用スレッドの起動)
        'fargs': (x, y),  # 関数の引数 (フレーム番号を除く)
        'interval': 200,  # グラフを更新する間隔 (ミリ秒)
    }
    anime = animation.FuncAnimation(**params)

    paramsb = {
        'fig': figb,
        'func': _redrawb,  # グラフを更新する関数
        'init_func': _initb,  # グラフ初期化用の関数 (今回はデータ更新用スレッドの起動)
        'fargs': (xb, yb, zb),  # 関数の引数 (フレーム番号を除く)
        'interval': 200,  # グラフを更新する間隔 (ミリ秒)
    }
    animeb = animation.FuncAnimation(**paramsb)

    root = Tk() # この下に画面構成を記述
    
    # ----------- ①Window作成 ----------- #
    root.title('AK5816')   # 画面タイトル設定
    root.geometry('1250x700')       # 画面サイズ設定
    #root.resizable(False, False)   # リサイズ不可に設定

    # ----------- ②Frameを定義 ----------- #
    #frame1 = Frame(root, width=400, height=200, borderwidth=0, relief='solid')
    labelframe_1 = LabelFrame(root, width=400, height=150, borderwidth=0, bd=0, text="", font=('meiryo', 12))
    #frame2 = Frame(root, width=400, height=200, borderwidth=0, relief='solid')
    labelframe_2 = LabelFrame(root, width=400, height=200, borderwidth=0, bd=4, text="One register setting", font=('meiryo', 12))
    #frame2 = Frame(root, borderwidth=0, relief='solid')
    #frame3 = Frame(root, width=400, height=200, borderwidth=0, relief='solid')
    labelframe_3 = LabelFrame(root, width=400, height=200, borderwidth=0, bd=4, text="All register read", font=('meiryo', 12))
    labelframe_4 = LabelFrame(root, width=400, height=200, borderwidth=0, bd=0, text="", font=('meiryo', 12))
    frame5 = Frame(root, width=400, height=350, borderwidth=1, relief='solid')
    frame6 = Frame(root, width=400, height=350, borderwidth=1, relief='solid')
    frame7 = Frame(root, width=400, height=350, borderwidth=1, relief='solid')
    frame8 = Frame(root, width=400, height=350, borderwidth=1, relief='solid')

    # Frameサイズを固定
    labelframe_1.grid_propagate(False)
    labelframe_2.grid_propagate(False)
    labelframe_3.grid_propagate(False)
    labelframe_4.grid_propagate(False)
    frame5.grid_propagate(False)
    frame6.grid_propagate(False)
    frame7.grid_propagate(False)
    frame8.grid_propagate(False)

    # Frameを配置（grid）
    labelframe_1.grid(row=0, column=0,padx=10,pady=10)
    labelframe_2.grid(row=1, column=0,padx=10,pady=10)
    labelframe_3.grid(row=2, column=0,rowspan=2, padx=10,pady=10)
    #frame4.grid(row=0, column=1, rowspan=3)
    frame5.grid(row=0, column=1, rowspan=2, sticky=S)
    frame6.grid(row=0, column=2, rowspan=2, sticky=S)
    frame7.grid(row=2, column=1, rowspan=2, sticky=N)
    frame8.grid(row=2, column=2, rowspan=2, sticky=N)

    # ---------- ③Widget配置  ----------- #
    # フレーム1
    #labelframe_1 = LabelFrame(frame1, bd=0, text="")
    button_1a = Button(labelframe_1, text=' Connect  ', width=10, command=click_btn_1a)
    button_1b = Button(labelframe_1, text='Disconnect', width=10, command=click_btn_1b)
    button_1c = Button(labelframe_1, text=' Startup  ', width=10, command=click_btn_1c)
    button_1d = Button(labelframe_1, text=' Radar go ', width=10, command=click_btn_1d)
    #labelframe_1.pack(padx=5, pady=5, anchor=W, side=TOP)
    #button_1a.pack(padx=5, pady=5, side=LEFT)
    #button_1a.grid_propagate(False)
    button_1a.grid(row=0,column=0,padx=5,pady=10,ipadx=5,ipady=5,sticky=W)
    #button_1b.pack(padx=5, pady=5, side=LEFT)
    #button_1b.grid_propagate(False)
    button_1b.grid(row=0,column=1,padx=5,pady=10,ipadx=5,ipady=5,sticky=W)
    #button_1c.pack(padx=5, pady=5, side=BOTTOM)
    #button_1c.grid_propagate(False)
    button_1c.grid(row=1,column=0,padx=5,pady=10,ipadx=5,ipady=5,sticky=W)
    #button_1d.pack(padx=5, pady=5, side=BOTTOM)
    #button_1d.grid_propagate(False)
    button_1d.grid(row=1,column=1,padx=5,pady=10,ipadx=5,ipady=5,sticky=W)

    # フレーム2
    #labelframe_2 = LabelFrame(frame2, bd=4, text="One register setting", font=('system', 14))
    #labelframe_2.propagate(FALSE)
    button_2a = Button(labelframe_2, text='REG WRITE', width=12, command=click_btn_2a)
    button_2b = Button(labelframe_2, text='REG READ ', width=12, command=click_btn_2b)
    label_2x  = Label(labelframe_2, text='', width=12)
    label_2a  = Label(labelframe_2, text='Page  ', width=10)
    label_2b  = Label(labelframe_2, text='Adress', width=10)
    label_2c  = Label(labelframe_2, text='Data  ', width=10)
    entry_2a  = Entry(labelframe_2, width=12)
    entry_2b  = Entry(labelframe_2, width=12)
    entry_2c  = Entry(labelframe_2, width=12)
    #button_2c = Button(frame2, width=30, text='Startup',    command=click_btn_2a)
    #button_2d = Button(frame2, width=30, text='Radar go',   command=click_btn_2a)
    #labelframe_2.pack(padx=5, pady=5, anchor=W, side=TOP)
    #labelframe_2.grid(row=0,column=0)
    button_2a.grid(row=0,column=0,padx=5,pady=10,ipadx=5,ipady=5,sticky=W)
    #button_2a.pack(padx=5,pady=10,ipadx=5,ipady=5,side=LEFT)
    button_2b.grid(row=0,column=1,padx=5,pady=10,ipadx=5,ipady=5,sticky=W)
    #button_2b.pack(padx=5,pady=10,ipadx=5,ipady=5,side=LEFT)
    label_2x.grid(row=0,column=2,padx=5,pady=10,ipadx=5,ipady=5,sticky=W)
    label_2a.grid(row=1,column=0,padx=5,pady=0,sticky=W)
    label_2b.grid(row=1,column=1,padx=5,pady=0,sticky=W)
    label_2c.grid(row=1,column=2,padx=5,pady=0,sticky=W)
    entry_2a.grid(row=2,column=0,padx=5,pady=5)
    entry_2b.grid(row=2,column=1,padx=5,pady=5)
    entry_2c.grid(row=2,column=2,padx=5,pady=5)
    #button_2c.pack(padx=5, pady=5, side=TOP)
    #button_2d.pack(padx=5, pady=5, side=TOP)
    #labelframe_2.propagate(FALSE)

    # フレーム3
    #labelframe_3 = LabelFrame(frame3, bd=4, text="All register read", font=('system', 14))
    #button_3a = Button(labelframe_3, text='READ ALL PAGE', width=12, command=click_btn_2a)
    #label_3x  = Label(labelframe_3, text='', width=12)
    #label_3y  = Label(labelframe_3, text='', width=12)
    #label_3a  = Label(labelframe_3, text='Page  ', width=10)
    #label_3b  = Label(labelframe_3, text='Adress', width=10)
    #label_3c  = Label(labelframe_3, text='Data  ', width=10)
    #entry_3a  = Entry(labelframe_3, width=12)
    #entry_3b  = Entry(labelframe_3, width=12)
    #entry_3c  = Entry(labelframe_3, width=12)
    #labelframe_3.propagate(FALSE)
    #labelframe_3.pack(padx=5,pady=5,anchor=W,side=TOP)
    #labelframe_3.grid(padx=5, pady=5, sticky=W)
    #button_3a.grid(row=0,column=0,padx=5,pady=5,ipadx=5,ipady=5,sticky=W)
    #label_3x.grid(row=0,column=1,padx=5,pady=5,ipadx=10,ipady=5,sticky=W)
    #label_3y.grid(row=0,column=1,padx=5,pady=5,ipadx=10,ipady=5,sticky=W)
    #label_3a.grid(row=1,column=0,padx=5,pady=0,sticky=W)
    #label_3b.grid(row=1,column=1,padx=5,pady=0,sticky=W)
    #label_3c.grid(row=1,column=2,padx=5,pady=0,sticky=W)
    #entry_3a.grid(row=2,column=0,padx=5,pady=5)
    #entry_3b.grid(row=2,column=1,padx=5,pady=5)
    #entry_3c.grid(row=2,column=2,padx=5,pady=5)      

    tree = ttk.Treeview(labelframe_3, columns=(1, 2, 3), show='headings', height=7)
    tree.column(1, anchor='center', width=90)
    tree.column(2, anchor='center', width=140)
    tree.column(3, anchor='center', width=140)
    tree.heading(1, text="Page")
    tree.heading(2, text="Adress")
    tree.heading(3, text="Data")
    tree.insert(parent='', index=0, iid=0, values=("0" , "00", "00"))
    tree.insert(parent='', index=1, iid=1, values=("1" , "00", "00"))
    tree.insert(parent='', index=2, iid=2, values=("2" , "00", "00"))
    tree.insert(parent='', index=3, iid=3, values=("3" , "00", "00"))
    tree.insert(parent='', index=4, iid=4, values=("4" , "00", "00"))
    tree.insert(parent='', index=5, iid=5, values=("5" , "00", "00"))
    tree.insert(parent='', index=6, iid=6, values=("6" , "00", "00"))
    tree.insert(parent='', index=7, iid=7, values=("7" , "00", "00"))
    tree.insert(parent='', index=8, iid=8, values=("8" , "00", "00"))
    tree.insert(parent='', index=9, iid=9, values=("9" , "00", "00"))
    button_3 = Button(labelframe_3, text='READ ALL PAGE', command=click_btn_3)
    style = ttk.Style()
    style.theme_use("winnative")
    style.map("Treeview")
    scrollbar = ttk.Scrollbar(labelframe_3, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    button_3.pack(padx=5,pady=5,ipadx=5,ipady=5,anchor=W,side=TOP)
    tree.pack(padx=5,pady=10,side=LEFT)
    scrollbar.pack(side=RIGHT, fill=Y)

    # フレーム4
    canvas_1a = Canvas(frame5,width=400,height=350)
    canvas_1a.propagate(False)
    canvas_1b = Canvas(frame6,width=400,height=350)
    canvas_1b.propagate(False)
    canvas_1c = Canvas(frame7,width=400,height=300)
    canvas_1d = Canvas(frame8,width=400,height=300)
    #canvas_1a.create_rectangle(10, 10, 290, 290, fill = 'white')
    canvas_1a_x = FigureCanvasTkAgg(figb, master=canvas_1a)
    #toolbar = NavigationToolbar2Tk(canvas_1a_x, canvas_1a)
    canvas_1a_x.draw()
    canvas_1a_x.get_tk_widget().pack()
    #label_1a_x = Label(canvas_1a, text='test', width=12)
    #label_1a_x.place(relx=0.02, rely=0.1, relheight=0.3, relwidth=0.95)
    #canvas_1b.create_rectangle(10, 10, 290, 290, fill = 'white')
    canvas_1b_x = FigureCanvasTkAgg(fig, master=canvas_1b)
    canvas_1b_x.draw()
    canvas_1b_x.get_tk_widget().pack()
    #canvas_1c.create_rectangle(10, 10, 290, 290)
    #canvas_1d.create_rectangle(10, 10, 290, 290)
    #canvas_1a.grid(row=0,column=0,padx=0,pady=0)
    canvas_1a.pack()
    canvas_1b.pack()
    canvas_1c.pack()
    canvas_1d.pack()
    #canvas_1b.grid(row=0,column=1,padx=0,pady=0)

    #canvas_1c.grid(row=1,column=0,padx=0,pady=0)
    #canvas_1d.grid(row=1,column=1,padx=0,pady=0)

    # Canvas操作用ボタン（フレーム5右下）
    #button_5a = Button(frame5, text='描く', width=15, 
    #                   command=lambda: canvas.create_rectangle(10, 10, 140, 140, tag='rect'))
    #button_5a.pack(padx=5, pady=10)
    #button_5b = Button(frame5, text='削除', width=15, 
    #                   command=lambda: canvas.delete('rect'))
    #button_5b.pack(padx=5, pady=10)

    #root.update()
    #root.deiconify()
    root.mainloop()