import json

# ~~~~~~~~~~~~~~~~~~~~~~~
# 関数
# ~~~~~~~~~~~~~~~~~~~~~~~
# JSONを出力する
def make_to(data, path):
	# ファイルパスを安全に構築
	with open(path, 'w', encoding='utf-8', newline='') as file:
		json.dump(data, file, ensure_ascii=False)
