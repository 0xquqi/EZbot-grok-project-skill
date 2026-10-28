# 方法来源与验证边界

Skill 作者：[@0xquqi](https://x.com/0xquqi)。v0.1以用户确认的项目发现、按需研究和聊天交付需求重新组织。第三方截图、自动交易提示词和其中的具体规则不作为本版设计依据。

## 自有研究基础

本轮核对 [EZbot-project-research-skill](https://github.com/0xquqi/EZbot-project-research-skill) 的当前本地独立模块：SKILL.md、automatic-research.md、web-research.md、contract-research.md、participation.md、question-cards.json（schemaVersion 3、14类方法）。本地仓库HEAD为00e13c8dd1f2f2e79d6fa2a9b5edb28b925617a2；所读工作区文件的哈希另记录在交付校验中，HEAD不代表所有工作区文件均已提交。

迁移的是网页取证、目标/合约角色识别、按机制追参与路径、必要只读核验和证据分层的方法。不复制未确认来源的历史报告/案例正文，不携带旧项目的价格、地址或安全结论；不宣称整个旧仓库从未接触过其他来源。本次未读取或迁移来源边界禁止的研究Skill及其支持资料。

本包将方法写成宿主可执行的研究指令，未捆绑上游Python脚本或钱包实现。Grok Bot使用实际可用工具完成同类工作；单个工具缺失时按能力路由补查，所有适用路径仍不足时说明缺口，不伪造自动核验成功。

## Grok Bot适配

本版进一步逐项核对产品公开X、浏览器/终端、`/workspace`文件与Bot记忆，以及开发者X Search、Web Search、Code Execution和Citations的区别。具体依据与执行映射见 [Grok能力与工具选择](grok-runtime.md)。检索、动态页与链上读取的顺序是本Skill根据任务设计的策略，不是官方保证的完整采集或审计服务。

[引用文档](https://docs.x.ai/developers/tools/citations)用于区分来源列表和具体结论的支持关系，不把API引用配置当成Bot已启用选项。

2026-10-28读取官方 [Skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations) 与 [Files and results](https://docs.x.ai/grok-bot/files-and-results)。前者区分研究方法与运行调度，后者说明附件与可检查交付。包内完整提示词可作为文本附件交给Bot；目录包供能读取该结构的宿主使用，不宣称上传ZIP即自动安装。是否保存为私有Skill、是否启用routine，以宿主实际结果为准。

## 检查范围

本地检查针对文件结构、配置、引用、打包一致性和情境规则审阅。交付校验记录实际结果。没有在用户的Grok Bot环境完成搜索召回、原帖完整性、复杂合约解释、跨轮状态或routine测试，不将本地校验或上游测试视为本包线上实测。指令与配置本身不是运行服务、持久化实现或计费硬限。


## 用户试运行反馈

v0.1根据用户提供的Grok Bot实际聊天输出与界面截图，完善启动设置说明、编号与分层项目排版、首轮/后续独立结束消息，并加深机制与证据研究。反馈能证明用户看到的输出形态，不能独立证明其中项目事实、链上读数或状态写入正确。本包不携带这些样本项目地址和价格，也不把旧输出当研究事实库。新版交付尚未在Grok Bot中复跑。
