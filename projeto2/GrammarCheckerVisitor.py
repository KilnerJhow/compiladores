# Generated from antlr4-python3-runtime-4.7.2/src/autogen/Grammar.g4 by ANTLR 4.7.2
from math import floor
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GrammarParser import GrammarParser
else:
    from GrammarParser import GrammarParser

# This class defines a complete generic visitor for a parse tree produced by GrammarParser.

'''
COMO RESGATAR INFORMAÇÕES DA ÁRVORE

Observe o seu Grammar.g4. Cada regra sintática gera uma função com o nome corespondente no Visitor e na ordem em que está na gramática.

Se for utilizar sua gramática do projeto 1, por causa de conflitos com Python, substitua as regras file por fiile e type por tyype. Use prints temporários para ver se está no caminho certo.  
"make tree" agora desenha a árvore sintática, se quiser vê-la para qualquer input, enquanto "make" roda este visitor sobre o a árvore gerada a partir de Grammar.g4 alimentada pelo input.

Exemplos:

# Obs.: Os exemplos abaixo utilizam nós 'expression', mas servem apra qualquer tipo de nó

self.visitChildren(ctx) # visita todos os filhos do nó atual
expr = self.visit(ctx.expression())  # visita a subárvore do nó expression e retorna o valor retornado na função "visitRegra"

for i in range(len(ctx.expression())): # para cada expressão que este nó possui...
    ident = ctx.expression(i) # ...pegue a i-ésima expressão


if ctx.FLOAT() != None: # se houver um FLOAT (em vez de INT ou VOID) neste nó (parser)
    return Type.FLOAT # retorne tipo float

ctx.identifier().getText()  # Obtém o texto contido no nó (neste caso, será obtido o nome do identifier)

token = ctx.identifier(i).IDENTIFIER().getPayload() # Obtém o token referente à uma determinada regra léxica (neste caso, IDENTIFIER)
token.line      # variável com a linha do token
token.column    # variável com a coluna do token
'''


# Dica: Retorne Type.INT, Type.FLOAT, etc. Nos nós e subnós das expressões para fazer a checagem de tipos enquanto percorre a expressão.
class Type:
    VOID = "void"
    INT = "int"
    FLOAT = "float"
    STRING = "char *"
    ERROR = "err"

