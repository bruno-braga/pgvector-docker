from bs4 import BeautifulSoup


class IEEExploreStrategy:
    def __init__(self):
        pass

    def extract(self, file):
        # Read the HTML file
        with open(file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract title from the specific class structure
        title_container = soup.find(class_=['document-title', 'text-2xl-md-lh'])
        title_text = title_container.find('span').get_text().strip() if title_container else "No title found"
        
        # Find the article container and extract content
        content_blocks = []
        article = soup.find(id='article')

        if article:
            # Find all sections (they have IDs like sec1, sec2, etc.)
            sections = article.find_all('div', id=lambda x: x and x.startswith('sec'))

            for section in sections:
                # Get all paragraphs in this section
                paragraphs = section.find_all('p')
                for p in paragraphs:
                    text = p.get_text(separator=' ', strip=True)
                    if text:  # Only add non-empty paragraphs
                        content_blocks.append(text)
        
        return title_text, content_blocks

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
        elif type == "ieeexplore":
            return IEEExploreStrategy()


    def extract(self, file):
        return self.strategy.extract(file)