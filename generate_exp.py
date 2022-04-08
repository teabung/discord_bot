import random

Ops = ['+', '-', '*', '/']

def generate_expression(difficulty):
    paranthesesmin = 0
    paranthesesmax = 0 + difficulty + 1
    nummin = 1
    nummax = 10 * difficulty
    sizemin = 2 + difficulty
    sizemax = 2 + (difficulty ** 2)
    
    parantheses = random.randint(paranthesesmin, paranthesesmax)
    expressionsize = random.randint(sizemin, sizemax)
    
    available_choice = []
    for i in range(expressionsize-parantheses):
        available_choice.append(str(random.randint(nummin, nummax)))
    for i in range(parantheses):
        available_choice.append('(')
    
    previous = ''
    expression = ''
    while len(available_choice) != 0:
        popout = random.randrange(len(available_choice))
          
        if available_choice[popout] != '(' and  available_choice[popout] != ')':
            if previous != '(' and previous != '':
                expression += random.choice(Ops)
            expression += available_choice[popout]
            previous = available_choice[popout]
            available_choice.pop(popout)
        elif available_choice[popout] == '(':
            if previous != '(' and previous != '':
                expression += random.choice(Ops)
            expression += available_choice[popout]
            previous = available_choice[popout]
            available_choice.pop(popout)
            available_choice.append(')')
            available_choice.append(str(random.randint(nummin, nummax))) #Removing a paranthese from the list means that it has to be replaced with a ')' and a number.
        elif available_choice[popout] == ')':
            if previous == '(':
                temp = 0
                for i in range(len(available_choice)):
                    if available_choice[i] != '(' and available_choice[i] != ')':
                        temp = i
                        break
                expression += available_choice[temp]
                available_choice.pop(temp)
            expression += available_choice[popout]
            previous = available_choice[popout]
            available_choice.pop(popout)
        
    return expression

def __ModifyExpression(exp):
    newexp = ''
    for i in range(len(exp)-1):
        newexp += exp[i]
    return newexp