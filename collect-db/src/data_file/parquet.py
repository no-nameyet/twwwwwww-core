import pyarrow as pa
import pyarrow.parquet as pq

# ~~~~~~~~~~~~~~~~~~~~~~~
# 関数
# ~~~~~~~~~~~~~~~~~~~~~~~
# PARQUETを出力する
def make_to(data, path, schema=None):
	if isinstance(data, dict):
		data = list(data.values())
	if not data:
		return
	# Parquetに変換して保存
	table = pa.Table.from_pylist(data, schema=schema)
	pq.write_table(table, path, compression='SNAPPY')
