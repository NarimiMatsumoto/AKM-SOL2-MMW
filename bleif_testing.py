import tkinter as tk
from tkinter import ttk

#import subprocess

#import pyautogui

import sys
import os
import asyncio
from integ_method import Integ_Method

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
	global event
	global readdata
	i = 0
	event = 0
	readdata = 0

	def __init__(self, loop):

		self.loop = loop
		self.root = tk.Tk()

		self.root.title('AK5816')
		self.root.geometry("1250x710")
		#self.label = tk.Label(text="")
		#self.label.grid(row=0, columnspan=2, padx=(8, 8), pady=(16, 0))
		
		labelframe_1 = tk.LabelFrame(self.root, width=400, height=200, borderwidth=0, bd=0, text="", font=('meiryo', 12))
		labelframe_2 = tk.LabelFrame(self.root, width=400, height=150, borderwidth=0, bd=4, text="One register setting", font=('meiryo', 12))
		labelframe_3 = tk.LabelFrame(self.root, width=400, height=200, borderwidth=0, bd=4, text="All register read", font=('meiryo', 12))
		labelframe_4 = tk.LabelFrame(self.root, width=400, height=150, borderwidth=0, bd=0, text="", font=('meiryo', 12))
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
		button_start   = tk.Button(labelframe_1, text=" Startup  ", width=10, command=lambda: click_btn_start())
		button_radargo = tk.Button(labelframe_1, text=" Radar go ", width=10, command=lambda: click_btn_radargo())
		button_pdnl    = tk.Button(labelframe_1, text="  PDN L   ", width=10, command=lambda: asyncio.create_task(self.pdngui(0)))
		button_pdnh    = tk.Button(labelframe_1, text="  PDN H   ", width=10, command=lambda: asyncio.create_task(self.pdngui(1)))
		button_rstnl   = tk.Button(labelframe_1, text="  RSTN L  ", width=10, command=lambda: asyncio.create_task(self.rstngui(0)))
		button_rstnh   = tk.Button(labelframe_1, text="  RSTN H  ", width=10, command=lambda: asyncio.create_task(self.rstngui(1)))
		button_execl   = tk.Button(labelframe_1, text="  EXEC L  ", width=10, command=lambda: asyncio.create_task(self.execgui(0)))
		button_exech   = tk.Button(labelframe_1, text="  EXEC H  ", width=10, command=lambda: asyncio.create_task(self.execgui(1)))

		button_connect.grid(row=0, column=0, sticky=tk.W, padx=5, pady=8, ipadx=5, ipady=5)
		button_discon.grid(row=0, column=1, sticky=tk.W, padx=5, pady=8, ipadx=5, ipady=5)
		button_start.grid(row=1, column=0, sticky=tk.W,  padx=5, pady=8, ipadx=5, ipady=5)
		button_radargo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=8, ipadx=5, ipady=5)
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
		button_allread = ttk.Button(labelframe_3, text='READ ALL PAGE', command=lambda: click_btn_allread())
		style = ttk.Style()
		style.theme_use("winnative")
		style.map("Treeview")
		scrollbar = ttk.Scrollbar(labelframe_3, orient=tk.VERTICAL, command=tree.yview)
		tree.configure(yscroll=scrollbar.set)
		button_allread.pack(padx=5,pady=5,ipadx=5,ipady=5,anchor=tk.W,side=tk.TOP)
		tree.pack(padx=5,pady=10,side=tk.LEFT)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		def readback(readdata):
			global i
			if (i == 0):#Readボタンが押されたら
				button_write['state'] = 'disabled'#Writeボタンを押せないようにする
				txt_wdata.delete(0,tk.END) #データ部分を空白にする(printによってデータを読み出せてはいるが表示はできないため)
				i += 1
			else:#Readボタンをもう一回押してもらったら
				button_write['state'] = 'normal'#Writeボタンを有効に戻す
				txt_wdata.insert(0,readdata) #データ部分にレジスタ読み出し結果を表示する
				i -= 1

		def click_btn_start():
			button_start['text'] = 'クリックしました'

		def click_btn_radargo():
			button_radargo['text'] = 'クリックしました'

		def click_btn_allread():
			button_allread['text'] = 'クリックしました'

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

	# Idling until button pushed
	async def idle(self):
		text = "sleep 0.5"
		data = text.encode
		return data

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
#MAIN
			if input_mode == 0 :# GUI control
				while True:
					if(event == 0):# idle state
						data = await loop.run_in_executor(None, await self.idle())
						await uart._exe_cmd(data)
					elif(event == 1):# Write command event
						data = await loop.run_in_executor(None, await self.command())
						await uart._exe_cmd(data)
					elif(event == 2):# Read back command event
						data = await loop.run_in_executor(None, await self.command_read())
						readdata = await uart._exe_cmd(data)
						print(readdata)
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