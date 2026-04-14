import os
import json
import datetime
import re
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

def generate_blog_content():
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
    
    try:
        # Using the new SDK syntax
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        
        text = response.text.strip()
        # Handle potential markdown fencing in response
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        
        blog_data = json.loads(text)
        blog_data["date"] = datetime.datetime.now().strftime("%d %B %Y")
        blog_data["author"] = "Sushil Sigdel (AI Generated)"
        blog_data["image"] = "assets/images/bloghome.png"
        blog_data["slug"] = slugify(blog_data["title"])
        blog_data["isPopular"] = False
        
        return blog_data
    except Exception as e:
        print(f"Error generating blog: {e}")
        return None

def create_static_page(blog_data):
    try:
        with open(TEMPLATE_FILE, 'r') as f:
            template = f.read()
        
        html_content = template
        html_content = html_content.replace("{{title}}", blog_data["title"])
        html_content = html_content.replace("{{summary}}", blog_data["summary"])
        html_content = html_content.replace("{{category}}", blog_data["category"])
        html_content = html_content.replace("{{author}}", blog_data["author"])
        html_content = html_content.replace("{{date}}", blog_data["date"])
        html_content = html_content.replace("{{image}}", blog_data["image"])
        html_content = html_content.replace("{{content}}", blog_data["content"])
        
        if not os.path.exists(BLOG_DIR):
            os.makedirs(BLOG_DIR)
            
        file_path = os.path.join(BLOG_DIR, f"{blog_data['slug']}.html")
        with open(file_path, 'w') as f:
            f.write(html_content)
        
        blog_data["link"] = f"blog/{blog_data['slug']}.html"
        print(f"Created static page: {file_path}")
        return True
    except Exception as e:
        print(f"Error creating static page: {e}")
        return False

def update_blogs_json(new_blog):
    # Remove large 'content' field before saving to JSON to keep it light
    json_entry = new_blog.copy()
    if "content" in json_entry:
        del json_entry["content"]
        
    if not os.path.exists(BLOGS_FILE):
        blogs = []
    else:
        with open(BLOGS_FILE, 'r') as f:
            blogs = json.load(f)
    
    # Check if slug already exists to avoid duplicates
    if any(b.get("slug") == json_entry["slug"] for b in blogs):
        print("Blog with this slug already exists. Skipping.")
        return

    json_entry["id"] = len(blogs) + 1
    blogs.insert(0, json_entry)
    
    # Keep latest 12 blogs
    blogs = blogs[:12]
    
    with open(BLOGS_FILE, 'w') as f:
        json.dump(blogs, f, indent=2)
    print(f"Updated blogs.json with: {json_entry['title']}")

if __name__ == "__main__":
    print("Starting generation with google-genai...")
    new_post = generate_blog_content()
    if new_post:
        if create_static_page(new_post):
            update_blogs_json(new_post)
    else:
        print("Failed to generate blog content.")
