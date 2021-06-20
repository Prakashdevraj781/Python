

nums = [1,2,3]
l=[[]]

for i in nums:
    newsubset=[subset + [i] for subset in l]
    l.extend(newsubset)
print(l)
    
    


