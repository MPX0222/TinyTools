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

        # 标签
        self.mem_label = tk.Label(self, text='Memory Usage:', bg='white', font='Consolas')
        self.cpu_label = tk.Label(self, text='CPU Usage:', bg='white', font='Consolas')
        self.prog_mem_label = tk.Label(self, text='Program Memory Usage:', bg='white', font='Consolas')

        self.top1 = tk.Label(self, text='TOP1', bg='white', font='Consolas')
        self.top2 = tk.Label(self, text='TOP2', bg='white', font='Consolas')
        self.top3 = tk.Label(self, text='TOP3', bg='white', font='Consolas')
        self.top4 = tk.Label(self, text='TOP4', bg='white', font='Consolas')
        self.top5 = tk.Label(self, text='TOP5', bg='white', font='Consolas')

        self.mem_label.pack()
        self.cpu_label.pack()
        self.prog_mem_label.pack()
        self.top1.pack()
        self.top2.pack()
        self.top3.pack()
        self.top4.pack()
        self.top5.pack()
        

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
        
        # 退出按钮
        self.bind('<Button-3>', self.show_menu)

    # 窗口拖动函数
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

    def read_pid(self):
        processes = []
        for pid in psutil.pids():
            try:
                process = psutil.Process(pid)
                processes.append(process)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # 按照内存使用量排序
        processes = sorted(processes, key=lambda p: p.memory_info().rss, reverse=True)
        top_dict = []

        # 获取前5个进程的信息并输出
        for process in processes[:5]:
            try:
                # 获取进程信息
                pid = process.pid
                name = process.name()
                status = process.status()
                cpu_percent = process.cpu_percent(interval=0.1)
                memory_precent = process.memory_percent()


                # 输出进程信息
                pid_info = {}
                pid_info['Name'], pid_info['Pid'], pid_info['Status'], pid_info['CPU'], pid_info['Memory'] = name, pid, status, cpu_percent, memory_precent
                top_dict.append(pid_info)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        return top_dict

    def update_usage(self):
        mem_usage = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent()
        pid = psutil.Process().pid
        prog_mem_usage = psutil.Process(pid).memory_percent()


        # 常规显示
        self.mem_label.config(text="Total Memory Usage: {:.2f}GB/{:.2f}GB, {}%".format(psutil.virtual_memory().total / 1024 / 1024 / 1024, 
                                                                               psutil.virtual_memory().used / 1024 / 1024 / 1024, 
                                                                               mem_usage), fg='blue')
        self.cpu_label.config(text="Total CPU Usage: {}%".format(cpu_usage), fg='blue')
        self.prog_mem_label.config(text="Program Memory Usage: {:.2f}%".format(prog_mem_usage), fg='blue')

        top_dict = self.read_pid()
        self.top1.config(text="Name: {}, Pid: {}, Status: {}, CPU: {}%, Memory: {:.2f}%".format(
            top_dict[0]['Name'], top_dict[0]['Pid'], top_dict[0]['Status'], top_dict[0]['CPU'], top_dict[0]['Memory']), fg='green', font=("Consolas", 12))
        self.top2.config(text="Name: {}, Pid: {}, Status: {}, CPU: {}%, Memory: {:.2f}%".format(
            top_dict[1]['Name'], top_dict[1]['Pid'], top_dict[1]['Status'], top_dict[1]['CPU'], top_dict[1]['Memory']), fg='green', font=("Consolas", 12))
        self.top3.config(text="Name: {}, Pid: {}, Status: {}, CPU: {}%, Memory: {:.2f}%".format(
            top_dict[2]['Name'], top_dict[2]['Pid'], top_dict[2]['Status'], top_dict[2]['CPU'], top_dict[0]['Memory']), fg='green', font=("Consolas", 12))
        self.top4.config(text="Name: {}, Pid: {}, Status: {}, CPU: {}%, Memory: {:.2f}%".format(
            top_dict[3]['Name'], top_dict[3]['Pid'], top_dict[3]['Status'], top_dict[3]['CPU'], top_dict[0]['Memory']), fg='green', font=("Consolas", 12))
        self.top5.config(text="Name: {}, Pid: {}, Status: {}, CPU: {}%, Memory: {:.2f}%".format(
            top_dict[4]['Name'], top_dict[4]['Pid'], top_dict[4]['Status'], top_dict[4]['CPU'], top_dict[0]['Memory']), fg='green', font=("Consolas", 12))


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