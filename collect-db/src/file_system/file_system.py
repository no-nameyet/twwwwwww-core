import os
import shutil

# ~~~~~~~~~~~~~~~~~~~~~~~
# 関数
# ~~~~~~~~~~~~~~~~~~~~~~~
# カレントディレクトリの取得
def current_dir():
	return os.getcwd()

# パスの結合
def join_path(*paths):
	return os.path.join(*paths)

# ディレクトリの再作成
def remake_dir(dir_path):
	if os.path.exists(dir_path):
		shutil.rmtree(dir_path)
	os.mkdir(dir_path)

# ディレクトリのコピー
def copy_dir(from_dir_path, to_dir_path):
	shutil.copytree(from_dir_path, to_dir_path, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.gitkeep'))
