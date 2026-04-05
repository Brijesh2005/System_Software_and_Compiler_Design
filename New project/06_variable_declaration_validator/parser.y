%{
#include <stdio.h>
#include <stdlib.h>

int yylex(void);
void yyerror(const char *s);
%}

%union {
    char *id;
}

%token TYPE
%token <id> ID

%%
input:
    declaration  { printf("Valid variable declaration\n"); }
;

declaration:
    TYPE id_list ';'
;

id_list:
    ID               { free($1); }
  | id_list ',' ID   { free($3); }
;
%%

void yyerror(const char *s) {
    fprintf(stderr, "Invalid declaration: %s\n", s);
}

int main(void) {
    printf("Brijesh Vishwakarma - 4SF24CS404\n");
    printf("Enter a declaration statement:\n");
    yyparse();
    return 0;
}
