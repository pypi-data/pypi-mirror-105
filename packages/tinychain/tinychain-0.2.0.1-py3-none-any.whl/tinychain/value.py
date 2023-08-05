""":class:`Value` types such as :class:`Nil`, :class:`Number`, and :class:`String`."""

from .ref import OpRef
from .reflect import Meta
from .state import Scalar
from .util import uri


# Scalar value types

class Value(Scalar, metaclass=Meta):
    """A scalar `Value` which supports equality and collation."""

    __uri__ = uri(Scalar) + "/value"

    def __eq__(self, other):
        return self.eq(other)

    def __ne__(self, other):
        return self.ne(other)

    def eq(self, other):
        """Returns `true` if `self` is equal to `other`."""

        return self._get("eq", other, Bool)

    def ne(self, other):
        """Returns `true` if `self` is not equal to `other`."""

        return self._get("ne", other, Bool)


class Nil(Value):
    """A Tinychain `None` Value."""

    __uri__ = uri(Value) + "/none"


class String(Value):
    """A string."""

    __uri__ = uri(Value) + "/string"


# Numeric types

class Number(Value):
    """A numeric :class:`Value`."""

    __uri__ = uri(Value) + "/number"

    def __add__(self, other):
        return self.add(other)

    def __div__(self, other):
        return self.div(other)

    def __gt__(self, other):
        return self.gt(other)

    def __ge__(self, other):
        return self.gte(other)

    def __lt__(self, other):
        return self.lt(other)

    def __le__(self, other):
        return self.lte(other)

    def __mul__(self, other):
        return self.mul(other)

    def __radd__(self, other):
        return self.add(other)

    def __rmul__(self, other):
        return self.mul(other)

    def __sub__(self, other):
        return self.sub(other)

    def __truediv__(self, other):
        return self.div(other)

    def add(self, other):
        """Return the sum of `self` and `other`."""

        return self._get("add", other, self.__class__)

    def div(self, other):
        """Return the quotient of `self` and `other`."""

        return self._get("div", other, self.__class__)

    def gt(self, other):
        """Return true if `self` is greater than `other`."""

        return self._get("gt", other, Bool)

    def gte(self, other):
        """Return true if `self` is greater than or equal to `other`."""

        return self._get("gte", other, Bool)

    def lt(self, other):
        """Return true if `self` is less than `other`."""

        return self._get("lt", other, Bool)

    def lte(self, other):
        """Return true if `self` is less than or equal to `other`."""

        return self._get("lte", other, Bool)

    def mul(self, other):
        """Return the product of `self` and `other`."""

        return self._get("mul", other, self.__class__)

    def sub(self, other):
        """Return the difference between `self` and `other`."""

        return self._get("sub", other, self.__class__)


class Bool(Number):
    """A boolean :class:`Value`."""

    __uri__ = uri(Number) + "/bool"


class Int(Number):
    """An integer."""

    __uri__ = uri(Number) + "/int"


class UInt(Number):
    """An unsigned integer."""

    __uri__ = uri(Number) + "/uint"

