# Model Info Object

模型信息，可以用于访问模型
以下是结构示例：

``` json
{
  "name": "Model Name", // 可读的模型名称
  "url": "https://api.example.com/v1", // 模型 API 的 URL
  "id": "model-id", // 面向厂商的模型 ID
  "uid": "deepseek/model-id", // 模型的唯一标识符，可用于查询
  "parent": "Deepseek", // 该模型所属的模型组
  "parent_id": "deepseek", // 模型组 ID，可用于查询
  "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", // API 密钥
  "uid": "deepseek-chat", // 面向查询的模型 ID
  "limit": { // 限制，包含以下字段
    "max_connections": 100, // 最大连接数
    "max_keepalive_connections": 20, // 最大保持连接数
    "keepalive_expiry": 5, // 保持连接的过期时间，单位为秒
  "timeout": { // 超时时间，单位为秒，这里也可以填写一个数字，表示总超时
    "connect": 10, // 连接超时
    "read": 30, // 读取超时
    "write": 30, // 写入超时
    "pool": 30 // 连接池超时
  }
}
```