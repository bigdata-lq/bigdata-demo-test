package com.demo.es;


import com.demo.es.impl.SelectSqlVo;
import com.demo.es.impl.SqlBaseVisitorImpl;
import com.demo.es.parser.SqlBaseLexer;
import com.demo.es.parser.SqlBaseParser;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.atn.PredictionMode;
import org.antlr.v4.runtime.tree.ParseTree;

public class demo1 {


    public static void main(String[] args) {
        String sql = "select name from a where city='chengdou'";
        CharStream stream = CharStreams.fromString(sql);
        SqlBaseLexer lexer1 = new SqlBaseLexer(stream);
        CommonTokenStream tokens1 = new CommonTokenStream(lexer1);
        SqlBaseParser parser1 = new SqlBaseParser(tokens1);
        parser1.getInterpreter().setPredictionMode(PredictionMode.SLL);
        parser1.removeErrorListeners(); // 移除所有错误的监听

        ParseTree tree = null;
        try {
            tree = parser1.singleStatement(); // STAGE 1
        } catch (Exception ex) {
            ex.printStackTrace();
        }

        SqlBaseVisitorImpl sqlBaseVisitor = new SqlBaseVisitorImpl();

        if (tree != null) {
            SelectSqlVo selectSqlVo = sqlBaseVisitor.visit(tree);
            System.out.println(selectSqlVo);
        }

    }

}
