import tkinter as tk
import psutil
from tkinter import ttk

class SystemMonitor(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(bg='white')
        self.overrideredirect(1)
        
        # 设置窗口透明度
        self.attributes("-alpha", 0.9)
        
        self.width = 500
        self.height = 20
        self.geometry("+{}+{}".format(int(self.winfo_screenwidth()/2), int(self.winfo_screenheight()/2)))

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, highlightthickness=0)
        self.canvas.pack()

        self.mem_label = tk.Label(self, text='Memory Usage:', bg='white', font='Consolas')
        self.cpu_label = tk.Label(self, text='CPU Usage:', bg='white', font='Consolas')
        self.temp_label = tk.Label(self, text='Current PID:', bg='white', font='Consolas')
        self.prog_mem_label = tk.Label(self, text='Program Memory Usage:', bg='white', font='Consolas')
        self.prog_cpu_label = tk.Label(self, text='Program CPU Usage:', bg='white', font='Consolas')

        self.mem_label.pack()
        self.cpu_label.pack()
        self.prog_mem_label.pack()
        self.prog_cpu_label.pack()

        # 添加鼠标事件
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<ButtonRelease-1>", self.stop_move)
        self.canvas.bind("<B1-Motion>", self.on_move)

        # 初始化鼠标位置
        self._x = 0
        self._y = 0

        # 将窗口设置为固定在最上层
        self.attributes("-topmost", True)

        # 更新状态
        self.update_usage()

        self.bind('<Button-3>', self.show_menu)

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def stop_move(self, event):
        self._x = None
        self._y = None

    def on_move(self, event):
        deltax = event.x - self._x
        deltay = event.y - self._y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+{}+{}".format(x, y))

    def update_usage(self):
        mem_usage = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent()
        pid = psutil.Process().pid
        prog_mem_usage = psutil.Process(pid).memory_percent()
        prog_cpu_usage = psutil.Process(pid).cpu_percent()

        self.mem_label.config(text="Total Memory Usage: {:.2f}GB/{:.2f}GB, {}%".format(psutil.virtual_memory().total / 1024 / 1024 / 1024, 
                                                                               psutil.virtual_memory().used / 1024 / 1024 / 1024, 
                                                                               mem_usage), fg='blue')
        self.cpu_label.config(text="Total CPU Usage: {}%".format(cpu_usage), fg='blue')
        self.temp_label.config(text="Current PID: {}".format(pid), fg='blue')
        self.prog_mem_label.config(text="Program Memory Usage: {:.1f}%".format(prog_mem_usage), fg='blue')
        self.prog_cpu_label.config(text="Program CPU Usage: {}%".format(prog_cpu_usage), fg='blue')

        self.after(1000, self.update_usage)

    def show_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Exit", command=self.destroy)
        menu.post(event.x_root, event.y_root)


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = SystemMonitor(root)
    app.mainloop()