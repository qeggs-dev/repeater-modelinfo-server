# Model Info Object

模型信息，可以用于访问模型
以下是结构示例：

``` json
{
  "name": "Model Name",
  "url": "https://api.example.com/v1",
  "id": "model-id", // 面向厂商的模型 ID
  "parent": "Deepseek", // 该模型所属的模型组
  "uid": "deepseek-chat", // 面向查询的模型 ID
  "type": "chat", // 模型类型
  "timeout": 600.0 // 超时时间，单位为秒
}
```

PS: API Key 需要另外的 API 获取