#
import tkinter as tk
from tkinter import ttk
import sys
import os
import asyncio
import time
from integ_method import Integ_Method
from tkinter import filedialog
from gen_graph import GEN_GRAPH
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

input_mode = 0 #0:GUI control #1:CUI control #2:File/CUI
cur_dir = os.path.dirname(__file__)
cmd_file = "1_rpu_exec.txt"
cmd_filepath = cur_dir + "\\" + cmd_file
init_file = "0_initial_set.txt"
init_filepath = cur_dir + "\\" + init_file
tgtlst_file = "tgtlst.xlsx"
fftlst_iq_file = "fftlst_iq.xlsx"
fftlst_mag_file = "fftlst_mag.xlsx"

class App:
    async def exec(self):
        self.window = Window(asyncio.get_event_loop())
        await self.window.show();

class Window(tk.Tk):

	# Global variables
	global i, j
	global event
	global readdata, p_readdata
	global lines
	global conchk
	global fpath
	i = 0
	j = 0
	event = 0
	readdata = 0
	p_readdata = [0] * 128
	lines = []
	conchk = 0

	# tikinter setting (GUI Window setting)
	def __init__(self, loop):

		self.loop = loop

		self.root = tk.Tk()
		self.root.title('AK5816 Control Software')
		self.root.geometry("1612x906")
		self.root.configure(bg="#FFFFFF")

		#Frame setting(1-14)
		labelframe_1 = tk.LabelFrame(self.root, width=250, height=225, bg='#FFFFFF', borderwidth=0, bd=2, text="Setup", font=('Arial', 13))
		labelframe_2 = tk.LabelFrame(self.root, width=250, height=225, bg='#FFFFFF', borderwidth=0, bd=2, text="One register setting", font=('Arial', 13))
		labelframe_3 = tk.LabelFrame(self.root, width=250, height=225, bg='#FFFFFF', borderwidth=0, bd=2, text="Page read", font=('Arial', 13))
		labelframe_4 = tk.LabelFrame(self.root, width=250, height=225, bg='#FFFFFF', borderwidth=0, bd=2, text="Radar Operation", font=('Arial', 13))
		labelframe_5 = tk.LabelFrame(self.root, width=250, height=225, bg='#FFFFFF', borderwidth=0, bd=2, text="Frame 5", font=('Arial', 13))
		labelframe_6 = tk.LabelFrame(self.root, width=250, height=225, bg='#FFFFFF', borderwidth=0, bd=2, text="Frame 6", font=('Arial', 13))
		labelframe_7 = tk.LabelFrame(self.root, width=250, height=225, bg='#FFFFFF', borderwidth=0, bd=2, text="Frame 7", font=('Arial', 13))
		labelframe_8 = tk.LabelFrame(self.root, width=250, height=225, bg='#FFFFFF', borderwidth=0, bd=2, text="Frame 8", font=('Arial', 13))
		frame11 = tk.Frame(self.root, width=500, height=450, bg='#FFFFFF', borderwidth=1, relief='solid')
		frame12 = tk.Frame(self.root, width=500, height=450, bg='#FFFFFF', borderwidth=1, relief='solid')
		frame13 = tk.Frame(self.root, width=500, height=450, bg='#FFFFFF', borderwidth=1, relief='solid')
		frame14 = tk.Frame(self.root, width=500, height=450, bg='#FFFFFF', borderwidth=1, relief='solid')

		labelframe_1.grid_propagate(False)
		labelframe_2.grid_propagate(False)
		labelframe_3.grid_propagate(False)
		labelframe_4.grid_propagate(False)
		labelframe_5.grid_propagate(False)
		labelframe_6.grid_propagate(False)
		labelframe_7.grid_propagate(False)
		labelframe_8.grid_propagate(False)
		frame11.grid_propagate(False)
		frame12.grid_propagate(False)
		frame13.grid_propagate(False)
		frame14.grid_propagate(False)

		labelframe_1.grid(row=0, column=0,padx=10,pady=0, ipadx=0, ipady=0)
		labelframe_2.grid(row=1, column=0,padx=10,pady=0, ipadx=0, ipady=0)
		labelframe_3.grid(row=2, column=0,padx=10,pady=0, ipadx=0, ipady=0)
		labelframe_4.grid(row=3, column=0,padx=10,pady=0, ipadx=0, ipady=0)
		labelframe_5.grid(row=0, column=1,padx=10,pady=0, ipadx=0, ipady=0)
		labelframe_6.grid(row=1, column=1,padx=10,pady=0, ipadx=0, ipady=0)
		labelframe_7.grid(row=2, column=1,padx=10,pady=0, ipadx=0, ipady=0)
		labelframe_8.grid(row=3, column=1,padx=10,pady=0, ipadx=0, ipady=0)
		frame11.grid(row=0, column=2, rowspan=2,padx=5,pady=2, ipadx=2, ipady=2)
		frame12.grid(row=0, column=3, rowspan=2,padx=5,pady=2, ipadx=2, ipady=2)
		frame13.grid(row=2, column=2, rowspan=2,padx=5,pady=2, ipadx=2, ipady=2)
		frame14.grid(row=2, column=3, rowspan=2,padx=5,pady=2, ipadx=2, ipady=2)

		#labelframe_1 widget setting
		button_connect = tk.Button(labelframe_1, text="Connect", font=('Arial', 11), width=7, height=1, relief='raised', fg='#000000', bg='#BFC0C0', command=lambda: self.loop.create_task(self.connect_ble()))
		button_discon  = tk.Button(labelframe_1, state="disabled", text="Disconnect", font=('Arial', 11), relief='groove', fg='#000000', bg='#F5F5F5', width=10, height=1, command=lambda: asyncio.create_task(self.discongui()))
		button_conchk  = tk.Button(labelframe_1, text="Check", font=('Arial', 11), width=7, height=1, relief='raised', fg='#000000', bg='#BFC0C0', command=lambda: ConnectStateCheck())
		label_conchk   = tk.Label(labelframe_1, text='Not Connected', font=('Arial', 11), bg='#F5F5F5', width=10, height=1)
		button_start   = tk.Button(labelframe_1, text="StrtUp", font=('Arial', 11), width=7, height=1, relief='raised', fg='#000000', bg='#BFC0C0', command=lambda: asyncio.create_task(self.strtup()))
		button_selfile = tk.Button(labelframe_1, text="FileSel", font=('Arial', 11), width=7, height=1, relief='raised', fg='#000000', bg='#BFC0C0', command=lambda: asyncio.create_task(self.filesel()))
		button_fileset = tk.Button(labelframe_1, text="FileSet", font=('Arial', 11), width=7, height=1, relief='raised', fg='#000000', bg='#BFC0C0', command=lambda: [asyncio.create_task(self.fileset()), fileview()])
		txt_selfile    = tk.Entry(labelframe_1, font=('Arial', 11), bg='#F5F5F5', justify=tk.LEFT, width=28)
		button_pdnl    = tk.Button(labelframe_1, text="PDN L", font=('Arial', 11), width=7, height=1, relief='raised', fg='#FFFFFF', bg='#BFC0C0', command=lambda: asyncio.create_task(self.pdnpin(0)))
		button_pdnh    = tk.Button(labelframe_1, text="PDN H", font=('Arial', 11), width=7, height=1, relief='raised', fg='#FFFFFF', bg='#BFC0C0', command=lambda: asyncio.create_task(self.pdnpin(1)))
		button_rstnl   = tk.Button(labelframe_1, text="RSTN L", font=('Arial', 11), width=7, height=1, relief='raised', fg='#FFFFFF', bg='#BFC0C0', command=lambda: asyncio.create_task(self.rstnpin(0)))
		button_rstnh   = tk.Button(labelframe_1, text="RSTN H", font=('Arial', 11), width=7, height=1, relief='raised', fg='#FFFFFF', bg='#BFC0C0', command=lambda: asyncio.create_task(self.rstnpin(1)))
		button_execl   = tk.Button(labelframe_1, text="EXEC L", font=('Arial', 11), width=7, height=1, relief='raised', fg='#FFFFFF', bg='#BFC0C0', command=lambda: asyncio.create_task(self.execpin(0)))
		button_exech   = tk.Button(labelframe_1, text="EXEC H", font=('Arial', 11), width=7, height=1, relief='raised', fg='#FFFFFF', bg='#BFC0C0', command=lambda: asyncio.create_task(self.execpin(1)))

		button_connect.grid(row=0, column=0, padx=3, pady=2, ipadx=0, ipady=0)
		button_discon.grid(row=0, column=1, columnspan=2, padx=3, pady=2, ipadx=0, ipady=0, sticky=tk.W)
		button_conchk.grid(row=1, column=0, padx=3, pady=2, ipadx=0, ipady=0)
		label_conchk.grid(row=1, column=1, columnspan=2, padx=3, pady=2, ipadx=0, ipady=0, sticky=tk.W)
		button_start.grid(row=2, column=0,  padx=3, pady=2, ipadx=0, ipady=0)
		button_selfile.grid(row=2, column=1, padx=3, pady=2, ipadx=0, ipady=0)
		button_fileset.grid(row=2, column=2, padx=3, pady=2, ipadx=0, ipady=0)
		txt_selfile.grid(row=3, column=0, columnspan=3, padx=3, pady=2, ipadx=0, ipady=1)
		button_pdnl.grid(row=4, column=0, padx=3, pady=2, ipadx=0, ipady=0)
		button_pdnh.grid(row=5, column=0, padx=3, pady=2, ipadx=0, ipady=0)
		button_rstnl.grid(row=4, column=1, padx=3, pady=2, ipadx=0, ipady=0)
		button_rstnh.grid(row=5, column=1, padx=3, pady=2, ipadx=0, ipady=0)
		button_execl.grid(row=4, column=2, padx=3, pady=2, ipadx=0, ipady=0)
		button_exech.grid(row=5, column=2, padx=3, pady=2, ipadx=0, ipady=0)

		txt_selfile.insert(0,"Not selected")
		
		def ConnectStateCheck():
			global conchk
			if(conchk == 1):
				label_conchk['text'] = "Connected"
				label_conchk['fg'] = '#005BAC'
				button_connect['state'] = 'disabled'
				button_connect['bg'] = '#F5F5F5'
				button_connect['relief'] = 'groove'
				button_discon['state'] = 'normal'
				button_discon['bg'] = '#BFC0C0'
				button_discon['relief'] = 'raised'
			else:
				label_conchk['text'] = "Not Connected"
				button_connect['state'] = 'normal'
				button_connect['bg'] = '#BFC0C0'
				button_connect['relief'] = 'raised'

		def fileview():
			filenameonly = os.path.basename(fpath)
			txt_selfile.delete(0, tk.END)
			txt_selfile.insert(0,filenameonly)

		#labelframe_2 widget setting
		button_write = tk.Button(labelframe_2, state="disabled", text="Write", font=('Arial', 11), relief='groove', fg='#000000', bg='#F5F5F5', width=24, command=lambda: [asyncio.create_task(self.writeone(txt_wpage.get(), txt_waddress.get(), txt_wdata.get())), wrdisable()])
		button_read  = tk.Button(labelframe_2, state="disabled", text="Read", font=('Arial', 11), relief='groove', fg='#000000', bg='#F5F5F5', width=24, command=lambda: [onereadback(readdata), wrdisable()])
		button_wrset  = tk.Button(labelframe_2, text="Set", font=('Arial', 11), relief='raised', fg='#000000', bg='#BFC0C0', width=24, command=lambda: [asyncio.create_task(self.readone(txt_wpage.get(), txt_waddress.get())), wrenable()])
		label_page   = tk.Label(labelframe_2, text='Page', font=('Arial', 11), relief='flat', fg='#000000', bg='#FFFFFF', width=8)
		label_address= tk.Label(labelframe_2, text='Address', font=('Arial', 11), relief='flat', fg='#000000', bg='#FFFFFF', width=8)
		label_data   = tk.Label(labelframe_2, text='Data', font=('Arial', 11), relief='flat', fg='#000000', bg='#FFFFFF', width=8)
		txt_wpage    = tk.Entry(labelframe_2, justify=tk.RIGHT, font=('Arial', 11), fg='#000000', bg='#F5F5F5', width=8)
		txt_waddress = tk.Entry(labelframe_2, justify=tk.RIGHT, font=('Arial', 11), fg='#000000', bg='#F5F5F5', width=8)
		txt_wdata    = tk.Entry(labelframe_2, justify=tk.RIGHT, font=('Arial', 11), fg='#000000', bg='#F5F5F5', width=8)
		label_memo   = tk.Label(labelframe_2, text='If text is "0x", its Hex. If not, its Dec.', font=('Arial', 8), relief='flat', fg='#000000', bg='#FFFFFF', width=38)

		label_page.grid(row=0, column=0, padx=1, pady=3, ipadx=0, ipady=0)
		label_address.grid(row=0, column=1, padx=1, pady=3, ipadx=0, ipady=0)
		label_data.grid(row=0, column=2, padx=1, pady=3, ipadx=0, ipady=0)
		txt_wpage.grid(row=1, column=0, padx=1, pady=3, ipadx=0, ipady=0)
		txt_waddress.grid(row=1, column=1, padx=1, pady=3, ipadx=0, ipady=0)
		txt_wdata.grid(row=1, column=2, padx=1, pady=3, ipadx=0, ipady=0)
		button_wrset.grid(row=2, column=0, columnspan=3, padx=1, pady=3, ipadx=0, ipady=0)
		button_write.grid(row=3, column=0, columnspan=3, padx=1, pady=3, ipadx=0, ipady=0)
		button_read.grid(row=4, column=0, columnspan=3, padx=1, pady=3, ipadx=0, ipady=0)
		label_memo.grid(row=5, column=0, columnspan=3, padx=1, pady=3, ipadx=0, ipady=0)

		txt_wpage.insert(0,"0")
		txt_waddress.insert(0,"0x01")
		txt_wdata.insert(0,"0x00")

		def wrenable():
			button_wrset['state'] = 'disabled'
			button_wrset['bg'] = '#F5F5F5'
			button_wrset['relief'] = 'groove'
			button_write['state'] = 'normal'
			button_write['bg'] = '#BFC0C0'
			button_write['relief'] = 'raised'
			button_read['state'] = 'normal'
			button_read['bg'] = '#BFC0C0'
			button_read['relief'] = 'raised'

		def wrdisable():
			button_wrset['state'] = 'normal'
			button_wrset['bg'] = '#BFC0C0'
			button_wrset['relief'] = 'raised'
			button_write['state'] = 'disabled'
			button_write['bg'] = '#F5F5F5'
			button_write['relief'] = 'groove'
			button_read['state'] = 'disabled'
			button_read['bg'] = '#F5F5F5'
			button_read['relief'] = 'groove'

		def onereadback(readdata):
			txt_wdata.delete(0,tk.END)
			#txt_wdata.insert(0,readdata) # Display the register read result in the data section (Decimal)
			txt_wdata.insert(0,f"0x{readdata:02X}") # (Hex.)

		#labelframe_3 widget setting
		txt_rpage      = tk.Entry(labelframe_3, justify=tk.CENTER, font=('Arial', 11), fg='#000000', bg='#F5F5F5', width=3)
		button_allset = tk.Button(labelframe_3, text='Set', font=('Arial', 11), relief='raised', fg='#000000', bg='#BFC0C0', width=7, command=lambda: [asyncio.create_task(self.pageread(txt_rpage.get())), prenable()])
		button_allread = tk.Button(labelframe_3, state="disabled", text='Read', font=('Arial', 11), relief='groove', fg='#000000', bg='#F5F5F5', width=7, command=lambda: [pagereadback(p_readdata), prdisable()])
		tree = ttk.Treeview(labelframe_3, columns=(1, 2, 3), show='headings', height=6)
		scrollbar = ttk.Scrollbar(labelframe_3, orient=tk.VERTICAL, command=tree.yview)

		txt_rpage.grid(row=0, column=0, padx=0, pady=3, ipadx=0, ipady=3, sticky=tk.E)
		button_allset.grid(row=0, column=1, padx=0, pady=3, ipadx=0, ipady=0, sticky=tk.E)
		button_allread.grid(row=0, column=2, padx=0, pady=3, ipadx=0, ipady=0)
		tree.grid(row=1, column=0, columnspan=3, padx=(12, 0), pady=5)
		scrollbar.grid(row=1, column=3, padx=0, pady=5, sticky=tk.NS)

		txt_rpage.insert(0,"0")

		tree.column(1, anchor='center', width=40)
		tree.column(2, anchor='center', width=77)
		tree.column(3, anchor='center', width=77)
		tree.heading(1, text="P.")
		tree.heading(2, text="Address")
		tree.heading(3, text="Data")
		tree.configure(yscroll=scrollbar.set)		

		n = 128
		for i in range(n):
			tree.insert(parent='', index=i, iid=i, values=("0", "0x00", "0x00"))

		style = ttk.Style(labelframe_3)
		style.theme_use("winnative")
		style.map("Treeview")
		style.configure("Treeview.Heading", font=("Arial", 11))
		style.configure("Treeview", font=("Arial", 11))

		def pagereadback(p_readdata):
			p = txt_rpage.get()
			for i, p_data in enumerate(p_readdata):
				#tree.item(i, values=(p, f"0x{i:02X}", p_data)) # Display the register read result in the data section (Decimal)
				tree.item(i, values=(p, f"0x{i:02X}", f"0x{p_data:02X}")) # (Hex.)
			p_readdata = [0] * 128

		def prenable():
			button_allread['state'] = 'normal'
			button_allread['bg'] = '#BFC0C0'
			button_allread['relief'] = 'raised'
			button_allset['state'] = 'disabled'
			button_allset['bg'] = '#F5F5F5'
			button_allset['relief'] = 'groove'

		def prdisable():
			button_allread['state'] = 'disabled'
			button_allread['bg'] = '#F5F5F5'
			button_allread['relief'] = 'groove'
			button_allset['state'] = 'normal'
			button_allset['bg'] = '#BFC0C0'
			button_allset['relief'] = 'raised'

		#labelframe_4 widget setting
		label_frmcnt  = tk.Label(labelframe_4, text='Frame count', font=('Arial', 11), bg='#FFFFFF', width=10, height=2)
		txt_captnum    = tk.Entry(labelframe_4, font=('Arial', 11), justify=tk.CENTER, width=7)
		button_captnumset = tk.Button(labelframe_4, text="Set", font=('Arial', 11), relief='raised', fg='#000000', bg='#BFC0C0', width=5, command=lambda: asyncio.create_task(self.captnumset(txt_captnum.get())))
		button_radargo = tk.Button(labelframe_4, text="EXEC & CUBE", font=('Arial', 11), relief='raised', fg='#000000', bg='#BFC0C0', width=24, command=lambda: asyncio.create_task(self.radar_go()))
		button_execfftcapt = tk.Button(labelframe_4, text="EXEC & FFT", font=('Arial', 11), relief='raised', fg='#000000', bg='#BFC0C0', width=24, command=lambda: asyncio.create_task(self.radar_go_and_fft_capt()))
		button_stop    = tk.Button(labelframe_4, text="STOP", font=('Arial', 11), relief='raised', fg='#000000', bg='#BFC0C0', width=24, command=lambda: asyncio.create_task(self.stpgui()))

		label_frmcnt.grid(row=0, column=0, padx=3, pady=3, ipadx=0, ipady=0)
		txt_captnum.grid(row=0, column=1, padx=3, pady=3, ipadx=0, ipady=0)
		button_captnumset.grid(row=0, column=2, padx=3, pady=3, ipadx=0, ipady=0)
		button_radargo.grid(row=1, column=0, columnspan=3, padx=3, pady=3, ipadx=0, ipady=0)
		button_execfftcapt.grid(row=2, column=0, columnspan=3, padx=3, pady=3, ipadx=0, ipady=0)
		button_stop.grid(row=3, column=0, columnspan=3, padx=3, pady=3, ipadx=0, ipady=0)

		txt_captnum.insert(0,"10")

		#labelframe_5 widget setting


		#labelframe_6 widget setting


		#labelframe_7 widget setting


		#labelframe_8 widget setting


		#frame_11 widget setting
		canvas_a = tk.Canvas(frame11,width=490,height=420)
		canvas_a.propagate(False)
		gen_graph_instance = GEN_GRAPH()
		[fig, ax] = gen_graph_instance._init_graph()
		canvas_a_x = FigureCanvasTkAgg(fig, master=canvas_a)
		canvas_a_x.draw()
		canvas_a_x.get_tk_widget().pack()
		canvas_a.pack()

		#frame_12 widget setting
		canvas_b = tk.Canvas(frame12,width=490,height=420)
		canvas_b.propagate(False)
		gen_graph_instance_b = GEN_GRAPH()
		[fig_b, ax] = gen_graph_instance_b._init_graph_2d()
		canvas_b_x = FigureCanvasTkAgg(fig_b, master=canvas_b)
		canvas_b_x.draw()
		canvas_b_x.get_tk_widget().pack()
		canvas_b.pack()

		#frame_13 widget setting
		canvas_c = tk.Canvas(frame13,width=490,height=420)
		canvas_c.propagate(False)
		gen_graph_instance_c = GEN_GRAPH()
		[fig_c, ax] = gen_graph_instance_c._init_graph_fft()
		canvas_c_x = FigureCanvasTkAgg(fig_c, master=canvas_c)
		canvas_c_x.draw()
		canvas_c_x.get_tk_widget().pack()
		canvas_c.pack()

		#frame_14 widget setting
		canvas_d = tk.Canvas(frame14,width=490,height=420)
		canvas_d.propagate(False)
		gen_graph_instance_d = GEN_GRAPH()
		[fig_d, ax] = gen_graph_instance_d._init_graph_d()
		canvas_d_x = FigureCanvasTkAgg(fig_d, master=canvas_d)
		canvas_d_x.draw()
		canvas_d_x.get_tk_widget().pack()
		canvas_d.pack()

	# For tkinter and asyncio operation (Don't change this code)
	async def show(self):
		while True:
			self.root.update()
			await asyncio.sleep(.1)

	# Disconnect
	async def discongui(self):
		global event
		print("now disconnecting...")
		event = 99 #break

	# Start up
	async def strtup(self):
		global d, event
		d = "startup"
		event = 1 # Write command

	# File select
	async def filesel(self):
		global lines, event, fpath
		initial_dir = os.getcwd()
		file_path = filedialog.askopenfilename(initialdir=initial_dir)
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
		event = 0 # Go to idle state
		fpath = file_path

	# File set
	async def fileset(self):
		global d, event
		d = "dummy" #If not enter a letter in d here, the program will stop, so put in a dummy." sleep 0.5" is also acceptable.
		event = 4 # File load

	# PDN pin control
	async def pdnpin(self,a):
		global d, event
		d = "pdn " + str(a)
		event = 1 # Write command

	# RSTN pin control
	async def rstnpin(self,a):
		global d, event
		d = "rstn " + str(a)
		event = 1 # Write command

	# EXEC pin control
	async def execpin(self,a):
		global d, event
		d = "execonly " + str(a)
		event = 1 # Write command

	# A Register Write
	async def writeone(self,page,address,data):
		global d, event
		if((str(address[0:2]) == "0x") & (str(data[0:2]) == "0x")):
			d = "reg_w " + str(page) +" " + str(int(address[2:],16)) + " " + str(int(data[2:],16))
		elif((str(address[0:2]) == "0x") & (str(data[0:2]) != "0x")):
			d = "reg_w " + str(page) +" " + str(int(address[2:],16)) + " " + str(data)
		elif((str(address[0:2]) != "0x") & (str(data[0:2]) == "0x")):
			d = "reg_w " + str(page) +" " + str(address) + " " + str(int(data[2:],16))
		else:
			d = "reg_w " + str(page) +" " + str(address) + " " + str(data)
		event = 1 # Write command

	# A Register Read
	async def readone(self,page,address):
		global d, event
		if(str(address[0:2]) == "0x"): # If it has "0x", treat it as a hex. number.
			d = "reg_r " + str(page) +" " + str(int(address[2:],16))
		else: # If there is no "0x" attached, it is treated as a decimal number.
			d = "reg_r " + str(page) +" " + str(address)
		event = 2 # Read register

	# A Page Read
	async def pageread(self,page):
		global d, event
		d = "read_pg " + str(page)
		event = 3 # Page Read

	# Capt number set
	async def captnumset(self,captnum):
		global d, event
		d = str(captnum)
		event = 5 # Capture number set

	# Radar go
	async def radar_go(self):
		global d,event
		d = "radar_go"
		event = 1 # Write command

	# Radar go and FFT capture
	async def radar_go_and_fft_capt(self):
		global d,event
		d = "radar_go_and_fft_capt"
		event = 1 # Write command

	# Stop
	async def stpgui(self):
		await Integ_Method._flg_stph(self)

	# Idling until button pushed
	async def idle(self):
		global conchk
		conchk = 1
		text = "sleep 0.5"
		data = text.encode
		return data

	#For asyncio and tkinter operation
	async def command(self):
		global event
		data = d.encode
		event = 0 # Go to idle state
		return data

	async def connect_ble(self):
		async with Integ_Method() as uart:
			#await uart.connect()
			await uart.connect()
			loop = asyncio.get_running_loop()
