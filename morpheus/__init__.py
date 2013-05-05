''' Dict schema helper for schema-free projects '''

# lets us do 'from morpheus import MorpheusDict' instead of
# 'from morpheus.dict import MorphesuDict'
__all__ = ['MorpheusDict', 'Schema']

from .dict import MorpheusDict

from __builtin__ import dict as Schema
