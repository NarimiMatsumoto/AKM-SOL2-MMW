import tkinter as tk
from tkinter import ttk

import sys
import os
import asyncio
from integ_method import Integ_Method

input_mode = 0 #0:comand line 1:file
cur_dir = os.path.dirname(__file__)
#cmd_file = "test.txt"
cmd_file = "1_rpu_exec.txt"
cmd_filepath = cur_dir + "\\" + cmd_file

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

				# ボタンが押されたときの処理
				# def button_click(event):
				async def button_click(event):
					print("rader GO from tkinter GUI!!!")
					# data = line.encode("reg_r 0 115")
					data = await loop.run_in_executor(None, sys.stdin.buffer.readline) #data format : b'reg r 1 2 5\r\n'
					await uart._exe_cmd(data)						

				# rootメインウィンドウの設定
				root = tk.Tk()
				root.title("Setting")
				root.geometry("400x200")

				# メインフレームの作成と設置
				frame = tk.Frame(root)
				frame.pack(padx=20, pady=10)

				# 各種ウィジェットの作成
				button = ttk.Button(frame, text="rader go")
				# button = ttk.Button(frame, text="rader go", command=lambda:await uart.button_click())
				# 各種ウィジェットの設置
				button.grid(row=0, column=0)

				# #イベント処理の設定
				# button.bind("<ButtonPress>", button_click)
				# button.bind("<ButtonPress>", await uart.button_click)
				button.bind("<ButtonPress>", lambda event: asyncio.ensure_future(button_click(event)))
				# loop = asyncio.get_event_loop() # get the event loop which schedule my coroutine
    			# loop.run_forever()
				# asyncio.get_event_loop().run_until_complete()

				root.mainloop()

				# print("start typing and press ENTER...")
				# data = await loop.run_in_executor(None, sys.stdin.buffer.readline) #data format : b'reg r 1 2 5\r\n'
				# await uart._exe_cmd(data)

				##### 2023/06/06 matsumoto end ####

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
	except asyncio.CancelledError as ce:
		print(ce)
		# task is cancelled on disconnect, so we ignore this error
		pass
	except asyncio.QueueEmpty as qe:
		print(qe)
		pass