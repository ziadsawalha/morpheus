''' Dict schema helper for schema-free projects '''

# lets us do from morpheus import MorpheusDict' instead of
# 'from morpheus.dict import MorphesuDict'
__all__ = ['MorpheusDict']

from .dict import MorpheusDict
