import os
import random
import subprocess

class cflags:
    CREATE_NO_WINDOW = 0x08000000

def translate2to3(text):
    v = str(random.randint(500*500, 4999*4999))
    open(v, 'w').write(text)
    
    t = subprocess.Popen(f'2to3 {v} -w', creationflags=cflags.CREATE_NO_WINDOW)
    t.communicate()
    
    out = open(v).read()
    os.remove(v)
    os.remove(v + '.bak')
    
    return out

def translate_python2_file_then_run(file):
    text = open(file).read()
    
    v = str(random.randint(500*500, 4999*4999))
    open(v, 'w').write(text)
    
    t = subprocess.Popen(f'2to3 {v} -w', creationflags=cflags.CREATE_NO_WINDOW)
    t.communicate()
    
    out = open(v).read()
    os.system(f'python3 {v}')
    os.remove(v)
    os.remove(v + '.bak')

def translate_python2_file(file):
    text = open(file).read()
    v = str(random.randint(500*500, 4999*4999))
    open(v, 'w').write(text)
    
    t = subprocess.Popen(f'2to3 {v} -w', creationflags=cflags.CREATE_NO_WINDOW)
    t.communicate()
    
    out = open(v).read()
    os.remove(v)
    
    return out

