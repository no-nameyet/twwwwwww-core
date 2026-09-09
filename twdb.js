'use strict';
import module, { initModule, } from './module/twdb.core.js';
import metadata from './module/data/metadata.json' with { type: 'json' };

// 初期化処理
await initModule(metadata);

export { metadata };
export default module;
