from morphs_modules import *
from general_modules import * 

chat = openlog('./tmp.txt')

reg = cut()

pre_chat = preprocessing_chat(chat, reg, 'list')

print(pre_chat)



