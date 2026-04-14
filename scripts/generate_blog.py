import os
import json
import datetime
import re
import time
from google import genai

# Configuration
API_KEY = os.environ.get("GEMINI_API_KEY")
BLOGS_FILE = "assets/data/blogs.json"
TEMPLATE_FILE = "scripts/blog-template.html"
BLOG_DIR = "blog"

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
        # The model object in the new SDK usually has 'name' which might be 'models/gemini-...'
        # We need to filter for models that support generation.
        available_models = []
        for m in raw_models:
            # Safer attribute check
            m_name = getattr(m, 'name', str(m))
            # Just collect everything that looks like a gemini model
            if "gemini" in m_name.lower() or "gemma" in m_name.lower():
                available_models.append(m_name)
        
        print(f"Found {len(available_models)} potential models.")
        
        # Priority: 2.0-flash, 1.5-flash, flash-latest, then others
        priority_list = []
        keywords = ["gemini-2.0-flash", "gemini-1.5-flash", "flash-latest", "flash"]
        
        for kw in keywords:
            for m in available_models:
                if kw in m and m not in priority_list:
                    priority_list.append(m)
        
        # Add everything else
        for m in available_models:
            if m not in priority_list:
                priority_list.append(m)
                
        return priority_list
    except Exception as e:
        print(f"Warning: Model listing failed: {e}. Falling back to defaults.")
        # Fallback to names that often work
        return ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-flash-latest"]

def generate_blog_content():
    models_to_try = get_prioritized_models()
    
    prompt = """
    Act as an expert software engineer and tech blogger. 
    Write a high-quality blog post about a trending topic in software development, AI, or IT.
    
    Return the response ONLY as a JSON object with the following fields:
    - category: A short category name (e.g., 'AI & ML', 'Web Dev')
    - title: An eye-catching title
    - summary: A 2-sentence summary hook
    - content: The full blog post content in HTML format (use <p>, <h3>, <ul>, <li> tags). Make it detailed (approx 500 words).
    
    Ensure the content is insightful and professional.
    """
    
    for model_name in models_to_try:
        # Note: Some SDK versions expect 'gemini-1.5-flash' while others 'models/gemini-1.5-flash'
        # We will try the name as provided by the list() call first.
        print(f"--- Attempting: {model_name} ---")
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            
            text = response.text.strip()
            if not text:
                print(f"Empty response from {model_name}.")
                continue
                
            # Vigorous JSON cleaning
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            # Remove any potential stray characters before/after JSON
            text = text[text.find("{"):text.rfind("}")+1]
            
            blog_data = json.loads(text)
            blog_data["date"] = datetime.datetime.now().strftime("%d %B %Y")
            blog_data["author"] = "Sushil Sigdel"
            blog_data["image"] = "assets/images/bloghome.png"
            blog_data["slug"] = slugify(blog_data["title"])
            blog_data["isPopular"] = False
            
            print(f"SUCCESS with {model_name}!")
            return blog_data
            
        except Exception as e:
            msg = str(e)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                print(f"Quota Hit for {model_name}. Trying next...")
            elif "404" in msg or "not found" in msg.lower():
                print(f"Model {model_name} not available for this key. Trying next...")
            else:
                print(f"Skipping {model_name} due to error: {e}")
            continue
                
    return None

def create_static_page(blog_data):
    try:
        if not os.path.exists(TEMPLATE_FILE):
            print(f"Template {TEMPLATE_FILE} not found.")
            return False
            
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            template = f.read()
        
        html_content = template
        for key in ["title", "summary", "category", "author", "date", "image", "content"]:
            html_content = html_content.replace(f"{{{{{key}}}}}", str(blog_data.get(key, "")))
        
        if not os.path.exists(BLOG_DIR):
            os.makedirs(BLOG_DIR)
            
        file_path = os.path.join(BLOG_DIR, f"{blog_data['slug']}.html")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        blog_data["link"] = f"blog/{blog_data['slug']}.html"
        print(f"Created page: {file_path}")
        return True
    except Exception as e:
        print(f"Error creating HTML: {e}")
        return False

def update_blogs_json(new_blog):
    json_entry = new_blog.copy()
    if "content" in json_entry:
        del json_entry["content"]
        
    if not os.path.exists(BLOGS_FILE):
        blogs = []
    else:
        try:
            with open(BLOGS_FILE, 'r', encoding='utf-8') as f:
                blogs = json.load(f)
        except:
            blogs = []
    
    if any(b.get("slug") == json_entry["slug"] for b in blogs):
        return

    json_entry["id"] = len(blogs) + 1
    blogs.insert(0, json_entry)
    blogs = blogs[:12]
    
    with open(BLOGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(blogs, f, indent=2, ensure_ascii=False)
    print(f"Updated blogs.json")

if __name__ == "__main__":
    print("Starting Final Reliable Generation...")
    new_post = generate_blog_content()
    if new_post:
        if create_static_page(new_post):
            update_blogs_json(new_post)
            print("--- PROCESS COMPLETE ---")
    else:
        print("CRITICAL: No models worked. Check API Key permissions.")
