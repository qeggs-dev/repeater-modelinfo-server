# API Info

该文件作为索引，用于指导模型信息获取与存储。

```json
{
  "type": "model_group_config.v1", // 一个固定的字符串，用于标识配置文件类型
  "providers": [
    {
      "name": "OpenAI API Group", // 模型组名称
      "id": "openai", // 模型组 ID，用于查询与唯一标识
      "api_key_env": "OPENAI_API_KEY", // 模型API密钥环境变量的名称，你也可以在这里填写列表以支持多个密钥随机访问
      "url": "https://api.openai.com/v1",
      "timeout": 30, // 请求超时时间
      "proxy": null, // HTTP 代理
    }
  ],
  "library_file": "providers_library.json", // 模型库文件，如果不写则每次都直接从供应商获取模型信息
}
```