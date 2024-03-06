grammar Calculator;

prog : stat+;

stat:
  expr NEWLINE          # print
  | ID '=' expr NEWLINE   # assign
  | NEWLINE               # blank
  ;

expr:
  expr op=('*'|'/') expr    # MulDiv
  | expr op=('+'|'-') expr        # AddSub
  | INT                           # int
  | ID                            # id
  | '(' expr ')'                  # parenthese
  ;

MUL : '*' ;
DIV : '/' ;
ADD : '+' ;
SUB : '-' ;
ID : [a-zA-Z]+ ;
INT : [0-9]+ ;
NEWLINE :'\r'? '\n' ;
DELIMITER : ';';
WS : [ \t]+ -> skip;
