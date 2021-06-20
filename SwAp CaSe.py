s="HackerRank.com presents \"Pythonist 2\""
print(s)
t=[]
for char in s:
    if char.islower():
        t.append(char.upper())
    elif char.isupper():
        t.append(char.lower())
    else:
        t.append(char)
new=""
for x in t:
    new+=x
print(new)

"""solution:hACKERrANK.COM PRESENTS "pYTHONIST 2"."""



