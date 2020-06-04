"""Vega parser

Check syntax of Vega program code. Return syntax errors on invalid syntax.
Create AST for further code analysis.
"""

from io import TextIOWrapper
from typing import Tuple
from typing import Union

from vega.data_structs.symbol_table import Symbol
from vega.data_structs.symbol_table import SymbolTable
from vega.data_structs.token_stream import TokenStream
from vega.front_end.exception import VegaAlreadyDefinedError
from vega.front_end.exception import VegaNoCallableError
from vega.front_end.exception import VegaNotAssignError
from vega.front_end.exception import VegaNotYetDefinedError
from vega.front_end.exception import VegaSyntaxError
from vega.front_end.lexer import Lexer
from vega.language.token import Tag
from vega.language.token import TokenType
from vega.language.token import Word
from vega.language.types import Array
from vega.language.types import String
from vega.language.types import Type
from vega.utils.data_types.lists import Queue


# pylint: disable=too-few-public-methods
class Parser:
    """Parser class

    Parses vega code. Calls lexer on initialization.

    """

    def __init__(self, code: TextIOWrapper) -> None:
        """Init method

        Call lexer on init of class and declare needed properties for parsing

        Args:
            code: Vega program code file
        """
        lexer: Lexer = Lexer(code)
        self.__token_stream: TokenStream = lexer.scan()
        self.__current_token: TokenType
        self.__table: SymbolTable = SymbolTable()
        self.__line: int = 0

    @staticmethod
    def __create_symbol(**kwargs) -> Symbol:
        """Create symbol

        Symbol for storing identifier in symbol table with additional
        information

        Args:
            **kwargs: name of identifier, if const, type and tag

        Returns:
            symbol
        """
        name: str = kwargs.pop('name')
        const: bool = kwargs.pop('const')
        call_able: bool = kwargs.pop('callable')
        identifier_type: Union[Type, None] = kwargs.pop('type')
        return Symbol(name, const, call_able, identifier_type)

    def parse(self) -> None:
        """Call parse method to start parsing

        Returns:

        """
        self.__parse_block()

    def __get_token(self) -> Tuple[TokenType, int]:
        """Retrieve token from token stream"""
        return self.__token_stream.remove()

    def __match(self, tag: Union[Tag, str]) -> None:
        """Match given tag

        Retrieve next token from token stream and set current token and line.
        Then match current token against given tag.

        Args:
            tag: to match for

        Returns:
            True if tag matches against current token tag, False otherwise
        """
        self.__current_token, self.__line = self.__get_token()
        if not self.__current_token.tag == tag:
            raise VegaSyntaxError(self.__current_token,
                                  self.__token_stream.head.data.token,
                                  self.__line)

    def __lookahead(self, tag: Union[Tag, str]) -> bool:
        """Look one token ahead on token stream

        Args:
            tag: tag to look for

        Returns:
            True if tag is found, otherwise False
        """
        try:
            return self.__token_stream.head.data.token.tag == tag
        except AttributeError:
            return False

    def __lookup_symbol(self, name: str) -> bool:
        """Lookup name in data_structs table

        Search for given identifier name in data_structs table

        Args:
            name: identifier name

        Returns:
            True if identifier name is found, false otherwise
        """
        return self.__table.lookup(name)

    def __retrieve_symbol(self, identifier: Word) -> Tuple[Symbol, str]:
        """Retrieve symbol from table

        Args:
            identifier: identifier

        Returns:
            symbol or none if not found
        """
        if self.__lookup_symbol(identifier.lexeme):
            return self.__table.retrieve(identifier.lexeme)
        raise VegaNotYetDefinedError(identifier.lexeme, self.__line)

    def __new_scope(self, scope_name) -> None:
        """Create new scope in hashtable

        Args:
            scope_name: name of scope

        Returns:

        """
        self.__table.enter_scope(scope_name)

    def __leave_scope(self) -> None:
        """Leave scope

        Returns:

        """
        self.__table.leave_scope()

    def __store_symbol(self, symbol: Symbol) -> None:
        """Store symbol in symbol table

        Args:
            symbol: symbol to store

        """
        self.__table.store(symbol)

    def __identifier_declared(self, identifier: Word) -> Symbol:
        """Recognize identifier

        Validates if identifier has already been declared and return Symbol
        object to be stored in symbol table.

        Args:
            identifier: identifier to check for

        Returns:
            symbol to be stored in symbol table
        """
        if not self.__lookup_symbol(identifier.lexeme):
            symbol: Symbol = self.__create_symbol(
                name=identifier.lexeme,
                const=False,
                callable=False,
                type=None)
            return symbol
        raise VegaAlreadyDefinedError(identifier, self.__line)

    def __parse_block(self) -> None:
        """Parse block statements

        block
            :   (FUNC ID LBRACKET functionParameterDeclaration? RBRACKET
            RETURN_TYPE functionReturnType scopeStatement)+ EOF
        ;

        Returns:

        """

        loop_control: bool = True
        while loop_control:

            self.__match(Tag.FUNC)
            self.__match(Tag.ID)
            symbol: Symbol = self.__identifier_declared(
                self.__current_token)
            symbol.callable = True
            self.__store_symbol(symbol)
            self.__new_scope(symbol.name)
            self.__match('(')
            if self.__lookahead(Tag.ID):
                self.__parse_function_param_declaration()
            self.__match(')')
            self.__match(Tag.RETURN_TYPE)
            self.__parse_function_return_type(symbol)
            self.__parse_scope_statement(symbol.name)
            self.__leave_scope()

            if not self.__lookahead(Tag.FUNC):
                loop_control = False

    def __parse_function_param_declaration(self) -> None:
        """Parse function parameter declaration statements

        functionParameterDeclaration
            :   functionParameterDefinition (COMMA
            functionParameterDefinition)*
            ;
        """
        loop_control: bool = True
        while loop_control:
            self.__parse_function_param_definition()

            if self.__lookahead(','):
                self.__match(',')
            else:
                loop_control = False

    def __parse_function_param_definition(self) -> None:
        """parse function parameter definitions

        functionParameterDefinition
            :   ID COLON variableTypes (ASSIGN expression)?
            ;
        """
        # ID COLON variableTypes
        self.__match(Tag.ID)
        symbol: Symbol = self.__identifier_declared(self.__current_token)
        self.__match(':')
        self.__parse_variable_type(symbol)

        # (ASSIGN expression)?
        if self.__lookahead('='):
            self.__match('=')
            self.__parse_expression()

    def __parse_variable_type(self, symbol: Symbol) -> None:
        """parse terminal variable types for variable definition

        variableTypes
            :   terminalVariableType (LARRAY INT RARRAY)*
            ;

        enrich identifier symbol with type information

        Args:
            symbol: identifier symbol

        Returns:

        """
        symbol: Symbol = self.__parse_terminal_variable_types(symbol)

        while self.__lookahead('['):
            self.__match('[')
            self.__match(Tag.NUM)
            self.__match(']')
            array: Array = Array(symbol.type)
            symbol.type = array

        self.__store_symbol(symbol)

    def __parse_function_return_type(self, symbol: Symbol) -> None:
        """Parse fucntion return types

        functionReturnType
            :   terminalVariableType (LARRAY RARRAY)*
            ;

        Args:
            symbol: identifier symbol

        Returns:

        """

        symbol: Symbol = self.__parse_terminal_variable_types(symbol)

        while self.__lookahead('['):
            self.__match('[')
            self.__match(']')
            array: Array = Array(symbol.type)
            symbol.type = array

        self.__store_symbol(symbol)

    def __parse_terminal_variable_types(self, symbol) -> Symbol:
        """Parse basic variable type terminal

        terminalVariableType
            :   INT_TYPE
            |   FLOAT_TYPE
            |   CHAR_TYPE
            |   BOOL_TYPE
            |   STRING_TYPE
            ;

        Args:
            symbol: symbol to set variable type for

        Returns:
            symbol with defined basic variable type
        """
        # INT_TYPE | FLOAT_TYPE | CHAR_TYPE | BOOL_TYPE
        if self.__lookahead(Tag.BASIC):
            self.__match(Tag.BASIC)
            symbol.type = self.__current_token
        # STRING_TYPE
        elif self.__lookahead(Tag.TYPE):
            self.__match(Tag.TYPE)
            if self.__current_token.lexeme == 'str':
                symbol.type = String()

        return symbol

    def __parse_scope_statement(self, scope_name: str) -> None:
        """Enter new scope

        Create new scope for statements

        scopeStatement
            :   LCURLY statement RCURLY
            ;

        Returns:

        """
        self.__match('{')
        self.__new_scope(scope_name)
        self.__parse_statement()
        self.__match('}')
        self.__leave_scope()

    def __parse_statement(self) -> None:
        """Parse statements

        statement
        :	(identifierStatement
        |   returnStatement
        |   CONTINUE DELIMITER
        |   BREAK DELIMITER
        |	whileStatement
        |	ifStatement
        |	block)+
        |   PASS DELIMITER
        ;

        Returns:

        """

        loop_control: bool = True

        if self.__lookahead(Tag.PASS):
            self.__match(Tag.PASS)
            self.__match(';')
            loop_control = False

        while loop_control:

            self.__parse_identifier_statement()
            self.__parse_return_statement()
            self.__parse_loop_control_statements(Tag.BREAK)
            self.__parse_loop_control_statements(Tag.CONTINUE)
            self.__parse_while_statement()
            self.__parse_if_statement()

            if self.__lookahead(Tag.FUNC):
                self.__parse_block()

            elif self.__lookahead('}'):
                loop_control = False

    def __parse_loop_control_statements(self, tag: Tag) -> None:
        """Utility function for loop control statements

        Parse loop control statements like continue or break

        Args:
            tag: to lookahead for decision making on statements

        Returns:

        """
        if self.__lookahead(tag):
            self.__match(tag)
            self.__match(';')

    def __parse_identifier_statement(self) -> None:
        """Identifier statement

        Declare a one or multiple identifiers, assign to a identifier
        or call a function

        identifierStatement
        :   ID (declarationStatement | assignStatement | funcCall) DELIMITER
        ;

        Returns:

        """
        if self.__lookahead(Tag.ID):
            self.__match(Tag.ID)
            # declarationStatement
            if self.__lookahead(',') or self.__lookahead(':'):
                self.__parse_declaration_statement()
            # assignStatement
            elif self.__lookahead('[') or self.__lookahead('='):
                self.__parse_assign_statement()
            # funcCall
            elif self.__lookahead('('):
                self.__parse_func_call()
            else:
                return
            self.__match(';')

    def __parse_declaration_statement(self) -> None:
        """Declare new variables

        Can be declaration statement or declaration and assignment.
        In one line multiple variables can be declared with the same type
        and the same value.

        Multiple variables are collected in a queue and later for each symbol
        element in the queue the correct symbols with variables types are
        stored in the symbol table.

        declarationStatement
        :   (COMMA ID)* COLON (CONST)? variableType (ASSIGN expression)?
        ;

        Returns:

        """

        symbol_queue: Queue = Queue()
        const_flag: bool = False
        first_identifier: Word = self.__current_token
        symbol_queue.add(self.__identifier_declared(first_identifier))

        # (COMMA ID)*
        while self.__lookahead(','):
            self.__match(',')
            self.__match(Tag.ID)
            symbol_queue.add(self.__identifier_declared(
                self.__current_token))

        # COLON (CONST)?
        self.__match(':')
        if self.__lookahead(Tag.CONST):
            self.__match(Tag.CONST)
            const_flag = True

        symbol: Symbol = symbol_queue.remove()
        symbol.const = const_flag
        self.__parse_variable_type(symbol)

        symbol, _ = self.__retrieve_symbol(first_identifier)
        symbol_type: Type = symbol.type

        # variableType
        while not symbol_queue.is_empty():
            symbol = symbol_queue.remove()
            symbol.const = const_flag
            symbol.type = symbol_type
            self.__store_symbol(symbol)

        # (ASSIGN expression)?
        if self.__lookahead('='):
            self.__match('=')
            self.__parse_expression()

    def __parse_assign_statement(self) -> None:
        """Assign expression to identifier or array element

        assignStatement
            :   (arrayAccess)? ASSIGN expression
            ;

        Returns:

        """

        symbol: Symbol
        symbol, _ = self.__retrieve_symbol(self.__current_token)

        if symbol.callable or symbol.const:
            raise VegaNotAssignError(self.__current_token, self.__line)

        self.__parse_array_access()

        self.__match('=')
        self.__parse_expression()

    def __parse_array_access(self) -> None:
        """Access element in array

        arrayAccess
            :   LARRAY expression RARRAY
            ;

        Returns:

        """
        if self.__lookahead('['):
            self.__match('[')
            self.__parse_expression()
            self.__match(']')

    def __parse_func_call(self) -> None:
        """Call function

        Verify if identifier is declared and callable

        funcCall
            :   LBRACKET ( expression (COMMA expression)*)? RBRACKET
            ;

        Returns:

        """

        symbol: Symbol
        symbol, _ = self.__retrieve_symbol(self.__current_token)
        if not symbol.callable:
            raise VegaNoCallableError(self.__current_token, self.__line)
        self.__match('(')
        if not self.__lookahead(')'):
            self.__parse_expression()

            # (COMMA expression)*
            while self.__lookahead(','):
                self.__match(',')
                self.__parse_expression()
        self.__match(')')

    def __parse_return_statement(self) -> None:
        """Return expression to caller

        returnStatement
            :   RETURN expression
            ;

        Returns:

        """
        if self.__lookahead(Tag.RETURN):
            self.__match(Tag.RETURN)
            self.__parse_expression()
            self.__match(';')

    def __parse_while_statement(self) -> None:
        """while loop

        whileStatement
            :   WHILE conditionalScope
            ;

        Returns:

        """
        if self.__lookahead(Tag.WHILE):
            self.__match(Tag.WHILE)
            self.__parse_conditional_scope('WHILE')

    def __parse_if_statement(self) -> None:
        """if clause

        ifStatement
            :   IF conditionalScope
                (ELIF conditionalScope)*
                (ELSE scopeStatement)?
            ;

        Returns:

        """

        #  IF conditionalScope
        if self.__lookahead(Tag.IF):
            self.__match(Tag.IF)
            self.__parse_conditional_scope('IF')

        # (ELIF conditionalScope)*
        while self.__lookahead(Tag.ELIF):
            self.__match(Tag.ELIF)
            self.__parse_conditional_scope('ELIF')

        #  (ELSE scopeStatement)?
        if self.__lookahead(Tag.ELSE):
            self.__match(Tag.ELSE)
            self.__parse_scope_statement('ELSE')

    def __parse_conditional_scope(self, scope_name: str) -> None:
        """conditional scope

        conditionalScope
            :   LBRACKET expression RBRACKET scopeStatement
            ;

        Returns:

        """
        self.__match('(')
        self.__parse_expression()
        self.__match(')')
        self.__parse_scope_statement(scope_name)

    def __parse_expression(self) -> None:
        """expressions

        expression
            :   term (PLUS term | MINUS term | OR term)*
            ;

        Returns:

        """

        # term
        self.__parse_term()

        # (PLUS term | MINUS term | OR term)*
        while self.__parse_expression_operands():
            self.__parse_term()

    def __parse_expression_operands(self) -> bool:
        """parse expression operands

        Returns:
            true on match, false otherwise
        """
        if self.__lookahead('+'):
            self.__match('+')
            return True
        if self.__lookahead('-'):
            self.__match('-')
            return True
        if self.__lookahead(Tag.OR):
            self.__match(Tag.OR)
            return True
        if self.__lookahead(Tag.BOOL_OR):
            self.__match(Tag.BOOL_OR)
            return True
        return False

    def __parse_term(self) -> None:
        """terms

        term
            :	factor (MULT factor | DIV factor| AND factor)*
            ;

        Returns:

        """
        # factor
        self.__parse_factor()

        # (MULT factor | DIV factor| AND factor)*
        while self.__parse_term_operands():
            self.__parse_factor()

    def __parse_term_operands(self) -> bool:
        """parse term operands

        Returns:
            true if operand matches, false otherwise

        """
        if self.__lookahead('*'):
            self.__match('*')
            return True
        if self.__lookahead('/'):
            self.__match('/')
            return True
        if self.__lookahead(Tag.AND):
            self.__match(Tag.AND)
            return True
        if self.__lookahead(Tag.BOOL_AND):
            self.__match(Tag.BOOL_AND)
            return True
        return False

    def __parse_factor(self) -> None:
        """factors

        factor
            :   NOT? MINUS? unary (comparisonOperator unary)*
            ;

        Returns:

        """

        # (MINUS | NOT) unary
        if self.__lookahead(Tag.NOT):
            self.__match(Tag.NOT)
        if self.__lookahead('-'):
            self.__match('-')
        self.__parse_unary()

        # unary (comparisonOperator unary)*
        while self.__parse_unary_operands():
            self.__parse_unary()

    # pylint: disable=R0911
    def __parse_unary_operands(self) -> bool:
        """parse unary operands

        Returns:
            true on match, false otherwise
        """
        if self.__lookahead(Tag.EQ):
            self.__match(Tag.EQ)
            return True
        if self.__lookahead(Tag.NE):
            self.__match(Tag.NE)
            return True
        if self.__lookahead(Tag.GE):
            self.__match(Tag.GE)
            return True
        if self.__lookahead(Tag.LE):
            self.__match(Tag.LE)
            return True
        if self.__lookahead('>'):
            self.__match('>')
            return True
        if self.__lookahead('<'):
            self.__match('<')
            return True
        return False

    def __parse_unary(self) -> None:
        """unaries

        unary
            :   terminal
            |   ID (arrayAccess)? // potential array access
            |   ID funcCall
            |   LBRACKET expression RBRACKET
            |   LARRAY (expression (COMMA expression)*)? RARRAY
            ;

        Returns:
        """

        # terminal
        if self.__parse_word_terminals():
            return
        if self.__parse_literal_terminal():
            return

        # ID (arrayAccess)? | ID funcCall
        if self.__lookahead(Tag.ID):
            self.__match(Tag.ID)
            self.__retrieve_symbol(self.__current_token)
            if self.__lookahead('['):
                self.__parse_array_access()
            elif self.__lookahead('('):
                self.__parse_func_call()

        # LBRACKET expression RBRACKET
        elif self.__lookahead('('):
            self.__match('(')
            self.__parse_expression()
            self.__match(')')

        # LARRAY (expression (COMMA expression)*)? RARRAY
        elif self.__lookahead('['):
            self.__match('[')
            self.__parse_expression()
            while self.__lookahead(','):
                self.__match(',')
                self.__parse_expression()
            self.__match(']')

    def __parse_word_terminals(self) -> bool:
        """parse terminal words

        Parse booleans and numbers

        Returns:
            true on terminal match, false otherwise
        """
        if self.__lookahead(Tag.NUM):
            self.__match(Tag.NUM)
            return True
        if self.__lookahead(Tag.REAL):
            self.__match(Tag.REAL)
            return True
        if self.__lookahead(Tag.TRUE):
            self.__match(Tag.TRUE)
            return True
        if self.__lookahead(Tag.FALSE):
            self.__match(Tag.FALSE)
            return True
        return False

    def __parse_literal_terminal(self) -> bool:
        """parse literals

        Returns:
            true on terminal match, false otherwise
        """
        if self.__lookahead('\''):
            self.__match('\'')
            self.__match(Tag.LITERAL)
            self.__match('\'')
            return True
        if self.__lookahead('"'):
            self.__match('"')
            self.__match(Tag.LITERAL)
            self.__match('"')
            return True
        return False
