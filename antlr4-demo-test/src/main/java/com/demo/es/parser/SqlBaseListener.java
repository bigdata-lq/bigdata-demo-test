// Generated from java-escape by ANTLR 4.11.1
package com.demo.es.parser;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link SqlBaseParser}.
 */
public interface SqlBaseListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link SqlBaseParser#singleStatement}.
	 * @param ctx the parse tree
	 */
	void enterSingleStatement(SqlBaseParser.SingleStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link SqlBaseParser#singleStatement}.
	 * @param ctx the parse tree
	 */
	void exitSingleStatement(SqlBaseParser.SingleStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link SqlBaseParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterStatement(SqlBaseParser.StatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link SqlBaseParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitStatement(SqlBaseParser.StatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link SqlBaseParser#fromClause}.
	 * @param ctx the parse tree
	 */
	void enterFromClause(SqlBaseParser.FromClauseContext ctx);
	/**
	 * Exit a parse tree produced by {@link SqlBaseParser#fromClause}.
	 * @param ctx the parse tree
	 */
	void exitFromClause(SqlBaseParser.FromClauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link SqlBaseParser#selectElements}.
	 * @param ctx the parse tree
	 */
	void enterSelectElements(SqlBaseParser.SelectElementsContext ctx);
	/**
	 * Exit a parse tree produced by {@link SqlBaseParser#selectElements}.
	 * @param ctx the parse tree
	 */
	void exitSelectElements(SqlBaseParser.SelectElementsContext ctx);
	/**
	 * Enter a parse tree produced by {@link SqlBaseParser#tableName}.
	 * @param ctx the parse tree
	 */
	void enterTableName(SqlBaseParser.TableNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link SqlBaseParser#tableName}.
	 * @param ctx the parse tree
	 */
	void exitTableName(SqlBaseParser.TableNameContext ctx);
	/**
	 * Enter a parse tree produced by {@link SqlBaseParser#whereExpress}.
	 * @param ctx the parse tree
	 */
	void enterWhereExpress(SqlBaseParser.WhereExpressContext ctx);
	/**
	 * Exit a parse tree produced by {@link SqlBaseParser#whereExpress}.
	 * @param ctx the parse tree
	 */
	void exitWhereExpress(SqlBaseParser.WhereExpressContext ctx);
}