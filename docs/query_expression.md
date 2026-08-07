# Query expression

用于描述查询条件，以供服务器进行模型检索

支持以下写法：

1. `all`: 返回所有模型
2. `<provider>`: 返回该供应商下的所有模型
3. `<model_id>`: 返回所有供应商下的该模型
4. `<provider>/<model_id>`: 返回该供应商下的指定模型，通常这种写法只能返回一个模型，可用于锁定模型请求
5. `match:<regex>`: 返回所有 `4` 格式下满足正则表达式的模型
6. `search:<regex>`: 返回所有 `4` 格式下满足正则表达式的模型，但是包含该模式而非全字匹配该模式
7. `schema:<schema>`: 返回所有模型资料满足提交的 json schema 的模型（不安全，攻击者可以构造匹配来爆破你的 API Key）
8. `fuzzy:<model_uid>:<count>`: 模糊匹配指定 `model_uid` 的模型，返回 `count` 个结果

当所有查询表达式无法匹配到时
使用模糊匹配，返回 `default_fuzzy_match_limit` 个结果