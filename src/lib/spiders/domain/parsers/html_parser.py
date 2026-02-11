from selectolax.lexbor import LexborHTMLParser

# HtmlParser + site-specific parsers


class HtmlParser:
    @staticmethod
    def parse_with_selectors(self, html_content: str, selectors: dict):
        """
        Parses HTML content using a dictionary of selectors.
        Returns a dictionary of extracted data.
        """
        tree = LexborHTMLParser(html_content)
        data = {}

        for key, selector in selectors.items():
            node = tree.css_first(selector)
            if node:
                data[key] = node.text(strip=True)
            else:
                data[key] = None

        return data
