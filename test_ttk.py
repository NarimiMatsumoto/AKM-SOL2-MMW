import tkinter as tk
from tkinter import ttk

##### 2023/06/06 matsumoto start ####
# rootメインウィンドウの設定
root = tk.Tk()
root.title("Setting")
root.geometry("400x200")

# メインフレームの作成と設置
frame = tk.Frame(root)
frame.pack(padx=20, pady=10)

# 各種ウィジェットの作成
button = ttk.Button(frame, text="ttk")
# 各種ウィジェットの設置
button.grid(row=0, column=0)

##### 2023/06/06 matsumoto end ####

root.mainloop()