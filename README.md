# EZbot Grok Scout v0.1

在 Grok Bot 中发现币安 Agent ID / Agentic Wallet 生态的具体项目，并研究玩法、资格、成本、产物、关键权限和退出条件。作者：[@0xquqi](https://x.com/0xquqi)。

## 安全与免责声明（使用前请阅读）

> 本内容为公开信息整理与有限研究，仅供参考，不构成投资建议或安全认证。请自主完成项目实际投研；作者不对项目安全、收益或履约提供保障。

项目被收录、源码验证通过或完成有限风险检查，都不代表作者推荐参与或为项目背书。请自主核实项目和参与条件；本 Skill 不连接钱包，不签名、授权、模拟或执行交易。

这段提示同时保留在首次启动说明与项目结果中；多项目同一回复末尾展示一次，独立卡片或导出结果也保留。MIT 开源许可不改变上述研究边界。

## 开始使用

下载 [Skill 安装包：ezbot-grok-scout-skill-v0.1.zip](ezbot-grok-scout-skill-v0.1.zip)。解压后得到 `ezbot-grok-scout/`，根目录是 `SKILL.md`，并含完整 `references/`、`assets/` 和 `LICENSE`；可供支持该目录结构的宿主读取。Grok Bot 是否能直接解析 ZIP 以实际工具为准，不能把上传成功当作安装成功。

在 Grok Bot 中直接使用时，可下载 [GrokBot完整提示词.txt](GrokBot完整提示词.txt)，作为可读取附件交给 Grok Bot，再发送：

> 请按附件中的 EZbot v0.1 工作流，搜索最近1小时的币安 Agent ID / Agentic Wallet 生态具体项目。自动查清理解玩法所需的规则、成本、产物和关键风险，直接在聊天里按编号介绍；资料不足说明缺口。本次只运行一轮。

完整提示词已展开全部必要引用。也可下载 [完整 ZIP 包](EZbot-Grok-Scout-v0.1.zip)，查看 [使用说明](开始使用.txt)。更新既有对话时，把新版附件与 [纠正指令](给现有Grok对话的纠正指令.txt) 一起发送。上传附件不代表已安装或持久保存；让 Bot 核对实际结果。同为 v0.1 的修订可用提示词顶部的内容标识和 [交付校验](交付校验.json) 区分。

## 默认行为

- 最近一小时、单次搜索、中文聊天交付；不自动创建定时任务。
- X 搜索找线索，原帖和官网核规则，动态页用浏览器，公开链上读取核关键状态。
- 具体预告也可编号展示；旧项目只报告重要变化，换合约等变化沿原项目追踪。
- 项目按 01、02……编号，使用普通文字和【栏目名】，保留来源链接及独立合约行。
- 首次成功试运行额外结束语为“首轮试运行结束”，后续为“本轮运行结束”；失败明确“本轮未完成”。静默定时任务无变化不提醒。

首次启动会说明可调整的频率、回看范围、时区、生态内搜索重点、研究关注点、每轮数量、通知方式与回复详略。调度必须由用户明确要求，并由 Bot 确认实际保存。

## 研究与能力边界

区分项目方声明、部署代码规则、当前链上状态与推断。研究追到必要步骤、追加成本和最终产物；代币激励不直接等于可兑现收益。缺资料时保留具体缺口，不以无 owner、源码验证或局部池余额作安全背书。

这是给 Grok Bot 的工作流指令，不是独立运行程序。搜索、浏览器、终端、持久文件和调度均依赖当前 Bot 环境；API 文档里的工具名不保证暴露给 Bot。方法与调度的区别见 [Grok 官方文档](https://docs.x.ai/grok-bot/skills-routines-and-automations)，本包路由见 [能力适配说明](skills/ezbot-grok-scout/references/grok-runtime.md)。

只读公开资料；不连接钱包、不签名、不授权、不模拟或执行交易，不运行项目提供的脚本。状态仅保存于本工作流目录，默认不导出研究报告或使用外部通知。

## 目录与校验

- `skills/ezbot-grok-scout/`：Skill 入口、参考流程与默认文案。
- `tools/build_release.py`：生成完整提示词、哈希清单、独立 Skill 包和完整资料包，并检查一致性。
- `evaluation/`：来源记录、人工情境审阅和审计说明。

构建需 Python 3.10+ 与 Ruby（使用标准库 Psych 解析 YAML）；Bot 使用文本附件时不需要本地构建工具。

```sh
python3 tools/build_release.py
python3 tools/build_release.py --check
python3 -m unittest discover -s tests -v
```

版本保持 v0.1。历史包、用户截图、聊天记录、运行状态及凭证不属于仓库交付。测试范围见 [审计记录](evaluation/audit-v0.1.md)：结构/打包和人工规则审阅通过不代表 Grok 真实召回、推理、跨轮去重已通过线上测试。

方法适配自同作者的 [EZbot-project-research-skill](https://github.com/0xquqi/EZbot-project-research-skill)，来源与具体读取快照见 [来源说明](skills/ezbot-grok-scout/references/sources.md)。沿用 MIT 许可及作者版权声明，见 [LICENSE](LICENSE)。
