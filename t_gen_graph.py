import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time


def gen_tsig():
	lst = []
	for i in range(128):
		rng = random.randint(0,2**8-1)
		razi = random.randint(0,2**5-1)
		rele = random.randint(0,2**5-1)
		ri = random.randint(-2**23, 2**23-1)
		rq = random.randint(-2**23, 2**23-1)
		rm = ((ri ** 2) + (rq ** 2)) ** 0.5
		dat = [i, rng, razi, rele, rm, ri, rq]
		lst.append(dat)
	col = ["id", "range", "azi", "ele", "mag", "i", "q"]
	df = pd.DataFrame(lst, columns=col)
	return df

def config_graph(ax):
	ax.set_xlabel('Range')
	ax.set_ylabel('Azimuth')
	ax.set_zlabel('Elevation')
	ax.set_xlim(0,127)
	ax.set_ylim(0,31)
	ax.set_zlim(0,31)
	# ax.legend(bbox_to_anchor=(1.1, 1.0), loc='upper left', title='id', ncol=4, fontsize=8)

def set_mrker(fig, df, num, ax):
	msize = [100*df.at[i, 'mag']/abs(complex(2**23-1, 2**23-1)) for i in range(num)]
	ax.scatter(df.loc[:num-1, 'range'], df.loc[:num-1, 'azi'], df.loc[:num-1, 'ele'], label=df.loc[:num-1,'id'], s=msize, marker='o', c='blue', alpha=0.5)
	# ax.legend(bbox_to_anchor=(1.1, 1.0), loc='upper left', title='id', ncol=4, fontsize=8)

def main():
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	fig.show()
	df = gen_tsig()

	for j in range(1000):
		df = gen_tsig()
		config_graph(ax)
		set_mrker(fig, df, 128, ax)
		fig.canvas.draw()
		fig.canvas.flush_events()
		ax.cla()



if __name__ == "__main__":
	try:
		main()
	except Exception:
		pass