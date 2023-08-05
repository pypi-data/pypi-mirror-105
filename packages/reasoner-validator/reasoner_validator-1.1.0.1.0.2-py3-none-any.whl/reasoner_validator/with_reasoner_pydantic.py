"""Build validation functions."""
from inspect import signature
import sys

from reasoner_pydantic import components


for component in components:

    def validate(obj, component=component):
        """Validate object against schema."""
        component(**obj)

    # Override signature
    sig = signature(validate)
    sig = sig.replace(parameters=tuple(sig.parameters.values())[:1])
    validate.__signature__ = sig

    validate.__name__ = f'validate_{component.__name__}'
    validate.__doc__ = (
        """Validate object against {component:s} schema.

        Parameters
        ----------
        obj : object
            Object to validate

        Raises
        ------
        `ValidationError <https://python-jsonschema.readthedocs.io/en/latest/errors/#jsonschema.exceptions.ValidationError>`_
          If the object is not a valid {component:s}.

        Examples
        --------
        >>> validate_{component:s}({{'message': {{}}}})

        """.format(
            component=component.__name__
        )
    )

    setattr(
        sys.modules[__name__],
        validate.__name__,
        validate,
    )

del validate
