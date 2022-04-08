#Expression should not include any spaces.
Ops = ['+', '-', '*', '/', '%', '^']#addition, subtraction, multiplication, division, modulo, exponent

def calc(expression):
    thelist = __exp_tolist(expression)
    #print(tolist)
    
    simplified = []
    skip = -1
    for i in range(len(thelist)):
        #skip through certain parentheses
        if(skip != -1 and i != skip):
            continue
        skip = -1
        if(thelist[i] == '('):
            values = __whenParentheses(thelist, i+1)
            simplified.append(values[0])
            skip = values[1]+1
        else:
            simplified.append(thelist[i])
    return __OrderOfOperation(simplified)

def spacesAdd(expression):
    thelist = __exp_tolist(expression)
    returningstr = ''
    previous = ''
    for i in range(len(thelist)):
        if(previous == '('):
            returningstr += thelist[i]
            previous = thelist[i]
        elif(thelist[i] == ')'):
            returningstr += thelist[i]
            previous = thelist[i]
        else:
            returningstr += ' ' + thelist[i]
            previous = thelist[i]
    return returningstr


def __exp_tolist(expression):
    tolist = []
    negative = True
    distributive_property = False
    pair = ''
    for i in range(len(expression)):
        if negative == True and expression[i] == '-':
            pair += expression[i]
            negative = False
            distributive_property = False
        elif expression[i] not in Ops and expression[i] != '(' and expression[i] != ')':
            pair += expression[i]
            negative = False
            distributive_property = False
        elif expression[i] == '^' and pair != '':
            if(pair[0] == '-'):
                tolist.append('-1')
                tolist.append('*')
                temps = ''
                for temp in range(1,len(pair)):
                    temps += pair[temp]
                tolist.append(temps)
            else:
                tolist.append(pair)
            tolist.append(expression[i])
            pair = ''
            negative = True
            distributive_property = False
        elif expression[i] in Ops and pair == '':
            tolist.append(expression[i])
            negative = True
            distributive_property = False
        elif expression[i] in Ops:
            tolist.append(pair)
            tolist.append(expression[i])
            pair = ''
            negative = True
            distributive_property = False
        elif expression[i] == '(' and pair != '':
            negative = True
            distributive_property = False
            if(pair == '-'):
                pair = '-1'
            tolist.append(pair)
            tolist.append('*')
            tolist.append(expression[i])
            pair = ''
        elif expression[i] == '(' and distributive_property == True:
            tolist.append('*')
            tolist.append(expression[i])
            distributive_property = False
            negative = True
        elif expression[i] == ')' and pair != '':
            tolist.append(pair)
            tolist.append(expression[i])
            pair = ''
            negative = False
            distributive_property = True
        elif expression[i] == ')':
            tolist.append(expression[i])
            negative = False
            distributive_property = True
        elif expression[i] == '(':
            negative = True
            tolist.append(expression[i])
            distributive_property = False
    if(pair != ''):
        tolist.append(pair)
    return tolist
#A list as its parameter
#Solve Exponents -> multiplication, division, modulo -> addition, subtraction.

#This returns the result of expression in parentheses and the location of closing parentheses.
def __whenParentheses(thelist, start):
    returnlist = ['N', 'N']
    simplified = []
    i = start
    skip = -1
    while(thelist[i] != ')'):
        while(skip != -1 and i != skip):
            i += 1
        skip = -1
        if(thelist[i] == '('):
            values = __whenParentheses(thelist, i+1)
            simplified.append(values[0])
            skip = values[1]
        elif thelist[i] != ')':
            simplified.append(thelist[i])
        i += 1
    #print("simplified: ", simplified)
    returnlist[1] = i
    returnlist[0] = __OrderOfOperation(simplified)
    return returnlist

def __OrderOfOperation(sfiedexp):
    Oexistence = True
    while Oexistence:
        goingOnce = False
        for i in range(len(sfiedexp)):
            if(sfiedexp[i] == '^'):
                goingOnce = True
                tempnum = float(sfiedexp[i-1]) ** float(sfiedexp[i+1])
                sfiedexp.insert(i-1, tempnum)
                sfiedexp.pop(i)
                sfiedexp.pop(i)
                sfiedexp.pop(i)
                break
        if not goingOnce:
            Oexistence = False
    #Solve multiplication, division, and modulo
    Oexistence = True
    while Oexistence:
        goingOnce = False
        for i in range(len(sfiedexp)):
            if(sfiedexp[i] == '*'):
                goingOnce = True
                tempnum = float(sfiedexp[i-1]) * float(sfiedexp[i+1])
                sfiedexp.insert(i-1, tempnum)
                sfiedexp.pop(i)
                sfiedexp.pop(i)
                sfiedexp.pop(i)
                break
            elif(sfiedexp[i] == '/'):
                goingOnce = True
                tempnum = float(sfiedexp[i-1]) / float(sfiedexp[i+1])
                sfiedexp.insert(i-1, tempnum)
                sfiedexp.pop(i)
                sfiedexp.pop(i)
                sfiedexp.pop(i)
                break
            elif(sfiedexp[i] == '%'):
                goingOnce = True
                tempnum = float(sfiedexp[i-1]) % float(sfiedexp[i+1])
                sfiedexp.insert(i-1, tempnum)
                sfiedexp.pop(i)
                sfiedexp.pop(i)
                sfiedexp.pop(i)
                break
        if not goingOnce:
            Oexistence = False
    #Solve addtion and subtraction
    Oexistence = True
    while Oexistence:
        goingOnce = False
        for i in range(len(sfiedexp)):
            if(sfiedexp[i] == '+'):
                goingOnce = True
                tempnum = float(sfiedexp[i-1]) + float(sfiedexp[i+1])
                sfiedexp.insert(i-1, tempnum)
                sfiedexp.pop(i)
                sfiedexp.pop(i)
                sfiedexp.pop(i)
                break
            elif(sfiedexp[i] == '-'):
                goingOnce = True
                tempnum = float(sfiedexp[i-1]) - float(sfiedexp[i+1])
                sfiedexp.insert(i-1, tempnum)
                sfiedexp.pop(i)
                sfiedexp.pop(i)
                sfiedexp.pop(i)
                break
        if not goingOnce:
            Oexistence = False
        
    return sfiedexp[0]