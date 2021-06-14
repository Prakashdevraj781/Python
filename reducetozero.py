num=8
count=0
while num > 0:
    if (num%2==0):
        num=num/2
        count=count+1
        print('The number updated in if statment to ',num)
        print('counter is ',count)
    else:
        num=num-1
        count=count+1
        print('The number updated in else statment to ',num)
        print('counter is ',count)
