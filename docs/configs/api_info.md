# API Info

用于记录模型信息

```json
[
  {
    "name": "OpenAI API Group",
    "api_key_env": "OPENAI_API_KEY", // 模型API密钥环境变量的名称
    "url": "https://api.openai.com/v1",
    "timeout": 30, // 共用超时时间
    "models": [
      {
        "name": "GPT 4", // 可读的模型名称
        "uid": "gpt-4",  // 面向查询的模型唯一标识符
        "id": "gpt-4", // 面向厂商的模型 ID
        "type": "chat", // 模型类型
        "url": "" // 可以为模型独立设置 URL
      },
      {
        "name": "GPT 3.5 Turbo",
        "uid": "gpt-3.5-turbo",
        "id": "gpt-3.5-turbo",
        "type": "chat",
        "timeout": 30 // 可以为模型独立设置超时
      }
    ]
  }
]
```