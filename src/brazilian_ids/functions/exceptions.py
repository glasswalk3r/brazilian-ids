"""Generic exceptions for bad formed ID's."""

from abc import abstractmethod


class InvalidIdError(ValueError):
    """Exception for an invalid ID."""

    @abstractmethod
    def id_type(self):
        pass

    def __init__(self, id: str, message: None | str = None) -> None:
        self.id = id

        if message is None:
            msg = f"The {self.id_type()} '{self.id}' is invalid"
            super().__init__(msg)
        else:
            super().__init__(message)


class InvalidIdLenghtError(InvalidIdError):
    """Exception for an ID that is missing some digits."""

    def __init__(self, id: str, expected_digits: int) -> None:
        msg = "A {0} must have at least {1} digits, '{2}' has only {3}".format(
            self.id_type(), expected_digits, id, len(id)
        )
        super().__init__(id=id, message=msg)
