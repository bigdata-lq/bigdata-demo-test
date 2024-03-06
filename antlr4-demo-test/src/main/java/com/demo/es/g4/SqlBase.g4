grammar SqlBase;

singleStatement : statement EOF ;

statement : 'SELECT' selectElements fromClause whereExpress;

fromClause : 'FROM' tableName ;

selectElements : ID ;

tableName : ID ;

whereExpress : 'where' ID '=' ID;

ID : [a-zA-Z]+ ;

WS : [ \r\n\t]+ -> skip ;

