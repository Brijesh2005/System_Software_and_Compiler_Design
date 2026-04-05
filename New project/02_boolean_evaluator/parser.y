%{
#include <stdio.h>

int yylex(void);
void yyerror(const char *s);
%}

%union {
    int num;
}

%token <num> BOOL
%token AND OR NOT
%type <num> expr

%left OR
%left AND
%right NOT

%%
input:
    expr '\n'   { printf("Result: %s\n", $1 ? "true" : "false"); }
;

expr:
    expr OR expr    { $$ = $1 || $3; }
  | expr AND expr   { $$ = $1 && $3; }
  | NOT expr        { $$ = !$2; }
  | '(' expr ')'    { $$ = $2; }
  | BOOL            { $$ = $1; }
;
%%

void yyerror(const char *s) {
    fprintf(stderr, "Invalid boolean expression: %s\n", s);
}

int main(void) {
    printf("Brijesh Vishwakarma - 4SF24CS404\n");
    printf("Enter boolean expression: ");
    yyparse();
    return 0;
}
