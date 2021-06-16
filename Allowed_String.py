accounts=["a","b","c","ab","ac","bc","abc"]
allowed = "abc"
c=len(accounts)
for i in accounts:
    
    for char in i:
        if char not in allowed:
            
            c=c-1
            break 
print(c)
            
