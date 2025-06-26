import os
import markdown
import yaml
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

with open("../config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
post_template = env.get_template("post.html")
index_template = env.get_template("index.html")

posts = []
for md_file in sorted(os.listdir("posts")):
    if not md_file.endswith(".md"):
        continue
    with open(os.path.join("posts", md_file), encoding="utf-8") as f:
        lines = f.read().splitlines()
        title = lines[0].replace("#", "").strip() if lines and lines[0].startswith("#") else md_file
        date_str = md_file.split("-")[0:3]
        date = "-".join(date_str) if len(date_str) == 3 else "不明"
        md_content = "\n".join(lines[1:]) if lines and lines[0].startswith("#") else "\n".join(lines)
        html_content = markdown.markdown(md_content)
        html_filename = md_file.replace(".md", ".html")
        posts.append({
            "title": title,
            "date": date,
            "content": html_content,
            "filename": html_filename,
        })
        # 記事HTML生成
        rendered = post_template.render(
            site_name=config["site_name"],
            title=title,
            bio=config["bio"],
            sns=config["sns"],
            theme_color=config["theme_color"],
            text_color=config["text_color"],
            background_color=config["background_color"],
            link_color=config["link_color"],
            content=html_content,
        )
        with open(os.path.join("docs", html_filename), "w", encoding="utf-8") as outf:
            outf.write(rendered)

posts_sorted = sorted(posts, key=lambda x: x["date"], reverse=True)
rendered_index = index_template.render(
    site_name=config["site_name"],
    bio=config["bio"],
    sns=config["sns"],
    theme_color=config["theme_color"],
    text_color=config["text_color"],
    background_color=config["background_color"],
    link_color=config["link_color"],
    posts=posts_sorted,
)
with open(os.path.join("docs", "index.html"), "w", encoding="utf-8") as outf:
    outf.write(rendered_index)
