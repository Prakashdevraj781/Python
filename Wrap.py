string='ABCDEFGHIJKLIMNOQRSTUVWXYZ'
w=4
i=0

for d in range(0,len(string),w):
    new=""
    while i in range(d):
        new+=string[i]
        i=i+1  
    print(new)
    
new=""
for z in range(d,len(string)):
    new+=string[z]
print(new)

solution:
ABCD
EFGH
IJKL
INNO
QRST
UVWX
YX



