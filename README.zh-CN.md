# aaa-research

[English](README.md)

面向 AI agent 的[亚洲艺术文献库（Asia Art Archive）](https://aaa.org.hk/en)研究技能。它帮助 agent 查询艺术家、展览、出版物、档案和口述历史，并给出可追溯的来源与明确的访问范围。

入口是仓库根目录的 [`SKILL.md`](SKILL.md)。技能使用 agent 已有的网页和浏览器工具，不提供 API、本地馆藏数据库或访问凭据。

## 能做什么

- 在馆藏、活动数据库、AAA 项目、研究文章和教学资源之间选择合适的查询入口。
- 处理姓名变体和多语言检索，区分艺术家、作者、策展人、出版方及档案所有者。
- 整理书目、展览时间线、档案概览和有明确范围的资料清单。
- 从目录记录追溯原始文件，区分元数据与实际阅读的内容，引用对应页码或时间点。
- 处理访问失败、分页不完整、扫描件、字幕和机器转录，并说明证据的局限。

适用于以 **aaa.org.hk** 为来源的研究；不替代一般亚洲艺术检索，也不连接独立的 AAA in America 馆藏目录。

## 安装

安装好 Node.js/npm 和 Git 后，运行：

```sh
npx skills add aaajiao/aaa-research
```

[Skills CLI](https://github.com/vercel-labs/skills) 默认安装到当前项目，并让你选择使用的 agent。若希望为 Codex 安装到用户级目录：

```sh
npx skills add aaajiao/aaa-research --skill aaa-research --agent codex --global
```

若要在当前项目中固定安装 **v1.0.0**：

```sh
npx skills add https://github.com/aaajiao/aaa-research/tree/v1.0.0 --skill aaa-research
```

**已经安装过？** 沿用已有安装的范围和 agent，避免在项目级、用户级或旧配置目录中保留重复副本，包括旧版 `~/.codex/skills` 路径。

也可从[版本页面](https://github.com/aaajiao/aaa-research/releases/tag/v1.0.0)下载 [v1.0.0 ZIP](https://github.com/aaajiao/aaa-research/releases/download/v1.0.0/aaa-research-v1.0.0.zip) 和 [SHA256SUMS](https://github.com/aaajiao/aaa-research/releases/download/v1.0.0/SHA256SUMS)。将两者放在同一目录，解压前校验：

```sh
shasum -a 256 -c SHA256SUMS
```

Linux 可使用 `sha256sum -c SHA256SUMS`。解压后，`SKILL.md` 应直接位于所选的 `aaa-research` 目录内，避免多套一层文件夹。Codex 手动安装目录可参考[官方技能指南](https://learn.chatgpt.com/docs/build-skills)，随后按所用 agent 的方式重新发现或加载技能。

## 环境要求与示例

通过 `npx` 安装需要 **Node.js/npm 和 Git**。Agent 需要支持目录形式的技能，并具备可用的网页读取或浏览器控制工具。交互式馆藏查询可能需要连接普通浏览器。可选的访问检查脚本和开发命令需要 **Python 3.10+**；访问检查还需要 **curl**。PDF 渲染、OCR 和音频转录使用当前环境提供的工具，不随技能打包。

可以这样提问：

```text
用 $aaa-research 查找 aaajiao 可在线访问的资料，区分作品记录、
展览相关印刷品和出版物，并附上具体馆藏链接。

用 $aaa-research 整理 1990 年代台湾艺术家自主空间的研究书目，
说明检索范围，以及哪些资料实际读过原文。

用 $aaa-research 查找彭锦耀的访谈，说明哪些录像和文字版本
可以在线阅读，哪些需要到馆。
```

## 已验证范围与限制

代表性流程于 **2026 年 10 月 6 日**完成检查。在测试环境中，连接的普通 Chrome 可以查询网站，而直接请求主站页面返回 HTTP 403；部分条目公开链接的 PDF 仍可读取。这证明了一条当时可用的访问路径，不能确定拒绝原因，也不保证其他环境可以无人值守运行。

原始媒体检查覆盖了 OCR 有误的英文扫描件、无文字层的中文剪报、可播放的访谈与抄本，以及一段 15 秒音频的本地转录。粤语转录存在误字；测试中的中文竖排正文未能被 OCR 正确识别，需要读图核对。这些检查不代表所有语言都能可靠转录、整段录像已完整审阅，或受限原件可以访问。

详细说明见[验证记录](docs/VALIDATION.md)、[跨环境访问](references/portability.md)和[原始媒体处理](references/media.md)。本项目尚未确认 AAA 提供公开 API，也未建立适用于所有环境的无人值守馆藏访问方式。

## 仓库结构

| 路径 | 用途 |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Agent 入口与研究流程 |
| [`references/`](references/) | 检索行为、网站栏目、研究方法、词汇、访问与媒体处理说明 |
| [`scripts/access_probe.py`](scripts/access_probe.py) | 可选的单条公开链接访问检查，不是爬虫 |
| [`agents/openai.yaml`](agents/openai.yaml) | 技能显示信息 |
| [`tests/`](tests/) | 离线回归测试 |
| [`docs/VALIDATION.md`](docs/VALIDATION.md) | 测试范围、证据与尚存限制 |

## 开发

在仓库根目录运行：

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_project.py
python3 scripts/build_release.py
```

离线测试验证项目自身的行为，不能证明新环境能够访问 AAA。修改与验证要求见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可与关联说明

这是 [aaajiao](https://github.com/aaajiao) 发起的独立项目，与亚洲艺术文献库无隶属关系。[MIT 许可](LICENSE)仅适用于本项目原创代码与文档。链接到的 AAA 资料仍适用各自的权利声明和访问条件；技能不附带馆藏原件或转录模型。详见 [NOTICE.md](NOTICE.md)。