#Register
			uart.T_LOOP = 100 #msec integer > 40msec due to frame dropped (100msec if FLG_PLOT=1)
			uart.SEQRD_DATSEL = 0
			uart.SEQRD_BEGIN = 0
			uart.SEQRD_END = 127
			uart.RPU_SMPLS = 256
#FILE, CONSOLE
			uart.FLG_SAVE = 1
			uart.LMT_SAVE_FRM = 50
			#uart.FILE_PATH = cur_dir + "\\tgtlst.xlsx"
			uart.FILE_PATH = cur_dir + "\\" + tgtlst_file
			uart.FILE_PATH_FFT_IQ = cur_dir + "\\" + fftlst_iq_file
			uart.FILE_PATH_FFT_MAG = cur_dir + "\\" + fftlst_mag_file
			uart.FLG_DISP = 1
			uart.UPDATE_FRM = 5
			uart.DISP_IDNUM = 4
#GRAPH
			uart.FLG_PLOT = 1 # T_LOOP > 100msec if you set 1

			#uart.CAPT_NUM = 5
			
			global readdata
			global p_readdata
			global lines
#MAIN
			if input_mode == 0 :# GUI control
				with open(init_filepath) as f:
					for line in f:
						if "#" in line[0] :
							pass
						else:
							data = line.encode()
							await uart._exe_cmd(data)
				while True:
					if(event == 0):# idle state
						data = await loop.run_in_executor(None, await self.idle())
						await uart._exe_cmd(data)
					elif(event == 1):# Write command
						data = await loop.run_in_executor(None, await self.command())
						#print(f"data={data}")
						await uart._exe_cmd(data)
					elif(event == 2):# Read register
						data = await loop.run_in_executor(None, await self.command())
						readdata = await uart._exe_cmd(data)
					elif(event == 3):# Page Read
						data = await loop.run_in_executor(None, await self.command())
						p_readdata = await uart._exe_cmd(data)
					elif(event == 4):# File load
						data = await loop.run_in_executor(None, await self.command())
						for cmd in lines:
							await uart._exe_cmd(cmd)
					elif(event == 5):# Capture number set
						data = await loop.run_in_executor(None, await self.command())
						await uart._capt_num(data)
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

