import tkinter as tk
from tkinter import ttk

#import subprocess

#import pyautogui

import sys
import os
import asyncio
from integ_method import Integ_Method
from tkinter import filedialog
from gen_graph import GEN_GRAPH
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

input_mode = 0 #0:GUI control #1:CUI control #2:File/CUI
cur_dir = os.path.dirname(__file__)
#cmd_file = "test.txt"
#cmd_file = "2_adcout_by_exec.txt"
cmd_file = "1_rpu_exec.txt"
cmd_filepath = cur_dir + "\\" + cmd_file

class App:
    async def exec(self):
        self.window = Window(asyncio.get_event_loop())
        await self.window.show();

class Window(tk.Tk):

	# グローバル変数を宣言
	global i
	global j
	global event
	global readdata
	global p_readdata
	global lines
	i = 0
	j = 0
	event = 0
	readdata = 0
	p_readdata = [0] * 128
	lines = []

	def __init__(self, loop):

		self.loop = loop
		self.root = tk.Tk()

		self.root.title('AK5816')
		self.root.geometry("1250x710")
		#self.label = tk.Label(text="")
		#self.label.grid(row=0, columnspan=2, padx=(8, 8), pady=(16, 0))
		
		labelframe_1 = tk.LabelFrame(self.root, width=400, height=200, borderwidth=0, bd=0, text="", font=('meiryo', 12))
		labelframe_2 = tk.LabelFrame(self.root, width=400, height=150, borderwidth=0, bd=4, text="One register setting", font=('meiryo', 12))
		labelframe_3 = tk.LabelFrame(self.root, width=400, height=250, borderwidth=0, bd=4, text="Page read", font=('meiryo', 12))
		labelframe_4 = tk.LabelFrame(self.root, width=400, height=100, borderwidth=0, bd=0, text="", font=('meiryo', 12))
		frame5 = tk.Frame(self.root, width=400, height=350, borderwidth=1, relief='solid')
		frame6 = tk.Frame(self.root, width=400, height=350, borderwidth=1, relief='solid')
		frame7 = tk.Frame(self.root, width=400, height=350, borderwidth=1, relief='solid')
		frame8 = tk.Frame(self.root, width=400, height=350, borderwidth=1, relief='solid')

		labelframe_1.grid_propagate(False)
		labelframe_2.grid_propagate(False)
		labelframe_3.grid_propagate(False)
		labelframe_4.grid_propagate(False)
		frame5.grid_propagate(False)
		frame6.grid_propagate(False)
		frame7.grid_propagate(False)
		frame8.grid_propagate(False)

		labelframe_1.grid(row=0, column=0,padx=10,pady=2)
		labelframe_2.grid(row=1, column=0,padx=10,pady=2)
		labelframe_3.grid(row=2, column=0,padx=10,pady=2)
		labelframe_4.grid(row=3, column=0,padx=10,pady=2)
		frame5.grid(row=0, column=1, rowspan=2, sticky=tk.N)
		frame6.grid(row=0, column=2, rowspan=2, sticky=tk.N)
		frame7.grid(row=2, column=1, rowspan=2, sticky=tk.N)
		frame8.grid(row=2, column=2, rowspan=2, sticky=tk.N)

		button_connect = tk.Button(labelframe_1, text=" Connect  ", width=10, command=lambda: self.loop.create_task(self.connect_ble()))
		button_discon  = tk.Button(labelframe_1, text="Disconnect", width=10, command=lambda: asyncio.create_task(self.discongui()))
		button_stop    = tk.Button(labelframe_1, text="   STOP   ", width=10, command=lambda: asyncio.create_task(self.stpgui()))
		button_start   = tk.Button(labelframe_1, text=" Startup  ", width=10, command=lambda: asyncio.create_task(self.sugui()))
		button_radargo = tk.Button(labelframe_1, text=" Radar go ", width=10, command=lambda: asyncio.create_task(self.rggui()))
		button_setfile = tk.Button(labelframe_1, text=" SET File ", width=10, command=lambda: asyncio.create_task(self.sfgui()))
		button_exefile = tk.Button(labelframe_1, text=" EXEC File", width=10, command=lambda: asyncio.create_task(self.efgui()))
		button_pdnl    = tk.Button(labelframe_1, text="  PDN L   ", width=10, command=lambda: asyncio.create_task(self.pdngui(0)))
		button_pdnh    = tk.Button(labelframe_1, text="  PDN H   ", width=10, command=lambda: asyncio.create_task(self.pdngui(1)))
		button_rstnl   = tk.Button(labelframe_1, text="  RSTN L  ", width=10, command=lambda: asyncio.create_task(self.rstngui(0)))
		button_rstnh   = tk.Button(labelframe_1, text="  RSTN H  ", width=10, command=lambda: asyncio.create_task(self.rstngui(1)))
		button_execl   = tk.Button(labelframe_1, text="  EXEC L  ", width=10, command=lambda: asyncio.create_task(self.execgui(0)))
		button_exech   = tk.Button(labelframe_1, text="  EXEC H  ", width=10, command=lambda: asyncio.create_task(self.execgui(1)))

		button_connect.grid(row=0, column=0, sticky=tk.W, padx=5, pady=8, ipadx=5, ipady=5)
		button_discon.grid(row=0, column=1, sticky=tk.W, padx=5, pady=8, ipadx=5, ipady=5)
		button_stop.grid(row=0, column=2, sticky=tk.W, padx=5, pady=8, ipadx=5, ipady=5)
		button_start.grid(row=1, column=0, sticky=tk.W,  padx=5, pady=8, ipadx=5, ipady=5)
		button_radargo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=8, ipadx=5, ipady=5)
		button_setfile.grid(row=1, column=2, sticky=tk.W, padx=5, pady=8, ipadx=5, ipady=5)
		button_exefile.grid(row=1, column=3, sticky=tk.W, padx=5, pady=8, ipadx=5, ipady=5)
		button_pdnl.grid(row=2, column=0, sticky=tk.W, padx=5, pady=8, ipadx=5, ipady=5)
		button_pdnh.grid(row=3, column=0, sticky=tk.W, padx=5, pady=8, ipadx=5, ipady=5)
		button_rstnl.grid(row=2, column=1, sticky=tk.W, padx=5, pady=8, ipadx=5, ipady=5)
		button_rstnh.grid(row=3, column=1, sticky=tk.W, padx=5, pady=8, ipadx=5, ipady=5)
		button_execl.grid(row=2, column=2, sticky=tk.W, padx=5, pady=8, ipadx=5, ipady=5)
		button_exech.grid(row=3, column=2, sticky=tk.W, padx=5, pady=8, ipadx=5, ipady=5)

		button_write = tk.Button(labelframe_2, text="Write", width=10, command=lambda: asyncio.create_task(self.wrgui(txt_wpage.get(), txt_waddress.get(), txt_wdata.get())))
		button_read  = tk.Button(labelframe_2, text="Read ", width=10, command=lambda: [asyncio.create_task(self.rdgui(txt_wpage.get(), txt_waddress.get())), readback(readdata)])		
		label_xx     = tk.Label(labelframe_2, text='',       width=12)
		label_page   = tk.Label(labelframe_2, text='Page  ', width=10)
		label_address= tk.Label(labelframe_2, text='Adress', width=10)
		label_data   = tk.Label(labelframe_2, text='Data  ', width=10)
		txt_wpage    = tk.Entry(labelframe_2, justify=tk.RIGHT, width=10)
		txt_waddress = tk.Entry(labelframe_2, justify=tk.RIGHT, width=10)
		txt_wdata    = tk.Entry(labelframe_2, justify=tk.RIGHT, width=10)

		button_write.grid(row=0, column=0, sticky=tk.W, padx=5, pady=10, ipadx=5, ipady=5)
		button_read.grid(row=0, column=1, sticky=tk.W, padx=5, pady=10, ipadx=5, ipady=5)
		label_xx.grid(row=0, column=2, sticky=tk.W, padx=5, pady=10, ipadx=5, ipady=5)
		label_page.grid(row=1, column=0, sticky=tk.W, padx=5, pady=0)
		label_address.grid(row=1, column=1, sticky=tk.W, padx=5, pady=0)
		label_data.grid(row=1, column=2, sticky=tk.W, padx=5, pady=0)
		txt_wpage.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
		txt_waddress.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
		txt_wdata.grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)

		txt_wpage.insert(0,"0")
		txt_waddress.insert(0,"1")
		txt_wdata.insert(0,"97")

		tree = ttk.Treeview(labelframe_3, columns=(1, 2, 3), show='headings', height=7)
		tree.column(1, anchor='center', width=90)
		tree.column(2, anchor='center', width=130)
		tree.column(3, anchor='center', width=130)
		tree.heading(1, text="Page")
		tree.heading(2, text="Adress")
		tree.heading(3, text="Data")
		tree.insert(parent='', index=0, iid=0, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=1, iid=1, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=2, iid=2, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=3, iid=3, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=4, iid=4, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=5, iid=5, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=6, iid=6, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=7, iid=7, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=8, iid=8, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=9, iid=9, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=10, iid=10, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=11, iid=11, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=12, iid=12, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=13, iid=13, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=14, iid=14, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=15, iid=15, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=16, iid=16, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=17, iid=17, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=18, iid=18, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=19, iid=19, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=20, iid=20, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=21, iid=21, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=22, iid=22, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=23, iid=23, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=24, iid=24, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=25, iid=25, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=26, iid=26, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=27, iid=27, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=28, iid=28, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=29, iid=29, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=30, iid=30, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=31, iid=31, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=32, iid=32, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=33, iid=33, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=34, iid=34, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=35, iid=35, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=36, iid=36, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=37, iid=37, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=38, iid=38, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=39, iid=39, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=40, iid=40, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=41, iid=41, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=42, iid=42, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=43, iid=43, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=44, iid=44, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=45, iid=45, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=46, iid=46, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=47, iid=47, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=48, iid=48, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=49, iid=49, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=50, iid=50, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=51, iid=51, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=52, iid=52, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=53, iid=53, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=54, iid=54, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=55, iid=55, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=56, iid=56, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=57, iid=57, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=58, iid=58, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=59, iid=59, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=60, iid=60, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=61, iid=61, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=62, iid=62, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=63, iid=63, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=64, iid=64, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=65, iid=65, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=66, iid=66, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=67, iid=67, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=68, iid=68, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=69, iid=69, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=70, iid=70, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=71, iid=71, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=72, iid=72, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=73, iid=73, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=74, iid=74, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=75, iid=75, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=76, iid=76, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=77, iid=77, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=78, iid=78, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=79, iid=79, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=80, iid=80, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=81, iid=81, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=82, iid=82, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=83, iid=83, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=84, iid=84, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=85, iid=85, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=86, iid=86, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=87, iid=87, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=88, iid=88, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=89, iid=89, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=90, iid=90, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=91, iid=91, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=92, iid=92, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=93, iid=93, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=94, iid=94, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=95, iid=95, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=96, iid=96, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=97, iid=97, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=98, iid=98, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=99, iid=99, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=100, iid=100, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=101, iid=101, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=102, iid=102, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=103, iid=103, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=104, iid=104, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=105, iid=105, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=106, iid=106, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=107, iid=107, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=108, iid=108, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=109, iid=109, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=110, iid=110, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=111, iid=111, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=112, iid=112, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=113, iid=113, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=114, iid=114, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=115, iid=115, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=116, iid=116, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=117, iid=117, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=118, iid=118, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=119, iid=119, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=120, iid=120, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=121, iid=121, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=122, iid=122, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=123, iid=123, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=124, iid=124, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=125, iid=125, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=126, iid=126, values=("0" , "0x00", "00"))
		tree.insert(parent='', index=127, iid=127, values=("0" , "0x00", "00"))
		button_allread = ttk.Button(labelframe_3, text='READ PAGE', command=lambda: [asyncio.create_task(self.p_rdgui(txt_rpage.get())), p_readback(p_readdata)])
		#label_rpage    = tk.Label(labelframe_3, text='Page', width=10)
		txt_rpage      = tk.Entry(labelframe_3, justify=tk.RIGHT, width=10)
		#txt_rpage.insert(0,"0")
		style = ttk.Style()
		style.theme_use("winnative")
		style.map("Treeview")
		scrollbar = ttk.Scrollbar(labelframe_3, orient=tk.VERTICAL, command=tree.yview)
		tree.configure(yscroll=scrollbar.set)
		button_allread.pack(side=tk.LEFT, padx=5, pady=5)
		button_allread.grid(row=0, column=0, padx=(5, 0), pady=5, ipadx=5, ipady=5, sticky=tk.W)
		#label_rpage.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky=tk.W)
		txt_rpage.grid(row=0, column=1, padx=(0, 5), pady=5, ipadx=2, ipady=2, sticky=tk.W)
		tree.grid(row=1, column=0, columnspan=3, padx=(5, 0), pady=10, sticky=tk.W)
		scrollbar.grid(row=1, column=3, padx=0, pady=10, sticky=tk.NS)

		def readback(readdata):
			global i
			if (i == 0):#Readボタンが押されたら
				button_write['state'] = 'disabled'#Writeボタンを押せないようにする
				txt_wdata.delete(0,tk.END) #データ部分を空白にする(printによってデータを読み出せてはいるが表示はできないため)
				i += 1
			else:#Readボタンをもう一回押してもらったら
				button_write['state'] = 'normal'#Writeボタンを有効に戻す
				#print(readdata)
				txt_wdata.insert(0,readdata) #データ部分にレジスタ読み出し結果を表示する
				i -= 1
		
		def p_readback(p_readdata):
			global j
			if (j == 0):#Readボタンが押されたら
				tree.item(0,values=("", "", "")) #データ部分を空白にする(printによってデータを読み出せてはいるが表示はできないため)
				tree.item(1,values=("", "", ""))
				tree.item(2,values=("", "", ""))
				tree.item(3,values=("", "", ""))
				tree.item(4,values=("", "", ""))
				tree.item(5,values=("", "", ""))
				tree.item(6,values=("", "", ""))
				tree.item(7,values=("", "", ""))
				tree.item(8,values=("", "", ""))
				tree.item(9,values=("", "", ""))
				tree.item(10,values=("", "", ""))
				tree.item(11,values=("", "", ""))
				tree.item(12,values=("", "", ""))
				tree.item(13,values=("", "", ""))
				tree.item(14,values=("", "", ""))
				tree.item(15,values=("", "", ""))
				tree.item(16,values=("", "", ""))
				tree.item(17,values=("", "", ""))
				tree.item(18,values=("", "", ""))
				tree.item(19,values=("", "", ""))
				tree.item(20,values=("", "", ""))
				tree.item(21,values=("", "", ""))
				tree.item(22,values=("", "", ""))
				tree.item(23,values=("", "", ""))
				tree.item(24,values=("", "", ""))
				tree.item(25,values=("", "", ""))
				tree.item(26,values=("", "", ""))
				tree.item(27,values=("", "", ""))
				tree.item(28,values=("", "", ""))
				tree.item(29,values=("", "", ""))
				tree.item(30,values=("", "", ""))
				tree.item(31,values=("", "", ""))
				tree.item(32,values=("", "", ""))
				tree.item(33,values=("", "", ""))
				tree.item(34,values=("", "", ""))
				tree.item(35,values=("", "", ""))
				tree.item(36,values=("", "", ""))
				tree.item(37,values=("", "", ""))
				tree.item(38,values=("", "", ""))
				tree.item(39,values=("", "", ""))
				tree.item(40,values=("", "", ""))
				tree.item(41,values=("", "", ""))
				tree.item(42,values=("", "", ""))
				tree.item(43,values=("", "", ""))
				tree.item(44,values=("", "", ""))
				tree.item(45,values=("", "", ""))
				tree.item(46,values=("", "", ""))
				tree.item(47,values=("", "", ""))
				tree.item(48,values=("", "", ""))
				tree.item(49,values=("", "", ""))
				tree.item(50,values=("", "", ""))
				tree.item(51,values=("", "", ""))
				tree.item(52,values=("", "", ""))
				tree.item(53,values=("", "", ""))
				tree.item(54,values=("", "", ""))
				tree.item(55,values=("", "", ""))
				tree.item(56,values=("", "", ""))
				tree.item(57,values=("", "", ""))
				tree.item(58,values=("", "", ""))
				tree.item(59,values=("", "", ""))
				tree.item(60,values=("", "", ""))
				tree.item(61,values=("", "", ""))
				tree.item(62,values=("", "", ""))
				tree.item(63,values=("", "", ""))
				tree.item(64,values=("", "", ""))
				tree.item(65,values=("", "", ""))
				tree.item(66,values=("", "", ""))
				tree.item(67,values=("", "", ""))
				tree.item(68,values=("", "", ""))
				tree.item(69,values=("", "", ""))
				tree.item(70,values=("", "", ""))
				tree.item(71,values=("", "", ""))
				tree.item(72,values=("", "", ""))
				tree.item(73,values=("", "", ""))
				tree.item(74,values=("", "", ""))
				tree.item(75,values=("", "", ""))
				tree.item(76,values=("", "", ""))
				tree.item(77,values=("", "", ""))
				tree.item(78,values=("", "", ""))
				tree.item(79,values=("", "", ""))
				tree.item(80,values=("", "", ""))
				tree.item(81,values=("", "", ""))
				tree.item(82,values=("", "", ""))
				tree.item(83,values=("", "", ""))
				tree.item(84,values=("", "", ""))
				tree.item(85,values=("", "", ""))
				tree.item(86,values=("", "", ""))
				tree.item(87,values=("", "", ""))
				tree.item(88,values=("", "", ""))
				tree.item(89,values=("", "", ""))
				tree.item(90,values=("", "", ""))
				tree.item(91,values=("", "", ""))
				tree.item(92,values=("", "", ""))
				tree.item(93,values=("", "", ""))
				tree.item(94,values=("", "", ""))
				tree.item(95,values=("", "", ""))
				tree.item(96,values=("", "", ""))
				tree.item(97,values=("", "", ""))
				tree.item(98,values=("", "", ""))
				tree.item(99,values=("", "", ""))
				tree.item(100,values=("", "", ""))
				tree.item(101,values=("", "", ""))
				tree.item(102,values=("", "", ""))
				tree.item(103,values=("", "", ""))
				tree.item(104,values=("", "", ""))
				tree.item(105,values=("", "", ""))
				tree.item(106,values=("", "", ""))
				tree.item(107,values=("", "", ""))
				tree.item(108,values=("", "", ""))
				tree.item(109,values=("", "", ""))
				tree.item(110,values=("", "", ""))
				tree.item(111,values=("", "", ""))
				tree.item(112,values=("", "", ""))
				tree.item(113,values=("", "", ""))
				tree.item(114,values=("", "", ""))
				tree.item(115,values=("", "", ""))
				tree.item(116,values=("", "", ""))
				tree.item(117,values=("", "", ""))
				tree.item(118,values=("", "", ""))
				tree.item(119,values=("", "", ""))
				tree.item(120,values=("", "", ""))
				tree.item(121,values=("", "", ""))
				tree.item(122,values=("", "", ""))
				tree.item(123,values=("", "", ""))
				tree.item(124,values=("", "", ""))
				tree.item(125,values=("", "", ""))
				tree.item(126,values=("", "", ""))
				tree.item(127,values=("", "", ""))
				j += 1
			else:#Readボタンをもう一回押してもらったら
				#print(p_readdata)
				p = txt_rpage.get()
				tree.item(0,values=(p, "0x00", p_readdata[0])) #データ部分にレジスタ読み出し結果を表示する
				tree.item(1,values=(p, "0x01", p_readdata[1]))
				tree.item(2,values=(p, "0x02", p_readdata[2]))
				tree.item(3,values=(p, "0x03", p_readdata[3]))
				tree.item(4,values=(p, "0x04", p_readdata[4]))
				tree.item(5,values=(p, "0x05", p_readdata[5]))
				tree.item(6,values=(p, "0x06", p_readdata[6]))
				tree.item(7,values=(p, "0x07", p_readdata[7]))
				tree.item(8,values=(p, "0x08", p_readdata[8]))
				tree.item(9,values=(p, "0x09", p_readdata[9]))
				tree.item(10,values=(p, "0x0A", p_readdata[10]))
				tree.item(11,values=(p, "0x0B", p_readdata[11]))
				tree.item(12,values=(p, "0x0C", p_readdata[12]))
				tree.item(13,values=(p, "0x0D", p_readdata[13]))
				tree.item(14,values=(p, "0x0E", p_readdata[14]))
				tree.item(15,values=(p, "0x0F", p_readdata[15]))
				tree.item(16,values=(p, "0x10", p_readdata[16]))
				tree.item(17,values=(p, "0x11", p_readdata[17]))
				tree.item(18,values=(p, "0x12", p_readdata[18]))
				tree.item(19,values=(p, "0x13", p_readdata[19]))
				tree.item(20,values=(p, "0x14", p_readdata[20]))
				tree.item(21,values=(p, "0x15", p_readdata[21]))
				tree.item(22,values=(p, "0x16", p_readdata[22]))
				tree.item(23,values=(p, "0x17", p_readdata[23]))
				tree.item(24,values=(p, "0x18", p_readdata[24]))
				tree.item(25,values=(p, "0x19", p_readdata[25]))
				tree.item(26,values=(p, "0x1A", p_readdata[26]))
				tree.item(27,values=(p, "0x1B", p_readdata[27]))
				tree.item(28,values=(p, "0x1C", p_readdata[28]))
				tree.item(29,values=(p, "0x1D", p_readdata[29]))
				tree.item(30,values=(p, "0x1E", p_readdata[30]))
				tree.item(31,values=(p, "0x1F", p_readdata[31]))
				tree.item(32,values=(p, "0x20", p_readdata[32]))
				tree.item(33,values=(p, "0x21", p_readdata[33]))
				tree.item(34,values=(p, "0x22", p_readdata[34]))
				tree.item(35,values=(p, "0x23", p_readdata[35]))
				tree.item(36,values=(p, "0x24", p_readdata[36]))
				tree.item(37,values=(p, "0x25", p_readdata[37]))
				tree.item(38,values=(p, "0x26", p_readdata[38]))
				tree.item(39,values=(p, "0x27", p_readdata[39]))
				tree.item(40,values=(p, "0x28", p_readdata[40]))
				tree.item(41,values=(p, "0x29", p_readdata[41]))
				tree.item(42,values=(p, "0x2A", p_readdata[42]))
				tree.item(43,values=(p, "0x2B", p_readdata[43]))
				tree.item(44,values=(p, "0x2C", p_readdata[44]))
				tree.item(45,values=(p, "0x2D", p_readdata[45]))
				tree.item(46,values=(p, "0x2E", p_readdata[46]))
				tree.item(47,values=(p, "0x2F", p_readdata[47]))
				tree.item(48,values=(p, "0x30", p_readdata[48]))
				tree.item(49,values=(p, "0x31", p_readdata[49]))
				tree.item(50,values=(p, "0x32", p_readdata[50]))
				tree.item(51,values=(p, "0x33", p_readdata[51]))
				tree.item(52,values=(p, "0x34", p_readdata[52]))
				tree.item(53,values=(p, "0x35", p_readdata[53]))
				tree.item(54,values=(p, "0x36", p_readdata[54]))
				tree.item(55,values=(p, "0x37", p_readdata[55]))
				tree.item(56,values=(p, "0x38", p_readdata[56]))
				tree.item(57,values=(p, "0x39", p_readdata[57]))
				tree.item(58,values=(p, "0x3A", p_readdata[58]))
				tree.item(59,values=(p, "0x3B", p_readdata[59]))
				tree.item(60,values=(p, "0x3C", p_readdata[60]))
				tree.item(61,values=(p, "0x3D", p_readdata[61]))
				tree.item(62,values=(p, "0x3E", p_readdata[62]))
				tree.item(63,values=(p, "0x3F", p_readdata[63]))
				tree.item(64,values=(p, "0x40", p_readdata[64]))
				tree.item(65,values=(p, "0x41", p_readdata[65]))
				tree.item(66,values=(p, "0x42", p_readdata[66]))
				tree.item(67,values=(p, "0x43", p_readdata[67]))
				tree.item(68,values=(p, "0x44", p_readdata[68]))
				tree.item(69,values=(p, "0x45", p_readdata[69]))
				tree.item(70,values=(p, "0x46", p_readdata[70]))
				tree.item(71,values=(p, "0x47", p_readdata[71]))
				tree.item(72,values=(p, "0x48", p_readdata[72]))
				tree.item(73,values=(p, "0x49", p_readdata[73]))
				tree.item(74,values=(p, "0x4A", p_readdata[74]))
				tree.item(75,values=(p, "0x4B", p_readdata[75]))
				tree.item(76,values=(p, "0x4C", p_readdata[76]))
				tree.item(77,values=(p, "0x4D", p_readdata[77]))
				tree.item(78,values=(p, "0x4E", p_readdata[78]))
				tree.item(79,values=(p, "0x4F", p_readdata[79]))
				tree.item(80,values=(p, "0x50", p_readdata[80]))
				tree.item(81,values=(p, "0x51", p_readdata[81]))
				tree.item(82,values=(p, "0x52", p_readdata[82]))
				tree.item(83,values=(p, "0x53", p_readdata[83]))
				tree.item(84,values=(p, "0x54", p_readdata[84]))
				tree.item(85,values=(p, "0x55", p_readdata[85]))
				tree.item(86,values=(p, "0x56", p_readdata[86]))
				tree.item(87,values=(p, "0x57", p_readdata[87]))
				tree.item(88,values=(p, "0x58", p_readdata[88]))
				tree.item(89,values=(p, "0x59", p_readdata[89]))
				tree.item(90,values=(p, "0x5A", p_readdata[90]))
				tree.item(91,values=(p, "0x5B", p_readdata[91]))
				tree.item(92,values=(p, "0x5C", p_readdata[92]))
				tree.item(93,values=(p, "0x5D", p_readdata[93]))
				tree.item(94,values=(p, "0x5E", p_readdata[94]))
				tree.item(95,values=(p, "0x5F", p_readdata[95]))
				tree.item(96,values=(p, "0x60", p_readdata[96]))
				tree.item(97,values=(p, "0x61", p_readdata[97]))
				tree.item(98,values=(p, "0x62", p_readdata[98]))
				tree.item(99,values=(p, "0x63", p_readdata[99]))
				tree.item(100,values=(p, "0x64", p_readdata[100]))
				tree.item(101,values=(p, "0x65", p_readdata[101]))
				tree.item(102,values=(p, "0x66", p_readdata[102]))
				tree.item(103,values=(p, "0x67", p_readdata[103]))
				tree.item(104,values=(p, "0x68", p_readdata[104]))
				tree.item(105,values=(p, "0x69", p_readdata[105]))
				tree.item(106,values=(p, "0x6A", p_readdata[106]))
				tree.item(107,values=(p, "0x6B", p_readdata[107]))
				tree.item(108,values=(p, "0x6C", p_readdata[108]))
				tree.item(109,values=(p, "0x6D", p_readdata[109]))
				tree.item(110,values=(p, "0x6E", p_readdata[110]))
				tree.item(111,values=(p, "0x6F", p_readdata[111]))
				tree.item(112,values=(p, "0x70", p_readdata[112]))
				tree.item(113,values=(p, "0x71", p_readdata[113]))
				tree.item(114,values=(p, "0x72", p_readdata[114]))
				tree.item(115,values=(p, "0x73", p_readdata[115]))
				tree.item(116,values=(p, "0x74", p_readdata[116]))
				tree.item(117,values=(p, "0x75", p_readdata[117]))
				tree.item(118,values=(p, "0x76", p_readdata[118]))
				tree.item(119,values=(p, "0x77", p_readdata[119]))
				tree.item(120,values=(p, "0x78", p_readdata[120]))
				tree.item(121,values=(p, "0x79", p_readdata[121]))
				tree.item(122,values=(p, "0x7A", p_readdata[122]))
				tree.item(123,values=(p, "0x7B", p_readdata[123]))
				tree.item(124,values=(p, "0x7C", p_readdata[124]))
				tree.item(125,values=(p, "0x7D", p_readdata[125]))
				tree.item(126,values=(p, "0x7E", p_readdata[126]))
				tree.item(127,values=(p, "0x7F", p_readdata[127]))
				p_readdata = [0] * 128
				j -= 1

		canvas_a = tk.Canvas(frame5,width=400,height=350)
		canvas_a.propagate(False)
		gen_graph_instance = GEN_GRAPH()
		[fig, ax] = gen_graph_instance._init_graph()
		#canvas_a.create_rectangle(2, 2, 400, 350, fill = 'white')
		canvas_a_x = FigureCanvasTkAgg(fig, master=canvas_a)
		canvas_a_x.draw()
		canvas_a_x.get_tk_widget().pack()
		canvas_a.pack()

	async def show(self):
		while True:
			self.root.update()
			await asyncio.sleep(.1)

	# Disconnect
	async def discongui(self):
		global event
		print("now disconnecting...")
		event = 99 #break

	# PDN pin control
	async def pdngui(self,a):
		global d, event
		d = "pdn " + str(a)
		event = 1 # Write command event

	# RSTN pin control
	async def rstngui(self,a):
		global d, event
		d = "rstn " + str(a)
		event = 1 # Write command event

	# EXEC pin control
	async def execgui(self,a):
		global d, event
		d = "execonly " + str(a)
		event = 1 # Write command event

	# A Register Write
	async def wrgui(self,page,address,data):
		global d, event
		d = "reg_w " + str(page) +" " + str(address) + " " + str(data)
		event = 1 # Write command event

	# A Register Read
	async def rdgui(self,page,address):
		global d, event
		d = "reg_r " + str(page) +" " + str(address)
		event = 2 # Read back command event

	# A Page Read
	async def p_rdgui(self,page):
		global d, event
		d = "read_pg " + str(page)
		event = 3 # Page Read back command event

	# Idling until button pushed
	async def idle(self):
		text = "sleep 0.5"
		data = text.encode
		return data

	# Start up
	async def sugui(self):
		global d, event
		d = "startup"
		event = 1 # command event

	# Radar go
	async def rggui(self):
		global d, event
		d = "radar_go"
		event = 1 # command event
		#global lines, event
		#cmd = "radar_go"
		#add_cmd = cmd.encode()
		#lines.append(add_cmd)
		#event = 4 # command event

	# Stop
	async def stpgui(self):
		await Integ_Method._flg_stph(self)
		return

	# Set file
	async def sfgui(self):
		global lines, event
		initial_dir = os.getcwd()
		file_path = filedialog.askopenfilename(initialdir=initial_dir)

		if not file_path:
			print("ファイルが選択されませんでした。")
			lines = []
			return lines

		try:
			with open(file_path, 'r', encoding='utf-8') as f:
				for line in f:
					if "#" in line[0]:
						pass
					else:
						lines.append(line.strip())
		except UnicodeDecodeError:
			with open(file_path, 'r', encoding='shift_jis') as f:
				for line in f:
					if "#" in line[0]:
						pass
					else:
						lines.append(line.strip())
		
		lines = [line.encode() for line in lines]
		event = 0 # command event
		return lines

	# Execute file
	async def efgui(self):
		global event
		event = 4 # command event

	async def command(self):
		global event
		data = d.encode
		event = 0 # Go to idle state
		return data

	async def command_read(self):
		global event
		global readdata
		data = d.encode
		event = 0 # Go to idle state
		return data

	async def command_p_read(self):
		global event
		global p_readdata
		data = d.encode
		event = 0 # Go to idle state
		return data

	async def command_exec(self):
		global event
		text = "sleep 0.5"
		data = text.encode
		event = 0 # Go to idle state
		return data

	async def connect_ble(self):
		async with Integ_Method() as uart:
			await uart.connect()
			loop = asyncio.get_running_loop()

