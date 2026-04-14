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
    """Dynamically detects available models from the key and prioritizes them."""
    try:
        raw_models = list(client.models.list())
        available_models = []
        for m in raw_models:
            m_name = getattr(m, 'name', str(m))
            if "gemini" in m_name.lower():
                available_models.append(m_name)
        
        priority_list = []
        keywords = ["gemini-2.0-flash", "gemini-1.5-flash", "flash-latest", "flash"]
        for kw in keywords:
            for m in available_models:
                if kw in m and m not in priority_list:
                    priority_list.append(m)
        
        for m in available_models:
            if m not in priority_list:
                priority_list.append(m)
        return priority_list
    except Exception as e:
        print(f"Warning: Model listing failed: {e}")
        return ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-flash-latest"]

def generate_blog_content():
    models_to_try = get_prioritized_models()
    
    # Pick a random target topic to ensure variety
    target_topic = random.choice(TECH_CATEGORIES)
    
    prompt = f"""
    Act as an expert software engineer and tech blogger. 
    Write a high-quality blog post about a trending topic in {target_topic}.
    
    Return the response ONLY as a JSON object with the following fields:
    - category: The category (must be one of: {", ".join(TECH_CATEGORIES)})
    - title: An eye-catching title
    - summary: A 2-sentence summary hook
    - content: The full blog post content in HTML format (use <p>, <h3>, <ul>, <li> tags). Approx 500 words.
    - image_keyword: A single descriptive English keyword for a featured image related to the post (e.g., 'robot', 'coding', 'cloud').
    
    Ensure the content is insightful, professional, and unique.
    """
    
    for model_name in models_to_try:
        print(f"--- Attempting: {model_name} ---")
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            
            text = response.text.strip()
            if not text: continue
            
            # JSON Cleaning
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            text = text[text.find("{"):text.rfind("}")+1]
            
            blog_data = json.loads(text)
            blog_data["date"] = datetime.datetime.now().strftime("%d %B %Y")
            blog_data["author"] = "Sushil Sigdel"
            
            # Dynamic Styling & Images
            blog_data["accent_color"] = random.choice(ACCENT_COLORS)
            keyword = blog_data.get("image_keyword", "technology")
            # Using LoremFlicker for truly dynamic, safe images
            blog_data["image"] = f"https://loremflickr.com/800/600/{keyword},tech"
            
            blog_data["slug"] = slugify(blog_data["title"])
            blog_data["isPopular"] = False
            
            return blog_data
            
        except Exception as e:
            print(f"Skipping {model_name} due to error: {e}")
            continue
                
    return None

def create_static_page(blog_data):
    try:
        if not os.path.exists(TEMPLATE_FILE): return False
            
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            template = f.read()
        
        html_content = template
        for key in ["title", "summary", "category", "author", "date", "image", "content", "accent_color"]:
            html_content = html_content.replace(f"{{{{{key}}}}}", str(blog_data.get(key, "")))
        
        if not os.path.exists(BLOG_DIR):
            os.makedirs(BLOG_DIR)
            
        file_path = os.path.join(BLOG_DIR, f"{blog_data['slug']}.html")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        blog_data["link"] = f"blog/{blog_data['slug']}.html"
        return True
    except Exception as e:
        print(f"Error creating HTML: {e}")
        return False

def update_blogs_json(new_blog):
    json_entry = new_blog.copy()
    # Keep only metadata in JSON
    for key in ["content", "image_keyword", "accent_color"]:
        if key in json_entry: del json_entry[key]
        
    if not os.path.exists(BLOGS_FILE):
        blogs = []
    else:
        try:
            with open(BLOGS_FILE, 'r', encoding='utf-8') as f:
                blogs = json.load(f)
        except:
            blogs = []
    
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
            print("--- PROCESS COMPLETE ---")
    else:
        print("CRITICAL: No models worked.")
