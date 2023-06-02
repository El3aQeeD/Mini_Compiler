import re
import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Compiler so8non")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Fonts
font = pygame.font.Font(None, 28)

output = []
def main():
    clock = pygame.time.Clock()
    code = "" #sting for user input
    output = [] #list for output

    scan_button_rect = pygame.Rect(30, 200, 100, 40) #botton to start scan

    clear_button_rect = pygame.Rect(150, 200, 100, 40)  #botton to clear

    memory_button_rect = pygame.Rect(270, 200, 100, 40)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    code += '\n'
                if event.key == K_BACKSPACE:
                    code = code[:-1]
                else:
                    code += event.unicode
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if scan_button_rect.collidepoint(mouse_pos):
                        print('######################')
                        print(varMap)
                        varMap.clear()
                        errorsList.clear()
                        output.clear()
                        lines = code.split(sep='\n')
                        print(lines)
                        for i in range(len(lines)):
                            if '\r' in lines[i]:
                                print('nice')
                                lines[i] = lines[i][1:]
                                print(lines[i])
                        line = []
                        for i in lines:
                            i = i.split(sep=' ')
                            line.append(i)
                        line = line[:]
                        print(line)

                        output = compiler(line)
                        print('ouutuutut')
                        print(output)

                    if clear_button_rect.collidepoint(mouse_pos):
                        code = ""
                        varMap.clear()
                        errorsList.clear()
                        output.clear()
                        memoryMap.clear()

                    if memory_button_rect.collidepoint(mouse_pos):
                        for key, value in memoryMap.items():
                            output.append(f'{key} : {value}')





        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, pygame.Rect(20, 20, WIDTH - 40, HEIGHT - 400), 1)
        pygame.draw.rect(screen, BLACK, pygame.Rect(20, 250, WIDTH - 40, 300), 3)
        draw_text(screen, "Enter your code:", (30, 30))
        draw_text(screen, code, (30, 70))
        draw_text(screen, "Output:", (30, 260))

        # Draw the Scan button
        pygame.draw.rect(screen, GRAY, scan_button_rect)
        draw_text(screen, "Scan", (scan_button_rect.x + 10, scan_button_rect.y + 10))

        # Draw the Clear button
        pygame.draw.rect(screen, GRAY, clear_button_rect)
        draw_text(screen, "Clear", (clear_button_rect.x + 10, clear_button_rect.y + 10))

        # Draw the Clear button
        pygame.draw.rect(screen, GRAY, memory_button_rect)
        draw_text(screen, "memory", (memory_button_rect.x + 10, memory_button_rect.y + 10))


        # Display each type on a new line
        x = 30
        y = 300
        for type in output:
            draw_text(screen, type, (x, y))
            y += 30
            if y > 520:
                x+=370
                y = 300


        pygame.display.flip()
        clock.tick(30)

def draw_text(surface, text, pos):
    lines = text.split('\n')
    y = pos[1]
    for line in lines:
        text_surface = font.render(line, True, BLACK)
        surface.blit(text_surface, (pos[0], y))
        y += font.get_height() + 5



Identifiers = ['int', 'float', 'string', 'double', 'bool', 'char']
Symbols = {"Operators1":'+',"Operators2": '-',"Operators3": '/',"Operators4": '%',"Operators5": '*', "Open_Bracket":'(',"Close_Bracket": ')',"Open_Curly_Bracket": '{',"Close_Curly_Brackets": '}', "Comma":',', "Semicolon":';', "And":'&&', "Or":'||', "Less than":'<', "Greater than":'>',"Equal" :'=',"Not" :'!=',"compare":"==",'One':">=","Two":"<="}
Reserved_Words = ['for', 'while', 'if', 'do', 'return', 'break', 'continue', 'end']
Numbers = r'\b\d+\b' #regular expression for all digits
# Operators=['+', '-', '/', '%', '*',';']
varMap = {}
errorsList = []
memoryMap = {}