#Register
			uart.T_LOOP = 100 #msec integer > 40msec due to frame dropped (100msec if FLG_PLOT=1)
			uart.SEQRD_DATSEL = 0
			uart.SEQRD_BEGIN = 0
			uart.SEQRD_END = 127
#FILE, CONSOLE
			uart.FLG_SAVE = 0
			uart.LMT_SAVE_FRM = 50
			uart.FILE_PATH = cur_dir + "\\tgtlst.xlsx"
			uart.FLG_DISP = 1
			uart.UPDATE_FRM = 20
			uart.DISP_IDNUM = 4
#GRAPH
			uart.FLG_PLOT = 1 # T_LOOP > 100msec if you set 1
			
			global readdata
			global p_readdata
			global lines
#MAIN
			if input_mode == 0 :# GUI control
				while True:
					if(event == 0):# idle state
						data = await loop.run_in_executor(None, await self.idle())
						#print(data)
						await uart._exe_cmd(data)
						#print(event)
					elif(event == 1):# Write command event
						data = await loop.run_in_executor(None, await self.command())
						#print(data)
						await uart._exe_cmd(data)
					elif(event == 2):# Read back command event
						data = await loop.run_in_executor(None, await self.command_read())
						readdata = await uart._exe_cmd(data)
					elif(event == 3):# Page Read back command event
						data = await loop.run_in_executor(None, await self.command_p_read())
						p_readdata = await uart._exe_cmd(data)
					elif(event == 4):# 
						for cmd in lines:
							#print(cmd)
							await uart._exe_cmd(cmd)
							#print(event)
						#await asyncio.sleep(0.1)
						data = await loop.run_in_executor(None, await self.command_exec())
						await uart._exe_cmd(data)
					elif(event == 99):# disconnect
						break

			elif input_mode == 1 :# CUI control
				while True:
					print("start typing and press ENTER...")
					data = await loop.run_in_executor(None, sys.stdin.buffer.readline) #data format : b'reg r 1 2 5\r\n'
					await uart._exe_cmd(data)

			else: # File/CUI
				with open(cmd_filepath) as f:
					for line in f:
						if "#" in line[0] :
							pass
						else:
							data = line.encode()
							await uart._exe_cmd(data)
				while True:
					print("start typing and press ENTER...")
					data = await loop.run_in_executor(None, sys.stdin.buffer.readline) #data format : b'reg r 1 2 5\r\n'
					await uart._exe_cmd(data)

if __name__ == "__main__":
	try:
		#asyncio.run(main())
		asyncio.run(App().exec())
	except asyncio.CancelledError as ce:
		print(ce)
		# task is cancelled on disconnect, so we ignore this error
		pass
	except asyncio.QueueEmpty as qe:
		print(qe)
		pass

