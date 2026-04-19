import os
import datetime
from xml.dom import minidom

def generate_sitemap():
    base_url = "https://sigdelsushil.com.np/"
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sitemap_path = os.path.join(root_dir, "sitemap.xml")
    
    # Files to include in the root
    root_files = [
        {"path": "index.html", "priority": "1.0", "changefreq": "daily", "loc": base_url},
        {"path": "index-ja.html", "priority": "0.8", "changefreq": "daily", "loc": base_url + "index-ja.html"},
        {"path": "privacy-policy.html", "priority": "0.3", "changefreq": "yearly", "loc": base_url + "privacy-policy.html"},
        {"path": "terms-of-service.html", "priority": "0.3", "changefreq": "yearly", "loc": base_url + "terms-of-service.html"},
        {"path": "sushil_sigdel.pdf", "priority": "0.5", "changefreq": "monthly", "loc": base_url + "sushil_sigdel.pdf"},
        {"path": "sushil_sigdel_jp.pdf", "priority": "0.5", "changefreq": "monthly", "loc": base_url + "sushil_sigdel_jp.pdf"},
    ]
    
    blog_dir = os.path.join(root_dir, "blog")
    blog_urls = []
    
    if os.path.exists(blog_dir):
        for file in os.listdir(blog_dir):
            if file.endswith(".html"):
                blog_urls.append({
                    "loc": base_url + "blog/" + file,
                    "priority": "0.8",
                    "changefreq": "monthly"
                })
    
    # Sort blog URLs for consistency
    blog_urls.sort(key=lambda x: x['loc'])
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Create the XML structure
    urlset = minidom.Document().createElement('urlset')
    urlset.setAttribute('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    doc = minidom.Document()
    doc.appendChild(urlset)
    
    def add_url(url_data):
        url_node = doc.createElement('url')
        
        loc_node = doc.createElement('loc')
        loc_node.appendChild(doc.createTextNode(url_data['loc']))
        url_node.appendChild(loc_node)
        
        lastmod_node = doc.createElement('lastmod')
        lastmod_node.appendChild(doc.createTextNode(today))
        url_node.appendChild(lastmod_node)
        
        freq_node = doc.createElement('changefreq')
        freq_node.appendChild(doc.createTextNode(url_data['changefreq']))
        url_node.appendChild(freq_node)
        
        pri_node = doc.createElement('priority')
        pri_node.appendChild(doc.createTextNode(url_data['priority']))
        url_node.appendChild(pri_node)
        
        urlset.appendChild(url_node)

    for root_file in root_files:
        if os.path.exists(os.path.join(root_dir, root_file['path'])):
            add_url(root_file)
            
    for blog_url in blog_urls:
        add_url(blog_url)
        
    xml_str = doc.toprettyxml(indent="  ", encoding="UTF-8")
    
    with open(sitemap_path, "wb") as f:
        f.write(xml_str)
    
    print(f"Successfully generated sitemap with {len(root_files) + len(blog_urls)} URLs at {sitemap_path}")

if __name__ == "__main__":
    generate_sitemap()
