%{
#include "parser.tab.h"
#include <stdlib.h>
#include <string.h>
%}

%%
"for"                   { return FOR; }
"++"                    { return INC; }
"--"                    { return DEC; }
"=="|"<="|">="|"!="|"<"|">" { return RELOP; }
[0-9]+                  { yylval.num = atoi(yytext); return NUMBER; }
[a-zA-Z_][a-zA-Z0-9_]*  { yylval.id = strdup(yytext); return ID; }
[ \t\r\n]+              ;
"="                     { return ASSIGN; }
";"                     { return ';'; }
"("                     { return '('; }
")"                     { return ')'; }
"{"                     { return '{'; }
"}"                     { return '}'; }
"+"                     { return '+'; }
"-"                     { return '-'; }
"*"                     { return '*'; }
"/"                     { return '/'; }
.                       { return yytext[0]; }
%%

int yywrap(void) {
    return 1;
}
