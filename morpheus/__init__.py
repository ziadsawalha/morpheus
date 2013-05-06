''' Dict schema helper for schema-free projects '''

# lets us do 'from morpheus import MorpheusDict' instead of
# 'from morpheus.dict import MorphesuDict'
__all__ = ['MorpheusDict', 'operations', 'Schema']

from .dict import MorpheusDict
from .schema import Schema
from morpheus import operations

