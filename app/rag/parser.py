from bs4 import BeautifulSoup

class ArxivStrategy:
    def __init__(self):
        pass

    def extract(self, file):
        # Read the HTML file
        with open(file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract title
        title = soup.find(class_=['ltx_title', 'ltx_title_document'])
        title_text = title.get_text().strip() if title else "No title found"
        
        # Find the article tag and extract content
        article = soup.find('article')
        content_blocks = []
        
        if article:
            # Get all sections
            sections = article.find_all('section', recursive=False)
            for section in sections:
                # Get section title if exists
                section_title = section.find('h2')
                if section_title:
                    content_blocks.append(section_title.get_text().strip())
                
                # Get all divs in this section
                divs = section.find_all('div', recursive=False)  # only direct children
                for div in divs:
                    div_text = div.get_text(separator=' ', strip=True)
                    if div_text:  # Only add non-empty blocks
                        content_blocks.append(div_text)
        
        return title_text, content_blocks

class ScientificDirectoryStrategy:
    def __init__(self):
        pass

    def extract(self, file):
        with open(file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        title = soup.find(class_='title-text')
        title_text = title.get_text().strip() if title else "No title found"
        
        body = soup.find('div', id='body')
        body_texts = []
        
        if body:
            sections = body.find_all('section')
            for section in sections:
                h2 = section.find('h2')
                if h2:
                    body_texts.append(h2.get_text().strip())
                
                divs = section.find_all('div', recursive=False)  # recursive=False to only get direct children
                for div in divs:
                    body_texts.append(div.get_text().strip())

        return title_text, body_texts

class Context:
    def __init__(self, folder):
        self.strategy = self.get(folder)

    def get(self, type):
        if type == "arxiv":
            return ArxivStrategy()
        elif type == "scientificdirect":
            return ScientificDirectoryStrategy()

    def extract(self, file):
        return self.strategy.extract(file)




# # Example usage
# if __name__ == "__main__":
#     html_file = "./article.html"
#     content = extract_content(html_file)
    
#     print("Title:", content['title'])
#     print("\nArticle Content:")
#     for i, block in enumerate(content['article'], 1):
#         print(f"\n{i}. {block}")