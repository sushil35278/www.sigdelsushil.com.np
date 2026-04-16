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
TECH_CATEGORIES = ["AI & Machine Learning", "Web Development", "Cloud Architecture", "Cybersecurity", "DevOps & SRE", "Software Engineering", "Mobile Development"]

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
    models_to_try = get_prioritized_models()
    target_topic = random.choice(TECH_CATEGORIES)
    
    prompt = f"""
    Act as a senior software architect and popular tech blogger. 
    Write a high-quality, deeply interesting blog post about a specific modern trend in {target_topic}.
    
    CRITICAL INSTRUCTIONS:
    1. Be bold and opinionated. Don't just list facts. 
    2. Include a 'Why this matters for developers' section.
    3. Include at least 3 'Pro Tips' or 'Future Predictions'.
    4. Format the content with <h3> headings, <p> paragraphs, and <ul>/<li> lists.
    
    Return ONLY a JSON object:
    - category: The category (must be one of: {", ".join(TECH_CATEGORIES)})
    - title: A catchy, magazine-style headline
    - summary: A 2-sentence hook that makes people want to click.
    - content: The full HTML content (approx 600 words).
    - image_keyword: A single English keyword for a beautiful tech photo (e.g., 'coding', 'minimalism', 'data', 'robot').
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
            blog_data["date"] = datetime.datetime.now().strftime("%d %B %Y")
            blog_data["author"] = "Sushil Sigdel"
            blog_data["accent_color"] = random.choice(ACCENT_COLORS)
            
            keyword = blog_data.get("image_keyword", "technology")
            # Using Unsplash with specific styling parameters for better quality
            blog_data["image"] = f"https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&q=80&w=1200" # fallback to a good one
            # Actually use keyword based unsplash
            blog_data["image"] = f"https://source.unsplash.com/featured/1200x800/?{keyword},dark,tech"
            
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
        for key in ["title", "summary", "category", "author", "date", "image", "content", "accent_color"]:
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
    blogs = blogs[:12]
    with open(BLOGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(blogs, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    new_post = generate_blog_content()
    if new_post:
        if create_static_page(new_post):
            update_blogs_json(new_post)
            print("--- SUCCESS ---")
