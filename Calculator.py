import enum
import re


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

# Funciones principales
def get_rpn(tokens:list)-> list: 
    """
    Convierte una expresion matemática de notación infija en una expresión en notación polaca inversa.
    """
    elements=tokens
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
def operate_rpn(rpn:list):
    """
    Evalua una expresión de notación polaca inversa.
    """
    convert_stringLy_to_numberLy(rpn) 
    while len(rpn)>2:
        print(rpn)
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
def separator2(string):
    """""
    Separador de expresiones con aridad 2
    """
    number= "([-+]*\d+\.\d+e[+-]\d+|[-+]*\d+\.\d+|[-+]*\d+)"
    operator= "[\^*%\/]"
    #regex= re.compile(fr"(([-+]?{number})?[^0-9]([-+]?{number}(?![*\^\/]))?)")
    regex= re.compile(fr"(((?<=[^0-9]|\d)[+-])?{number}[^0-9][+-]?{number}[^0-9]?)")
    
    groups= ["".join(group[0]) for group in regex.findall(string)]
    
    match=[] 
    for element in groups[:]:
        if count_operators(element)>=1:
            match.append(element) 
        if element=="":
            groups.remove(element)
    
    for i in match:
        operands= separator(i)
        
        index= groups.index(i)
        left= groups[0:index]
        right= groups[index+1:]
        left.extend(operands)
        left.extend(right)
        groups= left.copy() 
        
    for element in groups[:]:
        if element=="":
            groups.remove(element)
    return groups
    
def separator(string:str)->list:
    """
    Devuelve una lista con los elementos separados por operadores matemáticos.
    :return: 2+3*4 -> ['2','+','3','*','4']
    """
    
    regex= re.compile(r"\b(?<!e)[^0-9.](?!\d+\/)")

    # Encuentra en el limite de un «caracter de palabra» un «no digito» que no sea punto y no esté precedido por una e
    # \b significa límite de palabra.
    # (?<!e) significa que no se puede encontrar la letra e
    # [^0-9.] significa que no se puede encontrar un número ni un punto
    operands= regex.split(string)
    operators= regex.findall(string)

    operators.reverse()
    merge=[]
    for num in operands:
        merge.append(num)
        if len(operators)>0:
            op= operators.pop()
            merge.append(op)
    
    # regex= re.compile(r"([-+]\d*(\.\d*e[+-]\d*|\.\d*)?)")
    # # Elementos que tienen más de un operador.
    # match=[] 
    # for element in merge:
    #     if count_operators(element)>1:
    #         match.append(element)    
    
    # for i in match:
    #     operands= ["".join(group[0]) for group in regex.findall(i)]
        
    #     index= merge.index(i)
    #     left= merge[0:index]
    #     right= merge[index+1:]
    #     left.extend(operands)
    #     left.extend(right)
    #     merge= left.copy()                                   
    
    return merge

def operate_expression(string,print_result=True):
    tokens= separator2(string)
    rpn= get_rpn(tokens)
    result= operate_rpn(rpn)
    result= simplify_result(result)
    if print_result:
        print(f"{string} = {result}")
    return result

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
    try:
        potencia= base ** exponente
        printExpression(base,"^",exponente, potencia)
        if type(potencia)==complex:
            return potencia.real
        return potencia
    except OverflowError:
        return "Result too large"
def Resto(operando1,operando2):
    # https://en.wikipedia.org/wiki/Modulo_operation
    dividendo= operando1
    divisor= operando2
    resto= dividendo % divisor
    printExpression(dividendo,"%",divisor, resto)
    return resto

# Funciones auxiliares 
def getNumberDataType(string):       
    if isFloat(string) or isCientific(string):
        return float(string)
    elif isInterger(string):
        return int(string)
    raise ValueError("No es un número")
def isInterger(string):
    #match= re.search("^"+intergerRex+"$", string)
    match= re.search("[-+]*\d+", string)
    if match:
        return True
    return False
def isCientific(string):
    #match= re.search(isCientificRex+"$", string.replace("-",""))
    match= re.search("[-+]*\d+\.\d+e[+-]\d+", string)
    if match:
        return True
    return False     
def isFloat(string): 
    #match= re.search(floatRex+"$", string)
    match= re.search("[-+]*\d+\.\d+", string)
    if match:
        return True
    return False   
def printExpression(left, operator, right, result):
    #print(f"{left} {operator} {right} = {result}")  
    pass
def isOperator(element):
    if precedence["operador"].get(element):
        return True    
    return False
def isGroupingSign(element):
    if element in ["(",")", "[","]","{","}"]:
        return True
    return False
def isBracket(element):
    if element in ["(",")"]:
        return True
    return False
def isSign(element):
    if element in ["+","-"]:
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
def convert_stringLy_to_numberLy(tokens):
    for index, token in enumerate(tokens):
        if isOperator(token) or isGroupingSign(token):
            continue
        tokens[index]= getNumberDataType(token) 
    return tokens  
def simplify_result(result):
    string= str(result)
    if isFloat(string):
        if string.split(".")[1]=="0":
            return int(result)
        elif len(string.split(".")[1])=="00":
            return round(result, 2)
    elif isInterger(string):
        if len(string)>18:
            return float(result)
    return result
def count_type_of_operators(string):
    """
    Cuenta el tipo de operador que se encuentra en la expresión
    """
    operators=[]
    for element in string:
        if isOperator(element):
            operators.append(element)
    
    return len(set(operators))  
