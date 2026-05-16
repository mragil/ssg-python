from enum import Enum

from htmlnode import HTMLNode, HTMLNode, ParentNode, ParentNode 
from splithelper import text_to_text_nodes
from textnode import TextNode, TextNode, TextType

class BlockType(Enum):
  PARAGRAPH = "p"
  HEADING = "h"
  CODE = "code"
  QUOTE = "blockquote"
  UNORDERED_LIST = "ul"
  ORDERED_LIST = "ol"

def block_to_block_type(block: str) -> BlockType:
    block = block.strip()
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):        
      return BlockType.HEADING
    
    if block.startswith("- "):
      if all(line.strip().startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
      
      return BlockType.PARAGRAPH
      
    if block.startswith("1. "):
      if all(line.strip().startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
      
      return BlockType.PARAGRAPH
    
    if block.startswith(">"):
      if all(line.strip().startswith(">") for line in lines):
        return BlockType.QUOTE
      
      return BlockType.PARAGRAPH
    
    if block.startswith("```") and block.endswith("```"):
      if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    return [HTMLNode.text_node_to_html_node(tn) for tn in text_nodes]

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    raise ValueError("invalid block type")

def code_to_html_node(block):
  if not block.startswith("```") or not block.endswith("```"):
      raise ValueError("invalid code block")
  text = block[4:-3]
  raw_text_node = TextNode(text, TextType.TEXT)
  child = HTMLNode.text_node_to_html_node(raw_text_node)
  code = ParentNode("code", [child])
  return ParentNode("pre", [code])

def heading_to_html_node(block):
  level = 0
  for char in block:
      if char == "#":
          level += 1
      else:
          break
  if level + 1 >= len(block):
      raise ValueError(f"invalid heading level: {level}")
  text = block[level + 1:]
  children = text_to_children(text)
  return ParentNode(f"h{level}", children)

def quote_to_html_node(block):
  lines = block.split("\n")
  new_lines = []
  for line in lines:
    if not line.startswith(">"):
      raise ValueError("invalid quote block")
    new_lines.append(line.lstrip(">").strip())
  content = " ".join(new_lines)
  children = text_to_children(content)
  return ParentNode("blockquote", children)

def ulist_to_html_node(block):
  items = block.split("\n")
  html_items = []
  for item in items:
      text = item[2:]  # remove "- "
      children = text_to_children(text)
      html_items.append(ParentNode("li", children))
  return ParentNode("ul", html_items)

def olist_to_html_node(block):
  items = block.split("\n")
  html_items = []
  for i, item in enumerate(items):
      text = item[3:]
      children = text_to_children(text)
      html_items.append(ParentNode("li", children))
  return ParentNode("ol", html_items)

def paragraph_to_html_node(block):
  lines = block.split("\n")
  paragraph = " ".join(lines)
  children = text_to_children(paragraph)
  return ParentNode("p", children)

