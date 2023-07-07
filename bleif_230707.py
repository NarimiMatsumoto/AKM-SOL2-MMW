
import sys
import os
import asyncio
from integ_method import Integ_Method

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import nest_asyncio

input_mode = 0 #0:comand line 1:file
cur_dir = os.path.dirname(__file__)
#cmd_file = "test.txt"
cmd_file = "0325test.txt"
cmd_filepath = cur_dir + "\\" + cmd_file

nest_asyncio.apply()

async def async_function(data):
    uart = Integ_Method()
    #data1 = data.encode()
    print(data)
    #await Integ_Method._exe_cmd(data)
    #data1 = await asyncio.get_running_loop().run_in_executor(None, sys.stdin.buffer.readline)
    await uart._exe_cmd(data)

def GUI():

	def msg_show(message):
		messagebox.showinfo("メッセージ", message)

	def btn_click():
		print("rader GO from tkinter GUI!!!")					
		line = entry_2a.get()
		data = line.encode()
		#thread1 = threading.Thread(target=uart._exe_cmd, args=(data))
		#thread1.start()
		#await uart._exe_cmd(data)
		print(data)
		#asyncio.new_event_loop().run_in_executor(None, Integ_Method._exe_cmd, data)
        #asyncio.new_event_loop().run_in_executor(None, Integ_Method._exe_cmd, data)
        #return data
		#loop = asyncio.get_event_loop()
		#result = loop.run_until_complete(async_function(data))
		#data = 'reg_r 0 115'
		#print(data)
		#asyncio.run(async_function(data))
		#await Integ_Method._exe_cmd(data)

		asyncio.run(async_function(data))

#class GUI:
	root = Tk()
	
# ----------- ①Window作成 ----------- #
	root.title('tkinterの使い方')   # 画面タイトル設定
	root.geometry('500x200')       # 画面サイズ設定
	root.resizable(False, False)   # リサイズ不可に設定

# ----------- ②Frameを定義 ----------- #
	frame1 = Frame(root, width=250, height=100, borderwidth=1, relief='raised')
	frame2 = Frame(root, width=250, height=100, borderwidth=1, relief='ridge')
	frame3 = Frame(root, width=500, height=100, borderwidth=1, relief='raised')
# Frameサイズを固定
	frame1.propagate(False)
	frame2.propagate(False)
	frame3.propagate(False)
# Frameを配置（grid）
	frame1.grid(row=0, column=0)
	frame2.grid(row=0, column=1)
	frame3.grid(row=1, column=0, columnspan=2)

# Button（フレーム1）
	button_1a = Button(frame1, text="ボタン", command=lambda: msg_show("ボタンが押されました。"))
	button_1a.pack(padx=5, pady=10)
	button_1a.pack(anchor='center',expand=1)

# テキストボックス（フレーム2）
	entry_2a = Entry(frame2, width=14)
	text = StringVar()
	button_2a = Button(frame2, text='文字列コピー', command=lambda: text.set(entry_2a.get()))
	label_2a = Label(frame2, textvariable=text, font=('System', 12))
	entry_2a.pack(side=LEFT)
	button_2a.pack(side=LEFT)
	label_2a.pack(side=LEFT)

# テキストボックス（フレーム3）
	button_3a = Button(frame3, text='print', command=btn_click)
	label_3a = Label(frame3, textvariable=text, font=('System', 12))
	button_3a.pack(anchor='center',expand=1)

	#root.mainloop()

# アプリケーションを更新する関数を呼び出す
	root.update()

# イベントループを手動で制御
	while True:
		try:
			root.update()
		except TclError:
			break

async def main():

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
#MAIN
		if input_mode == 0 :
			while True:

				#root = Tk()

				#def msg_show(message):
					#messagebox.showinfo("メッセージ", message)

				#async def btn_click():
					#print("rader GO from tkinter GUI!!!")					
					#line = entry_2a.get()
					#data = line.encode()
					#thread1 = threading.Thread(target=uart._exe_cmd, args=(data))
					#thread1.start()
					#await uart._exe_cmd(data)
					#print(data)
					#asyncio.new_event_loop().run_in_executor(None, uart._exe_cmd(data))

				#root = Tk()

				# ----------- ①Window作成 ----------- #
				#root.title('tkinterの使い方')   # 画面タイトル設定
				#root.geometry('500x200')       # 画面サイズ設定
				#root.resizable(False, False)   # リサイズ不可に設定

				# ----------- ②Frameを定義 ----------- #
				#frame1 = Frame(root, width=250, height=100, borderwidth=1, relief='raised')
				#frame2 = Frame(root, width=250, height=100, borderwidth=1, relief='ridge')
				#frame3 = Frame(root, width=500, height=100, borderwidth=1, relief='raised')
				# Frameサイズを固定
				#frame1.propagate(False)
				#frame2.propagate(False)
				#frame3.propagate(False)
				# Frameを配置（grid）
				#frame1.grid(row=0, column=0)
				#frame2.grid(row=0, column=1)
				#frame3.grid(row=1, column=0, columnspan=2)

				# Button（フレーム1）
				#button_1a = Button(frame1, text="ボタン", command=lambda: msg_show("ボタンが押されました。"))
				#button_1a.pack(padx=5, pady=10)
				#button_1a.pack(anchor='center',expand=1)

				# テキストボックス（フレーム2）
				#entry_2a = Entry(frame2, width=14)
				#text = StringVar()
				#button_2a = Button(frame2, text='文字列コピー', command=lambda: text.set(entry_2a.get()))
				#label_2a = Label(frame2, textvariable=text, font=('System', 12))
				#entry_2a.pack(side=LEFT)
				#button_2a.pack(side=LEFT)
				#label_2a.pack(side=LEFT)

				# テキストボックス（フレーム3）
				#button_3a = Button(frame3, text='print', command=btn_click)
				#label_3a = Label(frame3, textvariable=text, font=('System', 12))
				#button_3a.pack(anchor='center',expand=1)

				#root.mainloop()

				gui = GUI()
				#loop1 = asyncio.get_event_loop()
				#loop1.run_until_complete(gui())
				thread = threading.Thread(target=gui)
				thread.start()

				#print("start typing and press ENTER...")
				#data = await loop.run_in_executor(None, sys.stdin.buffer.readline) #data format : b'reg r 1 2 5\r\n'
				#data = gui()
				#await uart._exe_cmd(data)
		else:
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
		asyncio.run(main())
		#loop = asyncio.get_event_loop()
		#loop.run_until_complete(main())
		#main()
	except asyncio.CancelledError as ce:
		print(ce)
		# task is cancelled on disconnect, so we ignore this error
		pass
	except asyncio.QueueEmpty as qe:
		print(qe)
		pass

