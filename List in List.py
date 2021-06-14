accounts = [[1,5],[7,3],[3,5]]
matrix=[]
for sublist in accounts:
    sum=0
    for j in sublist:
        sum=sum+j
    matrix.append(sum)
matrix.sort()
print(matrix[-1])
