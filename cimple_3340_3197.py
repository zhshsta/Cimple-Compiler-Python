#AUTHORS : ZHSHS PROKOPIOS TALAMAGKAS A.M. : 3340 cs username : cse63340
#	       BASILEIOS GEORGAKIS        A.M. : 3197 cs username : cse63197
 
import sys

###################
#Lektikos Analytis#
###################

global fileLine
fileLine = 1


	


def lex():
    global fileLine
    global keywords
    keywords = [['program',1],['declare',2],['if',3],['else',4],['while',5],['switchcase',6],['forcase',7],['incase',8],['case',9],['default',10],['not',11],['and',12],['or',13],['function',14],['procedure',15],['call',16],['return',17],['in',18],['inout',19],['input',20],['print',21]]
	
    starting_state = 0
    identifier_state = 100
    symbols_state = 200
    number_state = 300
    comment_state = 400
    smaller_state = 600
    larger_state = 700
    end_state = 1100
    
    lettercounter = 0 #Counts the number of letters in a word
    identifier = ''
    lm = []
    lt = []
    
    
    state = starting_state; #Starting state
    input = f.read(1)
    while(input == '\t' or input == ' ' or input == '\r' ):
        input = f.read(1)
    if input == '\n' : 
        fileLine += 1
        return lex()
    if(state == starting_state):
        print(input)
        if input.isalpha(): #Checking if the input is an identifier
            state = identifier_state
        elif input.isdigit(): #Checking if the input is a number
            state = number_state
        elif input == '<': #Checking if the input is the symbol <
            state = smaller_state
        elif input == '>': #Checking if the input is the symbol >
            state = larger_state
        elif input in ('+' , '-' , '*' , '/' , ':' , ',' , ';' , '(' , ')' , '[' , ']', '{' , '}'): #Checking if the input is one of the symbols
            state = symbols_state                
        elif input == '#': #Checking if the input is comments
            state = comment_state
        elif input == '.': #Checking if the input is the symbol .
            state = end_state
        elif input.isspace():
            state = starting_state
        else:
            print('An invalid input was given : ' + input) #Checking if the input is something invalid
            sys.exit()
    if state == identifier_state:
        identifier += input
        input = f.read(1)
        if not input.isalpha() and not input.isdigit():
            lt += [identifier] + [100]
        else :
            while input.isalpha() or input.isdigit():                    
                if lettercounter <= 30:
                    identifier += input
                    input = f.read(1)
                else:
                    error("The word is longer than 30 letters")
            for i in keywords:
                if identifier == i[0]:
                    lt += [identifier] + [i[1]]
                else:
                    lt += [identifier] + [100] 
        f.seek(f.tell()-1)
    if state == number_state:
        identifier += input 
        input = f.read(1)
        if not input.isdigit():
            lt += [identifier] + [300]
        else :
            while input.isdigit():
                #Checking if the number is acceptable within bounds
                if abs(int(identifier)) > 32767:
                    error("The number is out of bounds")
                identifier += input 
                
                lt += [identifier] + [300]
                input = f.read(1)   
        f.seek(f.tell()-1)
    if state == smaller_state:
        input = f.read(1)
        if input != '=' and input != '>':               
            identifier = '<'
            lt += [identifier] + [600]
        elif input == '=':
            identifier = '<='
            lt += [identifier] + [200]
        elif input == '>':
            identifier = '<>'
            lt += [identifier] + [200]
        f.seek(f.tell()-1)
    if state == larger_state:
        input = f.read(1)
        if input != '=' :
            identifier = '>'
            lt += [identifier] + [700]
        else:
            identifier = '>='
            lt += [identifier] + [200]
        f.seek(f.tell()-1)
    if state == symbols_state:
        identifier += input
        if input == '+':
            lt += [identifier] + [101]
        elif input == '-':
            lt += [identifier] + [102]
        elif input == '*':
            lt += [identifier] + [103]
        elif input == '/':
            lt += [identifier] + [113]
        elif input == ':':
            input = f.read(1)
            if input == '=':
                identifier = ':='
                lt += [identifier] + [104]
            else:
                error("Syntax error")
        elif input == ',':
            lt += [identifier] + [105]
            return lt
        elif input == ';':
            lt += [identifier] + [106]
        elif input == '(':
            lt += [identifier] + [107]
        elif input == ')':
            lt += [identifier] + [108]
        elif input == '[':
            lt += [identifier] + [109]
        elif input == ']':
            lt += [identifier] + [110]
        elif input == '{':
            lt += [identifier] + [111]
        elif input == '}':
            lt += [identifier] + [112]                   
    if state == comment_state:
        input = f.read(1)
        if input =='':
            error("The comments are not closed")
        else:
            while input != '#':
                input = f.read(1)
            state = starting_state
            return lex()
    if state == end_state:
        return 'EOF'
    return lt
    

