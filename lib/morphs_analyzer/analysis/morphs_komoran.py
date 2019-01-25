import sys
sys.path.insert(0, '/path/to/OnAD_project/lib/analysis/y_komoran3')

from komoran3py import KomoranPy

ko = KomoranPy()

test = '가나다라마'

print(ko.pos(test))