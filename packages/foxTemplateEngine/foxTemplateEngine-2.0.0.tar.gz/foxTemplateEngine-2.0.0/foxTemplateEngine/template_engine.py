from sys import argv
import re
import os

class FoxEngine:
    tags: list = [
        'a', 'abbr', 'adress', 'area',
        'article', 'aside', 'audio', 'b',
        'base', 'bdi', 'bdo', 'blockquote',
        'body', 'br', 'button', 'canvas',
        'caption', 'cite', 'code', 'col',
        'colgroup', 'data', 'datalist', 'dd',
        'del', 'details', 'dfn', 'dialog',
        'div', 'dl', 'dt', 'em', 'embed',
        'fieldset', 'figcaption', 'figure',
        'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'head', 'header', 'hr', 'html', 'i',
        'iframe', 'img', 'input', 'title', 'html'
    ]


    def __init__(self, path_to_file: str, context: dict={}):
        self.res_text: str = ''
        self.context: dict = context
        self.path_to_file: str = path_to_file


    def html_render(self, line: str) -> str:
        """
        This function renders the string.
        """
        context = self.context
        tag: str = re.search(r'\w+', line)
        if tag:
            tag = tag.group(0)
            if tag in self.tags:
                if ('.' + tag) in line:
                    line = line.replace('.' + tag, '</' + tag)
                    if '\n' in line:
                        line = line.replace('\n', '>\n')
                    else:
                        line += '>'
                else:
                    line = line.replace(tag, '<' + tag).replace('\n', '>\n')
        
        while '{{' in line and '}}' in line:
            left = line.find('{{')
            right = line.find('}}')
            code = line[left + 3 : right]
            line = line.replace(line[left:right + 2], str(eval(code)))
        return line



    def if_repeat(self, file, for_repeat: list, q: int):
        arr = []
        for line in file:
            if '% repeat ' in line:
                quantity = int(line[line.rfind(' %') - 1])
                self.if_repeat(file, arr, quantity)
                continue
            if '% end %' in line: 
                break
            arr.append(line)
        for i in range(q):
            for i in arr:
                for_repeat.append(i)


    def getRenderedTemplateAsText(self) -> str:
        """
        This function will render your template and return the result as text (string).
        """
        with open(self.path_to_file, 'r') as file:
            file_gen = (line for line in file)
            current_line = 0
            for line in file_gen:
                if '% repeat ' in line:
                    quantity = int(line[line.rfind(' %') - 1])
                    for_repeat = []
                    self.if_repeat(file_gen, for_repeat, quantity)
                    for i in for_repeat:
                        self.res_text += self.html_render(i)
                    continue
                self.res_text += self.html_render(line)

        return self.res_text


    def writeToFile(self, path_to_new: str):
        """
        This function writes your rendered template to file by path: path_to_new.
        """
        with open(path_to_new, 'w') as file:
            file.write(self.res_text)
