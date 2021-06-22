 Complete the solve function below.
def solve(s):
    t=[]
    new=''
    for c in s:
        t.append(c)
    t[0]=t[0].upper()
    for d in range(len(s)):
        if s[d]==' ' or s[d]=='  ':
            t[d+1]=t[d+1].upper() 
    for k in t:
        new+=k

    return new 
    

   

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = input()

    result = solve(s)

    fptr.write(result + '\n')

    fptr.close()
