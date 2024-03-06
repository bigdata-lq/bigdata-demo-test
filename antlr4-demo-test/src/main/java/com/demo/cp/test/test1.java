package com.demo.cp.test;

import com.demo.cp.parser.CalculatorBaseVisitor;
import com.demo.cp.parser.CalculatorLexer;
import com.demo.cp.parser.CalculatorParser;
import com.demo.cp.impl.CalculatorVistorImp;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;

public class test1 {
    public static void main(String[] args) {
        String expression = "a = 12\n" +
                "b = a * 3\n" +
                "a + b\n" +
                "a - b\n";
        CalculatorLexer lexer = new CalculatorLexer(CharStreams.fromString(expression));
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        CalculatorParser parser = new CalculatorParser(tokens);
        parser.setBuildParseTree(true);
        ParseTree root = parser.prog();
        CalculatorBaseVisitor<Integer> visitor = new CalculatorVistorImp();
        root.accept(visitor);
    }
}
