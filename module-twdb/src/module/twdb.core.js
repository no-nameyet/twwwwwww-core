'use strict';
import * as duckdb from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.28.1-dev106.0/+esm';

//
// 事前処理
//
// DuckDBのロード
let DB;

// Connectionの確立
let CONNECTION;

//
// 関数
//
/**
 * 初期化処理
 * @param {*} medadata メタデータ
 */
export async function initModule(metadata) {
	// DuckDBのロード
	DB = await (async () => {
		const bundles = duckdb.getJsDelivrBundles();
		const bundle = await duckdb.selectBundle(bundles);
		const worker = new Worker(URL.createObjectURL(
			new Blob([`importScripts('${bundle.mainWorker}');`], { type: 'text/javascript' })
		));
		// DBのインスタンス化
		let db = new duckdb.AsyncDuckDB({
			// ログ処理
			log: () => {},
		}, worker);
		await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
		return db;
	})();

	// Connectionの確立
	CONNECTION = await DB.connect();

	// ファイルの読み込み
	const fetchTasks = Object.entries(metadata.data_list).map(async ([tableName, fileName]) => {
		const response = await fetch(new URL('./data/' + fileName, import.meta.url));
		const buffer = await response.arrayBuffer();
		return { tableName, fileName, buffer };
	});
	const results = await Promise.all(fetchTasks);
	// テーブル生成
	for (const { tableName, fileName, buffer } of results) {
		await DB.registerFileBuffer(fileName, new Uint8Array(buffer));
		await CONNECTION.query(`
			CREATE TABLE ${tableName} AS
			SELECT * FROM read_parquet('${fileName}')
		`);
	}
}

/**
 * クエリの実行
 * @param {*} query クエリ
 * @returns 結果
 */
async function query(query) {
	if (!CONNECTION) {
		return;
	}
	const result = await CONNECTION.query(query);
	const columns = result.schema.fields.map(f => f.name);
	return result.toArray().map(row =>
		Object.fromEntries(columns.map(col => {
			if (typeof row[col] === 'object') {
				return [col, [...row[col]]];
			} else {
				return [col, row[col]];
			}
		}))
	);
}

/**
 * 切断
 */
async function disconnect() {
	if (CONNECTION) {
		await CONNECTION.close();
		CONNECTION = null;
	}
}

// エクスポート
export default {
	disconnect,
	query,
};
