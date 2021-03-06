#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests,json
from ..loggers  import orilogger
from antianti import USER_AGENTS,PROXIES
import random
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#17k小说站。
class Seventeenfree:

    s = requests.session()
    s.headers['User-Agent'] = random.choice(USER_AGENTS)
    chapter_num = 0
    freechap_num = 0
    vipchap_num = 0
    _chap_list = []

    origin = u'17K'
    bookstatus = ''

    def __init__(self, bookid, bookname):

        self.bookid = bookid
        self.bookname = bookname
        #self.raw_url = raw_url

    def get_info(self):
        _chaplist_api = 'http://client1.17k.com/rest/download/getBookVolumeSimpleListBybid?bookId='+self.bookid\
                        +'&tokenId=aGQxZWo2MkA6MTMxMTcyOTI5MToyMDAxMDY3'
        _info_api = 'http://client1.17k.com/rest/bookintroduction/getBookByid?bookId='+self.bookid
        self._chap_list = []
        try:
            _infodict = json.loads(self.s.get(_info_api,proxies=random.choice(PROXIES)).content)
            self.authorname = _infodict['book']['authorPenname']
            _chapdict = json.loads(self.s.get(_chaplist_api).content)
            for i in _chapdict['volumeList']:
                if i['name'] == u'作品相关':
                    continue
                for j in i['chapterList']:
                    self._chap_list.append((j['name'],j['id']))
                    if j['isFree'] == 'true':
                        self.freechap_num += 1
            self.chapter_num = len(self._chap_list)
            self.vipchap_num = self.chapter_num-self.freechap_num
        except:
            orilogger.exception(u'连接' + _chaplist_api + u'出错！\n' + u'无法获取\"' + self.bookname + u'\"章节信息。')

    def get_singel_novel(self,chapterid):
        _novel_api = 'http://client1.17k.com/rest/download/downChapterV2?chapterId='+\
                     chapterid+'&tokenId=aGQxZWo2MkA6MTMxMTcyOTI5MToyMDAxMDY3'
        try:
            _novel = json.loads(self.s.get(_novel_api,proxies=random.choice(PROXIES)).content)['content']
            realnovel = str(_novel).replace(u'\r\n', '    \n')
            return realnovel
        except:
            orilogger.warning(u'无法获取' + _novel_api + u'的章节内容。'+self.bookname)
            return ''

    def generate_txt(self):
        file = open(r'app/data/mobiworkshop/' + u'17K' + u'_' + self.bookname + '.txt', 'w')
        try:
            file.write(r'% '+self.bookname+'\n'+r'% '+u'作者： '+self.authorname+'\n'+r'% '+u'\n由fanclley推送。'+'\n\n')
            orilogger.info(self.bookname + str(self.freechap_num) + u'免费章节')
            for i in range(self.freechap_num):
                file.write('# '+self._chap_list[i][0] + '\n\n' + self.get_singel_novel(self._chap_list[i][1]) + '\n\n')
            orilogger.info(u'已生成\"' + self.bookname + u'\".txt')
            file.close()

        except:
            orilogger.exception(u'从17K生成\"' + self.bookname + u'\.txt"失败')



