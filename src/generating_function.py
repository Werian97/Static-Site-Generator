import os

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
    