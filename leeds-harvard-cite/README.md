# Leeds Harvard Citation Formatter / 利兹哈佛引用格式化工具

## Introduction / 简介

This tool helps students and researchers at UK universities automatically format academic citations in Harvard style. You can simply copy and paste journal article information from online sources, and the system will intelligently extract key details like authors, title, journal name, year, volume, pages and DOI, then generate a properly formatted citation. It supports both web-based and command-line usage, making it easy to maintain consistent citation standards across your academic work.

这个工具帮助英国高校的学生和研究人员自动生成哈佛格式的学术引用。你只需要从在线期刊网站复制文献信息，粘贴到网页或命令行中，系统就会自动识别作者、标题、期刊、年份、卷期、页码和DOI等关键信息，最后生成规范的引用文本。支持网页界面和命令行两种使用方式，让你轻松保持论文引用的一致性。

## Key Features / 主要功能

- **Automatic Extraction / 自动识别**: Recognizes structured and unstructured citation data from journal websites / 识别来自期刊网站的结构化和非结构化引用数据
- **Harvard Formatting / 哈佛格式化**: Generates properly formatted Harvard-style citations for UK universities / 为英国高校生成规范的哈佛格式引用
- **Flexible Interface / 灵活界面**: Available as both web interface and CLI tool / 支持网页界面和命令行工具两种方式
- **Multi-university Support / 多校支持**: Tailored for various UK university citation guidelines / 适配多所英国高校的引用规范

## Quick Start / 快速开始

**Web Interface / 网页版**: Open `index.html` in your browser, or run `python3 -m http.server 8000` and visit `http://localhost:8000/index.html`

**Command Line / 命令行版**: Use `main.py` to format citations with arguments like `--authors`, `--title`, `--year`, etc.

## Project Structure / 项目结构

- `index.html` - Web interface / 网页界面
- `main.py` - Command-line entry point / 命令行入口
- `formatter.py` - Citation formatting logic / 引用格式化核心逻辑
- `universities.py` - University data and metadata / 高校列表与元数据
- `UK_UNIVERSITIES_CITATION_GUIDELINES.md` - Research notes on UK university citation styles / 各高校引用风格调研记录

查看支持的高校：

```bash
python3 main.py --list-universities
```

格式化单条引文：

```bash
python3 main.py \
  --authors "Smith, John; Johnson, Amy" \
  --year 2024 \
  --title "Article Title" \
  --journal "Journal Name" \
  --volume 10 \
  --issue 2 \
  --pages 15-30 \
  --doi "10.1016/j.example.2024.01.001"
```

交互模式：

```bash
python3 main.py --interactive
```

## 输入建议

- 网页端最适合直接粘贴期刊网站复制出来的原始文本。
- 保持原始顺序通常最稳：
  作者、标题、期刊名、卷号、年份、页码或文章号、DOI 或 URL。
- 生成后仍建议人工快速检查一次标题、期刊名和页码。

## 当前实现说明

- 网页端和命令行端都以 Harvard 风格为核心。
- “学校选择”目前主要保留为扩展入口和信息展示，不同学校的细粒度差异模板还可以继续补充。
- 前端对常见的期刊复制文本格式做了启发式识别，但极端格式仍可能需要人工校对。

## 开发建议

- 如果继续扩展高校差异，建议先统一一个“学校配置 -> 格式规则”的结构，再让前后端共用。
- 如果继续优化前端识别，建议把 `index.html` 中的解析逻辑进一步抽成单独的 JS 模块。
