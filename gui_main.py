import tkinter as tk
import tkinter.filedialog
import hashlib
import time
import os
# from MainCalculator_ZN_mix_beta import main_cal
from MainCalculator_ZN_mix_beta_v01 import main_cal
import threading


class Signal:
    def __init__(self):
        self.signal = 100


class MainWindow:
    def __init__(self, root):
        self.root = root

        root.title("配置输入测试_v0.1")
        root.geometry('900x200+400+300')

        self.win_frame = tk.Frame(root)
        self.win_frame.pack(padx=0, pady=0, expand=True)

        self.main_frame = tk.LabelFrame(self.win_frame, text="邻线干扰仿真")
        self.main_frame.pack(padx=10, pady=10, side=tk.TOP)

        self.button_frame = tk.Frame(self.win_frame)
        self.button_frame.pack(padx=0, pady=0, side=tk.TOP)

        self.frame1 = tk.Frame(self.main_frame)
        self.frame1.pack(padx=8, pady=2, side=tk.TOP)

        self.frame2 = tk.Frame(self.main_frame)
        self.frame2.pack(padx=8, pady=2, side=tk.TOP)

        # path = 'C:/Users/李继隆/PycharmProjects/Calculator_ZN_mix/邻线干扰计算_站内混合_配置输入_v1.0.xlsx'
        # path = 'C:/Users/李继隆/PycharmProjects/Calculator_ZN_mix/邻线干扰单独核算区段输入模板-V1.0.xlsx'

        path = os.getcwd() + '\\邻线干扰单独核算区段输入模板-V1.0.xlsx'
        self.entry1 = tk.Entry(self.frame1, width=90)
        self.entry1.insert(0, path)
        self.entry1.config(state=tk.DISABLED)

        self.entry2 = tk.Entry(self.frame2, width=90, state=tk.DISABLED)

        self.button1 = tk.Button(self.frame1, text="导入路径", width=8, command=self.open_file)
        self.button2 = tk.Button(self.frame2, text="打开文件", width=8, command=self.get_path)

        self.button1.config(state=tk.NORMAL)
        self.button2.config(state=tk.DISABLED)

        self.label1 = tk.Label(self.frame1, text='配置路径:')
        self.label2 = tk.Label(self.frame2, text='结果路径:')

        self.label1.pack(padx=2, pady=2, side=tk.LEFT)
        self.entry1.pack(padx=2, pady=2, side=tk.LEFT)
        self.button1.pack(padx=5, pady=2, side=tk.LEFT)

        self.label2.pack(padx=2, pady=2, side=tk.LEFT)
        self.entry2.pack(padx=2, pady=2, side=tk.LEFT)
        self.button2.pack(padx=5, pady=2, side=tk.LEFT)

        self.button3 = tk.Button(self.button_frame, text="计算", width=12, command=self.calculate)
        self.button4 = tk.Button(self.button_frame, text="停止", width=12, command=self.stop_thread2)

        self.button3.config(state=tk.NORMAL)
        self.button4.config(state=tk.DISABLED)

        self.button3.pack(padx=2, pady=2, side=tk.LEFT)
        self.button4.pack(padx=2, pady=2, side=tk.LEFT)

        self.thread2 = threading.Thread()
        self.event = threading.Event()

        root.bind("<<event1>>", lambda e: self.open_file())

    def open_file(self):
        res = tk.filedialog.askopenfilename()
        if res:
            self.entry1.config(state=tk.NORMAL)
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, res)
            self.entry1.config(state=tk.DISABLED)

    def get_path(self):
        self.root.event_generate('<<event1>>')

    def stop_thread2(self):
        self.event.set()

    @staticmethod
    def set_entry(entry, text):
        entry.config(state=tk.NORMAL)
        entry.delete(0, tk.END)
        entry.insert(0, text)
        entry.config(state=tk.DISABLED)

    def calculate(self):
        if self.thread2.is_alive():
            return

        path1 = self.entry1.get()

        input_name = os.path.basename(path1)
        file_name = '仿真输出_%s_%s' % (time.strftime("%Y%m%d%H%M%S", time.localtime()), input_name)
        # file_name = '仿真输出_%s.xlsx' % time.strftime("%Y%m%d%H%M%S", time.localtime())
        path2 = '/'.join([os.path.dirname(path1), file_name])

        self.set_entry(self.entry2, path2)
        self.entry2.config(state=tk.NORMAL)
        self.entry2.delete(0, tk.END)
        self.entry2.insert(0, path2)
        self.entry2.config(state=tk.DISABLED)

        self.event.clear()
        self.thread2 = threading.Thread(name='t2', target=self.wrap_calc, args=(path1, path2))
        self.thread2.setDaemon(True)

        self.button3.config(state=tk.DISABLED)
        self.button4.config(state=tk.NORMAL)

        self.thread2.start()

    @property
    def current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    def wrap_calc(self, path1, path2):
        main_cal(path1, path2, self)
        self.event.clear()

        self.button3.config(state=tk.NORMAL)
        self.button4.config(state=tk.DISABLED)


if __name__ == '__main__':
    tk1 = tk.Tk()
    MainWindow(tk1)
    tk1.mainloop()

