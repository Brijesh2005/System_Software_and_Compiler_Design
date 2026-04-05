%{
#include "parser.tab.h"
%}

%%
"&&"        { return AND; }
"||"        { return OR; }
"!"         { return NOT; }
"true"      { yylval.num = 1; return BOOL; }
"false"     { yylval.num = 0; return BOOL; }
"1"         { yylval.num = 1; return BOOL; }
"0"         { yylval.num = 0; return BOOL; }
[ \t\r]+    ;
\n          { return '\n'; }
"("         { return '('; }
")"         { return ')'; }
.           { return yytext[0]; }
%%

int yywrap(void) {
    return 1;
}
