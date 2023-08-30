import pandas as pd
import matplotlib.pyplot as plt
import random

class GEN_GRAPH:

	def __init__(self) -> None:
		pass

	def _init_graph(self):
		fig = plt.figure(num=1, dpi=100)
		ax = fig.add_subplot(111, projection='3d')
		ax.view_init(elev=10, azim=-165)
		ax.set_title('3D VIEW') #
		ax.set_xticklabels([])
		ax.set_yticklabels([])
		ax.set_zticklabels([])
		#fig.show()
		while not plt.fignum_exists(1):
			pass
		return fig, ax

	def _init_graph_2d(self):
		fig = plt.figure(num=2, dpi=100)
		ax = fig.add_subplot(111)
		ax.set_title('Range/Azimuth VIEW') #
		ax.set_xticklabels([])
		ax.set_yticklabels([])
		#fig.show()
		while not plt.fignum_exists(2):
			pass
		return fig, ax

	def _init_graph_fft(self):
		fig = plt.figure(num=3, dpi=100)
		ax = fig.add_subplot(111)
		ax.set_title('Range FFT VIEW') #
		ax.set_xticklabels([])
		ax.set_yticklabels([])
		#fig.show()
		while not plt.fignum_exists(3):
			pass
		return fig, ax

	def _init_graph_d(self):
		fig = plt.figure(num=4, dpi=100)
		ax = fig.add_subplot(111)
		ax.set_title('Graph in frame 14') #
		ax.set_xticklabels([])
		ax.set_yticklabels([])
		#fig.show()
		while not plt.fignum_exists(4):
			pass
		return fig, ax

	def _config_graph(self, ax):
		ax.set_xlabel('Range')
		ax.set_ylabel('Azimuth')
		ax.set_zlabel('Elevation')
		ax.set_xlim(0,127)
		ax.set_ylim(0,31)
		ax.set_zlim(0,31)
		#ax.invert_yaxis()
		# ax.legend(bbox_to_anchor=(1.1, 1.0), loc='upper left', title='id', ncol=4, fontsize=8)

	def _config_graph_2d(self, ax):
		ax.set_xlabel('Azimuth')
		ax.set_ylabel('Range')
		ax.set_xlim(0,31)
		ax.set_ylim(0,20)#127

	def _config_graph_fft(self, ax):
		ax.set_xlabel('Range Bin')
		ax.set_ylabel('Magnitude')
		ax.set_xlim(0,127)
		ax.set_ylim(0,10000)#127

	def _set_mrker(self, ax, df, num):
		msize = [100000*200*df.at[i, 'mag']/abs(complex(2**23-1, 2**23-1)) for i in range(num)]
		ax.scatter(df.loc[:num-1, 'range'], df.loc[:num-1, 'azi'], df.loc[:num-1, 'ele'], label=df.loc[:num-1,'id'], s=msize, marker='o', c='blue', alpha=0.5)
		# ax.legend(bbox_to_anchor=(1.1, 1.0), loc='upper left', title='id', ncol=4, fontsize=8)

	def _set_mrker_2d(self, ax, df, num):
		msize = [100000*200*df.at[i, 'mag']/abs(complex(2**23-1, 2**23-1)) for i in range(num)]
		#colors = ['green', 'blue', 'yellow', 'purple']
		ax.scatter(df.loc[:num-1, 'azi'], df.loc[:num-1, 'range'], label=df.loc[:num-1,'id'], s=msize, marker='o', c='green', alpha=0.5)

	def _set_mrker_fft(self, ax, df, num):
		col_m = ['M_T0R0', 'M_T0R1', 'M_T0R2', 'M_T0R3', 'M_T1R0', 'M_T1R1', 'M_T1R2', 'M_T1R3',\
				'M_T2R0', 'M_T2R1', 'M_T2R2', 'M_T2R3',	'M_T3R0', 'M_T3R1', 'M_T3R2', 'M_T3R3']
		for column in col_m:
			ax.plot(df.loc[0:127, column])

	def _plt_graph(self, fig, ax, df, num):
		ax.cla()
		self._config_graph(ax)
		self._set_mrker(ax, df, num)
		fig.canvas.draw()
		fig.canvas.flush_events()

	def _plt_graph_2d(self, fig, ax, df, num):
		ax.cla()
		self._config_graph_2d(ax)
		self._set_mrker_2d(ax, df, num)
		fig.canvas.draw()
		fig.canvas.flush_events()

	def _plt_graph_fft(self, fig, ax, df, num):
		ax.cla()
		self._config_graph_fft(ax)
		self._set_mrker_fft(ax, df, num)
		fig.canvas.draw()
		fig.canvas.flush_events()

	def _clr_graph(self, ax):
		ax.cla()
		ax.set_xticklabels([])
		ax.set_yticklabels([])
		ax.set_zticklabels([])
		ax.set_xlabel('')
		ax.set_ylabel('')
		ax.set_zlabel('')

# For debug
	def _gen_tsig(self, num):
		lst = []
		for i in range(num):
			rng = random.randint(0,2**8-1)
			razi = random.randint(0,2**5-1)
			rele = random.randint(0,2**5-1)
			ri = random.randint(-2**23, 2**23-1)
			rq = random.randint(-2**23, 2**23-1)
			rm = abs(complex(ri, rq))
			dat = [i, rng, razi, rele, rm, ri, rq]
			lst.append(dat)
		col = ["id", "range", "azi", "ele", "mag", "i", "q"]
		df = pd.DataFrame(lst, columns=col)
		return df

