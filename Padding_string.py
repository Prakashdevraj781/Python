n=17
w=len(bin(n)[2:])
for i in range(1,n+1):
    print(str(i).rjust(w,' '),' ',
          str(oct(i)[2:]).rjust(w,' '),' ',
          str(hex(i)[2:]).rjust(w,' ').upper(),' ',
          str(bin(i)[2:]).rjust(w,' '))
