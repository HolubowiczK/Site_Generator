from textnode import TextNode, TextType
from extractfunctions import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        splitted_nodes = node.text.split(delimiter)
        if len(splitted_nodes) == 1:
            new_nodes.append(node)
            continue
        if len(splitted_nodes)%2 == 0:
            raise Exception("Delimiter not found")
        for i in range(0, len(splitted_nodes)):
            if i%2 == 0:
                new_nodes.append(TextNode(splitted_nodes[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(splitted_nodes[i], text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        
        text = node.text        
        for match in matches:
            image_alt, image_url = match
            match_string = f"![{image_alt}]({image_url})"
            split_text = text.split(match_string, 1)
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            text = split_text[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        for match in matches:
            link_text, link_url = match
            match_string = f"[{link_text}]({link_url})"
            split_text = text.split(match_string, 1)
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            text = split_text[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes



def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
