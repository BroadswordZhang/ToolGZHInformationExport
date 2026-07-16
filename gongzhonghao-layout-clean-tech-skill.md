---
name: gongzhonghao-layout-clean-tech
description: 当用户需要把公众号文章排成“张大刀修炼手册”修正版简洁技术文风格时使用。适用于将 Markdown 公众号文章转换为微信编辑器可粘贴的 HTML 排版稿，重点处理橙色前言/结语标题块、橙色编号短横线小节、15px 正文、2.05 行距、blockquote prompt 示例和整体克制的技术感版式。
---

# 公众号排版 Skill：简洁技术文版式

## 版式目标

把公众号文章排成一种“干净、克制、技术感强、适合长文阅读”的样式。当前标准参考 `templates/00.html` 的修正版：

- 页面整体是白底，不加外层卡片、阴影、边框。
- 文章标题保留为顶部 `h1`，字号 22px。
- 前言和结语使用简洁橙色标题块，即 `inline-block` 橙色短标签。
- 正文为黑灰色，字号适中，行距较大，适合手机阅读。
- 小节标题使用橙色编号和短横线，例如 `01 — 开新项目前...`。
- prompt 示例优先使用浅橙引用块，代码或命令才使用浅灰代码块。
- 整体不花哨，不使用大面积彩色背景，不堆装饰。

## 适用场景

使用本 skill 处理：

- AI / CV / 算法工程类公众号文章
- 技术教程、项目复盘、实战案例、工具推荐
- 已经写好的 Markdown 文章，需要转成公众号排版 HTML
- “张大刀修炼手册”类个人技术公众号内容

不要用于：

- 营销海报风格文章
- 大量卡片、渐变、emoji 装饰的内容
- 新闻快讯式短文
- 需要强品牌视觉系统的商业稿

## 输出要求

默认输出一份“可复制到微信公众号编辑器”的 HTML 片段。不要输出完整网页，不要包含 `<html>`、`<head>`、外链 CSS 或 JavaScript。

所有样式必须写成行内 `style`，因为微信公众号编辑器对外部 CSS 支持不稳定。

输出前先保留文章语义结构：

- `#` 文章标题：保留为顶部 `h1`，除非用户明确要求不输出标题。
- `## 前言` 或 `> **前言**`：转换为橙色短标题块。
- `## 01 案例分析`、`## 02 方案实现` 等编号小节：转换为橙色编号 + 短横线小节标题。
- 普通段落：转换为正文段落。
- 加粗内容：保留 `<strong>`。
- 代码块：转换为浅灰代码块。
- 图片：保留图片占位或 `<img>`，但不要强行加花哨边框。
- 结尾部分：默认只使用橙色 `结语` 短标题块和正文收束。只有原文已有 CTA 或用户明确要求时，才保留“顺手再看”“点个在看”等提示，不主动添加营销文案。

## 页面容器

所有正文内容包在一个容器里：

```html
<section style="font-size:15px;line-height:2.05;color:#2b2b2b;letter-spacing:0.2px;">
  ...
</section>
```

参数说明：

- `font-size: 15px`：技术长文正文不要太大。
- `line-height: 2.05`：正文行距偏舒展。
- `color: #2b2b2b`：避免纯黑刺眼。
- `letter-spacing: 0.2px`：保持轻微舒展，但不要扩大到影响中文阅读。

文章标题模板：

```html
<h1 style="font-size:22px;line-height:1.45;font-weight:700;color:#111;margin:0 0 22px 0;">
  文章标题
</h1>
```

## 前言标题块

将 `前言`、`结语`、`总结`、`背景` 等重要一级段落标题排成橙色短标题块。

模板：

```html
<section style="margin:0 0 28px 0;">
  <p style="display:inline-block;background:#f28c28;color:#ffffff;font-size:16px;line-height:1.6;font-weight:700;padding:4px 12px;margin:0 0 14px 0;">
    前言
  </p>
</section>
```

使用规则：

- 标题块背景使用橙色 `#f28c28`。
- 标题文字用白色 `#ffffff`，加粗，字号 `16px`。
- 标题块用短标签，不加左侧方块，不铺满整行。
- 标题块下方到正文保留 `14px` 左右。

## 橙色编号小节

将主要小节排成修正版中的橙色编号 + 短横线标题。

模板：

```html
<section style="margin:34px 0 0 0;">
  <h2 style="font-size:17px;line-height:1.7;font-weight:700;color:#111;margin:0 0 16px 0;">
    <span style="color:#f28c28;font-weight:700;">01</span>
    <span style="color:#f28c28;font-weight:700;"> — </span>
    开新项目前，先让它去 GitHub 找相似项目
  </h2>
</section>
```

使用规则：

- 编号格式用两位数：`01`、`02`、`03`。
- 编号和标题之间使用橙色短横线：`01 — 标题`。
- 橙色使用 `#f28c28`。
- 小节标题字号 `17px`，行高 `1.7`。
- 小节标题上方留白建议 `34px`。
- 小节标题下方到正文保留 `16px` 左右。
- 不再额外添加标题下划线，短横线已经在标题行中承担视觉分隔。