def checkLine(line):
    scanner = []
    for i in line:
        ct = 0

        # find identifier
        if i in Identifiers:
            scanner.append(i + " is Identifier")
            ct += 1

        ##########

        # Find symbols

        for operators, value in Symbols.items():
            if value == i:
                scanner.append(value + " is Symbol and " + operators)
                ct += 1

        ##########

        # Find reserved words
        if i in Reserved_Words:
            scanner.append(i + " is Reserved Word")
            ct += 1

        ##########

        # Find numbers
        matches = re.findall(Numbers, i)
        for match in matches:
            scanner.append(match + " is Number")
            ct += 1

        if ct == 0:
            scanner.append(i + " is Variable")

    return scanner


def calc(mapLists):
    # global
    var = {'x is Variable': ['0 is Number'], 'y is Variable': ['12 is Number'],
           'z is Variable': ['y is Variable', '+ is Symbol and Operators1', '12 is Number',
                             '+ is Symbol and Operators1', 'x is Variable']}
    map = {}
    listOperation = []
    flag = False
    for key, value in mapLists.items():
        listOperation.clear()
        if 'Not assigned' in value:
            return
        for i in value:
            stringNum = ''
            if 'Number' in i:
                i.index('is')
                stringNum = i[:i.index('is') - 1]
                listOperation.append(int(stringNum))
            if '+' in i:
                listOperation.append('+')
            elif '-' in i:
                listOperation.append('-')
            elif '*' in i:
                listOperation.append('*')
            elif '/' in i:
                listOperation.append('/')
            elif 'Not assigned' in i:
                flag = True
            elif 'is Variable' in i:
                for key2, value2 in memoryMap.items():
                    if i in key2:
                        flag = True
                        listOperation.append(value2)

                if not flag:
                    return
        for k in range(len(listOperation)-1):
            if k % 2 != 0:
                if listOperation[k] == '+':
                    listOperation[0] += listOperation[k + 1]
                elif listOperation[k] == '-':
                    listOperation[0] -= listOperation[k + 1]
                elif listOperation[k] == '*':
                    listOperation[0] *= listOperation[k + 1]
                elif listOperation[k] == '/':
                    listOperation[0] /= listOperation[k + 1]

        memoryMap[key] = listOperation[0]
        print('////////////////////')
        print(memoryMap)
        print('//////////////////////////')
        for key, value in memoryMap.items():
            print('hi')
            print(f'{key} : {value}')
            output.append(f'{key} : {value}')



