Hercy wants to save money for his first car. He puts money in the Leetcode bank every day.

He starts by putting in $1 on Monday, the first day. Every day from Tuesday to Sunday, he will put in $1 more than the day before. On every subsequent Monday, he will put in $1 more than the previous Monday.
Given n, return the total amount of money he will have in the Leetcode bank at the end of the nth day.


l=[1,2,3,4,5,6,7]
sum=0
for c in range(0,n):
    i=c%7
    if c<7:
        sum=sum+l[i]
        print(sum)
        
    else:
        l[i]=l[i]+1
        sum=sum+l[i]
        print(sum)
        
        

