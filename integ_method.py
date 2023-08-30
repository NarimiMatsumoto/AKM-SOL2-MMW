#
from ble_uart import BLE_UART
from gen_data import GEN_DATA
from gen_graph import GEN_GRAPH
import asyncio
import pandas as pd
import msvcrt
import time
# User need to import xlsxwriter by pip command

class Integ_Method(BLE_UART, GEN_DATA, GEN_GRAPH):
	PAGE = 0
	SEQRD_DATSEL = 0
	SEQRD_BEGIN = 0
	SEQRD_END = 127
	FLG_SAVE = 0
	LMT_SAVE_FRM = 50
	FILE_PATH = "D:\\tgtlst.csv"
	FILE_PATH_FFT_IQ = "D:\\fftlst_iq.csv"
	FILE_PATH_FFT_MAG = "D:\\fftlst_mag.csv"
	UPDATE_FRM = 5
	DISP_IDNUM = 4
	FLG_PLOT = 0
	FLG_DISP = 0
	T_LOOP = 50
	MAX_MTU = 512
	RPU_SMPLS = 256

	global CAPT_NUM
	CAPT_NUM = 5
	global FLG_STP_H
	FLG_STP_H = 0

	def __init__(self) -> None:
		BLE_UART.__init__(self)
		GEN_DATA.__init__(self)
		GEN_GRAPH.__init__(self)


######Access ESP32######
	async def _send_data(self, cmd:str):
		await self.write(cmd)


######Access SPI######

	#"_chg_pg": If a page-switching write is required during register access, send to change pages.
	#Input: Page number (string), command to rewrite page (ex.　256,2,3 ← write 3 to address 2 to make Page.3), print output (1)/not print (0)
	#Output: None
	#	If the input page number and the currently recognized page number (PAGE) are the same, nothing is done.
	#	If not, send a command to rewrite the page and overwrite the recognized page.
	async def _chg_pg(self, in_pg:str, pgcmd:str, logon:int):
		if int(in_pg) != self.PAGE: 
			await self._send_data(pgcmd)
			self.PAGE = int(in_pg)
			if logon == 1:
				print(f"Page={in_pg}")

	async def _write_spi(self, pgcmd:str, wrcmd:str, list, logon:int):
		await self._chg_pg(list[1], pgcmd, 1)
		await self._send_data(wrcmd)
		if logon == 1:
			print(f"W:Add={list[2]}, Data={list[3]}")

	async def _read_spi(self, pgcmd:str, wrcmd:str, list, logon:int):
		await self._chg_pg(list[1], pgcmd, 1)
		await self._send_data(wrcmd)
		rd = await self.read()
		dec_rd = int.from_bytes(rd, 'big')
		if logon == 1:
			print(f"R:Add={list[2]}, readback = {dec_rd}")
		return dec_rd

	async def _read_16bit(self, logon:int):
		rd = await self.read()#Recieve Rx data from buffer by ble I/F
		rdbuf = memoryview(rd).cast('H')
		rdlst = rdbuf.tolist()
		if logon == 1:
			print(f"read {2*len(rdlst)}bytes")
		return rdlst

	async def _read_pg(self, pgcmd:str, wrcmd:str, list, logon:int):
		await self._chg_pg(list[1], pgcmd, 1)
		await asyncio.sleep(0.3)
		await self._send_data(wrcmd)
		rd = await self.read()
		rdbuf = memoryview(rd).cast('B')
		rdlst = rdbuf.tolist()
		#print(rdlst)
		if logon == 1:
			for i in range(len(rdlst)):
				hex_value = hex(rdlst[i]) # also keep it in Hex.
				#print(f"add={i} rddata={rdlst[i]}") #Decimal output
				print(f"add={i} rddata={hex_value}") #Hex. output
				#print(f"add={i} rddata={rdlst[i]} hexdata={hex_value}") #in both decimal and hex.
		return rdlst

	async def _wait_state(self, state_type:str, state_num:int, logon:int):
		if state_type == "RPU" or state_type == "rpu":
			add = "9"
		else:
			add = "8"
		pre_cmd = "reg_r 0" + " " + add
		[pgcmd, wrcmd, list]  = self._sort_data(pre_cmd.encode())
		r_state = ""
		while r_state != state_num:
			rd = await self._read_spi(pgcmd, wrcmd, list, 0)
			r_state = (rd & 0x0F)
			if logon == 1:
				if state_type == "RPU" or state_type == "rpu":
					print(f"RPU_STATE = {r_state}")
				else:
					print(f"R_STATE = {r_state}")

