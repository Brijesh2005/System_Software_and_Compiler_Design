%{
#include "parser.tab.h"
%}

%%
"("         { return LPAREN; }
")"         { return RPAREN; }
\n          { return '\n'; }
.           { return OTHER; }
%%

int yywrap(void) {
    return 1;
}