## 正文段落

普通段落模板：

```html
<p style="margin:0 0 14px 0;font-size:15px;line-height:2.05;">
  正文内容
</p>
```

正文规则：

- 每段可以比传统公众号略长，修正版允许把紧密相关的几句话合成一段，但不要长到手机上一屏只有一段。
- 技术长句可以拆成两段，提高手机阅读体验。
- 段落之间用 `margin-bottom: 14px`。
- 行高保持 `2.05`。
- 中文正文不要首行缩进。
- 重点词用 `<strong>`，不要用大面积高亮背景。

重点词模板：

```html
<strong style="font-weight:700;color:#1f1f1f;">在图片中写字符（汉字）</strong>
```

## 引导段

如果文章开头有一句导语，例如“本文主要分享……”：

```html
<p style="margin: 0 0 18px; color: #2b2b2b; font-size: 15px; line-height: 2.05;">
  在做项目过程中会有一些功能需要反复的运用到，其中有的功能比较耗时间并且对内存资源的消耗也是比较大的。
</p>
```

导语要直接说明：

- 文章讲什么问题
- 为什么这个问题值得写
- 读者看完能获得什么

## 代码块

技术文章不可避免有代码。代码块要清爽，不要花哨。普通 prompt 示例如果不是代码，优先使用引用块。

模板：

```html
<pre style="margin:0 0 18px 0;padding:14px;background:#f7f7f7;border-radius:4px;white-space:pre-wrap;word-break:break-word;font-size:14px;line-height:1.85;color:#333;"><code style="font-family:Menlo,Consolas,monospace;">代码内容</code></pre>
```

代码块规则：

- 背景用浅灰 `#f7f7f7`。
- 字号 `14px`。
- 使用 `white-space:pre-wrap;word-break:break-word;`，适配公众号窄屏。
- 不要给代码块加复杂阴影。

## Prompt 引用块

prompt、关键句、操作要求等非代码内容，使用浅橙引用块。

模板：

```html
<blockquote style="margin:0 0 18px 0;padding:10px 14px;border-left:3px solid #f28c28;background:#fff7ef;color:#444;font-size:15px;line-height:2.05;">
  在 GitHub 上搜索相似项目，找 3 到 5 个有参考价值的仓库。<br />
  分析它们的功能范围、技术栈、目录结构、核心实现方式、优缺点。<br />
  不要写代码，先输出调研结论和我这个项目应该借鉴什么、避免什么。
</blockquote>
```

规则：

- 引用块用于强调 prompt、判断句、关键原则。
- 背景使用 `#fff7ef`，左边框使用 `#f28c28`。
- 多行内容用 `<br />` 或保留段内换行，避免嵌套列表导致微信编辑器样式不稳定。
- 不要把所有段落都做成引用块，只突出真正需要复制或记住的内容。

## 图片

图片模板：

```html
<section style="margin: 22px 0; text-align: center;">
  <img src="图片地址" alt="" style="max-width: 100%; height: auto; display: block; margin: 0 auto;">
</section>
```

图片说明：

```html
<p style="margin: 8px 0 18px; color: #888; font-size: 13px; line-height: 1.7; text-align: center;">
  图 1：功能模块示意图
</p>
```

图片规则：

- 不要加厚边框。
- 不要圆角过大。
- 图注颜色用灰色。
- 图注不是必须，有解释价值时再加。

## 结尾区域

默认按照 `templates/00.html` 使用“结语短标题块 + 正文收束”的结构，不主动添加营销模块。

结尾结构：

1. 橙色 `结语` 短标题块。
2. 一到两段自然总结，说明本文核心判断。
3. 如果原文已有“希望对大家有用”等朴素收尾，可以保留。
4. 不主动添加“顺手再看”“点个在看”、表情图、按钮 CTA。

### 结语标题块

`结语` 使用与 `前言` 相同的橙色短标题块。

```html
<section style="margin:0 0 28px 0;">
  <p style="display:inline-block;background:#f28c28;color:#ffffff;font-size:16px;line-height:1.6;font-weight:700;padding:4px 12px;margin:0 0 14px 0;">
    结语
  </p>
</section>
```

### 完整结尾模板

```html
<section style="margin:0 0 28px 0;">
  <p style="display:inline-block;background:#f28c28;color:#ffffff;font-size:16px;line-height:1.6;font-weight:700;padding:4px 12px;margin:0 0 14px 0;">
    结语
  </p>
</section>

<p style="margin:0 0 14px 0;font-size:15px;line-height:2.05;">
  vibe coding 不是把需求丢给 AI，然后等它吐代码。更像是你带一个很快、很能干、但容易冲太猛的工程师做项目。
</p>
```

## 列表

列表不使用默认样式，使用段落模拟，避免微信编辑器兼容问题。

模板：

```html
<p style="margin: 0 0 10px; color: #2b2b2b; font-size: 15px; line-height: 2.05;">
  <strong style="color: #1f1f1f;">1. 硬件资源评估：</strong>主要考虑 CPU、GPU、内存和并发量。
</p>
```

规则：

