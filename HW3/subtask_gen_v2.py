import os

ins = [f for f in os.listdir() if f.endswith('.in')]
ins.sort(key=lambda x:int(x[:-3]))

N = len(ins)

scores = [5]*N

rct = int((100-sum(scores))/5)
for i in range(rct):
    #print(i%N+1)
    scores[-(i%N+1)]+=5
    
if sum(scores)!=100:
    input('error...press enter to continue')
    exit(0)
    
s = '[\n'

for i,e in enumerate(ins):
    s += " [  %d, [ '%s',  '%s', 1, 4 << 20, 64 << 10]],\n"%(scores[i],e,e.replace('.in','.out'))
s += ']'

print(s)

with open('subtasks.py','w') as f:
    f.write(s)
