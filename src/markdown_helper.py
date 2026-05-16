from block import block_to_block_type, block_to_html_node
from htmlnode import HTMLNode, ParentNode
from splithelper import text_to_text_nodes

def markdown_to_blocks(markdown):
  lines = markdown.split("\n\n")
  blocks = []

  for line in lines:
    line = line.strip()
    if line:
      blocks.append(line)

  return blocks

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  children = [block_to_html_node(block) for block in blocks]
  return ParentNode("div", children)

def extract_title(markdown):
  blocks = markdown_to_blocks(markdown)
  if not blocks:
    raise ValueError("No title found")
  for block in blocks:
    if block.startswith("# "):
      return block[2:]
  raise ValueError("No title found")