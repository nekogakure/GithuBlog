import os
import markdown
import yaml
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

print("Start build.py")

current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
print(f"Current Date and Time (UTC): {current_time}")
print(f"Current User: nekogakure")

os.makedirs("docs", exist_ok=True)
print("Created docs/ dir")

with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
print("Loaded config.yml")

env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
post_template = env.get_template("post.html")
index_template = env.get_template("index.html")
print("Loaded templates")

posts = []
for md_file in sorted(os.listdir("posts")):
    print(f"Check file: {md_file}")
    if not md_file.endswith(".md"):
        continue
    path = os.path.join("posts", md_file)
    print(f"Processing {path}")
    
    filename_without_ext = md_file.replace(".md", "")
    
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
        if lines and lines[0].startswith("#"):
            title = lines[0].replace("#", "").strip()
        elif len(filename_without_ext.split("-")) >= 4:
            title = filename_without_ext[11:]
        else:
            title = filename_without_ext
            
    date_str = md_file.split("-")[0:3]
    date = "-".join(date_str) if len(date_str) == 3 else "不明"
    
    if date != "不明":
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            date_obj = datetime.min
    else:
        date_obj = datetime.min
    
    md_content = "\n".join(lines[1:]) if lines and lines[0].startswith("#") else "\n".join(lines)
    html_content = markdown.markdown(md_content)
    html_filename = md_file.replace(".md", ".html")
    
    posts.append({
        "title": title,
        "date": date,
        "date_obj": date_obj,
        "content": html_content,
        "filename": html_filename,
    })
    
    print(f"Rendering {html_filename}")
    rendered = post_template.render(
        site_name=config["site_name"],
        owner=config["owner"],
        title=title,
        bio=config["bio"],
        sns=config["sns"],
        theme_color=config["theme_color"],
        text_color=config["text_color"],
        background_color=config["background_color"],
        link_color=config["link_color"],
        content=html_content,
        current_year=datetime.now().year
    )
    
    with open(os.path.join("docs", html_filename), "w", encoding="utf-8") as outf:
        outf.write(rendered)
    print(f"Wrote docs/{html_filename}")

posts_sorted = sorted(posts, key=lambda x: x["date_obj"], reverse=True)
print(f"Rendering index.html with {len(posts_sorted)} posts")

rendered_index = index_template.render(
    site_name=config["site_name"],
    owner=config["owner"],
    bio=config["bio"],
    sns=config["sns"],
    theme_color=config["theme_color"],
    text_color=config["text_color"],
    background_color=config["background_color"],
    link_color=config["link_color"],
    posts=posts_sorted,
    current_year=datetime.now().year
)

with open(os.path.join("docs", "index.html"), "w", encoding="utf-8") as outf:
    outf.write(rendered_index)
print("Wrote docs/index.html")
print("Build complete!")
