import unittest

from splithelper import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_text_nodes
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
  def test_split_nodes_delimiter_code(self):
    expected = [
      TextNode("This is text with a ", TextType.TEXT),
      TextNode("code block", TextType.CODE),
      TextNode(" word ", TextType.TEXT),
      TextNode("other code block", TextType.CODE),
    ]
    
    node = TextNode("This is text with a `code block` word `other code block`", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    self.assertEqual(expected, new_nodes)

  def test_split_nodes_delimiter_bold(self):
    expected = [
      TextNode("This is text with a ", TextType.TEXT),
      TextNode("bold text", TextType.BOLD),
      TextNode(" word ", TextType.TEXT),
      TextNode("another bold text", TextType.BOLD),
      TextNode(" ", TextType.TEXT),
      TextNode("yet another bold text", TextType.BOLD),
    ]
    
    node = TextNode("This is text with a **bold text** word **another bold text** **yet another bold text**", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    self.assertEqual(expected, new_nodes)

  def test_split_nodes_delimiter_unmatched(self):
    node = TextNode("This is text with an unmatched `code block", TextType.TEXT)
    
    with self.assertRaises(ValueError) as context:
      split_nodes_delimiter([node], "`", TextType.CODE)

    self.assertTrue("Invalid markdown, formatted section not closed:" in str(context.exception))

  def test_split_nodes_delimiter_no_delimiter(self):
    expected = [
      TextNode("This is text with no delimiters", TextType.TEXT),
    ]
    
    node = TextNode("This is text with no delimiters", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    self.assertEqual(expected, new_nodes)


  def test_extract_markdown_images(self):
    text = "This is an image: ![alt text](image.jpg) and another one ![another image](another_image.png)"
    expected = [("alt text", "image.jpg"), ("another image", "another_image.png")]

    self.assertEqual(expected, extract_markdown_images(text))

  def test_extract_markdown_links(self):
    text = "This is a link: [Google](https://www.google.com) and another one [GitHub](https://www.github.com)"
    expected = [("Google", "https://www.google.com"), ("GitHub", "https://www.github.com")]

    self.assertEqual(expected, extract_markdown_links(text))

  def test_split_images_valid_image(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and another ![third image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )

    new_nodes = split_nodes_image([node])
    
    self.assertListEqual(
      [
          TextNode("This is text with an ", TextType.TEXT),
          TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
          TextNode(" and another ", TextType.TEXT),
          TextNode(
              "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
          ),
          TextNode(" and another ", TextType.TEXT),
          TextNode(
              "third image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
          ),
      ],
      new_nodes,
    )

  def test_split_images_no_images(self):
    node = TextNode("This is text with no images", TextType.TEXT)

    new_nodes = split_nodes_image([node])

    self.assertListEqual([TextNode("This is text with no images", TextType.TEXT)], new_nodes)

  def test_split_images_unmatched_image_tag(self):
    node = TextNode("This is text with an unmatched ![image](https://i.imgur.com/zjjcJKZ.png", TextType.TEXT)

    with self.assertRaises(ValueError) as context:
      split_nodes_image([node])

    self.assertTrue("Image tag found at the start of a split text but not at the end" in str(context.exception))

  def test_split_links_valid_link(self):
    node = TextNode(
        "This is text with a [link](https://www.google.com) and another [second link](https://www.github.com)",
        TextType.TEXT,
    )

    new_nodes = split_nodes_link([node])
    
    self.assertListEqual(
      [
          TextNode("This is text with a ", TextType.TEXT),
          TextNode("link", TextType.LINK, "https://www.google.com"),
          TextNode(" and another ", TextType.TEXT),
          TextNode("second link", TextType.LINK, "https://www.github.com"),
      ],
      new_nodes,
    )

  def test_text_to_text_nodes(self):
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    expected = [
      TextNode("This is ", TextType.TEXT),
      TextNode("text", TextType.BOLD),
      TextNode(" with an ", TextType.TEXT),
      TextNode("italic", TextType.ITALIC),
      TextNode(" word and a ", TextType.TEXT),
      TextNode("code block", TextType.CODE),
      TextNode(" and an ", TextType.TEXT),
      TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
      TextNode(" and a ", TextType.TEXT),
      TextNode("link", TextType.LINK, "https://boot.dev"),
    ]

    self.assertEqual(expected, text_to_text_nodes(text))

if __name__ == "__main__":
    unittest.main()