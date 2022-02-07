
import re

def isFloat(string):
    tokens= re.search("-*\d+\.\d+(e\+\d+)*", string)
    """
    -* es para que pueda tener un signo negativo o no
    \d+\.\d+ tiene que tener un  o más número, seguido de un punto y un número decimal
    (e\+\d+)* Si tiene e seguido de un signo + y un número entero es float como número cientifico
    """
    if tokens:
        return True
    return False   
def isScientificNumber(string):
    pass

# Operaciones aritmeticas
def Suma(valor1,valor2):
    suma=int(float(valor1))+int(float(valor2))
    print(valor1,valor2,sep="+",end=f"={suma}\n")
    return suma
def Multiplicar(factor, factor2):
    producto= int(float(factor)) * int(float(factor2))
    print(factor,factor2,sep="*",end=f"={producto}\n")
    return producto
def Restar(minuendo,substraendo):
    diferencia= int(float(minuendo)) - int(float(substraendo))
    print(minuendo,substraendo,sep="-",end=f"={diferencia}\n")
    return diferencia
def Dividir(dividendo,divisor):
    cociente= int(float(dividendo)) / int(float(divisor))
    print(dividendo,divisor,sep="/",end=f"={cociente}\n")
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
def operate_expression(rpn):
    while len(rpn)>2:
        index= get_index_first_operator(rpn)        
        right_operand= rpn[index - 2]
        left_operand= rpn[index - 1]
        operador= rpn[index]
                
        if operador=="+":
            resultado= Suma(right_operand,left_operand)
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
def get_token(string):
    """
    :TODO: Falta someter al regex a más pruebas
    De un String con una expresión matemática, devuelve una lista de los operandos y
    operadores que la componen.
    Obtiene: Decimales, enteros, números científicos tanto negativos y positivos, y operadores.
    """
    #2998.6666666666665/2
    tokens= re.findall("-*\d*\.\d*[e+]*\d+|-*\d+|[^0-9]", string)
    return tokens   
    
    
    
    
    
    
    
    
    
    
    




    



