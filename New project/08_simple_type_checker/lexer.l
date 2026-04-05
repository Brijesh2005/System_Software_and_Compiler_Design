%{
#include "parser.tab.h"
#include <stdlib.h>
#include <string.h>
%}

%%
"int"                     { return INT; }
"float"                   { return FLOAT; }
[0-9]+"."[0-9]+           { yylval.fval = (float)atof(yytext); return FVAL; }
[0-9]+                    { yylval.ival = atoi(yytext); return IVAL; }
[a-zA-Z_][a-zA-Z0-9_]*    { yylval.id = strdup(yytext); return ID; }
[ \t\r]+                  ;
\n                        { return '\n'; }
"="                       { return '='; }
";"                       { return ';'; }
"+"                       { return '+'; }
"-"                       { return '-'; }
"*"                       { return '*'; }
"/"                       { return '/'; }
"("                       { return '('; }
")"                       { return ')'; }
.                         { return yytext[0]; }
%%

int yywrap(void) {
    return 1;
}