######################
#Syntaktikos Analytis#
######################
def yacc():
    global fileLine
    global quad_identifier
    quad_identifier = 0
    global quad_final
    quad_final = []
    global keywords 
    global token
    def program():
        global token
        if token[0] == 'program':
            token = lex()
            id = token[0]
            if ID(token) == True:
                token = lex()
                block(id)
                genquad('halt','','','')
                genquad('end_block',id,'','')
            else:
                error("Expected an ID")
            
        else:
            error("Expected 'program'")
        if token[0] == '.':
            print("The lexical and synxtax analysis were correct")
        return
        
    def block(name):
        global token  
        declarations()
        subprograms()
        genquad('begin_block',name,'','')
        statements()
        return
        
    def declarations():
        global token
        while token[0] == 'declare':
            varlist()
            if token[0] == ';':
                token = lex()
            else:
                error("Expected ';'")
        return
        
    def varlist():
        global token
        token = lex()
        if ID(token) == True:
            token = lex()
            while token[0] == ',':
                token = lex()
                if ID(token[0]) == True:
                    token = lex()
                else:
                    error("Expected ID")
        return
        
    def subprograms():
        global token
        while token[0] == 'function' or token[0] == 'procedure':
            token = lex()
            subprogram()
            genquad('end_block',name,'','')
        return
        
    def subprogram(): 
        global token
        if token[0] == 'function':
            if ID(token):
                if token[0] == '(':
                    token = lex()
                    formalparlist()
                    if token[0] == ')':
                        token = lex()
                        block()
                    else:
                        error("Expected ')'")
                else:
                    error("Expected '('")
        if token[0] == 'procedure':
            if ID(token):
                if token[0] == '(':
                    token = lex()
                    formalparlist()
                    if token[0] == ')':
                        token = lex()
                        block()
                    else:
                        error("Expected ')'")
                else:
                    error("Expected '('")
        return
        
    def formalparlist():
        global token
        formalparitem()
        while token[0] == ',':
            token = lex()
            if token[0]== 'in' or token[0]=='inout':
                formalparitem()
            else:
                error("Expected 'in' or 'inout'")
        return
        
    def formalparitem():
        global token
        if token[0] == 'in':
            token = lex()
            if ID(token):
                token = lex()
                #genquad(par,a,CV,'')
                #genquad(par,b,REF,'')
                #genquad(call,assign_v,'','')
                return
            else:
                error("Expected id")       
        elif token[0] == 'inout':
            token = lex()
            if ID(token):
                token=lex()
                #genquad(par,a,CV,'')
                #genquad(par,b,REF,'')
                #genquad(call,assign_v,'','')
                return
            else:
                error("Expected id")
        else:
            error("Expected 'in' or 'inout'")
            #genquad(par,a,CV,'')
            #genquad(par,b,REF,'')
            w = newtemp()
            #genquad(par,w,RET,'')
            #genquad(call,assign_v,'','')
        return    
        
    def statements():
        global token
        if token[0] == ';':
            token= lex()
            return
        elif token[0] == '{':
            token = lex()
            statement()
            while token[0] == ';':
                token = lex()
                statement()
            if token[0]=='}':
                token = lex()
                return
            else:
                error("Expected '}'")       
        elif token[0] == '}':
            token = lex()
            statement()
            if token[0] == ';':
                token=lex()
            else:
                error("Expected ';'")
        return
        
    def statement():
        global token
        flag = False
        for i in keywords:
            if token[0] == i[0]:
                flag = True
        if flag == False:
            assignStat()
        elif token[0] == 'if':    
            ifStat()
        elif token[0] == 'while':    
            whileStat()
        elif token[0] == 'switch':
            switchStat()
        elif token[0] == 'forcase':
            forcaseStat()
        elif token[0] == 'incase':    
            incaseStat()
        elif token[0] == 'call':
            callStat()
        elif token[0] == 'return':
            returnStat()
        elif token[0] == 'input':
            inputStat()
        elif token[0] == 'print':
            printStat()
        return
        
    def assignStat():
        global token
        global quad_final
        if ID(token):
            b = token[0]
            token = lex()
            if token[0] == ':=':
                token = lex()
                A = expression()
                genquad(':=',A,'',b)
            else:
                error("Expected ':='")
        return 
        
    def ifStat():
        global token
        token = lex()
        if token[0] == '(':
            token=lex()
            B = condition()
            if token[0] == ')':
                token = lex()
                backpatch(B[0],nextquad())
                statements()
                ifList = makelist(nextquad())
                genquad('jump','','','')
                backpatch(B[1],nextquad())
                elsepart()
                backpatch(ifList,nextquad())
            else:
                error("Expected ')'")
        else:
            error("Expected '('")
        return

    def elsepart():
        global token
        if token[0]=='else':
            token = lex()
            statements()
        return
        
    def whileStat():
        global token
        token = lex()
        if token[0] == '(':
            token=lex()
            Bquad = nextquad()
            B = condition()
            if token[0] == ')':
                backpatch(B[0],nextquad())
                token = lex()
                S = statements()
                genquad('jump','','',Bquad)
                backpatch(B[1],nextquad())
            else:
                error("Expected ')'")
        else:
            error("Expected '('")
        return 
        
    def switchcase():
        global token
        token=lex()
        while token[0] == 'case':
            token=lex()
            if token[0] == '(':
                token=lex()
                condition()
                if token[0] == ')':
                    statements()
                else:
                    error("Expected ')'")
            else:
                error("Expcted '('")
        if token[0] == 'default':
            token=lex()
            statements()
        return
        
    def forcaseStat():
        global token
        token=lex()
        p1Quad = nextquad()
        while token[0] == 'case':
            token=lex()
            if token[0] == '(':
                token=lex()
                condition()
                backpatch(cond.true.nextquad())
                if token[0] == ')':
                    statements()
                    genquad('jump','','',p1Quad)
                    backpatch(cond.false,nextquad())
                else:
                    error("Expected ')'")
            else:
                error("Expcted '('")
        if token[0] == 'default':
            token=lex()
            statements()
        return
        
    def incaseStat():
        global token
        token=lex()
        while token[0] == 'case':
            token=lex()
            w = newtemp()
            p1Quad = nextquad()
            genquad(':=',1,'',w)
            if token[0] == '(':
                token=lex()
                condition()
                backpatch(cond.true.nextquad())
                genquad(':=',0,'',w)
                if token[0] == ')':
                    statements()
                    backpatch(cond.false.nextquad())
                else:
                    error("Expected ')'")
            else:
                error("Expcted '('")
        genquad('=',w,0,p1Quad)
        return
        
    def returnStat():
        global token
        token=lex()
        if token[0]=='(':
            token=lex()
            A = expression()
            genquad('retv',A,'','')
            if token[0] == ')':
                token = lex()
            else:
                error("Expected ')'")
        else:
            error("Expcted '('") 
        return A
        
    def callStat():
        global token
        token=lex()
        if ID(token):
            if token[0]=='(':
                token=lex()
                actualparlist()
                if token[0] == ')':
                    token = lex()
                else:
                    error("Expected ')'")
            else:
                error("Expcted '('") 
        return
        
    def printStat():
        global token
        token=lex()
        if token[0]=='(':
            token=lex()
            E = expression()
            if token[0] == ')':
                token = lex()
                genquad('out',E,'','')
            else:
                error("Expected ')'")
        else:
            error("Expcted '('") 
        return
        
    def inputStat():
        global token
        if token[0]=='input':
            token=lex()
            if token[0]=='(':
                token=lex()
                if ID(token) == True:
                    input_id = token[0]
                    token = lex()
                    if token[0] == ')':
                        token = lex()
                        #print(genquad())
                        genquad('inp', input_id, '','')
                    else:
                        error("Expected ')'")
            else:
                error("Expcted '('") 
        return
        
    def actualparlist():
        global token
        actualparitem()
        while token[0] == ',':
            token = lex()
            if token[0]== 'in' or token[0]=='inout':
                actualparitem()
            else:
                error("Expected 'in' or 'inout'")
        return
            
    def actualparitem():
        global token
        if token[0] == 'in':
            token = lex()
            expression()       
        elif token[0] == 'inout':
            token = lex()
            if ID(token):
                token=lex()
            else:
                error("Expected id")
        else:
            error("Expected 'in' or 'inout'")
        return
        
    def condition():
        global token
        BTrue = []
        BFalse = []
        B1 = boolterm()
        BTrue = B1[0]
        BFalse = B1[1]
        while token[0]=='or':       
            token=lex()
            backpatch(BFalse, nextquad())
            B2 = boolterm()
            BTrue = merge(BTrue, B2[0])
            BFalse = B2[1]
        return [BTrue,BFalse]
        
    def boolterm():
        global token
        BTrue2 = []
        BFalse2 = []
        Q1 = boolfactor()
        BTrue2 = Q1[0]
        BFalse2 = Q1[1]
        while token[0]=='and':
            token=lex()
            backpatch(BTrue2, nextquad())
            Q2 = boolfactor()
            BFalse2 = merge(BFalse2, Q2[1])
            BTrue2 = Q2[0]
        return [BTrue2,BFalse2]
        
    def boolfactor():
        global token
        RTrue = []
        RFalse = []
        if token[0] == 'not':
            token=lex()
            if token[0] == '[':
                token = lex()
                B = condition()
                #RTrue = B[0]
                #RFalse = B[1]
                if token[0] == ']':
                    token = lex()
                    return [B[1],B[0]]
                else:
                    error("Expected ']'")
            else:
                error("Expected '['")
        elif token[0] == '[':
            token = lex()
            G = condition()
            #RTrue = B[0]
            #RFalse = B[1]
            if token[0] == ']':
                token = lex()
                return [G[0],G[1]]
            else:
                error("Expected ']'")
        else:
            E1 = expression()
            relop = REL_OP()
            E2 = expression()
            RTrue = makelist(nextquad())
            genquad(relop,E1,E2,'')
            RFalse = makelist(nextquad())
            genquad('jump','','','')
        return [RTrue,RFalse]
        
    def expression():
        global token
        optimalSign()
        A = term()    
        while token[0] == '+' or token[0] == '-':
            C = ADD_OP()
            B = term()
            w = newtemp()
            genquad(C,A,B,w)
            A = w
        return A
        
    def term():
        global token
        A = factor()
        while token[0] == '*' or token[0]=='/':
            C = MUL_OP()
            B = factor()
            w = newtemp()
            genquad(C,A,B,w)
            A = w
        return A
        
    def factor():
        global token
        if token[0] == '(':
            token = lex()
            A = expression()
            if token[0] == ')':
                token = lex()
            else:
                error("Expected ')'")
            F = A
            return F
        elif ID(token):
            name = token[0]
            token = lex()
            B = idtail()
            #if B == str.kati
                       
            return name
        else:
            return INTEGER()
        
        
    def idtail():
        global token
        if token[0] == '(':
            token=lex()
            actualparlist()
            if token[0] == ')':
                token = lex()
                #return 'kati'
            else:
                error("Expected ')'")
        return
        
    def optimalSign():
        global token
        if token[0] == '+' or token[0] == '-':
            token = lex()
            ADD_OP()
        return
        
    def REL_OP():
        global token
        if token[0] == '=' or token[0] == '<=' or token[0] == '>=' or token[0] == '>' or token[0] == '<' or token[0] == '<>':
            rel_opp =token[0]
            token = lex()
        else:
            error("Expected realtional operator")
        return rel_opp
        
    def ADD_OP():
        global token
        if token[0] =='+' or token[0] == '-':
            add_opp = token[0]
            token = lex()
        else :
            error("Expected '+' or '-'")
        return add_opp

    def MUL_OP():
        global token
        if token[0] == '*' or token[0] == '/':
            mul_opp = token[0]
            token = lex()
        else:
            error("Expected '*' or '/'")
        return mul_opp
        
    def INTEGER():
        global token
        if token[0].isdigit():
            return True
        return False

    def ID(unit): #[a-zA-Z][a-zA-Z0-9]* The first char must be a char
        global token
        global keywords
        for i in keywords:
            if token[0] not in i[0] and token[0].isalnum():
                return True
            else:
                return False

    def error(x):
        global token
        print("Found: ",token)
        print("in Line " + str(fileLine))
        print(x)
        sys.exit()       

