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
  "timeout": 600.0 // 超时时间，单位为秒
}
```