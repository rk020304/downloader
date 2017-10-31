#動作環境
#windows10 
#python3.5.2 anacondaで仮想環境を作成して使用。

#別添使用モジュール
#Mecab 自然言語処理
#natto-py Mecab と組み合わせて使用
#google URL検索
#OpenCV3 画像処理

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
from google import search

# -*- coding: utf-8 -*-
from google import search
from natto import MeCab
import os
import sys
import time
import bs4
import urllib.request
import urllib.parse
from urllib.request import urlopen
from urllib.parse import urlparse
import re
import cv2

mc = MeCab()
# テキストは cookbiz.jp より
text = input('何をダウンロードする？ : ')

headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
        }

print('====================================================')

# -F / --node-format オプションでノードの出力フォーマットを指定する
#
# %m    ... 形態素の表層文
# %f[0] ... 品詞
# %h    ... 品詞 ID (IPADIC)
# %f[8] ... 発音
#

words = []
with MeCab('-F%m,%f[0],%h') as nm:
    for n in nm.parse(text, as_nodes=True):
        node = n.feature.split(',');
        if len(node) != 3:
            continue
        if node[1] == '名詞':
            # if True:
            words.append(node[0])
print(words)
words = "　".join(words)
words = words.strip('[]\'')
words = words.replace('\'','')
words = words.replace(',',' ')
print(words,"で検索")


def google_search(query, pause=8.0, limit=1):
    for url in search(query, lang="jp", num=limit, stop=1):
        print('答え：{0}'.format(url))

        return url

url = google_search(words)

def get_html_string(url):
	"""
		Content:
			HTML取得
		Param:
			url	HTMLを取得するURL
	"""
	decoded_html = ""

	# HTMLを取得
	try:
		request = urllib.request.Request(url=url, headers=headers)
		response = urllib.request.urlopen(request)
		html = response.read()
	except:
		return decoded_html

	# エンコードを取得
	enc = check_encoding(html)
	if enc == None:
		return decoded_html

	# HTMLをデコード
	decoded_html = html.decode(enc)

	return decoded_html




	# HTMLをデコード

	decoded_html = html.decode(enc)



	return decoded_html

def check_encoding(byte_string):

	"""

		Content:

			文字コード確認

		Param:

			byte_string: バイト文字列

	"""

	encoding_list = ["utf-8", "utf_8", "euc_jp",

					"euc_jis_2004", "euc_jisx0213", "shift_jis",

					"shift_jis_2004","shift_jisx0213", "iso2022jp",

					 "iso2022_jp_1", "iso2022_jp_2", "iso2022_jp_3",

					"iso2022_jp_ext","latin_1", "ascii"]



	for enc in encoding_list:

		try:

			byte_string.decode(enc)

			break

		except:

			enc = None



	return enc

html = get_html_string(url)
# 変数
title    = ""						# Webページのタイトル
img_tag  = []						# imgタグのリスト
img_url  = []						# 画像URLのリスト
img_path = os.getcwd() + "/downloads"			# ダウンロードした画像の保存パス

# 正規表現
pat_title  = re.compile('<title>(.*?)</title>')		# ページタイトルを抜き出す
pat_a1     = re.compile('<a[\s]*href[\s]*=.*?>')	# aタグを抜き出す
pat_a2     = re.compile('href[\s]*="(.*?)"')		# URL先を抜き出す
pat_img1   = re.compile('<img[\s]*src[\s]*=.*?>')	# imgタグを抜き出す
pat_img2   = re.compile('src[\s]*="(.*?)"')		# 画像元URLを抜き出す
pat_img3   = re.compile('.+/(.*)')			# 画像ファイル名をURLから決定
img_format = [".jpg", ".png", ".gif", ".bmp"]		# 画像ファイル形式

# 関数定義
# 画像をダウンロードする関数
def image_download(url, output):
	opener = urllib.request.build_opener()
	req = urllib.request.Request(url, headers=headers)
	img_file = open(output, 'wb')
	img_file.write(opener.open(req).read())
	img_file.close()



"""
これ以降はHTMLページの取得画像のダウンロード処理
"""



# 画像をダウンロードするディレクトリ名
dl_path = img_path + "/" + title

# ページタイトルと同名のディレクトリを作成する
if not os.path.exists(dl_path):
	os.makedirs(dl_path)

# ディレクトリ権限の変更
os.chmod(img_path, 0o0777)
os.chmod(dl_path, 0o0777)

# 正規表現を利用してaタグ, imgタグを抜き出してリストに格納
a_tag   = pat_a1.findall(html)
img_tag = pat_img1.findall(html)

# aタグのリストから画像のURLを抜き出す
for i in a_tag:
	# URLを抜き出す
	m = pat_a2.search(i)

	# 取得オブジェクトがNoneでない場合に処理を行う
	if not m is None:
		# URLの取得
		tmp = m.group(1)

		# 画像フォーマットが一致すればリストに追加
		for j in img_format:
			if tmp.find(j) > -1:
				img_url.append(tmp)
				break


# imgタグのリストから画像のURLを抜き出す
for i in img_tag:
	# URLを抜き出す
	m = pat_img2.search(i)

	# 取得オブジェクトがNoneでない場合に処理を行う
	if not m is None:
		tmp = m.group(1)

		# 画像フォーマットが一致すればリストに追加
		for j in img_format:
			if tmp.find(j) > -1:
				img_url.append(tmp)
				break


# 画像URLのリストから実際の画像をダウンロードする
for i in img_url:
	# 画像ファイル名を決定
    try:
        m = pat_img3.search(i)
        name = m.group(1)
        output = dl_path + "/" + name
        # 画像のダウンロード
        image_download(i, output)
    except:
        pass
