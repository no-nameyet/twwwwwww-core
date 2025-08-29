from file_system import file_system as fs, temp_dir as td
from twwwwwww import paradox as pd

# ~~~~~~~~~~~~~~~~~~~~~~~
# 定数
# ~~~~~~~~~~~~~~~~~~~~~~~
# モジュールページ ソースディレクトリ
module_path = fs.join_path(fs.current_dir(), 'module-twdb/src')
# 配信ディレクトリ
temp_web_path = fs.join_path(td.path(), 'web')
# 配信ディレクトリ
dist_dir = fs.join_path(fs.current_dir(), 'dist')

# ~~~~~~~~~~~~~~~~~~~~~~~
# main関数
# ~~~~~~~~~~~~~~~~~~~~~~~
def main():
	# モジュールページを一時ディレクトリへ複製
	fs.copy_dir(module_path, temp_web_path)
	# パラドクスデータベースの構築
	pd.make_db()
	# 配信ディレクトリの作成
	fs.remake_dir(dist_dir)
	# 一時ディレクトリから配信ディレクトリへコピー
	fs.copy_dir(temp_web_path, dist_dir)

# 直接呼出し時にmain関数を参照させる
if __name__ == '__main__':
	main()
