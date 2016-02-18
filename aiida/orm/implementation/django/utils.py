# -*- coding: utf-8 -*-

from aiida.orm.implementation.django.computer import Computer

from aiida.common.exceptions import InvalidOperation

def delete_computer(computer):
    """
    Delete a computer from the DB.
    It assumes that the DB backend does the proper checks and avoids
    to delete computers that have nodes attached to them.

    Implemented as a function on purpose, otherwise complicated logic would be
    needed to set the internal state of the object after calling
    computer.delete().
    """
    if not isinstance(computer, Computer):
        raise TypeError("computer must be an instance of "
                        "aiida.orm.computer.Computer")

    # TODO: abstract the ProtectedError, to the corresponding one with
    # SQLAlchemy. This will probably be a bit tedious because the error from
    # SQLAlchemy don't expose the error.
    from django.db.models.deletion import ProtectedError
    try:
        computer.dbcomputer.delete()
    except ProtectedError:
        raise InvalidOperation("Unable to delete the requested computer: there"
                               "is at least one node using this computer")