class GrammarCheckerVisitor(ParseTreeVisitor):
    ids_defined = {} # Dicionário para armazenar as informações necessárias para cada identifier definido
    inside_what_function = "" # String que guarda a função atual que o visitor está visitando. Útil para acessar dados da função durante a visitação da árvore sintática da função.

    # Visit a parse tree produced by GrammarParser#fiile.
    def visitFiile(self, ctx:GrammarParser.FiileContext):
        return self.visitChildren(ctx)


     # Visit a parse tree produced by GrammarParser#function_definition.
    def visitFunction_definition(self, ctx:GrammarParser.Function_definitionContext):
        tyype = ctx.tyype().getText()
        name = ctx.identifier().getText()
        params = self.visit(ctx.arguments())

        print("Inside function:", name, "salvando parametros: ",tyype, params)
        self.ids_defined[name] = {'tyype': tyype, 'params': params}
        self.inside_what_function = name
        self.visit(ctx.body())
        

        return


    # Visit a parse tree produced by GrammarParser#body.
    def visitBody(self, ctx:GrammarParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#statement.
    def visitStatement(self, ctx:GrammarParser.StatementContext):

        #TODO: implementar if_statement, for_loop, body,

        print(ctx.RETURN())

        if(ctx.variable_definition()):
            print("Statement variable definition")
            self.visit(ctx.variable_definition())
        elif(ctx.variable_assignment()):
            print("Statement variable assignment")
            self.visit(ctx.variable_assignment())
        elif(ctx.expression() and not ctx.RETURN()):
            print("Statement expr")
            self.visit(ctx.expression())
        elif(ctx.RETURN()):
            ret_expr = self.visit(ctx.expression())
            ret_type = ret_expr.get('tyype')
            print("Statement ret", ret_expr)

            token = ctx.RETURN().getPayload()

            f_info = self.ids_defined.get(self.inside_what_function)
            f_type = f_info.get('tyype')

            if(ret_type != f_type):

                if(ret_type == Type.INT and f_type == Type.VOID):
                    print('ERROR: trying to return a non void expression from void function \''+self.inside_what_function+'\' in line '+str(token.line)+' and column '+str(token.column))
                elif(ret_type == Type.FLOAT and f_type == Type.VOID):
                    print('ERROR: trying to return a non void expression from void function \''+self.inside_what_function+'\' in line '+str(token.line)+' and column '+str(token.column))
                elif(ret_type == Type.STRING and f_type == Type.VOID):
                    print('ERROR: trying to return a non void expression from void function \''+self.inside_what_function+'\' in line '+str(token.line)+' and column '+str(token.column))
                elif(ret_type == Type.FLOAT and f_type == Type.INT):
                    print('WARNING: possible loss of information returning float expression from int function \''+self.inside_what_function+'\' in line '+str(token.line)+ ' and '+str(token.column))
                elif(ret_type == Type.STRING and f_type == Type.INT):
                    print('ERROR: trying to return a string expression from int function \''+self.inside_what_function+'\' in line '+str(token.line)+' and column '+str(token.column))
                elif(ret_type == Type.STRING and f_type == Type.FLOAT):
                    print('ERROR: trying to return a string expression from float function \''+self.inside_what_function+'\' in line '+str(token.line)+' and column '+str(token.column))
        elif(ctx.for_loop()):
            self.visit(ctx.for_loop())
        
        elif(ctx.if_statement):
            self.visit(ctx.if_statement())
        
        elif(ctx.body()):
            self.visit(ctx.body)
                

                #checa se o tipo de retorno bate com o tipo da função


    # Visit a parse tree produced by GrammarParser#if_statement.
    def visitIf_statement(self, ctx:GrammarParser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#else_statement.
    def visitElse_statement(self, ctx:GrammarParser.Else_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#for_loop.
    def visitFor_loop(self, ctx:GrammarParser.For_loopContext):
        print("Dentro do for loop")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#for_initializer.
    def visitFor_initializer(self, ctx:GrammarParser.For_initializerContext):
        print("Dentro do for initializer")
        if(ctx.variable_definition()):
            return self.visit(ctx.variable_definition())
        elif(ctx.variable_assignment()):
            return self.visit(ctx.variable_assignment())


    # Visit a parse tree produced by GrammarParser#for_condition.
    def visitFor_condition(self, ctx:GrammarParser.For_conditionContext):
        print("Dentro do for condition")
        if(ctx.expression()):
            return self.visit(ctx.expression())


    # Visit a parse tree produced by GrammarParser#for_step.
    def visitFor_step(self, ctx:GrammarParser.For_stepContext):
        print("Dentro do for step")
        if(ctx.variable_assignment()):
            return self.visit(ctx.variable_assignment())


    # Visit a parse tree produced by GrammarParser#variable_definition.
    def visitVariable_definition(self, ctx:GrammarParser.Variable_definitionContext):

        # print("Variable definition")
        tyype = ctx.tyype().getText()


        array_name = ''
        ret_arr_literal = []
        if(ctx.array(0) != None):
            for i in range(len(ctx.array())):
                ret_arr = self.visit(ctx.array(i))
                token = ctx.array(i).identifier().IDENTIFIER().getPayload()
                array_name = ret_arr.get('name')
                value = ret_arr.get('value')

                if(value == Type.ERROR or value == Type.VOID):
                    return
                else:

                    print("Variable name and type:", tyype, array_name)

                    self.ids_defined[array_name] = {'tyype': tyype, 'value': value}
                    
                    if(ctx.array_literal()):
                        ret_arr_literal = self.visit(ctx.array_literal(i))

                        print("Ret arr literal", ret_arr_literal)
                        if(ret_arr_literal):
                            # print("Type:", tyype)
                            # print("Type.int", Type.INT)
                            # print(tyype == Type.INT and Type.STRING in ret_arr_literal)
                            if(tyype == Type.INT and Type.FLOAT in ret_arr_literal):
                                print('WARNING: possible loss of information assigning float expression to int variable \''+array_name+ '\' in line ' + str(token.line) +' and column ' + str(token.column))
                            elif(tyype == Type.FLOAT and Type.STRING in ret_arr_literal):
                                index = ret_arr_literal.index(Type.STRING)
                                print('ERROR: trying to initialize \''+ Type.STRING +'\' expression to \''+tyype+ '\' array \''+ array_name +'\' at index ' + str(index) + ' of array literal in line '+ str(token.line) +' and column ' + str(token.column))
                            elif(tyype == Type.INT and Type.STRING in ret_arr_literal):
                                index = ret_arr_literal.index(Type.STRING)
                                print('ERROR: trying to initialize \''+ Type.STRING +'\' expression to \''+tyype+ '\' array \''+ array_name +'\' at index ' + str(index) + ' of array literal in line '+ str(token.line) +' and column ' + str(token.column))

        else:
            for i in range(len(ctx.identifier())):
                
                name = ctx.identifier(i).getText()
                print("Variable name and type:", tyype, name)
                # self.ids_defined[name] = {'tyype': tyype, 'value': None}

                ret_expr = tyype
            
            # for i in range(len(ctx.expression())):

                if(ctx.expression(i)):
                    token = ctx.identifier(i).IDENTIFIER().getPayload() # Obtém o token referente à uma determinada regra léxica (neste caso, IDENTIFIER)
                    ret_expr = self.visit(ctx.expression(i))
                    ret_type = ret_expr.get('tyype')
                    value = ret_expr.get('value')
                    print("Ret expr:", ret_expr)
                    print("Ret type:", ret_type)
                    print("Tyype:", tyype)

                    if(ret_type == Type.VOID):
                        print('ERROR: trying to assign \'void\' expression to variable \''+name+'\' in line '+str(token.line)+' and column '+str(token.column) )
                    elif(ret_type == Type.ERROR):
                        print("Continuando após o erro")
                    else:
                        if(value):
                            if(tyype == Type.INT):
                                self.ids_defined[name] = {'tyype': tyype, 'value': floor(value)}
                            else:
                                self.ids_defined[name] = {'tyype': tyype, 'value': value}

                            print("Expr return:", ret_expr)

                            if(ret_type == None):
                                print("ERRO: tipo vazio")

                            elif(ret_type != tyype):

                                if(tyype == Type.INT and ret_type == Type.FLOAT):
                                    print('WARNING: possible loss of information assigning float expression to int variable \''+ str(ctx.identifier(i).getText())+ '\' in line ' + str(token.line) +' and column ' + str(token.column))
                                elif(tyype == (Type.INT or Type.FLOAT) and ret_type == Type.STRING):
                                    print('ERROR: trying to assign \''+ Type.STRING +'\' expression to variable \''+ str(ctx.identifier(i).getText())+'\' in line '+ str(token.line) + ' and column '+ str(token.column))
                                # elif(tyype == Type.STRING and ret_expr == (Type.INT or Type.FLOAT)):
                                #     print('ERROR: trying to assign \''+ ret_expr +'\' expression to variable \''+ str(ctx.identifier(i).getText())+'\' in line '+ str(token.line) + ' and column '+ str(token.column))
                else:
                    self.ids_defined[name] = {'tyype': tyype, 'value': None}


    # Visit a parse tree produced by GrammarParser#variable_assignment.
    def visitVariable_assignment(self, ctx:GrammarParser.Variable_assignmentContext):
        
        #TODO implementar os operadores de =, +=, -=, *=, /=, ++ e --

        print("Visitando variable assignment")
        name = ''
        index = ''
        token = ''
        if(ctx.array()):
            print("Array")
            ret_arr = self.visit(ctx.array())
            name = ret_arr.get('name')
            index = ret_arr.get('value')
            print("No assignment nome", name, "valor", index)
            token = ctx.array().identifier().IDENTIFIER().getPayload()
            if(index == Type.ERROR):
                return
        else:
            name = ctx.identifier().getText()
            token = ctx.identifier().IDENTIFIER().getPayload()

        
        var_info = self.ids_defined.get(name)
        if(var_info == None):
            token = ctx.identifier().IDENTIFIER().getPayload()
            print('ERROR: undefined variable \''+ name + '\' in line ' + str(token.line) +  ' and column ' + str(token.column))
        else:
            var_type = var_info.get('tyype')
            var_value = var_info.get('value')
            ret_expr = self.visit(ctx.expression())
            ret_type = ret_expr.get('tyype')
            ret_value = ret_expr.get('value')
            print("Inside variable assignment, name '", name, "' type", var_type, 'ret type', ret_expr)
            if(ret_type != Type.ERROR):
                if(ret_type == Type.VOID):
                    print('ERROR: trying to assign \''+ Type.VOID +'\' expression to variable \''+ name+'\' in line '+ str(token.line) + ' and column '+ str(token.column))
                elif(var_type == Type.INT and ret_type == Type.FLOAT):
                    print('WARNING: possible loss of information assigning float expression to int variable \''+name+ '\' in line ' + str(token.line) +' and column ' + str(token.column))
                elif(var_type == (Type.INT or Type.FLOAT) and ret_type == Type.STRING):
                    print('ERROR: trying to assign \''+ Type.STRING +'\' expression to variable \''+name+'\' in line '+ str(token.line) + ' and column '+ str(token.column))
                # elif(var_type == Type.STRING and ret_type == (Type.INT or Type.FLOAT)):
                #     print("ERRO: tipos incompativeis")
                else:
                    value = None
                    if(ctx.OP.text == '='):
                        value = ret_value
                    elif(ctx.OP.text == '-='):
                        value = var_value - ret_value
                    elif(ctx.OP.text == '+='):
                        value = var_value + ret_value
                    elif(ctx.OP.text == '*='):
                        value = var_value * ret_value
                    elif(ctx.OP.text == '/='):
                        value = var_value / ret_value
                    elif(ctx.OP.text == '++'):
                        value = var_value + 1
                    elif(ctx.OP.text == '--'):
                        value = var_value - 1
                    else:
                        print('ERROR: operador não reconhecido')
                    
                    if(ret_type == Type.INT):
                        value = floor (value)
                    self.ids_defined[name] = {'tyype': var_type, 'value': value}



    # Visit a parse tree produced by GrammarParser#expression.
    def visitExpression(self, ctx:GrammarParser.ExpressionContext):

        # retorno de expression: {'tyype':, 'value':}

        print("Visitando expression")
        if(ctx.integer()):
            return self.visit(ctx.integer())
        elif(ctx.floating()):
            return self.visit(ctx.floating())
        elif(ctx.string()):
            return self.visit(ctx.string())
        elif(ctx.identifier()):
            return self.visit(ctx.identifier())
        elif(ctx.array()):
            ret_arr = self.visit(ctx.array())
            arr = self.ids_defined.get(ret_arr.get('name'))
            if(arr == None):
                token = ret_arr.IDENTIFIER().getPayload()
                print('ERROR: undefined array \''+ret_arr.getText()+'\' in line ' + str(token.line) + ' and column ' +str(token.column))
                return {'tyype': Type.ERROR, 'value': None}
            else:
                return {'tyype': arr.get('tyype'), 'value': arr.get('value')}

        elif(ctx.expression(1)):
            print("3 filhos")
            ret_info_expr1 = self.visit(ctx.expression(0))
            ret_info_expr2 = self.visit(ctx.expression(1))


            print("Ret info expr1:", ret_info_expr1)
            print("Ret info expr2:", ret_info_expr2)

            ret_expr1 = ret_info_expr1.get('tyype')
            ret_expr2 = ret_info_expr2.get('tyype')

            op_type = ctx.OP.text
            ret_tyype = ret_expr1
            print('Operador:', ctx.OP.text)
            # if(ctx.OP.type == '+'):
                # print("Operador mais")

            #TODO implementar os operadores de >, >=, <=, <, !=, ==

            if((ret_expr1 == (Type.FLOAT or Type.INT) and ret_expr2 == Type.STRING) and (ret_expr1 == Type.STRING  and ret_expr2 == (Type.FLOAT or Type.INT))):
                print("ERRO: tipos incompativeis")
                return {'tyype': None,'value': Type.ERROR}
            elif((ret_expr1 == Type.FLOAT and ret_expr2 == Type.INT) or (ret_expr1 == Type.INT and ret_expr2 == Type.FLOAT)):
                if(op_type == '*' or op_type == '/'):
                    ret_tyype = Type.FLOAT
                elif(op_type == '+' or op_type == '-'):
                    ret_tyype = Type.INT
                
            elif((ret_expr1 == None) or (ret_expr2 == None)):
                print("ERRO: tipo vazio ou variavel indefinida")
                return {'tyype': Type.ERROR,'value': None}
            
            value_expr1 = ret_info_expr1.get('value')
            value_expr2 = ret_info_expr2.get('value')

            if(value_expr1 != None and value_expr2 != None):
                if(op_type == '*'):
                    return {'tyype': ret_tyype, 'value': value_expr1 * value_expr2}
                elif(op_type == '/'):
                    return {'tyype': ret_tyype, 'value': value_expr1 / value_expr2}
                elif(op_type == '+'):
                    return {'tyype': ret_tyype, 'value': value_expr1 + value_expr2}
                elif(op_type == '-'):
                    return {'tyype': ret_tyype, 'value': value_expr1 - value_expr2}
            else:
                return {'tyype': ret_tyype, 'value': None}


        elif(ctx.getChildCount() == 2): #OP expression
            print("2 filhos")

            ret_expr = self.visit(ctx.expression(0))
            if(ret_expr == None):
                print('ERRO: tipo vazio')
                return {'tyype': Type.ERROR,'value': None}
            elif(ret_expr == Type.ERROR):
                return {'tyype': Type.ERROR,'value': None}
            else:
                if(ctx.OP.text == '-'):
                    ret_expr['value'] = -ret_expr.get('value')
                    return ret_expr
                else:
                    return ret_expr
        elif(ctx.getChildCount() == 3 and ctx.expression(1) == None):
            print("parenteses")
            return self.visit(ctx.expression(0)) 
        
        elif(ctx.function_call()):
            ret_f = self.visit(ctx.function_call())

            if(ret_f == Type.VOID):
                return {'tyype': Type.VOID,'value': None}
            elif(ret_f == Type.ERROR):
                return {'tyype': Type.ERROR,'value': None}



    # Visit a parse tree produced by GrammarParser#array.
    def visitArray(self, ctx:GrammarParser.ArrayContext):

        #retorno de array: {'name': name, 'value': valor do indice}
        print("Visitando array")
        token = ctx.identifier().IDENTIFIER().getPayload() # Obtém o token referente à uma determinada regra léxica (neste caso, IDENTIFIER)
        name = ctx.identifier().getText()
        ret_expr = self.visit(ctx.expression())
        ret_type = ret_expr.get('tyype')
        index_value = ret_expr.get('value')

        if(ret_expr == Type.ERROR):
            return {'name': name, 'value': Type.ERROR}
        elif(ret_expr == Type.VOID):
            print('ERROR: trying to assign \'void\' expression to variable \'' + name + '\'in line '+ str(token.line)+ ' and column ' + str(token.column))
            return {'name': name, 'value': Type.VOID}
        else:
            print("Retorno do tipo do array:", ret_type, "valor:", index_value)
            if(index_value < 0):
                print('ERROR: array expression must be an positive integer, but it is ' + str(index_value) + ' in line '+ str(token.line)+' and column ' + str(token.column))
                index_value = Type.ERROR
            elif(ret_type != Type.INT):
                print('ERROR: array expression must be an integer, but it is ' + ret_type + ' in line '+ str(token.line)+' and column ' + str(token.column))
                index_value = Type.ERROR
            
            return {'name': name, 'value': index_value}


    # Visit a parse tree produced by GrammarParser#array_literal.
    def visitArray_literal(self, ctx:GrammarParser.Array_literalContext):
        print('Visitando array literal')
        ret_arr = []
        if(ctx.getChildCount() > 0):
            for i in range(len(ctx.expression())):
                ret_expr = self.visit(ctx.expression(i))
                ret_arr.append(ret_expr.get('tyype'))
                print("Ret expr arr literal", )
            return ret_arr

        else:
            return []



    # Visit a parse tree produced by GrammarParser#function_call.
    def visitFunction_call(self, ctx:GrammarParser.Function_callContext):

        # retorno do tipo: {'tyype': tipo da funcao, 'value': erro, se houver}

        print("Visitando function call")
        f_name = ctx.identifier().getText()
        f_info = self.ids_defined.get(f_name)

        token = ctx.identifier().IDENTIFIER().getPayload()

        # print("Info Function:", f_info)
        if(f_info == None):
            print('ERROR: undefined function \''+f_name+'\' in line '+ str(token.line) + ' and column ' +str(token.column) )
            return {'tyype': None, 'value': Type.ERROR}
        else:
            f_type = f_info.get('tyype')
            f_params = f_info.get('params')
            value = ''
            for i in range(len(ctx.expression())):
                ret_expr = self.visit(ctx.expression(i))
                ret_tyype = ret_expr.get('tyype')
                
                # print("Len params:", len(f_params), "i:", i)

                if(i > (len(f_params) - 1)):
                    print('ERROR: incorrect number of parameters for function \''+f_name+'\' in line ' +str(token.line)+' and column '+str(token.column)+'. Expecting '+str(len(f_params))+', but '+str(len(ctx.expression()))+' were given')
                    return{'tyype': f_type, 'value': Type.ERROR}
                    # return Type.ERROR
                else:
                    param = f_params[i][0] #pega o i-ésimo parametro, mas apenas o tipo dele
                    # checando os tipos
                    if(param == Type.INT and ret_tyype == Type.FLOAT):
                        print('WARNING: possible loss of information assigning float expression to int expression in parameter '+ str(i) +' of function \''+f_name+'\' in line '+ str(token.line) +' and column ' + str(token.column))
                    elif(param == Type.INT and ret_tyype == Type.STRING):
                        print('ERROR: trying to assign string expression to int expression in parameter '+ str(i) +' of function \''+f_name+'\' in line '+ str(token.line) +' and column ' + str(token.column))
                        value = Type.ERROR
                        #por algum motivo param == (Type.INT or Type.FLOAT) não funciona
                        # erro
                    elif(param == Type.FLOAT and ret_tyype == Type.STRING):
                        print('ERROR: trying to assign string expression to float expression in parameter '+ str(i) +' of function \''+f_name+'\' in line '+ str(token.line) +' and column ' + str(token.column))
                        value = Type.ERROR
                        # erro
                    elif(param == Type.STRING and ret_tyype == Type.INT):
                        print('ERROR: trying to assign int expression to string expression in parameter '+ str(i) +' of function \''+f_name+'\' in line '+ str(token.line) +' and column ' + str(token.column))
                        value = Type.ERROR
                        # erro
                    elif(param == Type.STRING and ret_tyype == Type.FLOAT):
                        print('ERROR: trying to assign float expression to string expression in parameter '+ str(i) +' of function \''+f_name+'\' in line '+ str(token.line) +' and column ' + str(token.column))
                        value = Type.ERROR
                    # erro
            return {'tyype': f_type, 'value': value}
            # checando os parametros


        


    # Visit a parse tree produced by GrammarParser#arguments.
    def visitArguments(self, ctx:GrammarParser.ArgumentsContext):
        params = []
        for i in range(len(ctx.identifier())): # para cada expressão que este nó possui...
            name = ctx.identifier(i).getText() # ...pegue a i-ésima expressão
            tyype = ctx.tyype(i).getText()
            self.ids_defined[name] = {'tyype': tyype}
            params.append([tyype, name]) 
            # params[name] = {'tyype': tyype}


        return params


    # Visit a parse tree produced by GrammarParser#tyype.
    def visitTyype(self, ctx:GrammarParser.TyypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#integer.
    def visitInteger(self, ctx:GrammarParser.IntegerContext):
        # print("Payload Integer: ", ctx.INTEGER().getText())
        return {'tyype':Type.INT, 'value': int(ctx.INTEGER().getText())}


    # Visit a parse tree produced by GrammarParser#floating.
    def visitFloating(self, ctx:GrammarParser.FloatingContext):
        # print("Payload Floating: ", ctx.FLOATING().getText())
        return {'tyype':Type.FLOAT, 'value': float(ctx.FLOATING().getText())}


    # Visit a parse tree produced by GrammarParser#string.
    def visitString(self, ctx:GrammarParser.StringContext):
        # print("Payload String: ", ctx.STRING().getText())
        return {'tyype':Type.STRING, 'value': ctx.STRING().getText()}


    # Visit a parse tree produced by GrammarParser#identifier.
    def visitIdentifier(self, ctx:GrammarParser.IdentifierContext):
        # print("Identifier: ", ctx.IDENTIFIER().getText())
        var_info = self.ids_defined.get(ctx.IDENTIFIER().getText())

        if(var_info == None):
            token = ctx.IDENTIFIER().getPayload()
            print('ERROR: undefined variable \''+ ctx.IDENTIFIER().getText() + '\' in line ' + str(token.line) +' and column ' +str(token.column))
            return {'tyype': None, 'value':Type.ERROR}
        else:
            print("Retornando identifier var info", var_info)
            return var_info

