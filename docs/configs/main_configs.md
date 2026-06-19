# Main Configs

指导绝大多数操作的配置文件

``` json
{
    "logger": {
        "file_path": "./logs/rmi-log-{time:YYYY-MM-DD_HH-mm-ss.SSS}.log", // 日志文件路径
        "level": "DEBUG", // 日志级别
        "rotation": "1 days",  // 日志轮转间隔
        "retention": "7 days",  // 日志保留时间
        "console_format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>", // 控制台输出格式
        "file_format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {message}", // 文件输出格式
        "compression": "zip" // 日志压缩格式
    },
    "model_api": {
        "api_file_path": "./configs/api_info.json", // 模型信息引导文件路径
        "default_timeout": 600.0, // 在模型没有定义超时时间时使用的超时时间
        "allow_schema_match": false, // 是否允许在任何地方使用 json schema 进行模型匹配
        "default_fuzzy_match_limit": 32, // 在模型没有定义模糊匹配上限时使用的值
        "refresh_interval": 21600.0, // 模型信息自动刷新的间隔时间
    },
    "server": {
        "host": "", // 服务器绑定的主机
        "port": "", // 服务器绑定的端口
        "api_key_env": "API_KEY", // API_KEY 环境变量名
        "workers": null, // 服务器使用的进程数
        "reload": null, // 服务器是否在代码更改时自动重启
        "run_server": true // 是否运行服务器
    }
}
```