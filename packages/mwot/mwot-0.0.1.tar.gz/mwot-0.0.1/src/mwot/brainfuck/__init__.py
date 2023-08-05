"""Brainfuck language: conversions between brainfuck and MWOT bits.

Instructions are mapped to bits in the following order:
    >   000
    <   001
    +   010
    -   011
    .   100
    ,   101
    [   110
    ]   111
"""

import itertools
from ..exceptions import CompilerError
from ..util import chunks, joinable

cmds = b'><+-.,[]'
allchunks = tuple(itertools.product((0, 1), repeat=3))  # 000 001 ...
cmdmap = dict(zip(allchunks, cmds))
chunkmap = dict(zip(cmds, allchunks))
hello_world = (b'++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.++++'
               b'+++..+++.>>.<-.<.+++.------.--------.>>+.>++.')


@joinable(bytes)
def from_bits(bits):
    """Yield brainfuck instructions from MWOT bits."""
    chunk_size = 3
    for chunk in chunks(bits, chunk_size):
        if len(chunk) != chunk_size:
            raise CompilerError(f'word count not divisible by {chunk_size}')
        yield cmdmap[chunk]


@joinable()
def to_bits(chars):
    """Convert a string of brainfuck to a chain of MWOT bits."""
    for cmd in chars:
        yield from chunkmap.get(cmd, ())


from . import interpreter
