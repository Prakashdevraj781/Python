string='ABCDCDC'
substring='CDC'
count=0
i=0
while i!=-1:
    i=string.find(substring,i+1)
    if(i!=-1):
        count=count+1
    else:
        break
print(count)




