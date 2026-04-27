import os
import json
import datetime
import re
import random
from google import genai

# Configuration
API_KEY = os.environ.get("GEMINI_API_KEY")
BLOGS_FILE = "assets/data/blogs.json"
TEMPLATE_FILE = "scripts/blog-template.html"
BLOG_DIR = "blog"

# Dynamic Styling Options
ACCENT_COLORS = ["#fa65b1", "#726ae3", "#00d2ff", "#44D7B6", "#ffc107", "#ff5722"]
TECH_CATEGORIES = ["AI & Machine Learning", "Web Development", "Cloud Architecture", "Cybersecurity", "DevOps & SRE", "Software Engineering", "Distributed Systems"]

BANNED_PHRASES = [
    "synergy",
    "disruptive",
    "game-changer",
    "best-in-class",
    "cutting edge",
    "thought leader",
    "mobilize",
    "monetize",
    "AI-powered",
    "next generation"
]

if not API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set.")
    exit(1)

# Initialize the new GenAI client
client = genai.Client(api_key=API_KEY)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = text.strip('-')
    return text

def word_count(text):
    return len(re.findall(r'\w+', text or ""))

def is_quality_blog(blog_data, existing_titles):
    required = ["category", "title", "summary", "content", "image_keyword"]
    if not all(blog_data.get(k) and isinstance(blog_data.get(k), str) and blog_data.get(k).strip() for k in required):
        return False

    title_lower = blog_data["title"].lower()
    if title_lower in existing_titles:
        return False

    content_lower = blog_data["content"].lower()
    aggregate_text = f"{title_lower} {blog_data['summary'].lower()} {content_lower}"
    if any(phrase in aggregate_text for phrase in BANNED_PHRASES):
        return False

    if word_count(blog_data["content"]) < 750:
        return False

    if "<h3>" not in content_lower or "<pre><code>" not in content_lower:
        return False

    return True


def get_prioritized_models():
    try:
        raw_models = list(client.models.list())
        available_models = [getattr(m, 'name', str(m)) for m in raw_models if "gemini" in getattr(m, 'name', '').lower()]
        
        priority_list = []
        keywords = ["gemini-2.0-flash", "gemini-1.5-flash", "flash-latest"]
        for kw in keywords:
            for m in available_models:
                if kw in m and m not in priority_list:
                    priority_list.append(m)
        priority_list.extend([m for m in available_models if m not in priority_list])
        return priority_list
    except:
        return ["gemini-2.0-flash", "gemini-1.5-flash"]

def generate_blog_content():
    # Load existing blogs to avoid duplicates
    try:
        with open(BLOGS_FILE, 'r') as f:
            existing_blogs = json.load(f)
        existing_titles = {b['title'].lower() for b in existing_blogs}
    except:
        existing_titles = set()
    
    models_to_try = get_prioritized_models()
    target_topic = random.choice(TECH_CATEGORIES)
    
    prompt = f"""
    Act as a senior software architect and respected tech blogger with 10+ years of experience.
    Write a high-quality, deeply interesting blog post about a SPECIFIC trend in {target_topic} that senior developers and engineering leaders are debating in 2026.

    CRITICAL INSTRUCTIONS:
    1. Write with a professional, evidence-driven tone. Avoid marketing fluff and AI-sounding filler.
    2. Do not use buzzword phrases like synergy, disruptive, game-changer, best-in-class, cutting edge, thought leader, mobilize, monetize, AI-powered, or next generation unless they are explicitly justified.
    3. Include real-world examples, code snippets (in <pre><code> tags), and concrete statistics or references.
    4. Structure: Intro hook, 3-4 main sections with <h3>, Pro Tips, Future Predictions, Conclusion with CTA.
    5. Make it unique: reference current events, experience from Nepal and Japan, and avoid generic advice.
    6. Length: 800-1200 words. Keep the article grounded and technical.
    7. Return ONLY a JSON object with the fields below and no extra commentary.

    Return ONLY a JSON object:
    - category: The category (must be one of: {", ".join(TECH_CATEGORIES)})
    - title: A catchy, SEO-optimized headline (include keywords like '2026', 'future')
    - summary: A compelling 2-3 sentence hook.
    - content: The full HTML content.
    - image_keyword: A specific keyword for image (e.g., 'neural-network-cyberpunk', 'quantum-computer').
    """
    
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(model=model_name, contents=prompt)
            text = response.text.strip()
            if not text: continue
            
            # JSON cleaning
            if "```json" in text: text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text: text = text.split("```")[1].split("```")[0].strip()
            text = text[text.find("{"):text.rfind("}")+1]
            
            blog_data = json.loads(text)
            
            if not is_quality_blog(blog_data, existing_titles):
                print(f"Low quality or invalid blog content detected. Regenerating...")
                continue

            blog_data["date"] = datetime.datetime.now().strftime("%d %B %Y")
            blog_data["author"] = "Sushil Sigdel"
            blog_data["accent_color"] = random.choice(ACCENT_COLORS)
            
            keyword = blog_data.get("image_keyword", "technology")
            # Use a keyword-driven Unsplash image URL and keep a fallback if the source fails
            blog_data["image"] = f"https://source.unsplash.com/featured/1200x800/?{keyword.replace(' ', '+')}"
            if not blog_data["image"]:
                blog_data["image"] = "assets/images/bloghome.png"
            
            blog_data["slug"] = slugify(blog_data["title"])
            blog_data["isPopular"] = False
            return blog_data
        except Exception as e:
            print(f"Failed with {model_name}: {e}")
            continue
    return None