def compiler(line):
    PosSemiColon = 0
    varMap.clear()
    checkList = []
    ctIdentifier = 0
    flagVarAssigned = False
    flagConditionOne = False
    flagErrorflagConditionOne = True
    flagIfCondition = False
    flagForCondition = False
    forLoopPos = -1
    found = False

    for i in range(len(line)):

        value = checkLine(line[i])

        checkList.append(value)

    for i in range(len(checkList)):
        ctIdentifier = 0
        found = False

        if len(checkList[i]) <= 2 and flagForCondition != True :
            print('error syntax')
            errorsList.append(f'error syntax in line {i + 1}')
            flagForCondition= False
            break

        for k in range(1,len(checkList[i])):
            flagVarAssigned = False
            flagConditionOne = False
            flagErrorflagConditionOne = True
            add = True
            ct2 = 0
            ct3 = 0
            ct4 = 0
            ct5 = 0
            ########
            if 'for is Reserved Word' in checkList[i][0] and k == 1:
                flagForCondition = True
                if k == 1 and len(checkList[i]) >= 15:
                    if '( is Symbol and Open_Bracket' in checkList[i][1]:
                        if 'is Variable' in checkList[i][2]:
                            if 'Symbol and Equal' in checkList[i][3]:
                                if 'is Variable' in checkList[i][4] or 'is Number' in checkList[i][4]:
                                    if '; is Symbol and Semicolon' in checkList[i][5]:
                                        if checkList[i][2] in checkList[i][6]:
                                            if 'Less than' in checkList[i][7] or 'Greater than' in checkList[i][7] or 'One' in checkList[i][7] or 'Two' in checkList[i][7]:
                                                if 'is Variable' in checkList[i][8] or 'is Number' in checkList[i][8]:
                                                    if '; is Symbol and Semicolon' in checkList[i][9]:
                                                        if checkList[i][2] in checkList[i][10]:
                                                            if 'Symbol and Equal' in checkList[i][11]:
                                                                if 'is Variable' in checkList[i][12] or 'is Number' in checkList[i][12]:
                                                                    if 'Operators5' in checkList[i][13] or 'Operators4'  in checkList[i][13] or 'Operators3' in checkList[i][13] or 'Operators2' in checkList[i][13]  or 'Operators1' in checkList[i][13]:
                                                                        if 'is Variable' in checkList[i][14] or 'is Number' in checkList[i][14]:
                                                                            if ') is Symbol and Close_Bracket' in checkList[i][15]:
                                                                                forLoopPos = i
                                                                                print('great loop')
                                                                            else:
                                                                                print(f'Error for loop condition must end with ) in line {i + 1}')
                                                                                errorsList.append(f'Error for loop condition must end with ) in line {i + 1}')
                                                                        else:
                                                                            print(f'Error var or number only allowed in line {i + 1}')
                                                                            errorsList.append(f'Error var or number only allowed in line {i + 1}')
                                                                    else:
                                                                        print(f'Error wrong operator in line {i + 1}')
                                                                        errorsList.append(f'Error wrong operator in line {i + 1}')
                                                                else:
                                                                    print(f'Error var or number allowed for increment or decrement in line {i + 1}')
                                                                    errorsList.append(f'Error var or number allowed for increment or decrement in line {i + 1}')
                                                            else:
                                                                print( f'sign = must followed by number var in line {i + 1}')
                                                                errorsList.append(f'sign = must followed by var in line {i + 1}')

                                                        else:
                                                            print(f'use same var please that u assigned in line {i + 1}')
                                                            errorsList.append( f'use same var please that u assigned in line {i + 1}')

                                                    else:
                                                        print(f'condition must followed by ; in line {i + 1}')
                                                        errorsList.append(f'condition must followed by ; in line {i + 1}')
                                                else:
                                                    print(f'Error use number or var after sign in line {i+1}')
                                                    errorsList.append(f'Error use number or var after sign in line {i+1}')
                                            else:
                                                print(f'use correct operator in line {i + 1}')
                                                errorsList.append(f'use correct operator in line {i + 1}')
                                        else:
                                            print(f'use same var please that u assigned in line {i + 1}')
                                            errorsList.append(f'use same var please that u assigned in line {i + 1}')
                                    else:
                                        print(f'condition must followed by ; in line {i + 1}')
                                        errorsList.append(f'condition must followed by ; in line {i + 1}')
                                else:
                                    print(f'sign = must followed by number or var in line {i + 1}')
                                    errorsList.append(f'sign = must followed by number or var in line {i + 1}')
                            else:
                                print(f'var must followed by = in line {i + 1}')
                                errorsList.append(f'var must followed by = in line {i + 1}')

                        else:
                            print(f'for must start with var in line {i + 1}')
                            errorsList.append(f'for must start with var in line {i + 1}')
                    else:
                        print(f'for loop must start with ( in line {i + 1}')
                        errorsList.append(f'for loop must start with ( in line {i + 1}')
                else:
                    print(f'for loop not complete in line {i + 1}')
                    errorsList.append(f'for loop not complete in line {i + 1}')
                    break

                print('for loop')
            if "if is Reserved Word" in checkList[i][0]: # conditions for if statement
                flagIfCondition = True
                if k == 1:
                    if 'if is Reserved Word' in checkList[i][0] :
                        if '( is Symbol and Open_Bracket' in checkList[i][1]:
                                if 'is Variable' in checkList[i][2]:
                                    for j in range(2,len(checkList[i])):
                                        # var var
                                        if 'is Variable' in checkList[i][j-1] or 'is Number' in checkList[i][j-1]:
                                            ct4 += 1
                                            if ct4 % 2 == 0 and ') is Symbol and Close_Bracket' not in checkList[i][j]:
                                                if '&& is Symbol and And' not in checkList[i][j] and '|| is Symbol and Or' not in checkList[i][j]:
                                                    print(f'Error put && or || between the conditions in line {i+1}')
                                                    errorsList.append(f'Error put && or || between the conditions in line {i+1}')


                                            if ct4 % 2 != 0 and 'Less than' not in checkList[i][j] and 'Greater than' not in checkList[i][j] and 'compare' not in checkList[i][j] and 'Not' not in checkList[i][j] and 'One' not in checkList[i][j] and 'Two' not in checkList[i][j]:
                                                print(f'Error write valid condition in line {i+1}')
                                                errorsList.append(f'Error write valid condition in line {i+1}')
                                        if 'is Variable' in checkList[i][j] == 'is Variable' in checkList[i][j-1]:
                                            print(f'Error two var in line {i+1}')
                                            errorsList.append(f'Error two var in line {i+1}')

                                        if 'is Number' in checkList[i][j] and 'is Variable' in checkList[i][j-1]:
                                            print(f'Error two conditions without split in line {i+1}')
                                            errorsList.append(f'Error two conditions without split in line {i+1}')
                                        if 'is Variable' in checkList[i][j] and 'is Number' in checkList[i][j-1]:
                                            print(f'Error two conditions without split in line {i+1}')
                                            errorsList.append(f'Error two conditions without split in line {i+1}')
                                        # num num
                                        if 'is Number' in checkList[i][j] == 'is Number' in checkList[i][j-1]:
                                            print(f'Error two numbers in line {i+1}')
                                            errorsList.append(f'Error two numbers in line {i+1}')
                                        if j == 4: # to print the error one time
                                            if 'is Symbol' in checkList[i][j] == 'is Symbol' in checkList[i][j-1]:
                                                print(f'Error two symbols in line {i+1}')
                                                errorsList.append(f'Error two symbols in line {i+1}')

                                            if ') is Symbol and Close_Bracket' not in checkList[i][len(checkList[i])-1]:
                                                print(f'error please end ur if statment with closed bracket ) line{i+1}')
                                                errorsList.append(f'error please end ur if statment with closed bracket ) line{i+1}')

                                            if 'is Number' not in checkList[i][len(checkList[i])-2] and 'is Variable' not in checkList[i][len(checkList[i])-2]:

                                                print(f'Error write correct statement in line {i+1}')
                                                errorsList.append(f'Error write correct statement in line {i+1}')


                                else:
                                    print(f'error must start with variable !!!! {i+1}')
                                    errorsList.append(f'error must start with variable !!!! {i+1}')
                        else:
                            print(f'put open bracket after if ( please in line !!!! {i+1}')
                            errorsList.append(f'put open bracket after if ( please in line !!!! {i+1}')


                    else:
                        print(f'start with if please in line !!!! {i+1}')
                        errorsList.append(f'start with if please in line !!!! {i+1}')

            ########### declare ******
            if k == 1:
                if 'is Identifier' in checkList[i][0]:
                    if 'is Variable' in checkList[i][1]:
                        if '; is Symbol and Semicolon' in checkList[i][2]:

                            for key, value in varMap.items():
                                print(value)
                                if key in checkList[i][1]:
                                    print(value)
                                    print(checkList[i][1])
                                    found = True
                                    print('Error declared')
                                    errorsList.append(f'Error var declared already in line  {i + 1}')
                                    break

                            if not found:
                                ##########################################
                                varMap[checkList[i][1]] = ['Not assigned']

                                print('add')





            #########

            if k == 1:
                if 'Number' in checkList[i][0]:
                    print(f'Error can not start with number in line {i+1}')
                    errorsList.append(f'Error can not start with number in line {i+1}')

            if k == 1:
                if 'is Identifier'  in checkList[i][0]:
                    if 'is Variable' in checkList[i][1]:
                        if 'Symbol and Equal' in checkList[i][2]:
                            for j in range(3, len(checkList[i]) - 1):
                                if 'is Variable' in checkList[i][j-1] or 'is Number' in checkList[i][j-1]:
                                    ct5 += 1
                                    if ct5 % 2 != 0 and 'Operators5' not in checkList[i][j] and 'Operators4' not in checkList[i][j] and 'Operators3' not in checkList[i][j] and 'Operators2' not in checkList[i][j] and 'Operators2' not in checkList[i][j] and 'Operators1' not in checkList[i][j]:
                                        print(f'Error wrong operator in line {i+1}')
                                        errorsList.append(f'Error wrong operator in line {i+1}')

                            if 'Number' in checkList[i][3] :
                                    for key,value in varMap.items():
                                        if key == checkList[i][1]:
                                            flagVarAssigned = True
                                            print(f'error this var already declared {checkList[i][1]} in line {i+1}')
                                            errorsList.append(f'error this var already declared {checkList[i][1]} in line {i+1}')
                                        for j in range(3,len(checkList[i])-1):
                                            if 'is Variable' in checkList[i][j]:
                                                if key not in checkList[i]:
                                                    print(f'error var {checkList[i][j]} not declared in line {i+1}')
                                                    errorsList.append(f'error var {checkList[i][j]} not declared in line {i+1}')
    #                                                 flagErrorflagConditionOne = False
                                            else:
                                                flagErrorflagConditionOne = False



                                    if len(varMap) == 0 or flagVarAssigned == False:
                                        if flagErrorflagConditionOne == False:
                                            varMap[checkList[i][1]] = checkList[i][3:len(checkList[i])-1]
                                            calc(varMap)
                                            print("added33")
                                        if len(varMap) == 0 :
                                            for j in range(3,len(checkList[i])-1):
                                                   if 'is Variable' in checkList[i][j]:
                                                        add = True
                                                        print(f"Error var {checkList[i][j]} not1 declared in line {i+1}")
                                                        errorsList.append(f"Error var {checkList[i][j]} not1 declared in line {i+1}")
                                            if add == True:
                                                ####################################
                                                varMap[checkList[i][1]] = checkList[i][3:len(checkList[i])-1]
                                                calc(varMap)
                                                print('added12222')
            if k == 1:
                # int x = y + 12 + qw ;
                if 'is Identifier'  in checkList[i][0]:
                    if 'is Variable' in checkList[i][1]:
                        if 'Symbol and Equal' in checkList[i][2]:
                            if 'is Variable' in checkList[i][3] :

                                flagConditionOne = True
                                for key,value in varMap.items():
                                    if key == checkList[i][1]:
                                        flagVarAssigned = True
                                        print(f'error this var already declared {checkList[i][1]} in line {i+1}')
                                        errorsList.append(f'error this var already declared {checkList[i][1]} in line {i+1}')
                                    for j in range(3,len(checkList[i])-1):
                                        if key == checkList[i][j]:
                                            flagErrorflagConditionOne = False

                                if len(varMap) == 0 or flagVarAssigned == False :

                                    if flagErrorflagConditionOne == False:
                                        varMap[checkList[i][1]] = checkList[i][3:len(checkList[i])-1]
                                        calc(varMap)
                                        #####################################
                                        print('added1')
                                    if len(varMap) == 0 :
                                        print('hiii')
                                        for j in range(3,len(checkList[i])-1):
                                               if 'is Variable' in checkList[i][j]:
                                                    add = False
                                                    print(f"Error var {checkList[i][j]} not declared in line {i+1}")
                                                    errorsList.append(f"Error var {checkList[i][j]} not declared in line {i+1}")
                                        if add == True:
                                            varMap[checkList[i][1]] = checkList[i][3:len(checkList[i])-1]
                                            calc(varMap)
                                            ############################
                                            print('added121')


            if '; is Symbol and Semicolon' in checkList[i][k]:
                PosSemiColon = k

            if 'is Identifier' in checkList[i][k]:
                if 'is Identifier' in checkList[i][k-1]:
                    print(f'error can not put two Identifiers {i+1}')
                    errorsList.append(f'error can not put two Identifiers {i+1}')

            if 'is Variable' in checkList[i][k]:
                if 'is Variable' in checkList[i][k-1]:
                    print(f'error can not put two variables {i+1}')
                    errorsList.append(f'error can not put two variables {i+1}')

            if 'is Number' in checkList[i][k]:
                if 'is Number' in checkList[i][k-1]:
                    print(f'error can not put two numbers {i+1}')
                    errorsList.append(f'error can not put two numbers {i+1}')
            ###
            if "if is Reserved Word" not in checkList[i-1] :
                if 'Symbol' in checkList[i][k]:
                    if 'Symbol' in checkList[i][k-1]:
                        print(f'error can not put two Symbol {i+1}')
                        errorsList.append(f'error can not put two Symbol {i+1}')

            if 'is Identifier' in checkList[i][k-1]:
                ctIdentifier += 1
            ####

            if k == 1:
                if 'is Identifier' not in checkList[i][0]:
                    if 'is Variable' in checkList[i][0]:
                        for key,value in varMap.items():
                            if key == checkList[i][0]:
                                flagVarAssigned = True
                        if  flagVarAssigned == True:
                            for j in range(2,len(checkList[i])-1):

                                if 'is Variable' in checkList[i][j]:
                                    for key2,value2 in varMap.items():
                                        if key2 == checkList[i][j]:
                                            ct3 += 1
                                            add = True

                                    if ct3 == 0:
                                        print(f"Error var {checkList[i][j]} not declared in line {i+1}")
                                        errorsList.append(f"Error var {checkList[i][j]} not declared in line {i+1}")
                                        break


                        if add == True:
                            #############################################################
                            varMap[checkList[i][0]] = checkList[i][2:len(checkList[i])-1]
                            calc(varMap)
                            print('added1212121')

                        if flagVarAssigned != True:
                            print(f'error var {checkList[i][0]} must be declared {i+1}')
                            errorsList.append(f'error var {checkList[i][0]} must be declared {i+1}')


            if k == 1:
                if 'is Identifier'  in checkList[i][0]:
                    if 'is Variable' not in checkList[i][1]:
                        print(f'error Identifier must be followed by var {i+1}')
                        errorsList.append(f'error Identifier must be followed by var {i+1}')

            if k == 1:
                if 'is Identifier'  in checkList[i][0]:
                    if 'is Variable' in checkList[i][1]:
                        if 'Symbol and Semicolon' not in checkList[i][2]:
                            if 'Symbol and Equal' not in checkList[i][2]:
                                print(f'error Identifier & var must be followed by assign (=) {i+1}')
                                errorsList.append(f'error Identifier & var must be followed by assign (=) {i+1}')



        if forLoopPos != -1:
            if '{ is Symbol and Open_Curly_Bracket' not in checkList[i][len(checkList[i])-1] and i == forLoopPos:
                print(f'Error missing open curly brackets')
                errorsList.append(f'Error missing open curly brackets')
            if i == len(checkList)-1 and '} is Symbol and Close_Curly_Brackets' not in checkList[i][0]:
                print(f'Error missing  closed curly brackets')
                errorsList.append(f'Error missing closed curly brackets')

        if "if is Reserved Word" not in checkList[i] and "if is Reserved Word" not in checkList[i-1] and "for is Reserved Word" not in checkList[i] and i == len(checkList)-1 and '} is Symbol and Close_Curly_Brackets' not in checkList[i][0]:
            # semi colon not in good postion
            if PosSemiColon != len(checkList[i])-1:
                print(f'Error put (;) in line {i+1}')
                errorsList.append(f'Error put (;) in line {i+1}')
            if ctIdentifier > 1:
                print(f'Error many Identifiers in same line {i+1}')
                errorsList.append(f'Error many Identifiers in same line {i+1}')
        if "if is Reserved Word" in checkList[i-1]:
            if '{ is Symbol and Open_Curly_Bracket' not in checkList[i][0] or '} is Symbol and Close_Curly_Brackets' not in checkList[i]:
                print(f'Error missing open and closed curly brackets')
                errorsList.append(f'Error missing open and closed curly brackets')
    if len(errorsList) == 0:
        print(varMap)
        errorsList.append('Correct code')
        return errorsList
    else:
        return errorsList
if __name__ == '__main__':
    main()