######Pin Control######
	async def _rst_ctrl(self, rst:int):
		if rst == 1:
			wrcmd  = self._sort_data(b"rstn 1")[1]
			await self._send_data(wrcmd)#Release RSTN
			print("Reset release")
		else:
			wrcmd  = self._sort_data(b"rstn 0")[1]
			await self._send_data(wrcmd)#Reset
			print("Reset")

	async def _pdn_ctrl(self, pdn:int):
		if pdn == 1:
			wrcmd  = self._sort_data(b"pdn 1")[1]
			await self._send_data(wrcmd)#Release RSTN
			print("PDN release")
		else:
			wrcmd  = self._sort_data(b"pdn 0")[1]
			await self._send_data(wrcmd)#Reset
			print("Power down")

	async def _execonly_ctrl(self, execonly:int):
		if execonly == 1:
			wrcmd  = self._sort_data(b"execonly 1")[1]
			await self._send_data(wrcmd)
			print("EXEC pin = high")
		else:
			wrcmd  = self._sort_data(b"execonly 0")[1]
			await self._send_data(wrcmd)
			print("EXEC pin = low")

	async def _exec_ctrl(self, exec:int, t_loop:int, txnum:int, repnum):
		if exec == 1:
			cmd = "exec 1 " + str(t_loop) + " " + str(txnum)
			for num in repnum:
				cmd += " " + str(num)
			wrcmd  = self._sort_data(cmd.encode())[1]
			await self._send_data(wrcmd)
			# await self._send_data(b'261,1,3,255,255,130')
			print("RADAR START")
		else:
			cmd = "exec 0 " + str("0 0 0")
			wrcmd  = self._sort_data(cmd.encode())[1]
			await self._send_data(wrcmd)
			print("RADAR END")

	async def _fft_exec_ctrl(self, exec:int, t_loop:int, tx_num:int, tx_byte):
		if exec == 1:
			cmd = "fftexec 1 " + str(t_loop) + " " + str(tx_num)
			for byte in tx_byte:
				cmd += " " + str(byte)
			wrcmd  = self._sort_data(cmd.encode())[1]
			await self._send_data(wrcmd)
			print("RADAR START & FFT Capture")
		else:
			cmd = "fftexec 0 " + str("0 0 0")
			wrcmd  = self._sort_data(cmd.encode())[1]
			await self._send_data(wrcmd)
			print("RADAR END")		

