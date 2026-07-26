import os
import pathlib

from MD_to_HTML import markdown_to_html_node
from markdown_handler import extract_title

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path)
    source: str = f.read()
    f = open(template_path)
    template: str = f.read()
    content: str = markdown_to_html_node(source).to_html()
    title = extract_title(source)
    full_HTML_page: str = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    dest_path_dir: str = os.path.dirname(dest_path)
    if not os.path.exists(dest_path_dir):
        os.makedirs(dest_path_dir)
    with open(dest_path, "w") as f:
        f.write(full_HTML_page)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    if os.path.isfile(dir_path_content):
        raise Exception("Not valid directory")
    for file in os.listdir(dir_path_content):
        from_path: str = os.path.join(dir_path_content, file)
        dest_path: str = os.path.join(dest_dir_path, file)
        if os.path.isfile(from_path):
            dest_path = str(pathlib.Path(dest_path).with_suffix(".html"))
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)