# Windows 可执行版使用说明

## 文件

- `GZHInformationExporter.exe`

## 启动

双击 `GZHInformationExporter.exe`，程序会启动本地 Web 服务并自动打开浏览器。

如果浏览器没有自动打开，请手动访问：

```text
http://127.0.0.1:7860
```

## 使用

在页面中填写：

- 公众号名称
- fakeid
- token
- Cookie
- 输出目录
- 请求间隔

然后点击「开始提取」。

## 注意

- 运行时不要关闭 exe 的命令行窗口，关闭窗口会停止本地服务。
- Cookie 和 token 是敏感登录凭证，请不要公开分享。
- 本工具仅用于本人拥有管理权限或已获得明确授权的公众号内容导出与分析。
