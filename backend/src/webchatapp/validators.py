from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import string

class SymbolValidator:
    def __init__(self, number_of_symbols=1, symbols=string.punctuation):

        self.number_of_symbols = number_of_symbols
        self.symbols = symbols

    def validate(self, password, user=None):
        symbols = [char for char in password if char in self.symbols]

        if len(symbols) < self.number_of_symbols:
            raise ValidationError(
                _("Password must contain at least %(min_length)d symbols. (%(symbols)s)"),
                code='password_too_short',
                params={'min_length': self.number_of_symbols, 'symbols': self.symbols}
            )

    def get_help_text(self):
        return _(
            "Password must contain at least %(number_of_symbols) symbols."
            % {'number_of_symbols': self.number_of_symbols}
        )
    
class CapitalValidator:
    def __init__(self, number_of_capitals=1):
        self.number_of_capitals = number_of_capitals

    def validate(self, password, user=None):
        password_capitals = [char for char in password if char.isupper()]

        if len(password_capitals) < self.number_of_capitals:
            raise ValidationError(
                _("Password must contain at least %(min_length)d capital letters."),
                code='password_too_short',
                params={'min_length': self.number_of_capitals},
            )

    def get_help_text(self):
        return _(
            "Password must contain at least %(number_of_capitals)d capital letters"
            % {'number_of_capitals': self.number_of_capitals}
        )