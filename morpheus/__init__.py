''' Dict schema helper for schema-free projects '''

# lets us do 'from morpheus import MorpheusDict' instead of
# 'from morpheus.dict import MorphesuDict'
__all__ = ['MorpheusDict', 'operations', 'Schema', 'Defn']

from .dict import MorpheusDict
from .schema import Schema
from morpheus import operations
from morpheus.operations import Defn
