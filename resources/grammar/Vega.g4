grammar Vega;


block : typeIdentifier ID LBRACKET parameterStatement RBRACKET (inlineStatement | LCURLY statement RCURLY)
      ;

typeIdentifier : (CONST)? type ;

parameterStatement
	:	;

inlineStatement
	:	;

assignStatement
	:	;

whileStatement
	:	;

ifStatement
	:	;

statement
	:	assignStatement
	|	whileStatement
	|	ifStatement
	|	block
	;



expression : (MINUS term | term) (PLUS term | MINUS term)*
    ;

term :	(factor) (MULT factor | DIV factor)*
	;


factor :
           terminal
       |   LBRACKET expression RBRACKET
       ;

terminal : ID | INT | FLOAT ;
type : INT | FLOAT | STRING | CHAR ;

// Tokens
PLUS: '+';
MINUS: '-';
MULT: '*';
DIV: '/';
LBRACKET: '(';
RBRACKET: ')';
LCURLY	: '{';
RCURLY	:	'}';

// Words
CONST: 'CONST';


ID  :	('a'..'z'|'A'..'Z'|'_') ('a'..'z'|'A'..'Z'|'0'..'9'|'_')*
    ;

INT :	'0'..'9'+
    ;

FLOAT
    :   ('0'..'9')+ '.' ('0'..'9')* EXPONENT?
    |   '.' ('0'..'9')+ EXPONENT?
    |   ('0'..'9')+ EXPONENT
    ;

STRING
    :  '"' ( ESC_SEQ | ~('\\'|'"') )* '"'
    ;

CHAR:  '\'' ( ESC_SEQ | ~('\''|'\\') ) '\''
    ;

fragment
EXPONENT : ('e'|'E') ('+'|'-')? ('0'..'9')+ ;

fragment
HEX_DIGIT : ('0'..'9'|'a'..'f'|'A'..'F') ;

fragment
ESC_SEQ
    :   '\\' ('b'|'t'|'n'|'f'|'r'|'\"'|'\''|'\\')
    |   UNICODE_ESC
    |   OCTAL_ESC
    ;

fragment
OCTAL_ESC
    :   '\\' ('0'..'3') ('0'..'7') ('0'..'7')
    |   '\\' ('0'..'7') ('0'..'7')
    |   '\\' ('0'..'7')
    ;

fragment
UNICODE_ESC
    :   '\\' 'u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
    ;
