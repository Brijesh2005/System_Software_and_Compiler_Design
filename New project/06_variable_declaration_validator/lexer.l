%{
#include "parser.tab.h"
#include <string.h>
%}

%%
"int"|"float"|"char"|"double"   { return TYPE; }
[a-zA-Z_][a-zA-Z0-9_]*          { yylval.id = strdup(yytext); return ID; }
[ \t\r\n]+                      ;
","                             { return ','; }
";"                             { return ';'; }
.                               { return yytext[0]; }
%%

int yywrap(void) {
    return 1;
}
