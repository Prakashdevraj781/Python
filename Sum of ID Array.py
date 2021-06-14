nums = [8,1,2,2,3]
output= []
count=0
for i in range(len(nums)):
    for j in range(i+1,len(nums)):
        
        if(nums[j] < nums[i]):
            count=count+1
        output.append(count)
        
    
print(output)
                       
