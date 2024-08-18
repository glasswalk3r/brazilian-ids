"""Generic exceptions for bad formed ID's."""

from abc import abstractmethod


class InvalidIdError(ValueError):
    """Exception for an invalid ID."""

    @abstractmethod
    def id_type(self):
        """Return the ID type. Subclasses must override this method."""
        pass

    def __init__(self, id: str, message: None | str = None) -> None:
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
        msg = "A {0} must have at least {1} digits, '{2}' has only {3}".format(
            self.id_type(), expected_digits, id, len(id)
        )
        super().__init__(id=id, message=msg)
