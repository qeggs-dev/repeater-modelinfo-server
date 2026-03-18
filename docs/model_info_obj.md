# Model Info Object

模型信息，可以用于访问模型
以下是结构示例：

## Model Info Object

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

## Static Model Info Object

如果是静态模型信息，则返回以下结构：

``` json
{
  "name": "Model Name",
  "url": "https://api.example.com/v1",
  "id": "model-id", // 面向厂商的模型 ID
  "parent": "Deepseek", // 该模型所属的模型组
  "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", // API 密钥
  "uid": "deepseek-chat", // 面向查询的模型 ID
  "type": "chat", // 模型类型
  "timeout": 600.0 // 超时时间，单位为秒
}
```