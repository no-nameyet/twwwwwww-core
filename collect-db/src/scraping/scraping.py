import requests

from file_system import file_system as fs, temp_dir as td

# ~~~~~~~~~~~~~~~~~~~~~~~
# 定数
# ~~~~~~~~~~~~~~~~~~~~~~~
# リクエストヘッダ
REQUEST_HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# ~~~~~~~~~~~~~~~~~~~~~~~
# 関数
# ~~~~~~~~~~~~~~~~~~~~~~~
# URLからHTMLを取得し、一時ディレクトリに保存する
def load(url: str, file_name: str) -> str:
	# HTML取得
	response = requests.get(url, headers=REQUEST_HEADERS)
	if response.status_code != requests.codes.ok:
		raise requests.exceptions.HTTPError(f'サーバーが無効です: {url}')
	# ファイル名を取得
	path = fs.join_path(td.path(), file_name)
	# HTMLを保管
	with open(path, 'w', encoding='UTF-8') as file:
		file.write(response.text.replace('\u200B', ''))
	return path
