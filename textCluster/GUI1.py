import tkinter as tk
from tkinter import ttk
import textCluster.movieCluster as cluster

win = tk.Tk()
win.title("电影推荐")  # 添加标题
#win.geometry("400x300")
kind = '全部'

ttk.Label(win, text="电影名字：").grid(column=0, row=0)  # 设置其在界面中出现的位置  column代表列   row 代表行
ttk.Label(win, text="电影类型：").grid(column=1, row=0)  # 添加一个标签，并将其列设置为1，行设置为0

# button被点击之后会被执行
def clickMe():  # 当acction被点击时,该函数则生效
    #action.configure(text='Hello ' + name.get())  # 设置button显示的内容
    #action.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态
    result = cluster.recommand(name.get(),numberChosen.get())
    win1 = tk.Tk()
    win1.title("电影推荐")  # 添加标题
    ttk.Label(win1, text=result,wraplength=300).grid()



# 按钮
action = ttk.Button(win, text="Click Me!", command=clickMe)  # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
action.grid(column=2, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
# 文本框
name = tk.StringVar()  # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
nameEntered = ttk.Entry(win, width=12, textvariable=name)  # 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
nameEntered.grid(column=0, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
nameEntered.focus()  # 当程序运行时,光标默认会出现在该文本框中
# 创建一个下拉列表
number = tk.StringVar()
numberChosen = ttk.Combobox(win, width=12, textvariable=number)
numberChosen['values'] = ('全部','剧情','犯罪','爱情','同性','动作','喜剧','战争','灾难','动画','奇幻','歌舞','音乐','古装','冒险','科幻','家庭','悬疑','传记','惊悚','历史','情色','西部','儿童')  # 设置下拉列表的值
numberChosen.grid(column=1, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
numberChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

win.mainloop()  # 当调用mainloop()时,窗口才会显示出来
