"""Generic exceptions for bad formed ID's."""

from abc import abstractmethod


class InvalidIdError(ValueError):
    """Exception for an invalid ID."""

    @abstractmethod
    def id_type(self):
        """Return the ID type. Subclasses must override this method."""
        pass

    def __init__(self, id: str, message: str | None = None) -> None:
        self.id_ = id

        if message is None:
            msg = f"The {self.id_type()} '{self.id_}' is invalid"
            super().__init__(msg)
        else:
            super().__init__(message)


class InvalidIdLengthError(InvalidIdError):
    """Exception for an ID that has missing digits, excluding the verification
    one in the expected number of digits."""

    def __init__(self, id: str, expected_digits: int) -> None:
        msg = f"A {self.id_type()} must have at least {expected_digits} digits, '{id}' has only {len(id)}"
        super().__init__(id=id, message=msg)
