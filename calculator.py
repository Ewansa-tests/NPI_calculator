def calculate (expression):
    # we assume that the expression is correctly formated so we seperate on spaces
    expression=expression.split()

    #create stack
    s=[]

    for element in expression:
        if element not in '*/+-':
            s.append(int(element))

        else:
            right = s.pop()
            left=s.pop()
            if element=='+':
                s.append(left+right)
            elif element=='-':
                s.append(left-right)
            elif element=='*':
                s.append(left*right)
            elif element=='/':
                s.append(int(left/right))
    
    return s.pop()

arr = "10 6 + 1 -"
print(calculate(arr))
