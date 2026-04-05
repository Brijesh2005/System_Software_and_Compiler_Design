%{
#include "parser.tab.h"
#include <string.h>
%}

%%
[0-9]+              { yylval.str = strdup(yytext); return NUMBER; }
[a-zA-Z_][a-zA-Z0-9_]* { yylval.str = strdup(yytext); return ID; }
[ \t\r]+            ;
\n                  { return '\n'; }
"+"                 { return '+'; }
"-"                 { return '-'; }
"*"                 { return '*'; }
"/"                 { return '/'; }
"("                 { return '('; }
")"                 { return ')'; }
.                   { return yytext[0]; }
%%

int yywrap(void) {
    return 1;
}
