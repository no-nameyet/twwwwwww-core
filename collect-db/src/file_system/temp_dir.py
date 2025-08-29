from file_system import file_system as fs

# ~~~~~~~~~~~~~~~~~~~~~~~
# 定数
# ~~~~~~~~~~~~~~~~~~~~~~~
# 一時ディレクトリ名
DIR_TEMP_NAME = 'temp'
# 一時ディレクトリパス
PATH_TEMP = fs.join_path(fs.current_dir(), DIR_TEMP_NAME)

# ~~~~~~~~~~~~~~~~~~~~~~~
# 初期化処理
# ~~~~~~~~~~~~~~~~~~~~~~~
# 一時ディレクトリの作成
fs.remake_dir(PATH_TEMP)

# ~~~~~~~~~~~~~~~~~~~~~~~
# 関数
# ~~~~~~~~~~~~~~~~~~~~~~~
# 一時ディレクトリのパスを取得
def path():
	return PATH_TEMP
