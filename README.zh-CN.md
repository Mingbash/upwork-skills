# Upwork Skills · 自由职业接单工具包

**先挑值得投的职位，再写一份说得清你能做什么的提案。**

贴一条 Upwork 职位，再说说你做过哪项类似的工作。Agent 可以帮你判断这单是否适合，也可以照着客户要交付的东西写一版投标草稿。另有两个 skill，分别用来从多条职位里找重复出现的需求、整理自由职业主页。

[English](README.md) · [看使用示例](examples/README.zh-CN.md) · [快速开始](docs/QUICKSTART.zh-CN.md)

## 今天要做哪件事

| 你现在想做的事 | 选这个 skill | 给它什么 |
|---|---|---|
| 写提案或回复客户 | [Proposal](skills/upwork-proposal/SKILL.md) | 职位和你在类似项目中负责的工作 |
| 判断一单值不值得投 | [Bid Screen](skills/upwork-bid-screen/SKILL.md) | 职位、你的经历，以及时间或报价限制 |
| 看客户反复在买什么 | [Needs Analysis](skills/upwork-needs-analysis/SKILL.md) | 一批职位文本或文件 |
| 写一份主页或改现有版本 | [Profile](skills/upwork-profile/SKILL.md) | 现有主页，或几条做过的项目经历 |

四个 skill 可以单独用。第一次试，在对话里贴材料就行，不用连接 Upwork 账号。

## 用手头的一条职位写份提案

在 Codex 安装 Proposal。

```sh
npx skills add Mingbash/upwork-skills --skill upwork-proposal -a codex
```

贴上职位，写两句自己做过的类似项目。说清你负责哪一段。

> 用 `$upwork-proposal` 帮我看这条职位。类似的项目里，我负责做报表和培训客户团队，数据清洗是他们自己做的。请起草提案，并告诉我报价前应该先问什么。

你会拿到一份待审阅的提案、职位里附带问题的回答，以及写清前提的报价建议。客户还没给访问权限，可以从权限到手那天起算工期。需要录视频时，再请它补一个提纲。

把命令里的 `upwork-proposal` 换成别的 skill 名就能单装，也可用 `--skill '*'` 一次装四个。手动安装时，从 [Releases](https://github.com/Mingbash/upwork-skills/releases) 下载单项或合集，复制完整的 skill 目录。[查看安装步骤。](docs/QUICKSTART.zh-CN.md)

## 筛完职位，你还是自己决定投不投

Bid Screen 会把经历对得上的地方、交付成本和需要核实的条件写出来。它先看你给的职位文本。如果你还想核对账号当前状态，需要有获准用于该场景的接口。导出文件和缓存只能说明记录当时的情况。

提案和回复都留作草稿。提交申请、发消息、购买 Connects（投标点数）或修改主页，由你在 Upwork 上操作。[Upwork 自动化规则](https://support.upwork.com/hc/en-us/articles/43342677368467-Use-bots-and-other-automation-properly)说明了平台允许的访问方式。

## 我为什么把它拆成四个

自己筛职位、写提案时，我发现网上很多建议在讲开头怎么写。实际卡住我的更早一步：客户究竟要买什么，我做过的事里哪一件能让对方放心？2026 年 9 月 23 日的原始任务里有三句话，决定了这套工具怎么做。

> “兼听则明，梳理里面的共识和专业建议，多方验证，将置信度高的原则和方法沉淀成skill”

我对照了已有的 skill、从业者经验和 Upwork 官方说明。最后保留下来的一条是：提案里每一句关于你能做什么的话，都尽量用一件你亲手做过、客户也在意的事来支撑。

> “Skills应能通用，skill本身不能包含任何关于我个人背景、业务背景的信息”

做法留在 skill 里。换个人用，带上自己的项目、报价和时间就行。

> “记录买方真正采购的业务流程、痛点、现有系统和验收标准，不只记关键词”

于是有了 Needs Analysis。你会跳过的职位也能告诉你客户在买什么。做研究时把它留下，再去看同样的麻烦有没有出现在其他职位里。

[查看原始指令、设计取舍和参考资料。](docs/ORIGIN.md)

## 经常用的时候再加设置

做一次就把结果留在对话里。经常筛职位时，可以指定工作区，把案例、偏好和筛选记录存下来。分析跟随你的语言。写给客户的内容优先用对方明确要求的语言，其次用职位里的语言。[查看可改的设置。](skills/upwork-proposal/references/options.md)

[实测范围](docs/VALIDATION.md) · [参与贡献](CONTRIBUTING.md) · [MIT 许可](LICENSE)
