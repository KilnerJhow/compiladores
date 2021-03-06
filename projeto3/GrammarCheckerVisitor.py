# Generated from antlr4-python3-runtime-4.7.2/src/autogen/Grammar.g4 by ANTLR 4.7.2
from math import floor
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GrammarParser import GrammarParser
else:
    from GrammarParser import GrammarParser


def float_to_hex(f):
    float_hex = hex(struct.unpack('<Q', struct.pack('<d', f))[0])
    if (int(float_hex[10],16) % 2 != 0):
        if (float_hex[10] == 'f'):
            float_hex = float(math.ceil(f))
        else:
            float_hex = float_hex[:10] + hex(int(float_hex[10],16) + 1)[2] + "0000000"

    else: 
        float_hex = float_hex[:11] + "0000000"
    return float_hex



class Type:
    VOID = "void"
    INT = "int"
    FLOAT = "float"
    STRING = "char *"
    ERROR = "err"

class GrammarCheckerVisitor(ParseTreeVisitor):
    # Dicionário para armazenar as informações necessárias para cada identifier definido
    ids_defined = {}
    # String que guarda a função atual que o visitor está visitando.
    # Útil para acessar dados da função durante a visitação da árvore sintática da função.
    inside_what_function = ""
    inside_statement = False
    stack_statement = [0]
    count = 0
    global_variable = False
    constant = True
    output = open("output.ll", "w")
    
    # Visit a parse tree produced by GrammarParser#fiile.
    def visitFiile(self, ctx:GrammarParser.FiileContext):
        if ctx.variable_definition():
            self.global_variable = True
            # print("global variable")
            for i in range(len(ctx.variable_definition())):
                self.visit(ctx.variable_definition(i))
            self.global_variable = False
        if ctx.function_definition():
            for i in range(len(ctx.function_definition())):
                self.visit(ctx.function_definition(i))



     # Visit a parse tree produced by GrammarParser#function_definition.
    def visitFunction_definition(self, ctx:GrammarParser.Function_definitionContext):
        tyype = ctx.tyype().getText()
        name = ctx.identifier().getText()
        params = self.visit(ctx.arguments())
        self.ids_defined[name] = {'tyype': tyype, 'params': params}
        self.inside_what_function = name
        self.visit(ctx.body())
        return


    # Visit a parse tree produced by GrammarParser#body.
    def visitBody(self, ctx:GrammarParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#statement.
    def visitStatement(self, ctx:GrammarParser.StatementContext):


        if ctx.variable_definition():
            # print("Statement variable definition")
            self.visit(ctx.variable_definition())
        elif ctx.variable_assignment():
            # print("Statement variable assignment")
            self.visit(ctx.variable_assignment())
        elif ctx.expression() and not ctx.RETURN():
            # print("Statement expr")
            self.visit(ctx.expression())
        elif ctx.RETURN():
            ret_expr = self.visit(ctx.expression())
            ret_type = ''
            if ret_expr != None:
                ret_type = ret_expr.get('tyype')
            token = ctx.RETURN().getPayload()
            f_info = self.ids_defined.get(self.inside_what_function)
            f_type = f_info.get('tyype')
            if ret_type != f_type:
                if(ret_type in [Type.STRING, Type.INT, Type.FLOAT] and f_type == Type.VOID):
                    print(  "ERROR: trying to return a non void expression from void function '"
                            +self.inside_what_function+"' in line "
                            +str(token.line)+" and column "+str(token.column)
                            )
                if(ret_type == Type.FLOAT and f_type == Type.INT):
                    print(  "WARNING: possible loss of information returning float expression"
                            " from int function '"+self.inside_what_function+"' in line "
                            +str(token.line)+ " and column "+str(token.column)
                            )
                if(ret_type == Type.STRING and f_type in [Type.INT, Type.FLOAT]):
                    print(  "ERROR: trying to return a string expression from int function '"
                            +self.inside_what_function+"' in line "
                            +str(token.line)+" and column "+str(token.column)
                            )
                if(ret_type == Type.VOID and f_type in [Type.STRING, Type.INT, Type.FLOAT]):
                    print(  "ERROR: trying to return void expression from function '"
                            +self.inside_what_function+"' in line "
                            +str(token.line)+" and column " +str(token.column)
                            )
        elif ctx.for_loop():
            self.count += 1
            self.constant = False
            self.stack_statement.append(self.count)
            self.visit(ctx.for_loop())
            self.constant = True
            self.stack_statement.pop()
        elif ctx.if_statement:
            self.count += 1
            self.stack_statement.append(self.count)
            self.visit(ctx.if_statement())
            self.stack_statement.pop()
        elif ctx.body():
            self.count += 1
            self.stack_statement.append(self.count)
            self.visit(ctx.body)
            self.stack_statement.pop()

    # Visit a parse tree produced by GrammarParser#if_statement.
    def visitIf_statement(self, ctx:GrammarParser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#else_statement.
    def visitElse_statement(self, ctx:GrammarParser.Else_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#for_loop.
    def visitFor_loop(self, ctx:GrammarParser.For_loopContext):
        # print("Dentro do for loop")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#for_initializer.
    def visitFor_initializer(self, ctx:GrammarParser.For_initializerContext):
        # print("Dentro do for initializer")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#for_condition.
    def visitFor_condition(self, ctx:GrammarParser.For_conditionContext):
        # print("Dentro do for condition")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#for_step.
    def visitFor_step(self, ctx:GrammarParser.For_stepContext):
        # print("Dentro do for step")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#variable_definition.
    def visitVariable_definition(self, ctx:GrammarParser.Variable_definitionContext):
        # print("Variable definition")
        tyype = ctx.tyype().getText()

        name = ''

        if ctx.array(0) != None:
            for i in range(len(ctx.array())):
                name = ctx.array(i).identifier().getText()
                self.ids_defined[name] = {
                    'tyype': tyype,
                    'index': None
                    }
                ret_arr = self.visit(ctx.array(i))
                token = ctx.array(i).identifier().IDENTIFIER().getPayload()
                array_name = ret_arr.get('name')
                index = ret_arr.get('index') # Valor do index
                ret_err = ret_arr.get('ret_err')
                literal = []
                if index != None:
                    literal = [None] * index
                ret_arr_literal_type = []
                if(ret_err == Type.ERROR or ret_err == Type.VOID):
                    return
                else:
                    if ctx.array_literal(i):
                        ret = self.visit(ctx.array_literal(i))
                        ret_arr_literal_type = ret.get('tyype')
                        literal = ret.get('literal')
                        if ret_arr_literal_type:

                            if(tyype == Type.FLOAT and Type.STRING in ret_arr_literal_type):
                                index = ret_arr_literal_type.index(Type.STRING)
                                print(  "ERROR: trying to initialize "
                                        +Type.STRING+" expression to "
                                        +tyype+ " array '"+ array_name +"' at index "
                                        + str(index) + " of array literal in line "
                                        + str(token.line) +" and column " + str(token.column)
                                    )
                            if(tyype == Type.INT and Type.STRING in ret_arr_literal_type):
                                index = ret_arr_literal_type.index(Type.STRING)
                                print(  "ERROR: trying to initialize "
                                        + Type.STRING +" expression to "
                                        +tyype+ " array '"+ array_name +"' at index "
                                        + str(index) + " of array literal in line "
                                        + str(token.line) +" and column " + str(token.column)
                                        )
                            if(tyype == Type.INT and Type.FLOAT in ret_arr_literal_type):
                                index = ret_arr_literal_type.index(Type.FLOAT)
                                print('WARNING: possible loss of information initializing '+ Type.FLOAT +' expression to '+tyype+ ' array \''+ array_name +'\' at index ' + str(index) + ' of array literal in line '+ str(token.line) +' and column ' + str(token.column))
                    if self.global_variable:
                        pass
                    
                    if(index != None and self.constant and not self.global_variable):
                        self.ids_defined[name] = {
                            'tyype': tyype,
                            'index': index,
                            'cte': True,
                            'id': self.stack_statement[-1],
                            'literal': literal
                            }
                    else:
                        self.ids_defined[name] = {
                            'tyype': tyype,
                            'index': index,
                            'cte': False,
                            'id': self.stack_statement[-1],
                            'literal': None
                            }
        else:
            for i in range(len(ctx.identifier())):
                name = ctx.identifier(i).getText()
                ret_expr = tyype
                if ctx.expression(i):
                    token = ctx.identifier(i).IDENTIFIER().getPayload() # Obtém o token referente à uma determinada regra léxica (neste caso, IDENTIFIER)
                    ret_expr = self.visit(ctx.expression(i))
                    ret_type = None
                    value = None
                    if(ret_expr != None):
                        ret_type = ret_expr.get('tyype')
                        value = ret_expr.get('value')
                        # print("Nome:", name, "tipo:", ret_type, "valor:", value)
                    if(ret_type == Type.VOID):
                        print("ERROR: trying to assign 'void' expression to variable"
                             "'"+name+"' in line "+str(token.line)+" and column "+str(token.column))
                    elif(ret_type == Type.ERROR):
                        # print("Continuando após o erro")
                        return
                    else:
                        hold = ""
                        if self.global_variable:
                            hold = "@" + name + " = " + llvm_type(tyype)) + " "
                        if(value != None and not self.global_variable and self.constant):
                            
                            if(tyype == Type.INT and not isinstance(value, str)):
                                val = str(value)
                                self.ids_defined[name] = {
                                    'tyype': tyype,
                                    'value': floor(value),
                                    'cte': True,
                                    'id': self.stack_statement[-1]
                                    }
                            else:
                                val = str(float_to_hex(value))
                                self.ids_defined[name] = {
                                    'tyype': tyype,
                                    'value': value,
                                    'cte': True,
                                    'id': self.stack_statement[-1]
                                    }

                            self.output.write(hold + val)

                            if(ret_type != tyype):

                                if(tyype == Type.INT and ret_type == Type.FLOAT):
                                    print('WARNING: possible loss of information assigning float expression to int variable \''+ str(ctx.identifier(i).getText())+ '\' in line ' + str(token.line) +' and column ' + str(token.column))
                                elif(tyype in [Type.INT, Type.FLOAT] and ret_type == Type.STRING):
                                    print('ERROR: trying to assign \''+ Type.STRING +'\' expression to variable \''+ str(ctx.identifier(i).getText())+'\' in line '+ str(token.line) + ' and column '+ str(token.column))
                        else:
                            self.ids_defined[name] = {
                                'tyype': tyype,
                                'value': None,
                                'cte': False,
                                'id': self.stack_statement[-1]
                                }
                else:
                    self.ids_defined[name] = {
                        'tyype': tyype,
                        'value': None,
                        'cte': False,
                        'id': self.stack_statement[-1]
                        }

    # Visit a parse tree produced by GrammarParser#variable_assignment.
    def visitVariable_assignment(self, ctx:GrammarParser.Variable_assignmentContext):
        name = ''
        index = None
        token = ''
        value = None
        cte = False
        var_value = None
        var_index = None
        if(ctx.array()):
            # print("Array")
            ret_arr = self.visit(ctx.array())
            name = ret_arr.get('name')
            index = ret_arr.get('index')
            ret_err = ret_arr.get('ret_err')
            token = ctx.array().identifier().IDENTIFIER().getPayload()
            if ret_err == Type.ERROR:
                return
        else:
            name = ctx.identifier().getText()
            token = ctx.identifier().IDENTIFIER().getPayload()

        
        var_info = self.ids_defined.get(name)

        if var_info == None:
            token = ctx.identifier().IDENTIFIER().getPayload()
            print('ERROR: undefined variable \''+ name + '\' in line ' + str(token.line) +  ' and column ' + str(token.column))
        else:
            var_type = var_info.get('tyype')
            literal = self.ids_defined[name].get('literal')
            var_index = self.ids_defined[name].get('index')
            if ctx.array():
                literal = var_info.get('literal')
                if var_index != None and index != None:
                    if index < var_index:
                        if literal != None and index != None:
                            var_value = literal[index]
                        else:
                            var_value = None
                    else:
                        print('ERROR: index out of bounds in variable \''+name+'\' in line '+str(token.line)+ ' and column '+ str(token.column))
                        return
                        var_value = None

            else:
                var_value = var_info.get('value')
            
            
            if(ctx.OP.text == '++'):
                if(self.stack_statement[-1] != var_info.get('id')): # Se for diferente, representa uma bifurcação
                    cte = False
                elif var_value != None:
                    cte = True
                    value = var_value + 1
            elif(ctx.OP.text == '--'):
                if(self.stack_statement[-1] != var_info.get('id')):
                    cte = False
                elif var_value != None:
                    cte = True
                    value = var_value - 1
            else:
                ret_expr = self.visit(ctx.expression())
                ret_type = ''
                ret_value = 0

            
                if(ret_expr != None):
                    ret_type = ret_expr.get('tyype')
                    ret_value = ret_expr.get('value')
            
                if(ret_type != Type.ERROR):
                    if(ret_type == Type.VOID):
                        print('ERROR: trying to assign \''+ Type.VOID +'\' expression to variable \''+ name+'\' in line '+ str(token.line) + ' and column '+ str(token.column))
                    elif(var_type == Type.INT and ret_type == Type.FLOAT):
                        print('WARNING: possible loss of information assigning float expression to int variable \''+name+ '\' in line ' + str(token.line) +' and column ' + str(token.column))
                    elif(var_type == (Type.INT or Type.FLOAT) and ret_type == Type.STRING):
                        print('ERROR: trying to assign \''+ Type.STRING +'\' expression to variable \''+name+'\' in line '+ str(token.line) + ' and column '+ str(token.column))
                    else:
                        if ret_value != None:
                            if(self.stack_statement[-1] != var_info.get('id')):
                                cte = False

                            else:
                                cte = True
                                if var_value == None:
                                    if(ctx.OP.text == '='):
                                        value = ret_value
                                else:
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
                                if(ret_type == Type.INT):
                                    value = floor(value)

            if ctx.array():
                if literal != None and index != None:
                    literal[index] = value
                self.ids_defined[name] = {'tyype': var_type, 'index': self.ids_defined[name].get('index'), 'cte': cte, 'id': var_info.get('id'), 'literal': literal}
            else:
                self.ids_defined[name] = {'tyype': var_type, 'value': value, 'cte': cte, 'id': var_info.get('id')}



    # Visit a parse tree produced by GrammarParser#expression.
    def visitExpression(self, ctx:GrammarParser.ExpressionContext):

        # retorno de expression: {'tyype':, 'value':}

        # print("Visitando expression")
        if ctx.integer():
            return self.visit(ctx.integer())
        elif ctx.floating():
            return self.visit(ctx.floating())
        elif ctx.string():
            return self.visit(ctx.string())
        elif ctx.identifier():
            return self.visit(ctx.identifier())
        elif ctx.array():
            ret_arr = self.visit(ctx.array())
            arr = self.ids_defined.get(ret_arr.get('name'))
            index = ret_arr.get('index') # index do array
            literal = arr.get('literal')
            if(ret_arr.get('ret_err') == Type.ERROR or arr == None):    
                return {'tyype': Type.ERROR, 'value': None}
            elif(literal != None and index < arr.get('index')):
                return {'tyype': arr.get('tyype'), 'value': literal[index]}
            else:
                return {'tyype': arr.get('tyype'), 'value': None}

        elif ctx.expression(1):
            # print("3 filhos") 
            ret_info_expr1 = self.visit(ctx.expression(0))
            ret_info_expr2 = self.visit(ctx.expression(1))

            ret_expr1 = ''
            ret_expr2 = ''
            value_expr1 = 0
            value_expr2 = 0

            if(ret_info_expr1 != None):
                ret_expr1 = ret_info_expr1.get('tyype')
                value_expr1 = ret_info_expr1.get('value')
                # print("Value expr1:", value_expr1)
            
            if(ret_info_expr2 != None):
                ret_expr2 = ret_info_expr2.get('tyype')
                value_expr2 = ret_info_expr2.get('value')
                # print("Value expr2:", value_expr2)


            ret_tyype = ret_expr1
            op_type = ctx.OP.text
            expr_line = ctx.OP.line

            if((ret_expr1 == (Type.FLOAT or Type.INT) and ret_expr2 == Type.STRING) and (ret_expr1 == Type.STRING  and ret_expr2 == (Type.FLOAT or Type.INT))):
                # print("ERRO: tipos incompativeis")
                return {'tyype': Type.ERROR,'value': None}
            elif((ret_expr1 == Type.FLOAT and ret_expr2 == Type.INT) or (ret_expr1 == Type.INT and ret_expr2 == Type.FLOAT)):
                if(op_type == '*' or op_type == '/'):
                    ret_tyype = Type.FLOAT
                elif(op_type == '+' or op_type == '-'):
                    ret_tyype = Type.FLOAT
            elif((ret_expr1 == None) or (ret_expr2 == None)):
                # print("ERRO: tipo vazio ou variavel indefinida")
                return {'tyype': Type.ERROR,'value': None}
            elif(ret_expr1 == Type.VOID or ret_expr2 == Type.VOID):
                # token = ctx.OP.getPayload()
                # print(ctx.OP.column)
                print("ERROR: binary operator '"+op_type+ "' used on type void in line "+str(ctx.OP.line)+" and column " +str(ctx.OP.column))
                return {'tyype': Type.ERROR,'value': None}
            
            if(value_expr1 == None or value_expr2 == None):
                return {'tyype': ret_tyype, 'value': None}

            if(
                not isinstance(value_expr1, str)
                and not isinstance(value_expr2, str)
                and not self.global_variable
                and self.constant):
                if(op_type == '*'):
                    print("line " + str(expr_line) + " Expression " + str(value_expr1) + " " + ctx.OP.text + " " + str(value_expr2) + " simplified to: " + str(value_expr1 * value_expr2))
                    return {'tyype': ret_tyype, 'value': value_expr1 * value_expr2}
                elif(op_type == '/'):
                    if(value_expr2 == 0):
                        print("ERROR: division by zero")
                        return {'tyype': ret_tyype, 'value': None}
                    print("line " + str(expr_line) + " Expression " + str(value_expr1) + " " + ctx.OP.text + " " + str(value_expr2) + " simplified to: " + str(value_expr1 / value_expr2))
                    return {'tyype': ret_tyype, 'value': value_expr1 / value_expr2}
                elif(op_type == '+'):
                    print("line " + str(expr_line) + " Expression " + str(value_expr1) + " " + ctx.OP.text + " " + str(value_expr2) + " simplified to: " + str(value_expr1 + value_expr2))
                    return {'tyype': ret_tyype, 'value': value_expr1 + value_expr2}
                elif(op_type == '-'):
                    print("line " + str(expr_line) + " Expression " + str(value_expr1) + " " + ctx.OP.text + " " + str(value_expr2) + " simplified to: " + str(value_expr1 - value_expr2))
                    return {'tyype': ret_tyype, 'value': value_expr1 - value_expr2}
                elif(op_type == '>'):       
                    value = 1 if value_expr1 > value_expr2 else 0
                    print("line " + str(expr_line) + " Expression " + str(value_expr1) + " " + ctx.OP.text + " " + str(value_expr2) + " simplified to: " + str(value))
                    return {'tyype': ret_tyype, 'value': value}         
                elif(op_type == '>='):
                    value = 1 if value_expr1 >= value_expr2 else 0
                    print("line " + str(expr_line) + " Expression " + str(value_expr1) + " " + ctx.OP.text + " " + str(value_expr2) + " simplified to: " + str(value))
                    return {'tyype': ret_tyype, 'value': value}        
                elif(op_type == '<'):    
                    value = 1 if value_expr1 < value_expr2 else 0
                    print("line " + str(expr_line) + " Expression " + str(value_expr1) + " " + ctx.OP.text + " " + str(value_expr2) + " simplified to: " + str(value))
                    return {'tyype': ret_tyype, 'value': value}           
                elif(op_type == '<='):                  
                    value = 1 if value_expr1 <= value_expr2 else 0
                    print("line " + str(expr_line) + " Expression " + str(value_expr1) + " " + ctx.OP.text + " " + str(value_expr2) + " simplified to: " + str(value))
                    return {'tyype': ret_tyype, 'value': value}         
                elif(op_type == '!='):         
                    value = 1 if value_expr1 != value_expr2 else 0
                    print("line " + str(expr_line) + " Expression " + str(value_expr1) + " " + ctx.OP.text + " " + str(value_expr2) + " simplified to: " + str(value))
                    return {'tyype': ret_tyype, 'value': value}
           
        elif ctx.getChildCount() == 2: #OP expression
            ret_expr = self.visit(ctx.expression(0))
            expr_line = ctx.OP.line
            if ret_expr == None:
                # print('ERRO: tipo vazio')
                return {'tyype': Type.ERROR,'value': None}
            elif ret_expr == Type.ERROR:
                return {'tyype': Type.ERROR,'value': None}
            elif ret_expr.get('value') == None:
                return ret_expr
            else:
                if(not self.global_variable and self.constant):
                    if ctx.OP.text == '-':
                        print("line " + str(expr_line) + " Expression " + ctx.OP.text + " " + str(ret_expr.get('value')) + " simplified to: " + str(-ret_expr.get('value')))
                        ret_expr['value'] = -ret_expr.get('value')
                        return ret_expr
                else:
                    return ret_expr
        elif(ctx.getChildCount() == 3 and ctx.expression(1) == None):
            return self.visit(ctx.expression(0)) 
        
        elif ctx.function_call():
            ret_f = self.visit(ctx.function_call())

            err = ret_f.get('ret_err')

            if err == Type.VOID:
                return {'tyype': ret_f.get('tyype'),'value': None, 'ret_err': Type.VOID}
            elif err == Type.ERROR:
                return {'tyype': ret_f.get('tyype'),'value': None, 'ret_err': Type.ERROR}
            else:
                return ret_f



    # Visit a parse tree produced by GrammarParser#array.
    def visitArray(self, ctx:GrammarParser.ArrayContext):

        token = ctx.identifier().IDENTIFIER().getPayload()
        name = ctx.identifier().getText()
        ret_expr = self.visit(ctx.expression())
        ret_type = ret_expr.get('tyype')
        index_value = ret_expr.get('value')
        if(ret_expr.get('var')):
            index_value = None
        tyype = ''

        # Se a variável não tiver sido declarada anteriormente
        if(self.ids_defined.get(name) == None):
            print('ERROR: undefined array \''+name+'\' in line ' + str(token.line) + ' and column ' +str(token.column))
            tyype = Type.ERROR

        if(ret_expr == Type.ERROR):
            return {'name': name, 'index': None, 'ret_err': Type.ERROR}
        elif(ret_expr == Type.VOID):
            print('ERROR: trying to assign \'void\' expression to variable \'' + name + '\'in line '+ str(token.line)+ ' and column ' + str(token.column))
            return {'name': name, 'index': None, 'ret_err': Type.VOID}
        else:
            if(index_value != None):
                if(index_value < 0):
                    print('ERROR: array expression must be an positive integer, but it is ' + str(index_value) + ' in line '+ str(token.line)+' and column ' + str(token.column))
                    tyype = Type.ERROR
                elif(ret_type != Type.INT):
                    print('ERROR: array expression must be an integer, but it is ' + ret_type + ' in line '+ str(token.line)+' and column ' + str(token.column))
                    tyype = Type.ERROR
            # print("Returning array", name, "index", index_value)
            return {'name': name, 'index': index_value, 'ret_err': tyype}


    # Visit a parse tree produced by GrammarParser#array_literal.
    def visitArray_literal(self, ctx:GrammarParser.Array_literalContext):    
        tyype = []
        literal = []
        if ctx.getChildCount() > 0:
            # Verifica os tipos dos literais e guarda 
            for i in range(len(ctx.expression())):
                ret_expr = self.visit(ctx.expression(i))
                tyype.append(ret_expr.get('tyype')) # Salva os tipos
                literal.append(ret_expr.get('value')) # Salva os valores
            return {'tyype': tyype, 'literal': literal}

        else:
            return {'tyype': None, 'literal': None}



    # Visit a parse tree produced by GrammarParser#function_call.
    def visitFunction_call(self, ctx:GrammarParser.Function_callContext):

        # retorno do tipo: {'tyype': tipo da funcao, 'value': erro, se houver}

        # print("Visitando function call")
        f_name = ctx.identifier().getText()
        f_info = self.ids_defined.get(f_name)
        f_type = f_info.get('tyype')
        f_params = f_info.get('params')

        token = ctx.identifier().IDENTIFIER().getPayload()

        # print("Info Function:", f_info)
        if f_info == None:
            print("ERROR: undefined function '"
            +f_name+"' in line "
            +str(token.line)+" and column "
            +str(token.column) )
            return {'tyype': f_type, 'value': None, 'ret_err': Type.ERROR}
        else:
            value = 0
            ret_err = ''
            for i in range(len(ctx.expression())):
                ret_expr = self.visit(ctx.expression(i))   
                ret_tyype = None
                if(ret_expr != None):
                    ret_tyype = ret_expr.get('tyype')
                
                # print("Len params:", len(f_params), "i:", i)

                if(i > (len(f_params) - 1)):
                    print('ERROR: incorrect number of parameters for function \''+f_name+'\' in line ' +str(token.line)+' and column '+str(token.column)+'. Expecting '+str(len(f_params))+', but '+str(len(ctx.expression()))+' were given')
                    return {'tyype': f_type, 'value': None, 'ret_err': Type.ERROR}
                    # return Type.ERROR
                else:
                    param = f_params[i][0] #pega o i-ésimo parametro, mas apenas o tipo dele
                    # checando os tipos
                    if(param == Type.INT and ret_tyype == Type.FLOAT):
                        print('WARNING: possible loss of information converting float expression to int expression in parameter '+ str(i) +' of function \''+f_name+'\' in line '+ str(token.line) +' and column ' + str(token.column))
                    elif(param == Type.INT and ret_tyype == Type.STRING):
                        print('ERROR: trying to assign string expression to int expression in parameter '+ str(i) +' of function \''+f_name+'\' in line '+ str(token.line) +' and column ' + str(token.column))
                        ret_err = Type.ERROR
                        #por algum motivo param == (Type.INT or Type.FLOAT) não funciona
                        # erro
                    elif(param == Type.FLOAT and ret_tyype == Type.STRING):
                        print('ERROR: trying to assign string expression to float expression in parameter '+ str(i) +' of function \''+f_name+'\' in line '+ str(token.line) +' and column ' + str(token.column))
                        ret_err = Type.ERROR
                        # erro
                    elif(param == Type.STRING and ret_tyype == Type.INT):
                        print('ERROR: trying to assign int expression to string expression in parameter '+ str(i) +' of function \''+f_name+'\' in line '+ str(token.line) +' and column ' + str(token.column))
                        ret_err = Type.ERROR
                        # erro
                    elif(param == Type.STRING and ret_tyype == Type.FLOAT):
                        print('ERROR: trying to assign float expression to string expression in parameter '+ str(i) +' of function \''+f_name+'\' in line '+ str(token.line) +' and column ' + str(token.column))
                        ret_err = Type.ERROR
                    # erro
            # print("Retornando da chamada de funcao:", {'tyype': f_type, 'value': value})
            return {'tyype': f_type, 'value': None, 'ret_err': ret_err}
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
            return {'tyype': Type.ERROR, 'value': None, 'var': False, 'cte': False}
        else:
            # print("Retornando identifier var info", var_info)
            return {'tyype': var_info.get('tyype'), 'value': var_info.get('value'), 'var':True, 'cte': var_info.get('cte')}

