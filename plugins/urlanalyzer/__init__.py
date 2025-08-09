from lib.utils import http_request_get
from bs4 import BeautifulSoup
import logging

def analyze_url(url):
    """
    Analyze a URL by fetching its content (title, meta description, and main content)
    
    Args:
        url (str): The URL to analyze
    
    Returns:
        str: Content of the webpage or None if failed
    """
    try:
        # Fetch the webpage content
        resp = http_request_get(url)
        if not resp:
            return "Failed to fetch the URL content."
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Extract title
        title = ""
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()
        
        # Extract meta description
        description = ""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            meta_desc = soup.find('meta', attrs={'property': 'og:description'})
        if meta_desc:
            description = meta_desc.get('content', '').strip()
        
        # Extract main content (remove script and style elements)
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()
        
        # Get text content, prioritizing main content areas
        content = ""
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        if main_content:
            content = main_content.get_text(separator=' ', strip=True)
        else:
            content = soup.get_text(separator=' ', strip=True)
        
        # Limit content length to avoid token limits
        content = content[:3000]
        
        result = ""

        if title:
            result += f"Title: {title}\n"
        if description:
            result += f"Meta Description: {description}\n"
        result += f"Content: {content}\n\n"

        return result
    
    except Exception as e:
        logging.error(f"Failed to analyze URL {url}: {e}")
        return f"Failed to analyze the URL: {str(e)}"

URL_ANALYZER_FUNCTION_DEFINITION = {
    "type": "function",
    "name": "analyze_url",
    "description": "Analyze a URL by fetching its content (title, meta description, and main content)",
    "parameters": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The URL to analyze and summarize"
            }
        },
        "required": ["url"],
        "additionalProperties": False
    },
    "strict": True
}

def register(bot):
    bot.register_command('analyze', lambda _channel, _sender, query: analyze_url(query) if query else "Please provide a URL to analyze.")
    bot.register_help('analyze', '!analyze <url> - Analyze a URL')
    # Register function for OpenAI function calling
    bot.register_function(analyze_url, URL_ANALYZER_FUNCTION_DEFINITION)