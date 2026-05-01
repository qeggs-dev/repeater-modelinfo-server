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
      "limit": { // 限制，包含以下字段
        "max_connections": 100, // 最大连接数
        "max_keepalive_connections": 20, // 最大保持连接数
        "keepalive_expiry": 5, // 保持连接的过期时间，单位为秒
      },
      "timeout": { // 超时时间，单位为秒，这里也可以填写一个数字，表示总超时
        "connect": 10, // 连接超时
        "read": 30, // 读取超时
        "write": 30, // 写入超时
        "pool": 30 // 连接池超时
      },
      "models": [], // 模型手动填充列表，目前为保留字段
      "proxy": null, // HTTP 代理
    }
  ],
  "library_file": "providers_library.json", // 模型库文件，如果不写则每次都直接从供应商获取模型信息
}
```