######Sequnece######
	async def _stup(self):
		await self._rst_ctrl(0)
		#await self._wait_state("IC", 1)#Wait LP
		# await self._wait_state("IC", 0, 1)#For debug
		await self._wait_state("IC", 1, 1)
		print("Low Power State")

		await self._rst_ctrl(1)

		await asyncio.sleep(0.1)

		[pgcmd, wrcmd, list]  = self._sort_data(b"reg_r 1 10")
		r_lpchk_done = ""
		while r_lpchk_done != 1:
			rd = await self._read_spi(pgcmd, wrcmd, list, 0) #Wait Low Check Done
			r_lpchk_done = self._get_bit(rd, 4, 0x01)
			print(f"R_LPCHK_DONE = {r_lpchk_done}")
		print("LP Cal Done")

		[pgcmd, wrcmd, list] = self._sort_data(b"reg_r 0 2")
		rd = await self._read_spi(pgcmd, wrcmd, list, 1)
		err = [0, 0, 0]
		for i in range(3):
			err[i] = self._get_bit(rd, 6-i, 0x01)
		print(f"ERR_SPI = {err[0]}, ERR_CONT = {err[1]}, ERR_ONESHOT = {err[2]}")
		if 1 in err:
			print(f"Error Detect")
			await self.disconnect()

	async def _autoexe_set(self):
		loop_set = (self.T_LOOP // 10) - 1
		pre_cmd = "reg_w 0 13" + " " + str(loop_set)
		[pgcmd, wrcmd, list]  = self._sort_data(pre_cmd.encode())
		await self._write_spi(pgcmd, wrcmd, list, 0)

	async def _tgtlst_set(self, datsel:int, begin:int, end:int):
		#Register Write
		temp_dict = {11:datsel, 12:begin, 13:end}
		for i in range(11,14):#Set SEQRD_DATASEL,BEGIN,END
			pre_cmd = "reg_w 3 " + str(i) + " " + str(temp_dict[i])
			[pgcmd, wrcmd, list]  = self._sort_data(pre_cmd.encode())
			await self._write_spi(pgcmd, wrcmd, list, 0)

		#Loop Set
		idnum = abs(end - begin) + 1
		temp_dict = {0:5, 1:2, 2:4, 3:1, 4:4, 5:1, 6:4, 7:1}
		byte_per_id = 2 * temp_dict[datsel] #2byte per 1 read
		maxid_tx = self.MAX_MTU // byte_per_id #rouddown
		maxbyte_tx = maxid_tx*byte_per_id
		tx_num = -(-idnum // maxid_tx) #roundup
		rem_byte = (idnum * byte_per_id) - (tx_num - 1) * maxbyte_tx

		lst_rep = []
		for i in range(tx_num):
			if i == tx_num - 1:
				lst_rep.append(rem_byte // 2)
			else:
				lst_rep.append(maxbyte_tx//2)

		return tx_num, lst_rep, temp_dict[datsel]

	async def _radar_ope(self, dat_type:int, id_begin:int, id_end:int, flg_save:int, save_path:str, flg_plot:int, flg_disp:int):
		global CAPT_NUM
		await self._queue_clr()

		p2a10 = await self._exe_cmd(b'reg_r 2 10')
		await asyncio.sleep(0.2)
		p2a10 = (p2a10 & 239) #d'239=0xEF
		pre_cmd = "reg_w 2 10" + " " + str(p2a10)
		[pgcmd, wrcmd, list]  = self._sort_data(pre_cmd.encode())
		await self._write_spi(pgcmd, wrcmd, list, 0)

		await self._autoexe_set()
		await asyncio.sleep(0.2)
		[txnum, repnum, num_2byte] = await self._tgtlst_set(dat_type, id_begin, id_end)
		await asyncio.sleep(0.2)
		await self._exe_cmd(b'reg_w 0 2 19') # ERR_ONESHOT temporary Disabled, and Page.3 select (d'19 = 0x13)
		await asyncio.sleep(0.5)
		frame = 0
			
		if flg_plot == 1:
			[fig, ax] = self._init_graph()
			[fig_2d, ax_2d] = self._init_graph_2d()

		if flg_save == 1:
			writer = pd.ExcelWriter(save_path, engine="xlsxwriter")

		await self._exec_ctrl(1, self.T_LOOP, txnum, repnum)

		flg_stp = 0

		while (True if CAPT_NUM==0 else frame <= CAPT_NUM -1):
			frame += 1
			global FLG_STP_H

			#If STOP button is pushed, this loop end.
			if ((msvcrt.kbhit() and msvcrt.getch() == b'\r') or (flg_stp == 1)):
				await self._exec_ctrl(0, 0, 0, [0])
				FLG_STP_H = 0
				self._clr_graph(ax)
				break

			await self._queue_clr()
			t_st = time.perf_counter()
			rd_all = []
			for _ in range(txnum):
				rd = await self._read_16bit(0)
				rd_all += rd
			if len(rd_all) != sum(repnum):
				print(f'Failed frame={frame} Expect{2*sum(repnum)}bytes Receive{2*len(rd_all)}bytes')
				continue
			tgtlst_per_id = self._split_list(rd_all, num_2byte)
			tgtlst = []
			for i in range(len(tgtlst_per_id)):
				lst_per_id = self._tgtlst_gen(dat_type, tgtlst_per_id[i])
				tgtlst.append(lst_per_id)
			col = ["id", "range", "azi", "ele", "mag", "i", "q"]
			df = pd.DataFrame(tgtlst, columns = col)
			if flg_save == 1 and frame <= self.LMT_SAVE_FRM:
				df.to_excel(writer, float_format='%.5f', header=True, index=False, sheet_name=str(frame))
			if flg_plot == 1:
				#df_temp = self._gen_tsig(self.DISP_IDNUM)#For debug
				#self._plt_graph(fig, ax, df_temp, self.DISP_IDNUM)##For debug
				self._plt_graph(fig, ax, df, self.DISP_IDNUM)#df_temp->df
				#df = df.reindex(columns=["id", "azi", "range", "ele", "mag", "i", "q"])
				self._plt_graph_2d(fig_2d, ax_2d, df, self.DISP_IDNUM)#df_temp->df
			t_tgt = self.T_LOOP / 1000
			while time.perf_counter() - t_st < t_tgt:
				pass
			t_fin = (time.perf_counter() - t_st)
			if flg_disp == 1:
				self._prnt_tgtlst(tgtlst, frame, self.UPDATE_FRM, self.DISP_IDNUM, t_fin)

			if FLG_STP_H == 0:
				flg_stp = 0
			else:
				flg_stp = 1

		writer.close()
		self._clr_graph(ax)
		await self._exe_cmd(b'execonly 0') # EXEC pin go to Low.

	async def _fft_set(self, fftpnt:int):

		maxbin = self.MAX_MTU // 6 # rounddown (ex. 512//6 = 85bin, Maximum number of bin that can be received at one time)
		maxbyte = 6 * maxbin #(ex. 6*85=510byte)

		tx_num_reg = fftpnt * 6 # (ex. 128*6=768) "I data = 3 registers and Q data = 3 registers"
		tx_num = -(-tx_num_reg // self.MAX_MTU) #roundup (ex. -(-768//512) = 2)

		if(fftpnt < maxbin):# if it can be received at one time
			rembin = fftpnt
		else:# not only at one time
			rembin = fftpnt - (maxbin * (tx_num-1)) #(ex.128-85=43bin, This is the final bin count)
		rembyte = 6 * rembin #(ex. 6*43=258byte)

		tx_byte = []
		for i in range(tx_num):
			if i == tx_num - 1:
				tx_byte.append(rembyte)
			else:
				tx_byte.append(maxbyte)

		return tx_num, tx_byte

	async def _exec_fft_ope(self, rpu_smpls:str, flg_save:int, save_path:str, save_path_mag:str, flg_plot:int, flg_disp:int):
		global CAPT_NUM
		await self._queue_clr()

		p2a10 = await self._exe_cmd(b'reg_r 2 10')
		await asyncio.sleep(0.2)
		p2a10 = (p2a10 | 16) #d'16=0x10
		pre_cmd = "reg_w 2 10" + " " + str(p2a10)
		[pgcmd, wrcmd, list]  = self._sort_data(pre_cmd.encode())
		await self._write_spi(pgcmd, wrcmd, list, 0)

		await self._autoexe_set()
		await asyncio.sleep(0.2)
		fftpnt = int(rpu_smpls) // 2
		[tx_num, tx_byte] = await self._fft_set(fftpnt)
		await self._exe_cmd(b'reg_w 0 2 19') # ERR_ONESHOT temporary Disabled, and Page.3 select (d'19 = 0x13)
		await asyncio.sleep(0.5)
		frame = 0
			
		if flg_plot == 1:
			[fig_fft, ax_fft] = self._init_graph_fft()

		if flg_save == 1:
			writer = pd.ExcelWriter(save_path, engine="xlsxwriter")
			writer_m = pd.ExcelWriter(save_path_mag, engine="xlsxwriter")

		await self._fft_exec_ctrl(1, self.T_LOOP, tx_num, tx_byte)

		await asyncio.sleep(0.5)

		flg_stp = 0

		while (True if CAPT_NUM==0 else frame <= CAPT_NUM -1):

			global FLG_STP_H

			#If STOP button is pushed, this loop end.
			if ((msvcrt.kbhit() and msvcrt.getch() == b'\r') or (flg_stp == 1)):
				await self._fft_exec_ctrl(0, 0, 0, [0])
				FLG_STP_H = 0
				break
			t_st = time.perf_counter()
			rd_all = []
			tx_num_16 = tx_num * 16
			for _ in range(tx_num_16):
				rd = await self.read()
				rdbuf = memoryview(rd).cast('B')
				rdlst = rdbuf.tolist()
				rd_all += rdlst
			tx_byte_16 = sum(tx_byte) * 16
			if len(rd_all) != tx_byte_16:
				print(f'Failed: Expect {tx_byte_16} bytes, but Receive {len(rd_all)} bytes')
			iqdata_per_bin_all = self._split_list(rd_all, 6)
			iqdata_per_bin_1tag_length = int(len(iqdata_per_bin_all) / 16)
			iqdata = []
			mdata = []
			for i in range(16):
				for j in range(iqdata_per_bin_1tag_length):
					j = j + (i * iqdata_per_bin_1tag_length)
					lst_per_bin = self._fftlst_gen(iqdata_per_bin_all[j])
					iqdata.append([lst_per_bin[0],lst_per_bin[1]])
					mdata.append([lst_per_bin[2]])
			j=fftpnt
			extracted_iq_data = [iqdata[frame] + iqdata[frame + (j*1)] + iqdata[frame + (j*2)] + iqdata[frame + (j*3)] + iqdata[frame + (j*4)] + \
							  iqdata[frame + (j*5)] + iqdata[frame + (j*6)] + iqdata[frame + (j*7)] + iqdata[frame + (j*8)] + \
							  iqdata[frame + (j*9)] + iqdata[frame + (j*10)] + iqdata[frame + (j*11)] + iqdata[frame + (j*12)] + \
							  iqdata[frame + (j*13)] + iqdata[frame + (j*14)] + iqdata[frame + (j*15)] for frame in range(j)]
			extracted_m_data = [mdata[frame] + mdata[frame + (j*1)] + mdata[frame + (j*2)] + mdata[frame + (j*3)] + mdata[frame + (j*4)] + \
							  mdata[frame + (j*5)] + mdata[frame + (j*6)] + mdata[frame + (j*7)] + mdata[frame + (j*8)] + \
							  mdata[frame + (j*9)] + mdata[frame + (j*10)] + mdata[frame + (j*11)] + mdata[frame + (j*12)] + \
							  mdata[frame + (j*13)] + mdata[frame + (j*14)] + mdata[frame + (j*15)] for frame in range(j)]
			#col = ["I_T0R0", "Q_T0R0", "M_T0R0", "I_T0R1", "Q_T0R1", "M_T0R1", "I_T0R2", "Q_T0R2", "M_T0R2", "I_T0R3", "Q_T0R3", "M_T0R3",\
			#	"I_T1R0", "Q_T1R0", "M_T1R0", "I_T1R1", "Q_T1R1", "M_T1R1", "I_T1R2", "Q_T1R2", "M_T1R2", "I_T1R3", "Q_T1R3", "M_T1R3",\
			#	"I_T2R0", "Q_T2R0", "M_T2R0", "I_T2R1", "Q_T2R1", "M_T2R1", "I_T2R2", "Q_T2R2", "M_T2R2", "I_T2R3", "Q_T2R3", "M_T2R3",\
			#	"I_T3R0", "Q_T3R0", "M_T3R0", "I_T3R1", "Q_T3R1", "M_T3R1", "I_T3R2", "Q_T3R2", "M_T3R2", "I_T3R3", "Q_T3R3", "M_T3R3"]
			col = ["I_T0R0", "Q_T0R0", "I_T0R1", "Q_T0R1", "I_T0R2", "Q_T0R2", "I_T0R3", "Q_T0R3",\
				"I_T1R0", "Q_T1R0", "I_T1R1", "Q_T1R1", "I_T1R2", "Q_T1R2", "I_T1R3", "Q_T1R3",\
				"I_T2R0", "Q_T2R0", "I_T2R1", "Q_T2R1", "I_T2R2", "Q_T2R2", "I_T2R3", "Q_T2R3",\
				"I_T3R0", "Q_T3R0", "I_T3R1", "Q_T3R1", "I_T3R2", "Q_T3R2", "I_T3R3", "Q_T3R3"]
			col_m = ["M_T0R0", "M_T0R1", "M_T0R2", "M_T0R3", "M_T1R0", "M_T1R1", "M_T1R2", "M_T1R3",\
				"M_T2R0", "M_T2R1", "M_T2R2", "M_T2R3",	"M_T3R0", "M_T3R1", "M_T3R2", "M_T3R3"]
			df = pd.DataFrame(extracted_iq_data, columns = col)
			df_m = pd.DataFrame(extracted_m_data, columns = col_m)
			if flg_save == 1:
				df.to_excel(writer, float_format='%.5f', header=True, index=True, sheet_name=str(frame))
				df_m.to_excel(writer_m, float_format='%.5f', header=True, index=True, sheet_name=str(frame))
			if flg_plot == 1:
				self._plt_graph_fft(fig_fft, ax_fft, df_m, 16)
			t_tgt = self.T_LOOP / 1000
			while time.perf_counter() - t_st < t_tgt:
				pass
			t_fin = (time.perf_counter() - t_st)
			if flg_disp == 1:
				pass

			if FLG_STP_H == 0:
				flg_stp = 0
			else:
				flg_stp = 1

			frame += 1

		writer.close()
		writer_m.close()
		await self._exe_cmd(b'execonly 0')

	#For STOP button
	async def _flg_stph(self):
		global FLG_STP_H
		FLG_STP_H = 1

######Master######
	async def _exe_cmd(self, data):
		#print("test000")
		[pgcmd, wrcmd, list]  = self._sort_data(data)
		if ((not wrcmd) and (not pgcmd)) or ("end" in wrcmd):
			print("Exit")
			await self.disconnect()
		else:
	#SPI
			if list[0] == "reg_r":
					await self._queue_clr()
					rd = await self._read_spi(pgcmd, wrcmd, list, 1)
					return rd
			elif list[0] == "read_pg":
				await self._queue_clr()
				rdlst = await self._read_pg(pgcmd, wrcmd, list, 1)
				return rdlst
			elif list[0] == "reg_w":
					await self._write_spi(pgcmd, wrcmd, list, 1)
			elif list[0] == "page":
					await self._chg_pg(list[1], pgcmd, 1)
	#Pin Control
			elif list[0] == "pdn":
				await self._pdn_ctrl(int(list[1]))
			elif list[0] == "rstn":
				await self._rst_ctrl(int(list[1]))
			elif list[0] == "execonly":
				await self._execonly_ctrl(int(list[1]))
	#Command
			elif list[0] == "startup":
				print("Startup")
				await self._stup()
			elif list[0] == "radar_go":
				await self._radar_ope(self.SEQRD_DATSEL, self.SEQRD_BEGIN, self.SEQRD_END, self.FLG_SAVE, self.FILE_PATH, self.FLG_PLOT, self.FLG_DISP)
			elif list[0] == "radar_end":
				await self._exec_ctrl(0, 0, 0, [0])
			elif list[0] == "sleep":
				await asyncio.sleep(float(list[1]))
			elif list[0] == "radar_go_and_fft_capt":
				await self._exec_fft_ope(self.RPU_SMPLS, self.FLG_SAVE, self.FILE_PATH_FFT_IQ, self.FILE_PATH_FFT_MAG, self.FLG_PLOT, self.FLG_DISP)


	async def _capt_num(self,data):
		global CAPT_NUM
		CAPT_NUM = int(data)

	async def _dummy(self,data):
		dummy = int(data)
		return dummy


				