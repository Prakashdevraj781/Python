iven the names and grades for each student in a class of N students, store them in a nested list and print the name(s) of any student(s) having the second lowest grade.

Note: If there are multiple students with the second lowest grade, order their names alphabetically and print each name on a new line.

input:
    
students = [['Harry', 37.21],
            ['Berry', 37.21],
            ['Tina', 37.2],
            ['Akriti', 41],
            ['Harsh', 39]]

solution:
    
if __name__ == '__main__':
    students=[]
    l=[]
    
    for _ in range(int(input())):
        students.append([input(), float(input())])
    for i in range(len(students)):
        l.append((students[i][1]))
    for k in range(len(l)):
        if l[k]!=min(l):
            sh=l[k]
            break
    students.sort()
    for j in range(len(students)):
        if(students[j][1]==sh):
            print(students[j][0])
