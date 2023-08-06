from pathlib import Path

from matplotlib import pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.animation import FuncAnimation

from . import common
import __main__
# chinese font
# no use
# plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
# plt.rcParams['axes.unicode_minus'] = False

font_path1 = Path('C:\Windows\Fonts\msjh.ttc')
font_path2 = Path('C:\Windows\Fonts\msjh.ttf')
if font_path1.exists():
    common.font = fm.FontProperties(fname=str(font_path1), size=13)
elif font_path2.exists():
    common.font = fm.FontProperties(fname=str(font_path2), size=13)
else:
    print('<< 找不到微軟正黑體 >> ')
    common.font = None

# style
plt.style.use('seaborn')



__all__ = [ 
            '繪製折線圖', '顯示圖表', 'XY尺度相同', 'Y軸顯示範圍', 'X軸顯示範圍', '設定圖表標題', 
            '設定X軸標籤', '設定Y軸標籤', '設置折線圖動畫', '開始折線圖動畫',
            ]

# init
#common.speaker = win32com.client.Dispatch("SAPI.SpVoice")


繪製折線圖 = plt.plot
Y軸顯示範圍 = plt.ylim
X軸顯示範圍 = plt.xlim


def XY尺度相同():
    return plt.axis('equal')

    
def 顯示圖表(等待=False):
    plt.show(block=等待)        

def 設定圖表標題(name):
    plt.title(name, fontproperties=common.font)

def 設定X軸標籤(name):
    plt.xlabel(name, fontproperties=common.font)

def 設定Y軸標籤(name):
    plt.ylabel(name, fontproperties=common.font)




def 設置折線圖動畫(*args, **kwargs):
    plt.ion()
    common.figure, common.axes = plt.subplots()
    common.line, = common.axes.plot(*args, **kwargs)
    common.line.更新X軸資料 = common.line.set_xdata
    common.line.更新Y軸資料 = common.line.set_ydata
    common.is_animation_setup = True

def 開始折線圖動畫():
    if common.is_animation_setup:
        if hasattr(__main__, '動畫更新時'):
            common.animation = FuncAnimation(common.figure, __main__.動畫更新時, fargs=(common.line,), interval=50) 
        else:
           print('<< 未定義 動畫更新時 >>')    
    else:
        print('<< 未設置動畫 >>')

if __name__ == '__main__' :
    pass
    
