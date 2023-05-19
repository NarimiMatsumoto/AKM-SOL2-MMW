
import tkinter as tk
from tkinter import ttk

import pyautogui

import sys
import os
import asyncio
from integ_method import Integ_Method

input_mode = 1 #0:comand line 1:file
cur_dir = os.path.dirname(__file__)
#cmd_file = "test.txt"
cmd_file = "0325test.txt"
cmd_filepath = cur_dir + "\\" + cmd_file


class App:
    async def exec(self):
        self.window = Window(asyncio.get_event_loop())
        await self.window.show();


class Window(tk.Tk):
    def __init__(self, loop):
        self.loop = loop
        self.root = tk.Tk()
        self.root.geometry("400x200")
        self.label = tk.Label(text="")
        self.label.grid(row=0, columnspan=2, padx=(8, 8), pady=(16, 0))

        button_connect = tk.Button(text="Connect", width=10, command=lambda: self.loop.create_task(self.con_ble()))
        button_connect.grid(row=0, column=0, sticky=tk.W, padx=8, pady=8)

        button_read = tk.Button(text="Read", width=10, command=lambda: self.loop.create_task(self.read_reg(txt_rpage.get(), txt_raddress.get())))
        button_read.grid(row=1, column=1, sticky=tk.W, padx=8, pady=8)

        button_write = tk.Button(text="Write", width=10, command=lambda: self.loop.create_task(self.write_reg(txt_wpage.get(), txt_waddress.get(), txt_wdata.get())))
        button_write.grid(row=2, column=1, sticky=tk.W, padx=8, pady=8)
     
        button_radargo= tk.Button(text="Radar_Go", width=10, command=lambda: self.loop.create_task(self.radargo()))
        button_radargo.grid(row=3, column=1, sticky=tk.W, padx=8, pady=8)

        txt_rpage = tk.Entry(width=4)
        txt_rpage.grid(row=1, column=2, sticky=tk.W, padx=8, pady=8)
        txt_rpage.insert(0,"0")
        txt_raddress = tk.Entry(width=6)
        txt_raddress.grid(row=1, column=3, sticky=tk.W, padx=8, pady=8)
        txt_raddress.insert(0,"1")

        txt_wpage = tk.Entry(width=4)
        txt_wpage.grid(row=2, column=2, sticky=tk.W, padx=8, pady=8)
        txt_wpage.insert(0,"0")
        txt_waddress = tk.Entry(width=6)
        txt_waddress.grid(row=2, column=3, sticky=tk.W, padx=8, pady=8)
        txt_waddress.insert(0,"2")
        txt_wdata = tk.Entry(width=6)
        txt_wdata.grid(row=2, column=4, sticky=tk.W, padx=8, pady=8)
        txt_wdata.insert(0,"64")

    async def show(self):
        while True:
            self.root.update()
            await asyncio.sleep(.1)

    async def radargo(self):
        pyautogui.hotkey('altleft','tab')
        pyautogui.write('radar_go')
        pyautogui.press('enter')
        pyautogui.hotkey('altleft','tab')

    async def read_reg(self, txt_rpage, txt_raddress):
        pyautogui.hotkey('altleft','tab')
        pyautogui.write('reg_r '+ txt_rpage + ' ' + txt_raddress)
        pyautogui.press('enter')
        pyautogui.hotkey('altleft','tab')

    async def write_reg(self, txt_wpage, txt_waddress, txt_wdata):
        pyautogui.hotkey('altleft','tab')
        pyautogui.write('reg_w ' + txt_wpage + ' ' + txt_waddress + ' ' + txt_wdata)
        pyautogui.press('enter')
        pyautogui.hotkey('altleft','tab')

    async def con_ble(self):
        async with Integ_Method() as uart:
            await uart.connect()
            loop = asyncio.get_running_loop()

#Register
            uart.T_LOOP = 1000 #msec integer > 40msec due to frame dropped (100msec if FLG_PLOT=1)
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
                    print("start typing and press ENTER...")
                    data = await loop.run_in_executor(None, sys.stdin.buffer.readline) #data format : b'reg r 1 2 5\r\n'
                    await uart._exe_cmd(data)
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
		asyncio.run(App().exec())
	except asyncio.CancelledError as ce:
		print(ce)
		# task is cancelled on disconnect, so we ignore this error
		pass
	except asyncio.QueueEmpty as qe:
		print(qe)
		pass

#asyncio.run(App().exec())