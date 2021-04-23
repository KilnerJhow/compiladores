# Generated from antlr4-python3-runtime-4.7.2/src/autogen/Grammar.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GrammarParser import GrammarParser
else:
    from GrammarParser import GrammarParser


import sys
err = sys.stderr.write
def printf(string, *args):
    sys.stdout.write(string % args)

import struct
import math
# Função utilizada para transformar um valor float para um valor hexadecimal 
# (o equivalente em hexadecimal dos valores dos bits de um float)
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


# retorne Type.INT, etc para fazer checagem de tipos
class Type:
    VOID = "void"
    INT = "int"
    FLOAT = "float"
    STRING = "char *"

def llvm_type(tyype):
    if tyype == Type.VOID:
        return "void"
    if tyype == Type.INT:
        return "i32"
    if tyype == Type.FLOAT:
        return "float"


# This class defines a complete generic visitor for a parse tree produced by GrammarParser.
class GrammarCheckerVisitor(ParseTreeVisitor):
    ids_defined = {} # armazenar informações necessárias para cada identifier definido
    loaded_var = {} #acessar variáveis já armazenadas
    inside_what_function = ""
    next_ir_register = 0
    output = open("output.ll", "w")
    global_variable = False

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
                self.next_ir_register = 0
                self.loaded_var = {}
                self.visit(ctx.function_definition(i))
        return self.output.close()


    # Visit a parse tree produced by GrammarParser#function_definition.
    def visitFunction_definition(self, ctx:GrammarParser.Function_definitionContext):
        tyype = ctx.tyype().getText()
        name = ctx.identifier().getText()

        params, params_name = self.visit(ctx.arguments())

        #TODO: Verificar o valor de align 4 e ver se é comum a todos!

        cte_value = None
        ir_register = None
        out_text = "define " + llvm_type(tyype) + " @" + name + "("
        body_text = ""
        if(len(params) == 1):
            param_type = llvm_type(params[0])
            out_text += param_type + " %0) {\n"
            out_text += "\t%"+params_name[0]+" = alloca " + param_type + ", align 4\n"
            out_text += "\tstore " + param_type + " %0, " + param_type + "* " + "%" + params_name[0] +", align 4\n"
            pass
        else:
            #Criando a linha dos parametros
            for i in range(len(params)):
                out_text += llvm_type(params[i]) + " %" + str(i)
                if(i + 1 != len(params)): 
                    out_text += ", "
                
                body_text += "\t%"+params_name[i]+" = alloca " + params[i] + ", align 4\n"
                body_text += "\tstore " + params[i] + " %" + str(i) + ", " + params[i] + "* " + "%" + params_name[i] +", align 4\n"
                #%x = alloca i32, align 4
                #store i32 %0, i32* %x, align 4

            out_text += ") {\n"
            out_text += body_text
        ir_register = "@" + name
        self.ids_defined [name] = tyype, params, cte_value, ir_register
        self.inside_what_function = name
        self.next_ir_register = len(params)
        self.output.write(out_text + "\t")
        self.visit(ctx.body())
        out_text = "\n}\n\n"
        self.output.write(out_text)
        return


    # Visit a parse tree produced by GrammarParser#body.
    def visitBody(self, ctx:GrammarParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#statement.
    def visitStatement(self, ctx:GrammarParser.StatementContext):
        if ctx.RETURN() != None:
            token = ctx.RETURN().getPayload()
            function_type, params, cte_value, ir_register = self.ids_defined[self.inside_what_function]
            if ctx.expression() != None:
                tyype, cte_value, ir_register = self.visit(ctx.expression())

                self.output.write("ret " + llvm_type(function_type) + " " + ir_register)

                if function_type == Type.INT and tyype == Type.FLOAT:
                    err("WARNING: possible loss of information returning float expression from int function '" + self.inside_what_function + "' in line " + str(token.line) + " and column " + str(token.column) + "\n")
                elif function_type != Type.VOID and tyype == Type.VOID:
                    err("ERROR: trying to return void expression from function '" + self.inside_what_function + "' in line " + str(token.line) + " and column " + str(token.column) + "\n")
                    exit(-1)
                elif function_type == Type.VOID and tyype != Type.VOID:
                    err("ERROR: trying to return a non void expression from void function '" + self.inside_what_function + "' in line " + str(token.line) + " and column " + str(token.column) + "\n")
                    exit(-1)
            elif function_type != Type.VOID:
                err("ERROR: trying to return void expression from function '" + self.inside_what_function + "' in line " + str(token.line) + " and column " + str(token.column) + "\n")
                exit(-1)
            else:
                self.output.write("ret " + llvm_type(function_type))
            self.output.write("\n\t")
        else:
            self.visitChildren(ctx)
        return


    # Visit a parse tree produced by GrammarParser#if_statement.
    def visitIf_statement(self, ctx:GrammarParser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#else_statement.
    def visitElse_statement(self, ctx:GrammarParser.Else_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#for_loop.
    def visitFor_loop(self, ctx:GrammarParser.For_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#for_initializer.
    def visitFor_initializer(self, ctx:GrammarParser.For_initializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#for_condition.
    def visitFor_condition(self, ctx:GrammarParser.For_conditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#for_step.
    def visitFor_step(self, ctx:GrammarParser.For_stepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#variable_definition.
    def visitVariable_definition(self, ctx:GrammarParser.Variable_definitionContext):
        tyype = ctx.tyype().getText()
        ir_register = None
        val = 0
        expr_type = None
        # identifiers
        
        for i in range(len(ctx.identifier())):
        
            name = ctx.identifier(i).getText()
            token = ctx.identifier(i).IDENTIFIER().getPayload()
            
            if self.global_variable:
                self.output.write("@" + name + " = global " + llvm_type(tyype) + " ")
                
            else:
                self.output.write("%" + name + " = alloca " + llvm_type(tyype) + ", align 4\n\t")
            
            if ctx.expression(i) != None:
                
                if(ctx.expression(i).function_call() != None):
                    reg = str(self.next_ir_register)
                    self.output.write("%"+reg+" = ")

                expr_type, cte_value, ir_register = self.visit(ctx.expression(i))

                print("Ret expr var \"", name, "\" type", expr_type, "value", cte_value, "ir register", ir_register)

                if expr_type == Type.VOID:
                    err("ERROR: trying to assign void expression to variable '" + name + "' in line " + str(token.line) + " and column " + str(token.column) + "\n")
                    exit(-1)
                elif expr_type == Type.FLOAT and tyype == Type.INT:
                    err("WARNING: possible loss of information assigning float expression to int variable '" + name + "' in line " + str(token.line) + " and column " + str(token.column) + "\n")
                
                val = ""

                if ir_register == None:

                    if cte_value != None:
                        if expr_type == Type.FLOAT:
                            val = float_to_hex(cte_value)
                        else:
                            val = str(int(cte_value))
                    else:
                        val = ir_register

                else:

                    ir_register = "%" + name
                    if cte_value != None:
                        if expr_type == Type.FLOAT:
                            val = float_to_hex(cte_value)
                        else:
                            val = str(int(cte_value))
                    else:
                        val = None

                if val != None:
                    if self.global_variable:
                        self.output.write(val + "\n")
                    else:
                        self.output.write("store " + llvm_type(expr_type) + " " + val + ", " +  llvm_type(expr_type) + "* %" + name + ", align 4\n\t")
            else:
                # unitialized variables now get value 0
                cte_value = 0
            if self.global_variable:
                ir_register = "@" + name
            else:
                ir_register = "%" + name
            self.ids_defined[name] = tyype, -1, cte_value, ir_register # -1 means not a array, therefore no length here (vide 15 lines below)
            print("Next ir register", self.next_ir_register)
        # arrays
        for i in range(len(ctx.array())):
            name = ctx.array(i).identifier().getText()
            token = ctx.array(i).identifier().IDENTIFIER().getPayload()

            array_length, _ = self.visit(ctx.array(i))
            if ctx.array_literal(i) != None:
                expr_types, cte_values_array, ir_registers_array = self.visit(ctx.array_literal(i))
                for j in range(len(expr_types)):
                    if expr_types[j] == Type.VOID:
                        err("ERROR: trying to initialize void expression to array '" + name + "' at index " + str(j) + " of array literal in line " + str(token.line) + " and column " + str(token.column) + "\n")
                        exit(-1)
                    elif expr_types[j] == Type.FLOAT and tyype == Type.INT:
                        err("WARNING: possible loss of information initializing float expression to int array '" + name + "' at index " + str(j) + " of array literal in line " + str(token.line) + " and column " + str(token.column) + "\n")
            else:
                # unitialized variables now get value 0
                cte_values_array = [0] * array_length
                ir_registers_array = [None] * array_length
            self.ids_defined[name] = tyype, array_length, cte_values_array, ir_registers_array

        return


    # Visit a parse tree produced by GrammarParser#variable_assignment.
    def visitVariable_assignment(self, ctx:GrammarParser.Variable_assignmentContext):
        op = ctx.OP.text
        # identifier assignment
        if ctx.identifier() != None:
            name = ctx.identifier().getText()
            token = ctx.identifier().IDENTIFIER().getPayload()
            try:
                tyype, _, cte_value, ir_register = self.ids_defined[name]
            except:
                err("ERROR: undefined variable '" + name + "' in line " + str(token.line) + " and column " + str(token.column) + "\n")
                exit(-1)
                return

        # array assignment
        else:
            name = ctx.array().identifier().getText()
            token = ctx.array().identifier().IDENTIFIER().getPayload()
            try:
                tyype, array_length, cte_values_array, ir_registers_array = self.ids_defined[name]
            except:
                err("ERROR: undefined array '" + name + "' in line " + str(token.line) + " and column " + str(token.column) + "\n")
                exit(-1)
            array_index_cte, array_index_ir = self.visit(ctx.array())
            if array_index_cte == None:
                cte_value = None
            else:
                if array_index_cte < 0 or array_index_cte >= array_length:
                    err("ERROR: array '" + name + "' index out of range in line " + str(token.line) + " and column " + str(token.column) + "\n")
                    exit(-1)
                else:
                    cte_value = cte_values_array[array_index_cte]
                    ir_register = ir_registers_array[array_index_cte]


        if op == '++' or op == '--':
            if cte_value != None:
                if op == '++':
                    cte_value += 1
                elif op == '--':
                    cte_value -= 1
            else:
                cte_value = None
        else:
            expr_type, expr_cte_value, expr_ir_register = self.visit(ctx.expression())
            if expr_type == Type.VOID:
                err("ERROR: trying to assign void expression to variable '" + name + "' in line " + str(token.line) + " and column " + str(token.column) + "\n")
                exit(-1)
            elif expr_type == Type.FLOAT and tyype == Type.INT:
                err("WARNING: possible loss of information assigning float expression to int variable '" + name + "' in line " + str(token.line) + " and column " + str(token.column) + "\n")

            if op == '=':
                cte_value = expr_cte_value
            if cte_value != None:
                if op == '+=':
                    cte_value += expr_cte_value
                elif op == '-=':
                    cte_value -= expr_cte_value
                elif op == '*=':
                    cte_value *= expr_cte_value
                elif op == '/=':
                    cte_value /= expr_cte_value

        if ctx.identifier() != None:
            self.ids_defined[name] = tyype, -1, cte_value, ir_register
        else: # array
            if array_index_cte != None:
                cte_values_array[array_index_cte] = cte_value
                ir_registers_array[array_index_cte] = ir_register
            self.ids_defined[name] = tyype, array_length, cte_values_array, ir_registers_array

        return


    # Visit a parse tree produced by GrammarParser#expression.
    def visitExpression(self, ctx:GrammarParser.ExpressionContext):
        tyype = Type.VOID
        cte_value = None
        ir_register = None

        if len(ctx.expression()) == 0:

            if ctx.integer() != None:
                tyype = Type.INT
                cte_value = int(ctx.integer().getText())

            elif ctx.floating() != None:
                tyype = Type.FLOAT
                cte_value = float(ctx.floating().getText())

            elif ctx.string() != None:
                tyype = Type.STRING

            elif ctx.identifier() != None:
                name = ctx.identifier().getText()
                try:
                    tyype, _, cte_value, ir_register = self.ids_defined[name]
                    self.loaded_var[name] = self.next_ir_register
                except:
                    token = ctx.identifier().IDENTIFIER().getPayload()
                    err("ERROR: undefined variable '" + name + "' in line " + str(token.line) + " and column " + str(token.column) + "\n")
                    exit(-1)

            elif ctx.array() != None:
                name = ctx.array().identifier().getText()
                try:
                    tyype, array_length, cte_values_array, ir_registers_array = self.ids_defined[name]
                except:
                    token = ctx.array().identifier().IDENTIFIER().getPayload()
                    err("ERROR: undefined array '" + name + "' in line " + str(token.line) + " and column " + str(token.column) + "\n")
                    exit(-1)

                array_index_cte, array_index_ir = self.visit(ctx.array())
                if array_index_cte != None:
                    if array_index_cte < 0 or array_index_cte >= array_length:
                        err("ERROR:  array '" + name + "' index out of bounds in line " + str(token.line) + " and column " + str(token.column) + "\n")
                        exit(-1)
                    else:
                        cte_value = cte_values_array[array_index_cte]
                        ir_register = ir_registers_array[array_index_cte]

            elif ctx.function_call() != None:
                tyype, cte_value, ir_register = self.visit(ctx.function_call())
                ir_register = "%" + str(self.next_ir_register)
                self.next_ir_register += 1

        elif len(ctx.expression()) == 1:

            if ctx.OP != None: #unary operators
                text = ctx.OP.text
                token = ctx.OP
                tyype, cte_value, ir_register = self.visit(ctx.expression(0))
                if tyype == Type.VOID:
                    err("ERROR: unary operator '" + text + "' used on type void in line " + str(token.line) + " and column " + str(token.column) + "\n")
                    exit(-1)
                elif cte_value != None:
                    if text == '-':
                        cte_value = -cte_value

            else: # parentheses
                tyype, cte_value, ir_register = self.visit(ctx.expression(0))

        elif len(ctx.expression()) == 2: # binary operators
            text = ctx.OP.text
            token = ctx.OP

            op_type = ""
            right_load_ir = None
            left_load_ir = None
            write_output = True
            left_global_var = False
            right_global_var = False

            left_type, left_cte_value, left_ir_register = self.visit(ctx.expression(0))
            right_type, right_cte_value, right_ir_register = self.visit(ctx.expression(1))

            if left_type == Type.VOID or right_type == Type.VOID:
                err("ERROR: binary operator '" + text + "' used on type void in line " + str(token.line) + " and column " + str(token.column) + "\n")
                exit(-1)

            if left_ir_register == None or right_ir_register == None:
                write_output = False

            if left_ir_register != None:
                if "@" in left_ir_register:
                    left_global_var = True    
            
            if right_ir_register != None:
                if "@" in right_ir_register:
                    right_global_var = True    

            if left_cte_value != None and right_cte_value != None and not right_global_var and not left_global_var:
                write_output = False

            if right_ir_register != left_ir_register:
                
                if left_cte_value == None or left_global_var:
                    self.output.write("%" + str(self.next_ir_register) + " = ")
                    self.output.write("load " + llvm_type(left_type) + ", " + llvm_type(left_type) + "* " + left_ir_register + ", align 4\n\t")
                    if write_output:
                        left_load_ir = "%" + str(self.next_ir_register)
                        self.next_ir_register += 1
            
                else:
                    if left_type == Type.FLOAT:
                        left_load_ir = float_to_hex(left_cte_value)
                    else:
                        left_load_ir = str(left_cte_value)

                if right_cte_value == None or right_global_var:
                    self.output.write("%" + str(self.next_ir_register) + " = ")
                    self.output.write("load " + llvm_type(right_type) + ", " + llvm_type(right_type) + "* " + right_ir_register + ", align 4\n\t")
                    if write_output:
                        right_load_ir = "%" + str(self.next_ir_register)
                        self.next_ir_register += 1
                else:
                    if right_type == Type.FLOAT:
                        right_load_ir = float_to_hex(right_cte_value)
                    else:
                        right_load_ir = str(right_cte_value)
            else:
                if left_cte_value == None or left_global_var:
                    self.output.write("%" + str(self.next_ir_register) + " = ")
                    self.output.write("load " + llvm_type(right_type) + ", " + llvm_type(right_type) + "* " + right_ir_register + ", align 4\n\t")
                    left_load_ir = right_load_ir = "%" + str(self.next_ir_register)
                    self.next_ir_register += 1
            
                else:
                    if left_type == Type.FLOAT:
                        left_load_ir = right_load_ir = float_to_hex(left_cte_value)
                    else:
                        left_load_ir = right_load_ir = str(left_cte_value)

            if text == '*' or text == '/' or text == '+' or text == '-':
                if write_output:
                    self.output.write("%" + str(self.next_ir_register) + " = ")
                    ir_register = "%" + str(self.next_ir_register)
                    self.next_ir_register += 1
                if left_type == Type.FLOAT or right_type == Type.FLOAT:
                    tyype = Type.FLOAT
                    op_type = "f"
                else:
                    tyype = Type.INT

                if left_cte_value != None and right_cte_value != None and not left_global_var and not right_global_var:
                    if text == '*':
                        cte_value = left_cte_value * right_cte_value
                        if write_output:
                            self.output.write(op_type+"mul " + llvm_type(tyype) + " ")
                    elif text == '/':
                        cte_value = left_cte_value / right_cte_value
                        if write_output:
                            self.output.write(op_type+"div " + llvm_type(tyype) + " ")
                    elif text == '+':
                        cte_value = left_cte_value + right_cte_value
                        if write_output:
                            self.output.write(op_type+"add " + llvm_type(tyype) + " ")
                    elif text == '-':
                        cte_value = left_cte_value - right_cte_value
                        if write_output:
                            self.output.write(op_type+"sub " + llvm_type(tyype) + " ")
                    if write_output:
                        self.output.write(left_load_ir + ", " + right_load_ir+"\n\t")               
                else:
                    if write_output:
                        if text == '*':
                            self.output.write(op_type+"mul " + llvm_type(tyype) + " ")
                        elif text == '/':
                            self.output.write(op_type+"div " + llvm_type(tyype) + " ")
                        elif text == '+':
                            self.output.write(op_type+"add " + llvm_type(tyype) + " ")
                        elif text == '-':
                            self.output.write(op_type+"sub " + llvm_type(tyype) + " ")
                        self.output.write(left_load_ir + ", " + right_load_ir+"\n\t")               
                    
                    cte_value = None

            else:
                tyype = Type.INT
                if left_cte_value != None and right_cte_value != None:
                    if text == '<':
                        if left_cte_value < right_cte_value:
                            cte_value = 1
                        else:
                            cte_value = 0
                    elif text == '>':
                        if left_cte_value > right_cte_value:
                            cte_value = 1
                        else:
                            cte_value = 0
                    elif text == '==':
                        if left_cte_value == right_cte_value:
                            cte_value = 1
                        else:
                            cte_value = 0
                    elif text == '!=':
                        if left_cte_value != right_cte_value:
                            cte_value = 1
                        else:
                            cte_value = 0
                    elif text == '<=':
                        if left_cte_value <= right_cte_value:
                            cte_value = 1
                        else:
                            cte_value = 0
                    elif text == '>=':
                        if left_cte_value >= right_cte_value:
                            cte_value = 1
                        else:
                            cte_value = 0
                else:
                    cte_value = None

        return tyype, cte_value, ir_register


    # Visit a parse tree produced by GrammarParser#array.
    def visitArray(self, ctx:GrammarParser.ArrayContext):
        tyype, cte_value, ir_register = self.visit(ctx.expression())
        if tyype != Type.INT:
            token = ctx.identifier().IDENTIFIER().getPayload()
            err("ERROR: array expression must be an integer, but it is " + str(tyype) + " in line " + str(token.line) + " and column " + str(token.column) + "\n")
            exit(-1)
        return cte_value, ir_register


    # Visit a parse tree produced by GrammarParser#array_literal.
    def visitArray_literal(self, ctx:GrammarParser.Array_literalContext):
        types_array = []
        cte_values_array = []
        ir_registers_array = []
        for i in range(len(ctx.expression())):
            tyype, cte_value, ir_register = self.visit(ctx.expression(i))
            types_array += [tyype]
            cte_values_array += [cte_value]
            ir_registers_array += [ir_register]
        return types_array, cte_values_array, ir_registers_array


    # Visit a parse tree produced by GrammarParser#function_call.
    def visitFunction_call(self, ctx:GrammarParser.Function_callContext):
        name = ctx.identifier().getText()
        token = ctx.identifier().IDENTIFIER().getPayload()
        try:
            tyype, args, cte_value, ir_register = self.ids_defined[name]
            if len(args) != len(ctx.expression()):
                err("ERROR: incorrect number of parameters for function '" + name + "' in line " + str(token.line) + " and column " + str(token.column) + ". Expecting " + str(len(args)) + ", but " + str(len(ctx.expression())) + " were given" + "\n")
                exit(-1)
        except:
            err("ERROR: undefined function '" + name + "' in line " + str(token.line) + " and column " + str(token.column) + "\n")
            exit(-1)
        
        self.output.write("call " + llvm_type(tyype) + " @" + name + " (")
        for i in range(len(ctx.expression())):
            arg_type, arg_cte_value, arg_ir_register = self.visit(ctx.expression(i))
            val = ""
            if(arg_type == Type.FLOAT):
                val = str(float_to_hex(arg_cte_value))
            elif(arg_type == Type.INT):
                val = str(int(arg_cte_value))
            self.output.write(llvm_type(arg_type) + " " + val)

            if i + 1 != len(ctx.expression()):
                self.output.write(", ")

            if i < len(args):
                if arg_type == Type.VOID:
                    err("ERROR: void expression passed as parameter " + str(i) + " of function '" + name + "' in line " + str(token.line) + " and column " + str(token.column) + "\n")
                    exit(-1)
                elif arg_type == Type.FLOAT and args[i] == Type.INT:
                    err("WARNING: possible loss of information converting float expression to int expression in parameter " + str(i) + " of function '" + name + "' in line " + str(token.line) + " and column " + str(token.column) + "\n")
        self.output.write(")\n\t")
        return tyype, cte_value, ir_register


    # Visit a parse tree produced by GrammarParser#arguments.
    def visitArguments(self, ctx:GrammarParser.ArgumentsContext):
        params = []
        params_name = []
        cte_value = None
        for i in range(len(ctx.identifier())):
            tyype = ctx.tyype(i).getText()
            name = ctx.identifier(i).getText()
            ir_register = "%" + name
            self.ids_defined[name] = tyype, -1, cte_value, ir_register
            params += [tyype]
            params_name.append(name)
        return params, params_name


    # Visit a parse tree produced by GrammarParser#tyype.
    def visitTyype(self, ctx:GrammarParser.TyypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#integer.
    def visitInteger(self, ctx:GrammarParser.IntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#floating.
    def visitFloating(self, ctx:GrammarParser.FloatingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#string.
    def visitString(self, ctx:GrammarParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#identifier.
    def visitIdentifier(self, ctx:GrammarParser.IdentifierContext):
        return self.visitChildren(ctx)


# warning: the use of uninitialized variables is not being warned!
