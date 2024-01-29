# from newspaper import Article
from util.base_logger import log
from bs4 import BeautifulSoup
from obj.cnn_article import CNNArticle


class CNNArticleParser:
    DELIMITER = " "
    def parse(self, jdata): 
        data = CNNArticle(**jdata)
        data = self._enrich(data)
        return data


    def _enrich(self, data):
        """ Extract highlights and body text from raw content """
        soup = BeautifulSoup(data.raw_content, 'html.parser')
        
        highlight_divs = soup.find_all("li", {"class": "el__storyhighlights--normal"})
        highlights = self.DELIMITER.join([x.text.strip() for x in highlight_divs])
        
        body_divs = soup.find_all("div", {"class": "zn-body__paragraph"})
        body = self.DELIMITER.join([x.text.strip().replace("\'", "'") for x in body_divs])
        
        data.body = body
        data.highlights = highlights
        
        return data
