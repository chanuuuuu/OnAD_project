import matplotlib.pyplot as plt
%matplotlib inline
import platform
from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Darwin' :#맥
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows' : 
    #폰트 차후 확인
    fontPath = 'c:/Windows/Fonts/malgun.ttf'
    fontName = font_manager.FontProperties(fname=fontPath).get_name()
    rc('font', family=fontName)
elif platform.system() == 'Linux' : 
    fontPath = '/usr/share/fonts/truetype/nanum/NanumSquareB.ttf'
    fontName = font_manager.FontProperties(fname=fontPath).get_name()
    rc('font', family=fontName)
#     fontPath =  '/usr/share/fonts/truetype/nanum/NanumMyeongjoEco.ttf',
else : print('알수없음')
import seaborn as sns