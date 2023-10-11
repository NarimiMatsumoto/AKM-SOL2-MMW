
class GEN_DATA:
	# ESP32 Command
	W_DAT = 256
	R_DAT = 257
	R_PG = 258
	PDN_CTRL = 259
	RSTN_CTRL = 260
	EXE_CTRL = 261
	EXE_CTRL_ONLY = 262
	W_ALLDAT = 263
	# ESP32 Command
	
	def __init__(self) -> None:
		pass

	def _sort_data(self, data):
		dec_data = data.decode()
		list = dec_data.split()
	# SPI
		if list[0] == "reg_w":
				page = self._gen_data(0x02, int(list[1]), 0)
				wr = self._gen_data(int(list[2]), int(list[3]), 0)
				pgcmd = self._enc_cmd(page)
				wrcmd = self._enc_cmd(wr)
		elif list[0] == "reg_r":
				page = self._gen_data(0x02, int(list[1]), 0)
				wr = self._gen_data(int(list[2]), 0x00, 1)
				pgcmd = self._enc_cmd(page)
				wrcmd = self._enc_cmd(wr)
		elif list[0] == "read_pg":
				page = self._gen_data(0x02, int(list[1]), 0)
				pgcmd = self._enc_cmd(page)
				wrcmd = self._enc_cmd([self.R_PG])
		elif list[0] == "page":
			page = self._gen_data(0x02, int(list[1]), 0)
			pgcmd = self._enc_cmd(page)
			wrcmd = ""
	# Pin Control
		elif list[0] == "pdn":
				pgcmd = ""
				wrcmd = self._enc_cmd([self.PDN_CTRL, int(list[1])])
		elif list[0] == "rstn":
				pgcmd = ""
				wrcmd = self._enc_cmd([self.RSTN_CTRL, int(list[1])])
		elif list[0] == "execonly":
				pgcmd = ""
				wrcmd = self._enc_cmd([self.EXE_CTRL_ONLY, int(list[1])])
		elif list[0] == "exec":
				pgcmd = ""
				wrcmd = self._enc_cmd([self.EXE_CTRL] + list[1:])
	# Command
		elif list[0] == "startup":
				pgcmd = ""
				wrcmd = list[0]
		elif list[0] == "radar_go":
				pgcmd = ""
				wrcmd = list[0]
		elif list[0] == "radar_end":
				pgcmd = ""
				wrcmd = list[0]
		elif list[0] == "end":
			pgcmd = ""
			wrcmd = "end"
		elif list[0] == "sleep":
			pgcmd = ""
			wrcmd = "sleep"
		else:
			pgcmd = ""
			wrcmd = ""
		return pgcmd, wrcmd, list

	def _gen_data(self, add:int, data:int, wr:int):
		# cmd_list = [add, self.SET_ADD, data, self.SET_DAT]
		cmd_list = []
		if(wr == 1):
			cmd_list.append(self.R_DAT)#Read
			cmd_list.append(0x80 | add)
		else:
			cmd_list.append(self.W_DAT)#Write
			cmd_list.append(add)
		cmd_list.append(data)
		return cmd_list

	def _enc_cmd(self, cmd_list):
		str_cmd = ""
		for i,cmd in enumerate(cmd_list):
			if(i != len(cmd_list) - 1):
				str_cmd += str(cmd) + ","
			else:
				str_cmd += str(cmd) + "\n"
		enc_cmd_list = str_cmd
		return enc_cmd_list

	def _sort_gen_data(self, cmdall):
		wrcmd_list = [self.W_ALLDAT]
		for line_cmdall in cmdall:
			dec_data = line_cmdall.decode()
			list_cmdall = dec_data.split()
			wrcmd_list.append(int(list_cmdall[2]))
			wrcmd_list.append(int(list_cmdall[3]))
		return wrcmd_list

	def _get_bit(self, dat:str, sft:int, mask:int):
		return ((int(dat) >> sft) & mask)

	def _tgtlst_gen(self, dat_sel:int, lst_dat):
		lst0_lsb_7bit = self._get_bit(lst_dat[0], 0, 0x7F)
		lst0_msb_7bit = self._get_bit(lst_dat[0], 8, 0x7F)
		lst0_lsb_5bit = self._get_bit(lst_dat[0], 0, 0x1F)
		# lst0_msb_5bit = self._get_bit(lst_dat[0], 8, 0x1F)
		lst1_lsb_5bit = self._get_bit(lst_dat[1], 0, 0x1F)
		lst1_msb_5bit = self._get_bit(lst_dat[1], 8, 0x1F)
		dict_id = {0:lst0_msb_7bit, 1:lst0_msb_7bit, 2:lst0_msb_7bit, 3:lst0_msb_7bit, 4:"-", 5:"-", 6:"-", 7:"-"}
		dict_range = {0:lst0_lsb_7bit, 1:lst0_lsb_7bit, 2:lst0_lsb_7bit, 3:lst0_lsb_7bit, 4:lst0_msb_7bit, 5:lst0_msb_7bit, 6:lst0_msb_7bit, 7:lst0_msb_7bit}
		dict_azi = {0:lst1_msb_5bit, 1:lst1_msb_5bit, 2:"-", 3:"-", 4:lst0_lsb_5bit, 5:lst0_lsb_5bit, 6:"-", 7:"-"}
		dict_ele = {0:lst1_lsb_5bit, 1:lst1_lsb_5bit, 2:"-", 3:"-", 4:"-", 5:"-", 6:lst0_lsb_5bit, 7:lst0_lsb_5bit}

		lst_id = dict_id[dat_sel]
		lst_range = dict_range[dat_sel]
		lst_azi = dict_azi[dat_sel]
		lst_ele = dict_ele[dat_sel]
		iqlst_num = 2 if dat_sel == 0 else 1
		if dat_sel % 2 == 0:
			lsti_23_8 = int(lst_dat[iqlst_num]) << 8
			pre_lst_i = lsti_23_8 + self._get_bit(lst_dat[iqlst_num+1], 8, 0xFF)
			# pre_lst_i = int(lst_dat[iqlst_num]) * (2 ** 8) + self._get_bit(lst_dat[iqlst_num+1], 8, 0xFF)
			# pre_lst_i = int(lst_dat[iqlst_num]) << 8 + self._get_bit(lst_dat[iqlst_num+1], 8, 0xFF)
			lst_i = pre_lst_i - 2**24 if pre_lst_i > (2**23 - 1) else pre_lst_i

			lstq_23_16 = self._get_bit(lst_dat[iqlst_num+1], 0, 0xFF) << 16
			pre_lst_q = lstq_23_16 + int(lst_dat[iqlst_num+2])
			# pre_lst_q = self._get_bit(lst_dat[iqlst_num+1], 0, 0xFF) * (2 ** 16) + int(lst_dat[iqlst_num+2])
			# pre_lst_q = self._get_bit(lst_dat[iqlst_num+1], 0, 0xFF) << 16 + int(lst_dat[iqlst_num+2])
			lst_q = pre_lst_q - 2**24 if pre_lst_q > (2**23 - 1) else pre_lst_q

			# lst_mag = ((lst_i ** 2) + (lst_q ** 2)) ** 0.5
			lst_mag = abs(complex(lst_i, lst_q))/30
		else:
			lst_i = "-"
			lst_q = "-"
			lst_mag = "-"

		return [lst_id, lst_range, lst_azi, lst_ele, lst_mag, lst_i, lst_q]

	def _split_list(self, l, n:int):
		result = []
		for idx in range(0, len(l), n):
			result.append(l[idx:idx + n])
		return result

	def _prnt_tgtlst(self, lst_all, frm:int, update_frm:int, idnum:int, t_fin:float):
		if update_frm != 0:
			if frm % update_frm == 0:
				fps = 1/t_fin
				print(f"Frame:{frm} {t_fin*10**3:.1f}msec ({fps:.1f} fps)")
				for i in range(idnum):
					print(f"ID:{lst_all[i][0]} R:{lst_all[i][1]} A:{lst_all[i][2]} E:{lst_all[i][3]} M:{lst_all[i][4]} I:{lst_all[i][5]} Q:{lst_all[i][6]}")