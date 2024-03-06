package com.demo.es.impl;

import com.demo.es.parser.SqlBaseParser;
import com.demo.es.parser.SqlBaseVisitor;
import org.antlr.v4.runtime.tree.AbstractParseTreeVisitor;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.TerminalNode;


import java.util.ArrayList;

/**
 * 此处代码需要结合antlr 语法树来写
 */
public class SqlBaseVisitorImpl extends AbstractParseTreeVisitor<SelectSqlVo> implements SqlBaseVisitor<SelectSqlVo> {

    private SelectSqlVo selectSql;

    public SqlBaseVisitorImpl() {
        this.selectSql = new SelectSqlVo();
        selectSql.setFields(new ArrayList<>());
    }

    @Override
    public SelectSqlVo visit(ParseTree tree) {
        int childCount = tree.getChildCount();
        for (int i = 0; i < childCount; i++) {
            ParseTree child = tree.getChild(i);
            if (child instanceof SqlBaseParser.StatementContext) {
                SqlBaseParser.StatementContext statementContext = (SqlBaseParser.StatementContext) child;
                System.out.println("statementContext");
                handlerWithStatement(statementContext);
            }
        }
        return selectSql;
    }

    private void handlerWithStatement(SqlBaseParser.StatementContext statementContext) {

        int childCount = statementContext.getChildCount(); // 必定以select开头
        int i = 0;
        for (; i < childCount; i++) {
            ParseTree child = statementContext.getChild(i);
            if (child instanceof SqlBaseParser.SelectElementsContext) {
                System.out.println("SelectElementsContext");
                this.visitSelectElements((SqlBaseParser.SelectElementsContext)child);
            } else if (child instanceof SqlBaseParser.FromClauseContext) {
                System.out.println("FromClauseContext");
                this.visitFromClause((SqlBaseParser.FromClauseContext)child);
            } else if (child instanceof TerminalNode) {
                selectSql.setStartToken(child.getText());; // 这个就是SELECT
                // System.out.println("TerminalNode==>" + terminalNode);
            } else if (child instanceof SqlBaseParser.WhereExpressContext) {
                this.visitWhereExpress((SqlBaseParser.WhereExpressContext)child);
            }

        }
    }

    @Override
    public SelectSqlVo visitSingleStatement(SqlBaseParser.SingleStatementContext ctx) {
        return null;
    }

    @Override
    public SelectSqlVo visitStatement(SqlBaseParser.StatementContext ctx) {
        return null;
    }

    @Override
    public SelectSqlVo visitFromClause(SqlBaseParser.FromClauseContext ctx) {
        selectSql.setTableName(ctx.getChild(1).getText());
        selectSql.setFrom(true);
        return selectSql;
    }

    @Override
    public SelectSqlVo visitSelectElements(SqlBaseParser.SelectElementsContext ctx) {
        selectSql.getFields().add(ctx.getText());// 这里应该是有多个
        return selectSql;
    }

    @Override
    public SelectSqlVo visitTableName(SqlBaseParser.TableNameContext ctx) {
        return null;
    }

    @Override
    public SelectSqlVo visitWhereExpress(SqlBaseParser.WhereExpressContext ctx) {
        return null;
    }
}
