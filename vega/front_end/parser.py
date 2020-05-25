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
from vega.front_end.exception import VegaSyntaxError
from vega.front_end.lexer import Lexer
from vega.language.token import Tag
from vega.language.token import TokenType
from vega.language.token import Word
from vega.language.types import Array
from vega.language.types import String
from vega.language.types import Type


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
        self.__block()

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
        if not self.__current_token == tag:
            raise VegaSyntaxError(self.__current_token, self.__line)

    def __lookahead(self, tag: Union[Tag, str]) -> bool:
        """Look one token ahead on token stream

        Args:
            tag: tag to look for

        Returns:
            True if tag is found, otherwise False
        """
        try:
            return self.__token_stream.head.data.tag == tag
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

    def __retrieve_symbol(self, name: str) -> Tuple[Union[Symbol, None], str]:
        """Retrieve symbol from table

        Args:
            name: symbol name

        Returns:
            symbol or none if not found
        """
        return self.__table.retrieve(name)

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

    def __identifier_declaration(self, identifier: Word) -> Symbol:
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

    def __block(self) -> None:
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
            symbol: Symbol = self.__identifier_declaration(
                self.__current_token)
            symbol.callable = True
            self.__store_symbol(symbol)
            self.__match('(')
            if self.__lookahead(Tag.ID):
                self.__function_param_declaration()
            self.__match(')')
            self.__match(Tag.RETURN_TYPE)
            self.__function_return_type(symbol)
            self.__scope_statement(symbol.name)

            if not self.__lookahead(Tag.FUNC):
                loop_control = False

    def __function_param_declaration(self) -> None:
        """Parse function parameter declaration statements

        functionParameterDeclaration
            :   functionParameterDefinition (COMMA
            functionParameterDefinition)*
            ;
        """
        loop_control: bool = True
        while loop_control:
            self.__function_param_definition()

            if self.__lookahead(','):
                self.__match(',')
                self.__function_param_definition()
            else:
                loop_control = False

    def __function_param_definition(self) -> None:
        """parse function parameter definitions

        functionParameterDefinition
            :   ID COLON variableTypes (ASSIGN expression)?
            ;
        """
        self.__match(Tag.ID)
        symbol: Symbol = self.__identifier_declaration(self.__current_token)
        self.__match(':')
        self.__variable_type(symbol)

        if self.__lookahead('='):
            self.__match('=')
            self.__expression()

    def __variable_type(self, symbol: Symbol) -> None:
        """parse terminal variable types for variable definition

        variableTypes
            :   terminalVariableType (LARRAY INT RARRAY)*
            ;

        enrich identifier symbol with type information

        Args:
            symbol: identifier symbol

        Returns:

        """
        symbol: Symbol = self.__terminal_variable_types(symbol)

        while self.__lookahead('['):
            self.__match('[')
            self.__match(Tag.NUM)
            self.__match(']')
            array: Array = Array(symbol.type)
            symbol.type = array

        self.__store_symbol(symbol)

    def __function_return_type(self, symbol: Symbol) -> None:
        """Parse fucntion return types

        functionReturnType
            :   terminalVariableType (LARRAY RARRAY)*
            ;

        Args:
            symbol: identifier symbol

        Returns:

        """

        symbol: Symbol = self.__terminal_variable_types(symbol)

        while self.__lookahead('['):
            self.__match('[')
            self.__match(']')
            array: Array = Array(symbol.type)
            symbol.type = array

        self.__store_symbol(symbol)

    def __terminal_variable_types(self, symbol) -> Symbol:
        """Parse basic variable type terminal

        terminalVariableType
            :   INT_TYPE
            |   FLOAT_TYPE
            |   STRING_TYPE
            |   CHAR_TYPE
            |   BOOL_TYPE
            ;

        Args:
            symbol: symbol to set variable type for

        Returns:
            symbol with defined basic variable type
        """
        token: TokenType
        line: int
        token, line = self.__get_token()
        if token.tag == Tag.BASIC:
            symbol.type = token
        elif token.tag == Tag.TYPE:
            if token.lexeme == 'str':
                string: String = String()
                symbol.type = string
        else:
            raise VegaSyntaxError(token, line)

        return symbol

    def __scope_statement(self, scope_name: str) -> None:
        """Enter new scope

        Create new scope for statements

        scopeStatement
            :   LCURLY statement RCURLY
            ;

        Returns:

        """
        self.__match('{')
        self.__new_scope(scope_name)
        self.__statement()
        self.__match('}')
        self.__leave_scope()

    def __statement(self) -> None:
        """Parse statements

        statement
        :	(identifierStatement DELIMITER
        |   returnStatement DELIMITER
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
            self.__match('pass')
            self.__match(';')
            loop_control = False

        while loop_control:

            self.__return_statement()
            self.__while_statement()
            self.__if_statement()
            self.__identifier_statement()
            self.__loop_control_statements(Tag.CONTINUE, 'continue')
            self.__loop_control_statements(Tag.BREAK, 'break')

            if self.__lookahead(Tag.FUNC):
                self.__block()

            elif self.__lookahead('}'):
                loop_control = False

            else:
                raise VegaSyntaxError(self.__current_token, self.__line)

    def __loop_control_statements(self, tag: Tag, lexeme: str) -> None:
        """Utility function for loop control statements

        Parse loop control statements like continue or break

        Args:
            tag: to lookahead for decision making on statements
            lexeme: keyword to match token stream for

        Returns:

        """
        if self.__lookahead(tag):
            self.__match(lexeme)
            self.__match(';')

    def __identifier_statement(self) -> None:
        """Identifier statement

        Declare a one or multiple identifiers, assign to a identifier
        or call a function

        identifierStatement
        :   ID (declarationStatement | assignStatement | funcCall)
        ;

        Returns:

        """
        if self.__lookahead(Tag.ID):
            self.__match(Tag.ID)
            self.__variable_declaration()
            self.__assign_statement()
            self.__func_call()
            self.__match(';')

    def __variable_declaration(self) -> None:
        if self.__lookahead(',') or self.__lookahead(':'):
            pass

    def __assign_statement(self) -> None:
        if self.__lookahead('[') or self.__lookahead('='):
            pass

    def __func_call(self) -> None:
        if self.__lookahead('('):
            pass

    def __return_statement(self) -> None:
        if self.__lookahead(Tag.RETURN):
            pass
        self.__match(';')

    def __while_statement(self) -> None:
        if self.__lookahead(Tag.WHILE):
            pass

    def __if_statement(self) -> None:
        if self.__lookahead(Tag.IF):
            pass

    def __expression(self) -> None:
        pass
