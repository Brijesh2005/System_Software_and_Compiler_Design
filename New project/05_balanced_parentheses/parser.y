%{
#include <stdio.h>

int yylex(void);
void yyerror(const char *s);
%}

%token LPAREN RPAREN OTHER

%%
input:
    sequence '\n' { printf("Parentheses are balanced\n"); }
;

sequence:
    /* empty */
  | sequence element
;

element:
    OTHER
  | LPAREN sequence RPAREN
;
%%

void yyerror(const char *s) {
    fprintf(stderr, "Parentheses are not balanced\n");
}

int main(void) {
    printf("Brijesh Vishwakarma - 4SF24CS404\n");
    printf("Enter a string: ");
    yyparse();
    return 0;
}
