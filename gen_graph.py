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

	def _config_graph(self, ax):
		ax.set_xlabel('Range')
		ax.set_ylabel('Azimuth')
		ax.set_zlabel('Elevation')
		ax.set_xlim(0,127)
		ax.set_ylim(0,31)
		ax.set_zlim(0,31)
		#ax.invert_yaxis()
		# ax.legend(bbox_to_anchor=(1.1, 1.0), loc='upper left', title='id', ncol=4, fontsize=8)

	def _set_mrker(self, ax, df, num):
		#msize = [200*df.at[i, 'mag']/abs(complex(2**23-1, 2**23-1)) for i in range(num)] # Case of beamformer selected
		msize = [100000*200*df.at[i, 'mag']/abs(complex(2**23-1, 2**23-1)) for i in range(num)] # Case of Angle FFT selected
		#print(f"msize:{msize}")
		ax.scatter(df.loc[:num-1, 'range'], df.loc[:num-1, 'azi'], df.loc[:num-1, 'ele'], label=df.loc[:num-1,'id'], s=msize, marker='o', c='blue', alpha=0.5)
		# ax.legend(bbox_to_anchor=(1.1, 1.0), loc='upper left', title='id', ncol=4, fontsize=8)

	def _plt_graph(self, fig, ax, df, num):
		ax.cla()
		self._config_graph(ax)
		self._set_mrker(ax, df, num)
		fig.canvas.draw()
		fig.canvas.flush_events()

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