def create_static_page(blog_data):
    try:
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            template = f.read()
        
        html_content = template
        for key in ["title", "summary", "category", "author", "date", "image", "content", "accent_color", "slug"]:
            html_content = html_content.replace(f"{{{{{key}}}}}", str(blog_data.get(key, "")))
        
        if not os.path.exists(BLOG_DIR): os.makedirs(BLOG_DIR)
        file_path = os.path.join(BLOG_DIR, f"{blog_data['slug']}.html")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        blog_data["link"] = f"blog/{blog_data['slug']}.html"
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def update_blogs_json(new_blog):
    json_entry = new_blog.copy()
    for key in ["content", "image_keyword", "accent_color"]:
        if key in json_entry: del json_entry[key]
        
    if not os.path.exists(BLOGS_FILE): blogs = []
    else:
        try:
            with open(BLOGS_FILE, 'r', encoding='utf-8') as f: blogs = json.load(f)
        except: blogs = []
    
    if any(b.get("slug") == json_entry["slug"] for b in blogs): return

    json_entry["id"] = len(blogs) + 1
    blogs.insert(0, json_entry)
    blogs = blogs[:100] # Increased limit to show more blogs
    with open(BLOGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(blogs, f, indent=2, ensure_ascii=False)

def update_sitemap(blog_data):
    try:
        import subprocess
        # Use the absolute path to the sync_sitemap.py script
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sync_sitemap.py")
        subprocess.run(["python3", script_path], check=True)
        print(f"Sitemap synchronized successfully.")
    except Exception as e:
        print(f"Error updating sitemap: {e}")

def update_noscript(blog_data):
    try:
        index_files = ["index.html", "index-ja.html"]
        new_link = f'                <li><a href="{blog_data["link"]}">{blog_data["title"]}</a></li>'
        
        for index_file in index_files:
            if not os.path.exists(index_file): continue
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Insert the new link at the top of the <ul> inside <noscript>
            pattern = r'(<noscript>[\s\n]*<div class="col-lg-12">[\s\n]*<ul>)'
            if re.search(pattern, content):
                content = re.sub(pattern, rf'\1\n{new_link}', content)
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(content)
        print("Noscript sections updated.")
    except Exception as e:
        print(f"Error updating noscript: {e}")

if __name__ == "__main__":
    new_post = generate_blog_content()
    if new_post:
        if create_static_page(new_post):
            update_blogs_json(new_post)
            update_sitemap(new_post)
            update_noscript(new_post)
            print("--- SUCCESS ---")
