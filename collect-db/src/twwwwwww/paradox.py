import re
import datetime
import pytz
from bs4 import BeautifulSoup
import pyarrow as pa

from file_system import file_system as fs, temp_dir as td
from scraping import scraping
from data_file import parquet, json
from hash import crc32

# ~~~~~~~~~~~~~~~~~~~~~~~
# 定数
# ~~~~~~~~~~~~~~~~~~~~~~~
# ダウンロードするURLの一覧
PARADOX_URL = 'https://tw7.t-walker.jp/garage/gravity/all'

# スキーマ定義
SCHEMA = {
	'tw7_paradox': [
		('index', pa.uint32()),
		('id', pa.uint32()),
		('name', pa.string()),
		('status', pa.string()),
		('target', pa.string()),
		('effect1', pa.string()),
		('effect2', pa.string()),
		('skills', pa.list_(pa.uint32())),
	],
	'tw7_skills': [
		('index', pa.uint32()),
		('id', pa.uint32()),
		('skill', pa.string()),
		('prefix', pa.string()),
	],
}

# データディレクトリ名
DIR_DATA_NAME = 'web/module/data'
# データディレクトリパス
PATH_DATA = fs.join_path(td.path(), DIR_DATA_NAME)

# ~~~~~~~~~~~~~~~~~~~~~~~
# 関数
# ~~~~~~~~~~~~~~~~~~~~~~~
# DBの作成
def make_db():
	# HTMLの取得
	html_path = scraping.load(PARADOX_URL, 'paradox.html')
	with open(html_path, 'r', encoding='utf-8') as file:
		soup = BeautifulSoup(file, 'html.parser')
	# スキル一覧
	skills = __skills(soup)
	parquet.make_to(skills, fs.join_path(PATH_DATA, 'tw7_skills.parquet'), pa.schema(SCHEMA['tw7_skills']))
	# パラドクス一覧
	paradox = __paradox(soup, skills)
	parquet.make_to(paradox, fs.join_path(PATH_DATA, 'tw7_paradox.parquet'), pa.schema(SCHEMA['tw7_paradox']))
	# メタ情報
	json.make_to({
		'updateAt': datetime.datetime.now(pytz.timezone('Asia/Tokyo')).ctime(),
		'skill_count': len(skills),
		'paradox_count': len(paradox),
		'data_list': {
			'tw7_paradox': 'tw7_paradox.parquet',
			'tw7_skills': 'tw7_skills.parquet',
		},
	}, fs.join_path(PATH_DATA, 'metadata.json'))

# スキル一覧の取得
def __skills(soup):
	skills = []
	index = 1
	for optgroup in soup.select('.filter-skill > optgroup'):
		prefix = optgroup.get('label')
		options = optgroup.select('option')
		for option in options:
			value = option.get('value')
			skills.append({
				'index': index,
				'id': crc32.hash(value),
				'skill': value,
				'prefix': prefix
			})
			index += 1
	return skills

# パラドクス一覧の取得
def __paradox(soup, skills):
	skills_map = { skill['skill']: skill for skill in skills }
	paradox = []
	for idx, part in enumerate(soup.select('.grid-parts')):
		id = part.select('a')[0].get('href').split('#')[-1]
		paradox.append({
			'index': idx + 1,
			'id': int(id),
			'name': part.select('h4')[0].text,
			'status': part.select('span')[0].text,
			'target': re.findall(r'対象：(\d)体', part.text)[0],
			'effect1': re.findall(r'効果1：【([^】]+)】', part.text)[0],
			'effect2': re.findall(r'効果2：【([^】]+)】', part.text)[0],
			'skills': [
				skills_map[name]['id']
				for name in re.split(r'[　 ]', re.findall(r'使用技能：([^\n]+)', part.text)[0]) if name in skills_map
			]
		})
	return paradox
