import re

domain = "http://arxiv.org"

def value_from_tree(tree, path, sep=''):
    return sep.join(tree.xpath(path)).strip()

class Paper:
    path = {
        'id': '//div[@id="dlpage"]/dl[{}]/dt[{}]/span/a[1]/text()',
        'link': '//div[@id="dlpage"]/dl[{}]/dt[{}]/span/a[2]/@href',

        'title': '//div[@id="dlpage"]/dl[{}]/dd[{}]/div/div[@class="list-title"]/text()',
        'authors': '//div[@id="dlpage"]/dl[{}]/dd[{}]/div/div[@class="list-authors"]/a/text()',
        'comment': '//div[@id="dlpage"]/dl[{}]/dd[{}]/div/div[@class="list-comments"]/text()',
        'p-subject': '//div[@id="dlpage"]/dl[{}]/dd[{}]/div/div[@class="list-subjects"]/span[@class="primary-subject"]/text()',
        'o-subjects': '//div[@id="dlpage"]/dl[{}]/dd[{}]/div/div[@class="list-subjects"]/text()',
 
        'abstract': '//div[@id="dlpage"]/dl[{}]/dd[{}]/div/p/text()',
    }
    
    def __init__(self, tree, num, cat=1):
        self.id = value_from_tree(tree, self.__class__.path['id'].format(cat, num))
        
        lnk = value_from_tree(tree, self.__class__.path['link'].format(cat, num))
        self.link = domain + lnk

        self.title = value_from_tree(tree, self.__class__.path['title'].format(cat, num))
        self.comment = value_from_tree(tree, self.__class__.path['comment'].format(cat, num))
        
        auth = value_from_tree(tree, self.__class__.path['authors'].format(cat, num), ';')
        self.authors = auth.split(';')
        
        sub  = value_from_tree(tree, self.__class__.path['p-subject'].format(cat, num))
        sub += value_from_tree(tree, self.__class__.path['o-subjects'].format(cat, num))
        self.subjects  = [x.strip() for x in sub.split(';')]

        ab = value_from_tree(tree, self.__class__.path['abstract'].format(cat, num))
        self.abstract = re.sub('\n', ' ', ab)
    
    def is_interest(self, criteria):
        for x in criteria:
            if re.search(x, self.title):
                return True
            if re.search(x, self.abstract):
                return True

        return False

    @property
    def html(self):
        author_list = ", ".join(self.authors)
        subject_list = "; ".join(self.subjects)
        
        chunk  = '<br><br>'
        chunk += '<h2><a href="{}">{}</a>: {}</h2>'.format(self.link, self.title, self.id)
        chunk += '{}<br>'.format(author_list)
        chunk += 'Comments: {}<br>'.format(self.comment)
        chunk += 'Subjects: {}<br>'.format(subject_list)
        chunk += '<br>{}'.format(self.abstract)
    
    def __str__(self):
        return self.title

    def __repr__(self):
        return "<Paper {}>".format(self.id)

import requests
from lxml import html

class Page:
    def __init__(self, category):
        r = requests.get(domain + '/list/{}/new'.format(category))
        tree = html.fromstring(r.content)
        
        self.papers = []

        for x in range(1, int(tree.xpath('count(//div[@id="dlpage"]/dl[1]/dt)')) + 1):
            self.papers.append(Paper(tree, x, 1))
        for x in range(1, int(tree.xpath('count(//div[@id="dlpage"]/dl[2]/dt)')) + 1):
            self.papers.append(Paper(tree, x, 2))

        self.title = value_from_tree(tree, '//*[@id="dlpage"]/h3[1]/text()')

    def get_interesting(self, lst):
        interesting = []

        for x in self.papers:
            if x.is_interest(lst):
                interesting.append(x)

        return interesting

