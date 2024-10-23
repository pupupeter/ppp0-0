import os

#c = [e for e in os.listdir() if e.endswith('.c')][0]
#os.system('gcc '+c+' -o '+c.replace('.c','.exe'))

#exe = [e for e in os.listdir() if e.endswith('.exe')][0]
exe = 'python AC_code.py'

ins = [e for e in os.listdir() if e.endswith('.in')]

encode1 = 'utf-8'
encode2 = 'cp950'

for ine in ins:
    os.system(exe+' < '+ine+' > '+ine.replace('.in','.out'))

for i,ine in enumerate(ins):
    print('----------------------------')
    print('# '+str(i+1))
    print('----------------------------')
    with open(ine,encoding=encode2) as f:
        print(f.read())
    print('----------------------------')
    with open(ine.replace('.in','.out'),encoding=encode2) as f:
        print(f.read())
#input('press enter to continue')
