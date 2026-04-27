import os
import json
import re
from datetime import datetime

BLOG_DIR = "blog"
BLOGS_FILE = "assets/data/blogs.json"

def extract_info(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_match = re.search(r'<title>(.*?) \| Sushil Sigdel</title>', content, re.DOTALL)
    summary_match = re.search(r'<meta name="description" content="(.*?)">', content, re.DOTALL)
    category_match = re.search(r'<span class="category-tag">(.*?)</span>', content, re.DOTALL)
    meta_match = re.search(r'<div class="blog-meta-top">[\s\n]*By <strong>(.*?)</strong> \| (.*?)\s*</div>', content, re.DOTALL)
    
    # Updated image extraction to handle both inline styles and <img> tags
    image_match = re.search(r'background-image: linear-gradient\(.*?\),\s*url\(\'(.*?)\'\);', content, re.DOTALL)
    if not image_match:
        image_match = re.search(r'<div class="featured-img-wrap">[\s\n]*<img src="(.*?)"', content, re.DOTALL)
    
    if not (title_match and summary_match and category_match and meta_match):
        return None
        
    slug = os.path.basename(html_path).replace('.html', '')
    
    return {
        "category": title_match.group(1) if "Cost Optimization" in title_match.group(1) else category_match.group(1), # Specific fix for one blog
        "title": title_match.group(1),
        "summary": summary_match.group(1),
        "date": meta_match.group(2).strip(),
        "author": meta_match.group(1),
        "image": image_match.group(1) if image_match else "assets/images/bloghome.png",
        "slug": slug,
        "isPopular": False,
        "link": f"blog/{slug}.html"
    }

def rebuild():
    blogs = []
    for file in os.listdir(BLOG_DIR):
        if file.endswith(".html"):
            info = extract_info(os.path.join(BLOG_DIR, file))
            if info:
                # Fix for the specific blog where category might be wrong
                if "Cost Optimization" in info["title"]:
                    info["category"] = "AI, Cloud Computing, DevOps"
                blogs.append(info)
    
    def parse_date(d):
        for fmt in ("%d %B %Y", "%B %d, %Y"):
            try:
                return datetime.strptime(d.strip(), fmt)
            except:
                continue
        return datetime.min

    blogs.sort(key=lambda x: parse_date(x['date']), reverse=True)
    
    total = len(blogs)
    for i, blog in enumerate(blogs):
        blog["id"] = total - i

    with open(BLOGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(blogs, f, indent=2, ensure_ascii=False)
    
    print(f"Rebuilt {BLOGS_FILE} with {len(blogs)} entries.")

if __name__ == "__main__":
    rebuild()