####################
#Endiamesos Kwdikas#
####################

    
    global temp_counter
    temp_counter = 0

    def nextquad():
        global quad_identifier
        return quad_identifier
        
    def genquad(op,x,y,z):
        global quad_identifier
        quad = []
        global quad_final
        quad.append(op)
        quad.append(x)
        quad.append(y)
        quad.append(z)
        quad.append(nextquad())
        quad_identifier += 1
        quad_final.append(quad)
        return quad
        
    def newtemp():
        global temp_counter
        temp_counter += 1
        return 'T_' + str(temp_counter)
        
    def emptylist():
        emptyquad = [None]*4
        return emptyquad
        
    def makelist(x):
        xquad = [x]
        return xquad

    def merge(list1,list2):
        new_list = list1.extend(list2)
        return new_list
        
    def backpatch(list,z):
        global quad_final   
        for i in range(len(list)):            
            for j in range(len(quad_final)):
                if(list[i]==quad_final[j][0] and quad_final[j][3]=='_'):
                    quad_final[j][3] = z
        return
    token = lex()
    program()
    return
        
def intFile():
    #global quad_final
    file = open('intfile.int', 'w')
    for i in quad_final:
        file.write(str(i[4]) + '|' + str(i[0])  + ','  + str(i[1]) + ','  + str(i[2]) + ','  + str(i[3]) + '\n')
    file.close

