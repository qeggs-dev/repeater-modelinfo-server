<div align="center">

# ModelAPI Info Server

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-63b9ff.svg)](https://opensource.org/licenses/MIT)

一个用于管理和提供模型 API 信息的 HTTP 服务，支持多模型配置、API密钥管理，为 Repeater 提供模型信息查询接口。
</div>

## WARNING:

**本项目默认使用 HTTP 作为数据传输协议**
**请勿暴露于公网**

### 环境变量

| 环境变量 | 描述 | 是否必填 | 默认值(*示例值*) |
| :---: | :---: | :---: | :---: |
| *`*API_KEY`* | API_Key (具体变量名由`API_INFO.API_FILE_PATH`指向 文件中`ApiKeyEnv`字段的名称) | **必填** | 从你所使用的AI厂商开放平台获取 API Key |
| `CONFIG_FILE_PATH` | 配置文件路径 | **选填** | `./config/main_configs.json` |

**HTTP状态码**：
- `200`: 成功
- `404`: 资源不存在
- `500`: 服务器内部错误

## 详细说明

如果你需要更详细的帮助，请查看 [详细文档](./docs/index.md)

## 许可证

[MIT License](LICENSE)