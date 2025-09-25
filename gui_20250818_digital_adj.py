import tkinter.messagebox
from MainCalculator_ZN_20250818_digital_adj import main_cal_20250818_digital_adj

import threading
import tkinter as tk
import tkinter.filedialog
# import hashlib
import time
import os
# import tkinter.font as ft


class Signal:
    def __init__(self):
        self.signal = 100


class MainWindow:
    def __init__(self, root):
        self.root = root

        root.title("车站数字化调整表计算_V0.1")
        root.geometry('900x250+400+300')

        # font = ft.nametofont("TkDefaultFont")
        # print(font.actual())

        self.win_frame = tk.Frame(root)
        self.win_frame.pack(padx=0, pady=0, expand=True)

        self.main_frame = tk.LabelFrame(self.win_frame, text="参数配置", font=("Microsoft YaHei UI", 12))
        self.main_frame.pack(padx=10, pady=10, side=tk.TOP)

        self.button_frame = tk.Frame(self.win_frame)
        self.button_frame.pack(padx=0, pady=0, side=tk.TOP)

        # 单选按钮变量
        self.selected = tk.StringVar(value="一送一受")

        # 创建单选按钮
        self.radio1 = tk.Radiobutton(self.main_frame, text="一送一受", variable=self.selected, value="一送一受")
        self.radio2 = tk.Radiobutton(self.main_frame, text="两送一受", variable=self.selected, value="两送一受")
        self.radio3 = tk.Radiobutton(self.main_frame, text="一送两受", variable=self.selected, value="一送两受")

        # path = 'C:/Users/李继隆/PycharmProjects/Calculator_ZN_mix/邻线干扰计算_站内混合_配置输入_v1.0.xlsx'
        # path = 'C:/Users/李继隆/PycharmProjects/Calculator_ZN_mix/邻线干扰单独核算区段输入模板-V1.0.xlsx'

        # path = os.getcwd() + '\\邻线干扰单独核算区段输入模板-V1.0.xlsx'
        path = 'C:\\Users\\李继隆\\Desktop\\车站数字化调整表\\车站数字化调整表——一送两受.xlsx'

        self.entry1 = tk.Entry(self.main_frame, width=90)
        self.entry1.insert(0, path)
        self.entry1.config(state=tk.DISABLED)

        self.entry2 = tk.Entry(self.main_frame, width=90, state=tk.DISABLED)

        self.button1 = tk.Button(self.main_frame, text="导入路径", width=8, command=self.open_file)
        self.button2 = tk.Button(self.main_frame, text="保存路径", width=8, command=self.save_file)

        self.button1.config(state=tk.NORMAL)
        self.button2.config(state=tk.NORMAL)
        # self.button2.config(state=tk.DISABLED)

        self.label1 = tk.Label(self.main_frame, text='配置路径:')
        self.label2 = tk.Label(self.main_frame, text='结果路径:')
        self.label3 = tk.Label(self.main_frame, text='发送模式:')

        self.label1.grid(row=1, column=0, padx=12, pady=5)
        self.label2.grid(row=2, column=0, padx=12, pady=5)
        self.label3.grid(row=0, column=0, padx=12, pady=5)

        self.entry1.grid(row=1, column=1, padx=2, pady=2, columnspan=5)
        self.entry2.grid(row=2, column=1, padx=2, pady=2, columnspan=5)

        self.button1.grid(row=1, column=6, padx=5, pady=2)
        self.button2.grid(row=2, column=6, padx=5, pady=2)

        self.radio1.grid(row=0, column=1, padx=5, pady=5)
        self.radio2.grid(row=0, column=2, padx=5, pady=5)
        self.radio3.grid(row=0, column=3, padx=5, pady=5)

        self.main_frame.grid_rowconfigure(0, minsize=40)
        self.main_frame.grid_rowconfigure(1, minsize=40)
        self.main_frame.grid_rowconfigure(2, minsize=40)

        self.button3 = tk.Button(self.button_frame, text="计算", width=12, command=self.calculate)
        self.button4 = tk.Button(self.button_frame, text="停止", width=12, command=self.stop_thread2)

        self.button3.config(state=tk.NORMAL)
        self.button4.config(state=tk.DISABLED)

        self.button3.pack(padx=2, pady=2, side=tk.LEFT)
        self.button4.pack(padx=2, pady=2, side=tk.LEFT)

        self.thread2 = threading.Thread()
        self.event = threading.Event()

        # root.bind("<<event1>>", lambda e: self.open_file())

    def open_file(self):
        res = tk.filedialog.askopenfilename()
        if res:
            self.entry1.config(state=tk.NORMAL)
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, res)
            self.entry1.config(state=tk.DISABLED)

    def save_file(self):

        mode = self.selected.get()

        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        file_name = f"车站数字化调整表输出_{mode}_{timestamp}.xlsx"

        res = tk.filedialog.asksaveasfilename(
            initialfile=file_name,
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="保存选择结果"
        )
        if res:
            self.entry2.config(state=tk.NORMAL)
            self.entry2.delete(0, tk.END)
            self.entry2.insert(0, res)
            self.entry2.config(state=tk.DISABLED)

    # def get_path(self):
    #     self.root.event_generate('<<event1>>')

    def stop_thread2(self):
        self.event.set()

    @staticmethod
    def set_entry(entry, text):
        entry.config(state=tk.NORMAL)
        entry.delete(0, tk.END)
        entry.insert(0, text)
        entry.config(state=tk.DISABLED)

    def generate_output_path(self, mode, path1):

        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        file_name = f"车站数字化调整表输出_{mode}_{timestamp}_.xlsx"
        path2 = '/'.join([os.path.dirname(path1), file_name])

        self.entry2.config(state=tk.NORMAL)
        self.entry2.delete(0, tk.END)
        self.entry2.insert(0, path2)
        self.entry2.config(state=tk.DISABLED)

    def calculate(self):
        if self.thread2.is_alive():
            return

        mode = self.selected.get()
        path1 = self.entry1.get()
        path2 = self.entry2.get()

        if path2 == '':
            self.generate_output_path(mode, path1)
            path2 = self.entry2.get()

        self.event.clear()
        self.thread2 = threading.Thread(name='t2', target=self.wrap_calc, args=(mode, path1, path2))
        self.thread2.setDaemon(True)

        self.button3.config(state=tk.DISABLED)
        self.button4.config(state=tk.NORMAL)

        self.thread2.start()

    @property
    def current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    def wrap_calc(self, mode, path1, path2):
        try:
            main_cal_20250818_digital_adj(mode, path1, path2)
        except BaseException as e:
            print(e)

        self.event.clear()

        self.button3.config(state=tk.NORMAL)
        self.button4.config(state=tk.DISABLED)


if __name__ == '__main__':
    tk1 = tk.Tk()
    MainWindow(tk1)
    tk1.mainloop()
