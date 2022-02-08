
import re

def getNumberDataType(string):
    if type(string)!=str:
        string= str(string)
    
    if isFloat(string):
        return float(string)
    elif string.isdigit():
        return int(string)
    raise ValueError("No es un número")
def isFloat(string):
    if type(string)!=str: 
        string= str(string)        
        
    match= re.search("\d*\.\d*[e+]*\d+", string.replace("-",""))
    if match:
        return True
    return False   
def printExpression(left, operator, right, result):
    print(f"{left} {operator} {right} = {result}")    
# Operaciones aritmeticas
def Sumar(operando1,operando2):
    operando1= getNumberDataType(operando1)  
    operando2= getNumberDataType(operando2)
    
    suma=operando1+operando2
    printExpression(operando1,"+",operando2,suma)
    return suma
def Multiplicar(operando1,operando2):
    factor= getNumberDataType(operando1)  
    factor2= getNumberDataType(operando2)
    
    producto= factor * factor2
    printExpression(operando1,"*",operando2, producto)
    return producto
def Restar(operando1,operando2):
    minuendo= getNumberDataType(operando1) 
    substraendo= getNumberDataType(operando2)
    
    diferencia= minuendo - substraendo
    printExpression(operando1,"-",operando2, diferencia)
    return diferencia
def Dividir(operando1,operando2):
    dividendo= getNumberDataType(operando1) 
    divisor= getNumberDataType(operando2)
    
    cociente= dividendo / divisor
    printExpression(operando1,"/",operando2, cociente)
    return cociente
# Precedencia
precedence={
    "operador": {
        "*":{"precedence":3, "associativity":"left"},
        "/":{"precedence":3, "associativity":"left"},
        "+":{"precedence":2, "associativity":"left"},
        "-":{"precedence":2, "associativity":"left"},
    }
}
def isPrecedenceLower(element, lastOperator):
    precedence_operator= precedence["operador"][element]["precedence"] 
    precedence_last_operator= precedence["operador"][lastOperator]["precedence"]
    
    if precedence_operator <= precedence_last_operator:
        return True
    return False
def isOperator(element):
    if precedence["operador"].get(element):
        return True    
    return False
def isBracket(element):
    if element in ["(",")"]:
        return True
    return False
def get_rpn(elements): 
    out= []
    operadores= []    
    for element in elements: 
        if isOperator(element): 
            if len(operadores)>0:          
                lastOperator= operadores[-1]                                                
                if not isBracket(lastOperator) and isPrecedenceLower(element, lastOperator): # True si el operator(element) tiene una procedencia mayor o igual al último operador de la lista de operadores
                    operadores.pop()
                    out.append(lastOperator)                    
                    operadores.append(element)
                else:
                    operadores.append(element)  
            else:                       
                operadores.append(element)        
        elif isBracket(element):
            operadores.append(element)
        else:
            out.append(element) 
            
    if "(" in operadores: operadores.remove("(")            
    if ")" in operadores: operadores.remove(")")
        
    out.extend(operadores[::-1] )  
    return out
def get_index_first_operator(elements):
    for index, element in enumerate(elements):
        if isOperator(element):
            return index
    return -1
def operate_expression(rpn)-> "different values":
    while len(rpn)>2:
        index= get_index_first_operator(rpn)        
        right_operand= rpn[index - 2]
        left_operand= rpn[index - 1]
        operador= rpn[index]
                
        if operador=="+":
            resultado= Sumar(right_operand,left_operand)
        if operador=="*":
            resultado= Multiplicar(right_operand,left_operand)
        if operador=="/":
            resultado= Dividir(right_operand,left_operand)
        if operador=="-":
            resultado= Restar(right_operand,left_operand)           

        left= rpn[0:index - 2]
        righ= rpn[index + 1:]
        left.append(resultado)
        left.extend(righ)
        rpn= left.copy()    
    return resultado   
def parser(string) -> "list of strings":
    """
    :TODO: Falta someter al regex a más pruebas
    De un String con una expresiones matemática, devuelve una lista de los operadores y operandos que la componen.
    """
    tokens=[]
    index=0

    match= re.search("^-\d+\.\d+[e+]*\d+|^-\d+", string) # Número negativo # Solo puede ser la primero expresión
    if match: # Número 
        init, end= match.span()
        index= end
        tokens.append(match.group())        
    matchs= re.findall("\d*\.\d*[e+]*\d+|\d+|[^0-9]", string[index:]) # Solo números positivos
    tokens.extend(matchs)     
    return tokens
def isExpression(string):
    elements=parser(string)
    if len(elements)>2:
        return True
    return False
    
    
    
    
    
    
    
    
    




    