- 技术文中列表项可以加粗前缀。
- 每一项只讲一个点。
- 不要嵌套太深。

## 分割与留白

留白比装饰重要。

推荐间距：

- 前言/结语标题块所在 section 下方：`28px`
- 标题块下方：`14px`
- 小节标题上方：`34px`
- 小节标题下方：`16px`
- 正文段落下方：`14px`
- 图片上下：`22px`
- 代码块上下：`18px`

不要连续堆多个分割线。

## 颜色系统

只使用少量颜色：

- 正文黑灰：`#2b2b2b`
- 标题黑：`#222`
- 橙色标题块 / 小节：`#f28c28`
- 标题块文字：`#ffffff`
- 图注灰：`#888`
- 代码背景：`#f7f7f7`
- 引用块背景：`#fff7ef`
- 引用块文字：`#444`

避免：

- 大面积纯黑背景。
- 多种高饱和颜色混用。
- 渐变背景。
- 花哨边框和阴影。

## Markdown 到排版稿转换规则

转换时按以下规则处理：

| Markdown | 转换结果 |
|---|---|
| `## 前言` | 橙色短标题块 |
| `> **前言**` | 橙色短标题块 |
| `## 01 案例分析` | 橙色编号 + 短横线小节 |
| `## 案例分析` | 自动编号为橙色小节 |
| 普通段落 | 正文 `<p>` |
| `**重点**` | `<strong>` |
| 代码块 | 浅灰 `<pre><code>` |
| prompt 示例 / 关键原则 | 浅橙 `<blockquote>` |
| 图片 | 居中 `<img>` |
| `## 结语` / `> **结语**` | 橙色结语短标题块 + 正文收束 |
| `如果觉得写的内容...顺手再看` | 仅原文已有时保留为普通正文 |
| `如果有用 点个在看` | 仅用户明确要求 CTA 时才转换 |
| 引用解释 | 可转为普通段落，除非确实需要强调 |

自动编号规则：

- 从第一个非“前言”的二级标题开始编号。
- 编号使用 `01`、`02`、`03`。
- 如果原文已经有编号，保留原编号。

## 示例：输入 Markdown

```markdown
## 前言

在做项目过程中会有一些功能需要反复的运用到，其中有的功能比较耗时间并且对内存资源的消耗也是比较大的。

在本文中将分享如何通过 **c++ 的动态库** 节约开发时间成本以及项目实施过程中的硬件资源成本。

## 案例分析

在这里我以自己在项目的经常用到的功能：**在图片中写字符（汉字）**。
```

## 示例：输出 HTML

```html
<section style="font-size:15px;line-height:2.05;color:#2b2b2b;letter-spacing:0.2px;">
  <section style="margin:0 0 28px 0;">
    <p style="display:inline-block;background:#f28c28;color:#ffffff;font-size:16px;line-height:1.6;font-weight:700;padding:4px 12px;margin:0 0 14px 0;">
      前言
    </p>
  </section>

  <p style="margin:0 0 14px 0;font-size:15px;line-height:2.05;">
    在做项目过程中会有一些功能需要反复的运用到，其中有的功能比较耗时间并且对内存资源的消耗也是比较大的。
  </p>

  <p style="margin:0 0 14px 0;font-size:15px;line-height:2.05;">
    在本文中将分享如何通过 <strong style="font-weight:700;color:#1f1f1f;">c++ 的动态库</strong> 节约开发时间成本以及项目实施过程中的硬件资源成本。
  </p>

  <section style="margin:34px 0 0 0;">
    <h2 style="font-size:17px;line-height:1.7;font-weight:700;color:#111;margin:0 0 16px 0;">
      <span style="color:#f28c28;font-weight:700;">01</span>
      <span style="color:#f28c28;font-weight:700;"> — </span>
      案例分析
    </h2>
  </section>

  <p style="margin:0 0 14px 0;font-size:15px;line-height:2.05;">
    在这里我以自己在项目的经常用到的功能：<strong style="font-weight:700;color:#1f1f1f;">在图片中写字符（汉字）</strong>。
  </p>
</section>
```

## 排版前检查

在输出排版稿前检查：

- 是否所有样式都为行内样式。
- 是否没有外链 CSS 和 JavaScript。
- 是否没有过度装饰。
- 是否正文行距足够。
- 是否小节编号统一为两位数。
- 是否前言块符合“橙色短标签 + 白色标题”。
- 是否小节标题符合“橙色编号 + 橙色短横线 + 黑色标题”。
- 是否结尾默认没有额外营销文案。
- 是否保留了加粗重点。
- 是否适合直接复制到微信公众号编辑器。

## 快速提示词模板

```text
请使用“公众号排版 Skill：简洁技术文版式”，把下面这篇 Markdown 文章转换成微信公众号编辑器可粘贴的 HTML 排版稿。
要求：
1. 前言使用橙色标题块；
2. 小节标题使用橙色编号和短横线；
3. 正文保持 15px 字号、2.05 行距；
4. 所有样式写成行内 style；
5. 不要添加额外营销文案。

文章如下：
【粘贴 Markdown】
```
