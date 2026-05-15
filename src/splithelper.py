import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for old_node in old_nodes:
      if old_node.text_type != TextType.TEXT:
          new_nodes.append(old_node)
          continue
      split_nodes = []
      sections = old_node.text.split(delimiter)
      if len(sections) % 2 == 0:
          raise ValueError(f"Invalid markdown, formatted section not closed: {old_node.text}")
      for i, section in enumerate(sections):
          if section == "":
              continue
          if i % 2 == 0:
              split_nodes.append(TextNode(section, TextType.TEXT))
          else:
              split_nodes.append(TextNode(section, text_type))
      new_nodes.extend(split_nodes)
  return new_nodes

def extract_markdown_images(text):
  matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

  return matches

def extract_markdown_links(text):
  matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

  return matches

def split_nodes_image(old_nodes):
  new_nodes = []

  for old_node in old_nodes:
    if old_node.text_type != TextType.TEXT:
        new_nodes.append(old_node)
        continue

    start_tag_at = None
    continue_at = 0

    for i in range(len(old_node.text)):
      if old_node.text[i] == "!" and old_node.text[i + 1] == "[" and start_tag_at is None:
        start_tag_at = i
      elif old_node.text[i] == ")" and start_tag_at is not None:
        new_nodes.append(TextNode(old_node.text[continue_at:start_tag_at], TextType.TEXT))
        continue_at = i + 1

        [alt_text, url] = extract_markdown_images(old_node.text[start_tag_at:continue_at])[0]
        new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
        start_tag_at = None

    if start_tag_at is not None:
      raise ValueError(f"Image tag found at the start of a split text but not at the end: '{old_node.text}'")
    
    if continue_at < len(old_node.text):
      new_nodes.append(TextNode(old_node.text[continue_at:], TextType.TEXT))

  return new_nodes

def split_nodes_link(old_nodes):
  new_nodes = []

  for old_node in old_nodes:
    if old_node.text_type != TextType.TEXT:
      new_nodes.append(old_node)
      continue

    start_tag_at = None
    continue_at = 0

    for i in range(len(old_node.text)):
      if old_node.text[i] == "[" and (i == 0 or old_node.text[i - 1] != "!") and start_tag_at is None:
          start_tag_at = i
      elif old_node.text[i] == ")" and start_tag_at is not None:
        new_nodes.append(TextNode(old_node.text[continue_at:start_tag_at], TextType.TEXT))
        continue_at = i + 1

        [alt_text, url] = extract_markdown_links(old_node.text[start_tag_at:continue_at])[0]
        new_nodes.append(TextNode(alt_text, TextType.LINK, url))
        start_tag_at = None

    if start_tag_at is not None:
      raise ValueError(f"Link tag found at the start of a split text but not at the end: '{old_node.text}'")
    
    if continue_at < len(old_node.text):
      new_nodes.append(TextNode(old_node.text[continue_at:], TextType.TEXT))

  return new_nodes

def text_to_text_nodes(text):
  result = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
  result = split_nodes_delimiter(result, "_", TextType.ITALIC)
  result = split_nodes_delimiter(result, "`", TextType.CODE)
  result = split_nodes_image(result)
  result = split_nodes_link(result)

  return result