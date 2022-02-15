import re

# Precedencia
precedence={
    # https://en.wikipedia.org/wiki/Shunting-yard_algorithm
    "operador": {
        "*":{"precedence":3, "associativity":"left"},
        "/":{"precedence":3, "associativity":"left"},
        "+":{"precedence":2, "associativity":"left"},
        "-":{"precedence":2, "associativity":"left"},
        "%":{"precedence":3, "associativity":"left"},
        "^":{"precedence":4, "associativity":"Right"},
    }
}

def get_rpn(elements): 
    out= []
    operadores= []    
    for element in elements: 
        if isOperator(element): 
            if len(operadores)>0:          
                lastOperator= operadores[-1]                                                
                if not isBracket(lastOperator) and isPrecedenceLower(element, lastOperator): # True si el operator(element) tiene una procedencia menor o igual al último operador de la lista de operadores
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
def operate_expression(rpn):
    while len(rpn)>2:
        index= get_index_first_operator(rpn)        
        
        right_operand= rpn[index - 2]
        left_operand= rpn[index - 1]
        operador= rpn[index]
                
        if operador=="+":
            resultado= Sumar(right_operand,left_operand)
        elif operador=="*":
            resultado= Multiplicar(right_operand,left_operand)
        elif operador=="/":
            resultado= Dividir(right_operand,left_operand)
        elif operador=="-":
            resultado= Restar(right_operand,left_operand)  
        elif operador=="^":
            resultado= Potencia(right_operand,left_operand)
        elif operador=="%":
            resultado= Resto(right_operand,left_operand)
        else:
            raise ValueError(f"Operador no reconocido {operador}")         

        left= rpn[0:index - 2]
        righ= rpn[index + 1:]
        left.append(resultado)
        left.extend(righ)
        rpn= left.copy()    
    return resultado   
def parser(string) -> "list of strings":
    """
    :TODO: Falta someter al regex a más pruebas
    De un String con una expresion matemática, devuelve una lista de los operadores y operandos que la componen.
    """
    
    init= getFirstNegative(string)
    string= string.replace(init,"")
    
    end= getLastNegative(string)
    string= string.replace(end,"")
    
    tokens=[]
               
    matchs= re.findall("\d+\.\d+e\+\d+|\d\.\d|\d+\.\d+|\d+|[^0-9]", string) # Solo números positivos
    
    if init: tokens.append(init)
    tokens.extend(matchs) 
    if end: tokens.append(end)  
    
    convert_stringLy_to_numberLy(tokens)     
    return tokens

# Operaciones aritmeticas
def Sumar(operando1,operando2):    
    suma=operando1+operando2
    printExpression(operando1,"+",operando2,suma)
    return suma
def Multiplicar(operando1,operando2):
    factor= operando1 
    factor2= operando2
    
    producto= factor * factor2
    printExpression(factor,"*",factor2, producto)
    return producto
def Restar(operando1,operando2):
    minuendo= operando1
    substraendo= operando2
    
    diferencia= minuendo - substraendo
    printExpression(minuendo,"-",substraendo, diferencia)
    return diferencia
def Dividir(operando1,operando2):
    dividendo= operando1
    divisor= operando2
    
    cociente= dividendo / divisor
    printExpression(dividendo,"/",divisor, cociente)
    return cociente
def Potencia(operando1,operando2):
    base= operando1
    exponente= operando2
    if exponente==0:
        return 1
    if exponente==1:
        return base
    potencia= base ** exponente
    printExpression(base,"^",exponente, potencia)
    return potencia
def Resto(operando1,operando2):
    # https://en.wikipedia.org/wiki/Modulo_operation
    dividendo= operando1
    divisor= operando2
    resto= dividendo % divisor
    printExpression(dividendo,"%",divisor, resto)
    return resto

# Funciones para parsear la expresion matemática (string)
def getNumberDataType(string):        
    absoluteNumber= string.replace("-", "")
    
    if isFloat(absoluteNumber):
        return float(string)
    elif absoluteNumber.isdigit():
        return int(string)
    raise ValueError("No es un número")
def isFloat(string):    
    match= re.search("\d*\.\d*[e+]*\d+", string.replace("-",""))
    if match:
        return True
    return False   
def printExpression(left, operator, right, result):
    print(f"{left} {operator} {right} = {result}")    
def isExpression(string):
    elements=parser(string)
    if len(elements)>2:
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
def count_operators(string):
    operators=0
    for element in string:
        if isOperator(element):
            operators+=1
    eplus=string.count("e+")
    operators-=eplus
    return operators
def isPrecedenceLower(element, lastOperator):
    precedence_operator= precedence["operador"][element]["precedence"] 
    precedence_last_operator= precedence["operador"][lastOperator]["precedence"]
    
    if precedence_operator <= precedence_last_operator:
        return True
    return False
def get_index_first_operator(elements):
    for index, element in enumerate(elements):
        if isOperator(element):
            return index
    return -1
def getFirstNegative(string):
    """
    Si el primer número de la expresion es positivo, lo retorna
    """
    match= re.search("^-\d+\.\d+[e+]*\d+|^-\d+", string) # coincide con un número negativo al principio
    if match and count_operators(string) > 1: # Número 
        number= match.group()
        return number
    return ""
def getLastNegative(string):
    """
    Si el último número es negativo, lo retorna
    """
    match= re.search("-\d+\.\d+[e+]*\d+$|-\d+$", string) # coincide con un número negativo al final  
    
    if match and count_operators(string) > 1: # Número 
        number= match.group()
        return number
    return ""
def convert_stringLy_to_numberLy(tokens):
    for index, token in enumerate(tokens):
        if isOperator(token):
            continue
        tokens[index]= getNumberDataType(token) 
    return tokens  
