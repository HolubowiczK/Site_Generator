from enum import Enum
import re

def markdown_to_blocks(markdown):
    splited = markdown.split("\n\n")
    blocks = []
    for block in splited:
        block = block.strip()
        if block:
            blocks.append(block)
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"



def block_to_block_type(block):
    if re.match(r"^#{1,6} (.*)$", block):
        return BlockType.HEADING
    elif re.match(r"^```\n.*```$", block, re.DOTALL):
        return BlockType.CODE
    elif all(re.match(r"^>.*$", line) for line in block.splitlines()):
        return BlockType.QUOTE
    elif all(re.match(r"^- ", line) for line in block.splitlines()):
        return BlockType.UNORDERED_LIST
    elif all(re.match(r"^([0-9]+)\. (.*)$", line) and int(re.match(r"^([0-9]+)\. (.*)$", line).group(1)) == i for i, line in enumerate(block.splitlines(), start=1)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