#def cfile():
#    global quad_final
#    file2 = open('cfile.int', 'w')
 #   for i in range(len(quad_final)):
 #       file2.wrire(quad_final[i])
   # for j in range(len(quad))
   #    

f = open(sys.argv[1])
yacc()
intFile()
#cfile()





##########################
#PARAGOGI PINAKA SYMBOLWN#
##########################

#firstScope = None

#class Entity():
#	def init(test):
#		test.name = ''					
#		test.type = ''	
#		
#		test.variable = test.Variable()
#        test.function = test.Function()
#		test.constant = test.Constant()
#		test.parameter = test.Parameter()
#		test.tempVar = test.TempVar()
#		
#	class Variable:
#		def init(test):
#            test.name = ''
#			test.type = 'Int'
#			test.offset = 0
#           
#	class Function:					
#		def init(test):
#            test.name = ''
#			test.type = 'Int'				
#			test.startQuad = 0					
#			test.argumentList = []
#            test.frameLength = 0       
#	
#    class Constant:
#		def init(test):
#            test.name = ''
#			test.value = ''	
#	
#    class Parameter:
#		def init(test):
#           test.name = ''
#			test.parMode = 0				
#			test.offset = 0	
#			
#	class TempVar:
#		def init(test):	
#           test.name = ''
#			test.offset = 0
            
#class Scope():
#	def init(test):						
#		test.entityList = []				
#		test.nestingLevel = 0					
		
#class Argument():
#	def init(test):	
#		test.type = 'Int'	
#		test.parMode = 0
        
#def new_scope():
#    global firstScope
    
#    freshScope = Scope()
    
#    if(firstScope == None):
#        freshScope.nestingLevel = 0
#    else:
#        freshScope.nestingLevel = firstScope.nestingLevel + 1
    
#def delete_scope():
#    global firstScope
    
#def new_entity(new):
#    global firstScope
    
#    firstScope.entityList.append(new)
    
#def new_argument(new):
#    global firstScope
    
#    firstScope.entityList[-1].function.argumentList.append(new)
    
#def search_entity():
#    global firstScope