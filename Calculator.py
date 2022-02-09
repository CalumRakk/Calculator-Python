
import re
def getNumberDataType(string):
    if type(string)!=str:
        string= str(string)
    
    string= string.replace("-", "")
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
def Potencia(operando1,operando2):
    base=getNumberDataType(operando1)
    exponente=getNumberDataType(operando2)
    if exponente==0:
        return 1
    if exponente==1:
        return base
    potencia= base ** exponente
    printExpression(operando1,"^",operando2, potencia)
    return potencia
def Resto(operando1,operando2):
    # https://en.wikipedia.org/wiki/Modulo_operation
    dividendo= getNumberDataType(operando1)
    divisor= getNumberDataType(operando2) 
    resto= dividendo % divisor
    printExpression(operando1,"%",operando2, resto)
    return resto
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
def get_number_operators(string):
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
    De un String con una expresione matemática, devuelve una lista de los operadores y operandos que la componen.
    """
    tokens=[]
    index=0
    end= len(string)

    match= re.search("^-\d+\.\d+[e+]*\d+|^-\d+", string) # coincide con un número negativo al principio
    if match and get_number_operators(string) > 1: # Número 
        index= match.span()[1]
        tokens.append(match.group())    
    match= re.search("-\d+\.\d+[e+]*\d+$|-\d+$", string) # coincide con un número negativo al final  
    if match and get_number_operators(string) > 1: # Número 
        end= match.span()[0]
        tokens.append(match.group()) 
               
    matchs= re.findall("\d+\.\d+e\+\d+|\d\.\d|\d+\.\d+|\d+|[^0-9]", string[index:end]) # Solo números positivos
    tokens.extend(matchs)  
    # Corregido temporal:
    while True:
        if tokens.count("0")>1:
            if "0" in tokens:
                tokens.remove("0")
        break
    # end   
    return tokens
def isExpression(string):
    elements=parser(string)
    if len(elements)>2:
        return True
    return False

#:FIXME: La precedencia da error con esta expresion 0-3.3*-6. La solución fue eliminar el cero de los rpn, pero eso no parece ser una solución elegante.
