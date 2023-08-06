import tkinter as tk
import tkinter.font as tf
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory
import time
import threading
from functools import wraps


from xyw_macro.utils import SingletonType
from xyw_macro.contants import SLEEP_TIME


class Notification(metaclass=SingletonType):
    def __init__(self, text='xyw'):
        self.__text = text
        self.__visible = False
        self.__vnum = 0
        self.__window, self.__label, self.__width = self.__init__window()
        self.set_visible(self.__visible)

    def show(self):
        if self.__vnum == 0:
            self.set_visible(True)
        self.__vnum = self.__vnum + 1

    def hide(self):
        self.__vnum = self.__vnum - 1
        if self.__vnum == 0:
            self.set_visible(False)

    def __init__window(self):
        window = tk.Tk()
        window.wm_attributes('-topmost', True)
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        width = round(screen_width / 10)
        height = round(screen_width / 10)
        window.geometry('{}x{}+{}+{}'.format(width, height, (screen_width - width) // 2, (screen_height - height) // 2))
        window.overrideredirect(True)
        window.configure(background='black')
        window.attributes('-alpha', 0.7)
        font_size = self.__get_font_size(width)
        outer_border_size = round(font_size * 0.08)
        inner_border_size = round(font_size * 0.05)
        font = tf.Font(size=font_size, weight=tf.BOLD)
        label_border = tk.LabelFrame(window, background='white', relief='flat')
        label = tk.Label(label_border, text=self.__text, font=font, bg='black', fg='white',
                              height=height, width=width, justify='center', anchor='center',
                              borderwidth=0, relief='flat')
        label_border.pack(fill='both', expand=True, padx=outer_border_size, pady=outer_border_size)
        label.pack(fill='both', expand=True, padx=inner_border_size, pady=inner_border_size)
        return window, label, width

    def get_text(self):
        """
        获取标签文本
        :return:
        """
        return self.__text

    def __get_font_size(self, width):
        # 根据换行符拆分文本
        texts = self.__text.split('\n')
        # 英文半角字符集
        alnum = r'abcdefghijklmnopqrstuvwxyz0123456789+-*/=`~!@#$%^&*()_\|?><.,'
        # 计算最大单行字符长度
        length = [1]
        for item in texts:
            tem = 0
            for i in item:
                if i.lower() in alnum:
                    # 英文半角字符算半个字符长度
                    tem = tem + 0.5
                else:
                    # 其他字符算一个字符长度
                    tem = tem + 1
            length.append(tem)
        length = max(length)
        # 根据字符长度动态更改字体尺寸
        font_size = round(width * 0.6 / length)
        return font_size

    def set_text(self, text):
        """
        设置标签文本
        :param text:
        :return:
        """
        self.__text = text
        font_size = self.__get_font_size(self.__width)
        # 更改标签文本
        font = tf.Font(size=font_size, weight=tf.BOLD)
        self.__label.config(text=self.__text, font=font)

    def get_visible(self):
        """
        获取窗体可见性
        :return:
        """
        return self.__visible

    def set_visible(self, visible):
        """
        设置窗体可见性
        :param visible:
        :return:
        """
        self.__visible = visible
        if self.__visible:
            self.__window.update()
            self.__window.deiconify()
        else:
            self.__window.withdraw()

    def run(self):
        """
        启动窗体主循环
        :return:
        """
        self.__window.mainloop()

    text = property(get_text, set_text)
    visible = property(get_visible, set_visible)


class InputBox:
    """
    参数输入框类
    """
    def __init__(self, title='输入框', normal=None, file=None, dir=None):
        """
        初始化实例
        :param title: 对话框标题
        :param normal: 普通参数，皆为string类型
        :param file: 文件地址参数，通过文件选择对话框输入
        :param dir: 文件夹地址参数，通过文件夹选择对话框输入
        """
        self.title = title
        self.normal = normal
        self.file = file
        self.dir = dir

        if self.normal is None:
            self.normal = []
        if self.file is None:
            self.file = []
        if self.dir is None:
            self.dir = []

        self.top = None
        self.entries = []
        self.vars = []

        # 输入框中输入的参数值，顺序按照normal、file、dir的数序依次排列
        self.values = []

    def show(self):
        """
        显示输入对话框
        :return: 输入的参数列表
        """
        return self.top_window()

    @staticmethod
    def select_file(var):
        filepath = askopenfilename()
        var.set(filepath)

    @staticmethod
    def select_dir(var):
        dirpath = askdirectory()
        var.set(dirpath)

    def clear_all(self):
        for entry in self.entries:
            entry.delete(0, tk.END)
        for var in self.vars:
            var.set('')

    def close_window(self, flag=False):
        if flag:
            self.values = None
        else:
            self.values = [item.get() for item in self.entries]
        self.top.destroy()

    def top_window(self):
        self.top = tk.Toplevel()
        self.top.withdraw()
        self.top.update()
        self.top.wm_attributes('-topmost', True)
        self.top.attributes('-toolwindow', True)
        self.top.title(self.title)
        self.top.grab_set()

        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        width = 300
        height = ((len(self.normal) + len(self.file) + len(self.dir)) * 2 + 1) * 30
        self.top.geometry('{}x{}+{}+{}'
                          .format(width, height, (screen_width - width) // 2, (screen_height - height) // 2))

        for param in self.normal:
            frame = tk.Frame(self.top, takefocus=True)
            frame.pack(fill=tk.X, padx=10, pady=2, expand=1)
            tk.Label(frame, text=param).pack(side=tk.TOP, anchor=tk.W)
            self.entries.append(tk.Entry(frame, show=None))
            self.entries[-1].pack(fill=tk.X, side=tk.TOP)

        for param in self.file:
            self.vars.append(tk.StringVar())
            frame = tk.Frame(self.top, takefocus=True)
            frame.pack(fill=tk.X, padx=10, pady=2, expand=1)
            tk.Label(frame, text=param).pack(side=tk.TOP, anchor=tk.W)
            self.entries.append(tk.Entry(frame, show=None, textvariable=self.vars[-1], state=tk.DISABLED))
            self.entries[-1].pack(fill=tk.X, side=tk.TOP)
            self.entries[-1].pack(fill=tk.X, side=tk.LEFT, expand=1)
            tk.Button(frame, text='选择文件', command=lambda var=self.vars[-1]: self.select_file(var)) \
                .pack(fill=tk.X, side=tk.LEFT)

        for param in self.dir:
            self.vars.append(tk.StringVar())
            frame = tk.Frame(self.top, takefocus=True)
            frame.pack(fill=tk.X, padx=10, pady=2, expand=1)
            tk.Label(frame, text=param).pack(side=tk.TOP, anchor=tk.W)
            self.entries.append(tk.Entry(frame, show=None, textvariable=self.vars[-1], state=tk.DISABLED))
            self.entries[-1].pack(fill=tk.X, side=tk.TOP)
            self.entries[-1].pack(fill=tk.X, side=tk.LEFT, expand=1)
            tk.Button(frame, text='选择文件夹', command=lambda var=self.vars[-1]: self.select_dir(var)) \
                .pack(fill=tk.X, side=tk.LEFT)

        frame = tk.Frame(self.top, takefocus=True)
        frame.pack(fill=tk.X, padx=10, pady=2, expand=1)
        button1 = tk.Button(frame, text='确定', command=lambda: self.close_window(False))
        button1.pack(side=tk.LEFT, fill=tk.X, expand=1)
        button2 = tk.Button(frame, text='清空', command=self.clear_all)
        button2.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.top.protocol("WM_DELETE_WINDOW", lambda: self.close_window(True))
        self.top.bind('<Return>', lambda event: self.close_window(False))
        self.top.bind('<Escape>', lambda event: self.close_window(True))

        self.top.deiconify()
        self.top.focus_force()
        self.top.focus_set()
        self.entries[0].focus_set()

        self.top.wait_window()
        return self.values


def input_box(normal=None, file=None, dir=None, title='输入框'):
    """
    参数输入框装饰器
    :param normal:
    :param file:
    :param dir:
    :param title: 输入框标题
    :return:
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            time.sleep(SLEEP_TIME)
            res = InputBox(title=title, normal=normal, file=file, dir=dir).show()
            if res is not None:
                return f(*res)
        return decorated
    return decorator


def confirm_box(message='确定执行此操作吗？'):
    """
    操作确认框装饰器
    :param message: 提示信息
    :return:
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            time.sleep(SLEEP_TIME)
            if messagebox.askokcancel('提示', message):
                return f(*args, **kwargs)
        return decorated
    return decorator


if __name__ == '__main__':
    def sub():
        time.sleep(2)
        notify.text = 'xue'
        notify.show()
        time.sleep(2)
        notify.hide()
    #     notify = Notification()
    #     threading.Thread(target=auto_hide).start()
    #     notify.start()
    # thd = threading.Thread(target=sub)
    # thd.start()
    # def auto_hide():
    #     time.sleep(2)
    #     # notify.destroy()
    #     # flag = False
    #     notify.hide()
    notify = Notification('xyw_macro\n已启动')
    threading.Thread(target=sub).start()
    notify.run()
    # notify.show(0.2)
    # print('end')
    # time.sleep(2)
    # notify.set_text('changed')
    # notify.show()

    # notify.start()
    # print('xue')
    # print(type(notify.get_window()))
    # notify.start()
    # flag = True
    # while flag:
    #     # notify.get_window().update_idletasks()
    #     notify.get_window().update()
