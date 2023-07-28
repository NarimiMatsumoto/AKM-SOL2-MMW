from ble_uart import BLE_UART
from gen_data import GEN_DATA
from gen_graph import GEN_GRAPH
import asyncio
import pandas as pd
import msvcrt
import time

class Integ_Method(BLE_UART, GEN_DATA, GEN_GRAPH):
	PAGE = 0
	SEQRD_DATSEL = 0
	SEQRD_BEGIN = 0
	SEQRD_END = 127
	FLG_SAVE = 0
	LMT_SAVE_FRM = 50
	FILE_PATH = "D:\\tgtlst.csv"
	UPDATE_FRM = 5
	DISP_IDNUM = 4
	FLG_PLOT = 0
	FLG_DISP = 0
	T_LOOP = 50
	MAX_MTU = 512
	def __init__(self) -> None:
		BLE_UART.__init__(self)
		GEN_DATA.__init__(self)
		GEN_GRAPH.__init__(self)


######Access ESP32######
	async def _send_data(self, cmd:str):
		await self.write(cmd)
		# await asyncio.sleep(0.02)


######Access SPI######
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
		#if rd=b'\x00\x01\x00\x02\x00\x03'
		#mv = memoryview(rd).cast('H') <- 2byte unsigned
		#mv[0] = 256, mv[1] = 512, mv[2] = 768
		rdlst = rdbuf.tolist()
		if logon == 1:
			print(f"read {2*len(rdlst)}bytes")
		return rdlst

	async def _read_pg(self, pgcmd:str, wrcmd:str, list, logon:int):
		await self._chg_pg(list[1], pgcmd, 1)
		await self._send_data(wrcmd)
		rd = await self.read()
		rdbuf = memoryview(rd).cast('B')
		#if rd=b'\x00\x01\x00\x02\x00\x03'
		#mv = memoryview(rd).cast('H') <- 2byte unsigned
		#mv[0] = 256, mv[1] = 512, mv[2] = 768
		rdlst = rdbuf.tolist()
		#print(rdlst)
		if logon == 1:
			for i in range(len(rdlst)):
				print(f"add={i} rddata={rdlst[i]}")
		return rdlst

	async def _wait_state(self, state_type:str, state_num:int, logon:int):
		if state_type == "RPU" or state_type == "rpu":
			add = "9"
		else:
			add = "8"
		pre_cmd = "reg_r 0" + " " + add
		[pgcmd, wrcmd, list]  = self._sort_data(pre_cmd.encode())
		r_state = ""
		#print(f"r_state = {r_state}")
		#print(f"state_num = {state_num}")
		while r_state != state_num:
			rd = await self._read_spi(pgcmd, wrcmd, list, 0)
			r_state = (rd & 0x0F)
			#print(f"r_state = {r_state}")
			#print(f"state_num = {state_num}")
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
		await self._queue_clr()
		await self._autoexe_set()
		[txnum, repnum, num_2byte] = await self._tgtlst_set(dat_type, id_begin, id_end)
		frame = 0
			
		if flg_plot == 1:
			[fig, ax] = self._init_graph()

		if flg_save == 1:
			writer = pd.ExcelWriter(save_path, engine="xlsxwriter")

		await self._exec_ctrl(1, self.T_LOOP, txnum, repnum)

		# print(f"exec:{time.perf_counter()}")
		# await asyncio.sleep(0.4)

		while True:
			#ESP32 Sequense
			#	Wait STBY
			#	Wait TRX
			#	Wait RPU_DONE
			#	TGTLST_HOLD
			#	SEQRD_ST
			#	Read List
			#ESP32 Sequense
			frame += 1

			#If Enter button is pushed, this loop end.
			if msvcrt.kbhit() and msvcrt.getch() == b'\r':
				await self._exec_ctrl(0, 0, 0, [0])
				if flg_save == 1:
					writer.save()
				# writer.close()
				break
			#
			t_st = time.perf_counter()
			rd_all = []
			for _ in range(txnum):
				rd = await self._read_16bit(0)
				rd_all += rd
			t_read = time.perf_counter() - t_st
			if len(rd_all) != sum(repnum):
				print(f'Failed frame={frame} Expect{2*sum(repnum)}bytes Receive{2*len(rd_all)}bytes')
				# print(rd_all)
				continue
			tgtlst_per_id = self._split_list(rd_all, num_2byte)
			tgtlst = []
			for i in range(len(tgtlst_per_id)):
				lst_per_id = self._tgtlst_gen(dat_type, tgtlst_per_id[i])
				tgtlst.append(lst_per_id)
			# self._prnt_tgtlst(tgtlst, frame, self.UPDATE_FRM, self.DISP_IDNUM)
			col = ["id", "range", "azi", "ele", "mag", "i", "q"]
			df = pd.DataFrame(tgtlst, columns = col)
			if flg_save == 1 and frame <= self.LMT_SAVE_FRM:
				df.to_excel(writer, float_format='%.5f', header=True, index=False, sheet_name=str(frame))
			t_frame = (time.perf_counter() - t_st)#unit sec
			
			if flg_plot == 1:
				df_temp = self._gen_tsig(self.DISP_IDNUM)#For debug
				#self._plt_graph(fig, ax, df_temp, self.DISP_IDNUM)#df_temp->df
				self._plt_graph(fig, ax, df, self.DISP_IDNUM)#df_temp->df

			t_tgt = self.T_LOOP / 1000
			while time.perf_counter() - t_st < t_tgt:
				pass
			t_fin = (time.perf_counter() - t_st)
			# print(f"frame = {frame} t_frm = {t_frame*1000:.1f}msec t_read = {t_read*1000:.1f}msec t_fin = {t_fin*1000:.1f}msec")
			if flg_disp == 1:
				self._prnt_tgtlst(tgtlst, frame, self.UPDATE_FRM, self.DISP_IDNUM, t_fin)

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
					#print("test001")
					await self._queue_clr()
					#print("list = ", pgcmd, wrcmd, list)
					rd = await self._read_spi(pgcmd, wrcmd, list, 1)
					return rd
			elif list[0] == "read_pg":
				await self._queue_clr()
				#print("list = ", pgcmd, wrcmd, list)
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
			# elif list[0] == "exec":
			# 	await self._send_data(wrcmd)
			# 	print(f"EXEC={list[1]}")
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

				