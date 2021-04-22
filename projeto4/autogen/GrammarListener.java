// Generated from autogen/Grammar.g4 by ANTLR 4.7.2
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link GrammarParser}.
 */
public interface GrammarListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link GrammarParser#fiile}.
	 * @param ctx the parse tree
	 */
	void enterFiile(GrammarParser.FiileContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#fiile}.
	 * @param ctx the parse tree
	 */
	void exitFiile(GrammarParser.FiileContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#function_definition}.
	 * @param ctx the parse tree
	 */
	void enterFunction_definition(GrammarParser.Function_definitionContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#function_definition}.
	 * @param ctx the parse tree
	 */
	void exitFunction_definition(GrammarParser.Function_definitionContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#body}.
	 * @param ctx the parse tree
	 */
	void enterBody(GrammarParser.BodyContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#body}.
	 * @param ctx the parse tree
	 */
	void exitBody(GrammarParser.BodyContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterStatement(GrammarParser.StatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitStatement(GrammarParser.StatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#if_statement}.
	 * @param ctx the parse tree
	 */
	void enterIf_statement(GrammarParser.If_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#if_statement}.
	 * @param ctx the parse tree
	 */
	void exitIf_statement(GrammarParser.If_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#else_statement}.
	 * @param ctx the parse tree
	 */
	void enterElse_statement(GrammarParser.Else_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#else_statement}.
	 * @param ctx the parse tree
	 */
	void exitElse_statement(GrammarParser.Else_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#for_loop}.
	 * @param ctx the parse tree
	 */
	void enterFor_loop(GrammarParser.For_loopContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#for_loop}.
	 * @param ctx the parse tree
	 */
	void exitFor_loop(GrammarParser.For_loopContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#for_initializer}.
	 * @param ctx the parse tree
	 */
	void enterFor_initializer(GrammarParser.For_initializerContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#for_initializer}.
	 * @param ctx the parse tree
	 */
	void exitFor_initializer(GrammarParser.For_initializerContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#for_condition}.
	 * @param ctx the parse tree
	 */
	void enterFor_condition(GrammarParser.For_conditionContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#for_condition}.
	 * @param ctx the parse tree
	 */
	void exitFor_condition(GrammarParser.For_conditionContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#for_step}.
	 * @param ctx the parse tree
	 */
	void enterFor_step(GrammarParser.For_stepContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#for_step}.
	 * @param ctx the parse tree
	 */
	void exitFor_step(GrammarParser.For_stepContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#variable_definition}.
	 * @param ctx the parse tree
	 */
	void enterVariable_definition(GrammarParser.Variable_definitionContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#variable_definition}.
	 * @param ctx the parse tree
	 */
	void exitVariable_definition(GrammarParser.Variable_definitionContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#variable_assignment}.
	 * @param ctx the parse tree
	 */
	void enterVariable_assignment(GrammarParser.Variable_assignmentContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#variable_assignment}.
	 * @param ctx the parse tree
	 */
	void exitVariable_assignment(GrammarParser.Variable_assignmentContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterExpression(GrammarParser.ExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitExpression(GrammarParser.ExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#array}.
	 * @param ctx the parse tree
	 */
	void enterArray(GrammarParser.ArrayContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#array}.
	 * @param ctx the parse tree
	 */
	void exitArray(GrammarParser.ArrayContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#array_literal}.
	 * @param ctx the parse tree
	 */
	void enterArray_literal(GrammarParser.Array_literalContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#array_literal}.
	 * @param ctx the parse tree
	 */
	void exitArray_literal(GrammarParser.Array_literalContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#function_call}.
	 * @param ctx the parse tree
	 */
	void enterFunction_call(GrammarParser.Function_callContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#function_call}.
	 * @param ctx the parse tree
	 */
	void exitFunction_call(GrammarParser.Function_callContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#arguments}.
	 * @param ctx the parse tree
	 */
	void enterArguments(GrammarParser.ArgumentsContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#arguments}.
	 * @param ctx the parse tree
	 */
	void exitArguments(GrammarParser.ArgumentsContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#tyype}.
	 * @param ctx the parse tree
	 */
	void enterTyype(GrammarParser.TyypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#tyype}.
	 * @param ctx the parse tree
	 */
	void exitTyype(GrammarParser.TyypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#integer}.
	 * @param ctx the parse tree
	 */
	void enterInteger(GrammarParser.IntegerContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#integer}.
	 * @param ctx the parse tree
	 */
	void exitInteger(GrammarParser.IntegerContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#floating}.
	 * @param ctx the parse tree
	 */
	void enterFloating(GrammarParser.FloatingContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#floating}.
	 * @param ctx the parse tree
	 */
	void exitFloating(GrammarParser.FloatingContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#string}.
	 * @param ctx the parse tree
	 */
	void enterString(GrammarParser.StringContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#string}.
	 * @param ctx the parse tree
	 */
	void exitString(GrammarParser.StringContext ctx);
	/**
	 * Enter a parse tree produced by {@link GrammarParser#identifier}.
	 * @param ctx the parse tree
	 */
	void enterIdentifier(GrammarParser.IdentifierContext ctx);
	/**
	 * Exit a parse tree produced by {@link GrammarParser#identifier}.
	 * @param ctx the parse tree
	 */
	void exitIdentifier(GrammarParser.IdentifierContext ctx);
}