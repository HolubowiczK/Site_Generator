import re
from htmlnode import ParentNode
from textnode import TextNode, TextType
from texttohtml import text_node_to_html_node
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from mdtoblocks import BlockType, block_to_block_type, markdown_to_blocks


def text_to_children(text):
    # text -> textnodes -> htmlnodes
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                num_hashes = len(block) - len(block.lstrip("#"))
                cleaned = re.sub(r"^#{1,6} ", "", block)
                nodes = text_to_children(cleaned)
                children.append(ParentNode(f"h{num_hashes}", nodes))
            case BlockType.CODE:
                cleaned = re.sub(r"^```\n", "", block)
                cleaned = re.sub(r"```$", "", cleaned)
                node = TextNode(cleaned, TextType.CODE)
                html_node = text_node_to_html_node(node)
                children.append(ParentNode("pre", [html_node]))
            case BlockType.QUOTE:
                splitted = block.split("\n")
                splitted = list(map(lambda line: re.sub(r"^> ", "", line), splitted))
                joined = " ".join(splitted)
                nodes = text_to_children(joined)
                children.append(ParentNode("blockquote", nodes))
            case BlockType.UNORDERED_LIST:
                splitted = block.split("\n")
                nodes = []
                for line in splitted:
                    line = re.sub(r"^- ", "", line)
                    line_nodes = text_to_children(line)
                    nodes.append(ParentNode("li", line_nodes))
                children.append(ParentNode("ul", nodes))
            case BlockType.ORDERED_LIST:
                splitted = block.split("\n")
                nodes = []
                for line in splitted:
                    line = re.sub(r"^([0-9]+)\. ", "", line)
                    line_nodes = text_to_children(line)
                    nodes.append(ParentNode("li", line_nodes))
                children.append(ParentNode("ol", nodes))
            case BlockType.PARAGRAPH:
                cleaned = block.replace("\n", " ")
                nodes = text_to_children(cleaned)
                children.append(ParentNode("p", nodes))
            case _:
                raise ValueError(f"Unknown block type: {block_type}")
    return ParentNode("div", children)

