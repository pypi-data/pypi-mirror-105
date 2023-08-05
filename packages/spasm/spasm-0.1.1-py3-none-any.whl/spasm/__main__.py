"""
Run the entrypoint method.

Used in cases where the shell cannot be trusted to use the right python version,
in which case '/path/to/python -m spasm' can be used as an alternative.
"""

import spasm

spasm.main()
