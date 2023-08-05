# -*- coding: utf-8 -*-
import json
import base64
import logging
import re

from ..utils.cleaner import cleanup_text
from ..utils.crawler import Crawler

logger = logging.getLogger(__name__)
search_url = 'https://www.foxteller.com/search'
chapter_aux_url = 'https://www.foxteller.com/aux_dem'


class FoxtellerCrawler(Crawler):
    base_url = 'https://www.foxteller.com/'

    def search_novel(self, query):
        self.get_response(self.home_url)    # for cookies

        query = query.lower().replace(' ', '+')
        soup = self.post_soup(search_url, data=dict(query=query))

        results = []
        for a in soup.select('a[href*="/novel/"]'):
            results.append({
                'title': a.select_one('span .ellipsis-1').text.strip(),
                'url': self.absolute_url(a['href']),
                'info': a.select_one('span .text-brand').text.strip(),
            })
        # end for

        return results
    # end def

    def read_novel_info(self):
        '''Get novel title, autor, cover etc'''
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)

        self.novel_title = soup.select_one('.novel-title h2').text.strip()
        logger.info('Novel title: %s', self.novel_title)

        self.novel_cover = self.absolute_url(soup.select_one('.novel-featureimg img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)

        used_vol_id = set([])
        used_chap_id = set([])
        for card in soup.select('#myTabContent #accordion .card'):
            vol_title = card.select_one(".card-header .title").text
            vol_id = card.select_one(".card-header .volume").text
            if not vol_id.isdigit() or (vol_id in used_vol_id):
                vol_id = str(self.volumes[-1]['id'] + 1) if len(self.volumes) else '1'
            # end if
            used_vol_id.add(vol_id)
            vol_id = int(vol_id)
            if vol_id == 0:
                continue   # Skip Glossary
            # end if
            self.volumes.append({
                'id': vol_id,
                'title': vol_title,
            })

            for a in card.select('.card-body a'):
                chap_title = a.text.strip()
                chap_id = re.findall(r'(\d+)', chap_title)
                chap_id = int(chap_id[0]) if len(chap_id) else len(self.chapters) + 1
                if chap_id in used_chap_id:
                    chap_id = self.chapters[-1]['id'] + 1
                # end if
                used_chap_id.add(chap_id)
                self.chapters.append({
                    'id': chap_id,
                    'volume': vol_id,
                    'url':  self.absolute_url(a['href']),
                    'title': chap_title,
                })
            # end for
        # end for
    # end def

    @cleanup_text
    def download_chapter_body(self, chapter):
        '''Download body of a single chapter and return as clean html format.'''
        logger.info('Downloading %s', chapter['url'])

        novel_id = None
        chapter_id = None
        soup = self.get_soup(chapter['url'])
        for script in soup.select('head script'):
            novel_id = re.findall(r"'novel_id': '(\d+)'", str(script))
            chapter_id = re.findall(r"'chapter_id': '(\d+)'", str(script))
            if novel_id and chapter_id:
                novel_id = novel_id[0]
                chapter_id = chapter_id[0]
                break
            # end if
        # end for

        if not (novel_id and chapter_id):
            return None
        # end if
        data = json.dumps({
            'x1': novel_id,
            'x2': chapter_id,
        })
        headers={
            'Origin': self.home_url.strip('/'),
            'Referer': chapter['url'].strip('/'),
            'X-XSRF-TOKEN': self.cookies['XSRF-TOKEN'],
            'X-CSRF-TOKEN': soup.select_one('meta[name="csrf-token"]')['content'],
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
        }
        logger.debug("Request to %s with:\ndata = %s\nheaders=%s",
                     chapter_aux_url, data, headers)
        response = self.scraper.post(chapter_aux_url, data=data, headers=headers)
        data = response.json()

        # From https://www.foxteller.com/js/chapter.js line 4397:4403
        # Search text for the code block: Cookies.get("gdb1")
        aux = data['aux']
        aux = re.sub(r'%Ra&', "A", aux)
        aux = re.sub(r'%Rc&', "B", aux)
        aux = re.sub(r'%Rb&', "C", aux)
        aux = re.sub(r'%Rd&', "D", aux)
        aux = re.sub(r'%Rf&', "E", aux)
        aux = re.sub(r'%Re&', "F", aux)
        aux = base64.b64decode(aux)

        content = self.make_soup(aux)
        content = '\n'.join(str(p) for p in content.select('p'))
        return content
    # end def
# end class
