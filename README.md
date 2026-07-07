# 公众号文章导出工具

这个工具用于导出微信公众号文章正文和可获取的统计数据，并保存为 Markdown。

## 能拿到什么

- 文章标题、作者、发布时间、原文链接
- 正文 Markdown
- 微信接口返回的统计字段，例如 `read_num`、`like_num`、`old_like_num` 等
- 如果接口返回转发量、转载量相关字段，脚本会原样保存到 Markdown front matter、`summary.csv` 和 `summary.json`

注意：阅读量、点赞量等统计通常需要微信登录 Cookie。转发量、转载量不一定对普通访问者开放，接口不返回时脚本会留空。

## 安装依赖

```powershell
python -m pip install -r requirements.txt
```

## 方式一：按公众号名称自动找文章

1. 在浏览器登录微信公众平台：`https://mp.weixin.qq.com/`
2. 打开开发者工具，从任意后台请求里复制完整 `Cookie`
3. 从当前后台 URL 里复制 `token` 参数，例如 `token=123456789`
4. 运行：

```powershell
python .\wechat_public_account_exporter.py account --account "修炼手册" --cookie "你的Cookie" --token "你的token" --output .\output
```

也可以把 Cookie 保存到 `cookie.txt` 后运行，避免命令历史里出现 Cookie：

```powershell
python .\wechat_public_account_exporter.py account --account "修炼手册" --cookie-file .\cookie.txt --token "你的token" --output .\output
```

## 方式二：给文章链接列表

把文章链接逐行放进 `article_urls.txt`，然后运行：

```powershell
python .\wechat_public_account_exporter.py urls --input .\article_urls.txt --output .\output
```

如果还想抓阅读/点赞统计，也加上 Cookie：

```powershell
python .\wechat_public_account_exporter.py urls --input .\article_urls.txt --cookie "你的Cookie" --output .\output
```

或：

```powershell
python .\wechat_public_account_exporter.py urls --input .\article_urls.txt --cookie-file .\cookie.txt --output .\output
```

## 输出

- `output/articles/*.md`：每篇文章一个 Markdown 文件
- `output/summary.csv`：汇总表
- `output/summary.json`：完整结构化数据
