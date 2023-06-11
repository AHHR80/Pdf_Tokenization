import re
from abc import ABC
from typing import List, Optional

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader

from pdf_bookmark import json_mbk


class AiFarmTextLoader(BaseLoader, ABC):
    """Load text files."""

    def __init__(self, text_file_path: str, pdf_file_path: str, encoding: Optional[str] = None, name: str = None):
        """Initialize with file path."""
        self.text_file_path = text_file_path
        self.pdf_file_path = pdf_file_path
        self.encoding = encoding
        self.name = name

    def load(self) -> List[Document]:
        """Load from file path."""
        bmk = json_mbk(self.pdf_file_path)
        bmk = bmk['bookmark']
        level_bmk = dict()
        for i in bmk:
            if level_bmk.get(i['level']):
                level_bmk[i['level']].append(i)
                continue
            level_bmk[i['level']] = [i]
        # print(bmk)
        ########################
        with open(self.text_file_path, 'r', encoding=self.encoding) as file:
            source = file.read()

        page_pattern = r'(-+ Page \d+-+\n+)(.*?)(?=\n-+ Page|\Z)'
        pages = re.findall(page_pattern, source, flags=re.DOTALL)
        pages = [page[1] for page in pages]
        pages.insert(0, '')
        pages_with_metadata = []
        for i in range(0, len(bmk) - 1):
            pattern = ''
            for ii in re.findall(r'\S*', bmk[i]['title']):
                pattern += (re.escape(ii.replace(':', '')) + '\:*\s*\n*')
            pattern2 = ''
            for ii in re.findall(r'\S*', bmk[i + 1]['title']):
                pattern2 += (re.escape(ii.replace(':', '')) + '\:*\s*\n*')

            if bmk[i + 1]['page'] - bmk[i]['page'] != 0:
                page_num = f"{bmk[i]['page']}-{bmk[i + 1]['page']}"
                source = ''
                for x in pages[bmk[i]['page']: bmk[i + 1]['page'] + 1]:
                    source += x
            else:
                page_num = f"{bmk[i]['page']}"
                source = pages[bmk[i]['page']]

            level = bmk[i]['level']
            title = bmk[i]['title']
            for ii in range(i - 1, -1, -1):
                if level <= 0:
                    break
                elif level > bmk[ii]['level']:
                    level -= 1
                    title = bmk[ii]['title'] + ':' + title

            matches = re.findall(pattern + "(.+)\s*\n*" + pattern2, source, flags=re.DOTALL)
            pages_with_metadata.append(
                Document(page_content=matches[0], metadata={'source': self.name, 'title': title, 'page': page_num}))
            # with open('test.txt', 'a+', encoding=self.encoding) as file:
            #     file.write(matches[0] + '\n++++++++++++++++++++++++++++++++++++++++\n')

        ########################
        return pages_with_metadata
