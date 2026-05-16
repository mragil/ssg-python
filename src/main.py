from shutil import rmtree, copy
from os import mkdir, listdir, path, makedirs

from markdown_helper import markdown_to_html_node, extract_title


def copy_directory(src, dst):
  if not path.exists(dst):
    mkdir(dst)
  for item in listdir(src):
    src_path = path.join(src, item)
    dst_path = path.join(dst, item)
    if path.isdir(src_path):
        copy_directory(src_path, dst_path)
    else:
      print(f"Copying {src_path} to {dst_path}...")
      copy(src_path, dst_path)

def read_file(file_path):
  if not path.exists(file_path):
    raise FileNotFoundError(f"File {file_path} does not exist.")
  
  with open(str(file_path), mode="r", encoding="utf-8") as file:
    file_content = file.read()
    return file_content
  
def write_file(file_path, content):
  print(f"Writing to {file_path}...")
  parent_dir = path.dirname(file_path)
  if not path.exists(parent_dir):
    print(f"Creating directory {parent_dir}...")
    makedirs(parent_dir)

  with open(str(file_path), mode="w", encoding="utf-8") as file:
    file.write(content)

def generate_page(from_path, template_path, dest_path):
  print(f"Generating page from {from_path} to {dest_path} using template {template_path}")

  content = read_file(from_path)
  template = read_file(template_path)

  content_html = markdown_to_html_node(content).to_html()
  title_html = extract_title(content)

  generated_html = template.replace("{{ Content }}", content_html).replace("{{ Title }}", title_html)

  write_file(dest_path, generated_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
  for item in listdir(dir_path_content):
    src_path = path.join(dir_path_content, item)
    dst_path = path.join(dest_dir_path, item)

    if path.isdir(src_path):
      generate_pages_recursive(src_path, template_path, dst_path)
    elif src_path.endswith(".md"):
      dst_path = dst_path[:-3] + ".html"
      generate_page(src_path, template_path, dst_path)

def main():
  print("Cleaning public directory...")
  rmtree("public", ignore_errors=True)

  copy_directory("static", "public")
  
  generate_pages_recursive("content", "template.html", "public")


main()