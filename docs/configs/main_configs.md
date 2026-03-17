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
        "api_file_path": "./configs/api_info.json", // 模型API信息文件路径
        "case_sensitive": false, // 模型 UID 是否区分大小写
        "default_timeout": 600.0 // 在模型没有定义超时时间时使用的超时时间
    },
    "server": {
        "host": "", // 服务器绑定的主机
        "port": "", // 服务器绑定的端口
        "workers": null, // 服务器使用的进程数
        "reload": null, // 服务器是否在代码更改时自动重启
        "run_server": true // 是否运行服务器
    }
}
```