---
title: "Frontmatter 规范（OKF 对齐）"
created: 2026-09-17
updated: 2026-09-24
tags: [系统, 指南, frontmatter]
type: "machine-index"
generated:
  by: "human:terry"
  at: "2026-09-17T00:00:00Z"
---

# Frontmatter 规范（OKF 对齐）

> 本仓库是人机共用的 AI 上下文仓库，frontmatter 不只是给人看的分类标签，也是给 Claude Code 等工具做机器解析的结构化字段。字段设计对齐 [Open Knowledge Format v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format)，本文档是字段字典，`vault-lint` 在运行时直接解析其中的类型表和枚举表。

## 核心字段

### 本 Vault 的基础字段

新建笔记统一包含 `title`、`type`、`created`、`updated`、`tags`。这是本 Vault 的写作约定；外部格式的最低要求不能替代本地约定。`created` 和 `updated` 使用 `YYYY-MM-DD`，修改内容时更新 `updated`。模板在创建时填入这五项，类型专属字段按需添加。

历史笔记随编辑补齐，不为本次规范调整批量改写全库。缺少 `created` 时，优先采用已有的创建记录或 `generated.at` 日期；无法确认时保留空值并注明待核实，不用本次修改日期冒充创建日期。

本文件负责字段含义和枚举，[[00-系统/📖 使用手册]] 负责工作流，模板和各目录看板使用同一套字段。修改字段时，同时检查默认模板、查询和一篇实际样本。

### `type`：笔记类别

英文短语命名笔记类型。判定优先级：**已有类型字段 > 目录路径**——卡片盒的三类卡片、Diátaxis 的 reference/explanation/howto 等已经有类型信息的，直接沿用；只有完全没有类型线索时才按所在目录推断。

新建笔记时，先查所在目录的 [[#槽位契约：目录 README 的 `slot` 字段|槽位契约]]，从 `slot.accepts` 里选值；没有契约的目录参考同目录已有笔记，不要自创新值。常见值包括（非穷举，实际以 `grep -rh '^type:' .` 为准）：

| 场景 | 常见 `type` 值 |
|------|----------------|
| 收件箱捕获（思考捕获、快速笔记） | `Inbox Capture` |
| 项目笔记（`02-项目/`） | `Project Note` |
| 领域概览（`03-领域/`） | `Area Note` |
| 读书笔记（整本书，用自己的话写） | `Reading Note` |
| 书摘（整本书的摘录与结构整理） | `Book Excerpt` |
| 文章/帖子笔记（含 AI agent 入库的外部文章） | `Article Note` |
| 链接收藏（只存链接和收藏理由，不做笔记） | `Bookmark` |
| 视频、播客等音视频笔记 | `Media Note` |
| 课程与教程笔记 | `Course Note` |
| 学术论文笔记 | `Paper Note` |
| 外部参考资料（`04-资源/`） | `Reference` |
| 工具使用笔记 | `Tool Note` |
| 卡片盒三类卡片 | `Concept Card` / `Method Card` / `Opinion Card` |
| MOC 索引卡片 | `MOC` |
| 目录 README | `README` |
| 日志（日/周/月/年） | `Daily Log` / `Weekly Log` / `Monthly Log` / `Annual Log` |
| 软件工程文档（Diátaxis） | `Explanation` / `How-To` / `Reference` |
| 财务笔记 | `Finance Note` |
| 对外发布成品 | `Output` |
| 可执行可校验的计算类笔记 | `Attested Computation`（见下） |
| 系统级索引文档（本文档、README-写作范式等） | `machine-index` |

### `status`：文档成熟度

收敛为三个英文值，**不再用中文或 emoji**：

- `draft`：内容仍在起草或修订
- `stable`：内容相对稳定、可供当前使用
- `deprecated`：已废弃、已过时、仅供历史参考

此字段只描述文档，不表示项目进度、阅读进度或领域健康度。稳定的方案可能服务于仍在执行的项目；阅读笔记仍在起草，也可能已经读完原书。

历史文档缺少 `status` 时保持原样，不据此认定内容经过核验，也不推断任何业务进度。新建普通笔记默认 `draft`，由实际修订情况决定何时调整。

### 业务状态：按场景独立记录

| 字段 | 用途 | 允许值 |
|------|------|--------|
| `project_status` | 项目总览的执行进度 | `planned` / `active` / `paused` / `completed` / `cancelled` |
| `reading_status` | 书籍或资料的阅读进度 | `to_read` / `reading` / `completed` / `paused` / `abandoned` |
| `health` | 领域当前健康度 | `healthy` / `attention` / `at_risk` |
| `adr_status` | 架构决策的采纳状态 | `proposed` / `accepted` / `deprecated` / `superseded` |
| `decision_status` | 一般决策的执行状态 | `pending` / `decided` / `executed` / `cancelled` |
| `publication_status` | 对外作品的发布进度 | `drafting` / `ready` / `published` |

只在相关笔记上填写；项目内的芯片资料、架构方案等不因所在目录而自动成为独立项目。业务状态不明时留空，看板显示为待确认或不列入明确状态分组。`health` 必须依据实际评估填写，不能从 `status: stable`、最近更新时间或默认模板推断为健康。

新字段优先于旧值。迁移旧中文/emoji `status` 时，先把可确认的业务含义保存在对应字段，再单独判断文档成熟度。例如 `🚧 进行中` → `project_status: active`；`正在阅读` → `reading_status: reading`；`🟡 需关注` → `health: attention`。已经变为 `draft/stable` 的记录不能反推出旧进度，也不自动补齐。旧值含义不明确时保留原记录，等待核实。

项目模板默认 `project_status: planned`，阅读模板默认 `reading_status: to_read`；开始执行或阅读后再修改。领域模板的 `health` 留空。项目关联领域统一用 `area`，截止日期用 `due_date`，实际完成日期用 `end_date`，不再混用 `category` 或把截止日期当完成日期。

### `generated`：产出来源

```yaml
generated:
  by: "human:<id>"         # 或 AI 来源，如 "Claude Code/<model>"
  at: "2026-09-17T00:00:00Z"
```

标注内容是人写的还是 AI 生成的，`at` 是创建时间（缺失 `created` 字段的历史文件用 git 首次提交时间兜底）。Spec 建议 AI 来源用 `<producer>/<version>` 格式（如 `Claude Code/claude-opus-5-5`）。

### `verified`：验证事件

```yaml
verified:
  - { by: "human:<id>", at: "2026-09-07T00:00:00Z" }
```

数组（或单个映射），记录"谁在什么时候确认过这份内容/这次计算是对的"。决定信任等级：没有 `verified` 键 → unverified；只有非 `human:` 身份验证过 → machine-confirmed；有 `human:<id>` 验证过 → human-reviewed。不是所有笔记都需要，主要用在 [[00-系统/Frontmatter 规范#Attested Computation：可执行、可校验的计算类笔记\|Attested Computation]] 这类需要"证明算对了"的场景。

### `sources`：结构化来源（阅读笔记/参考资料类）

```yaml
sources:
  - resource: "https://zhanghandong.github.io/pi-book/"   # 必需：URL 或 bundle 内相对路径
    id: primary                                            # 可选：稳定键，供正文内引用
    title: "《书名》"                                        # 可选
    author: "human:张汉东"                                  # 可选，actor 格式见下
```

`resource` 是 spec 要求的**必需**子字段，标明来源的实际地址或路径——单纯的 `{id, title, author}` 不满足 spec。`author` 建议按 actor 惯例写：AI 生成用 `<producer>/<version>`（如 `Claude Code/claude-opus-5-5`），人类用 `human:<id>`，自动化流程用 `process:<id>`。

## 槽位契约：目录 README 的 `slot` 字段

目录结构按"系统需要容纳什么内容"设计，空目录是预留的槽位，不因为暂时没有内容而删除。每个槽位收什么，写在它 README 的 frontmatter 里：

```yaml
slot:
  accepts: ["Article Note"]   # 本槽位收录的 type；["*"] 表示不限
  lifecycle: durable          # transient / active / durable / frozen
  max_age_days: 14            # 仅 transient 使用：内容停留超过该天数即提醒处理
  owner: distill              # 负责维护的 skill；没有则留空
```

**继承**：子目录没有自己的 `slot` 时，沿用最近上级 README 的契约。只在收录内容发生变化的边界写契约；按主题细分的子目录（如 `技术文档/操作系统`）不需要单独写。空槽位收录的类型与上级不同时必须写契约（它没有内容可以反推用途）；与上级相同则直接继承。和相邻槽位容易混淆时（如 `20-日志/周记` 与 `自省/每周复盘`），即使 type 相同也写 README 说明边界。`README` 类型在任何槽位都合法，不必列入 `accepts`。`00-系统/` 与 `90-附件/` 不是内容槽位，不做契约检查。

**`lifecycle` 含义**：

| 值 | 含义 | 检查方式 |
|----|------|----------|
| `transient` | 临时停留，应尽快流出 | 超过 `max_age_days` 提醒 |
| `active` | 有退出条件，完成后流出 | 项目 `project_status: completed` 后提醒归档 |
| `durable` | 长期存放 | 只检查 `type` 是否在 `accepts` 内 |
| `frozen` | 冻结，只读 | 不检查 |

**分工**：槽位契约只管"什么内容放在哪里"，某类笔记有哪些字段仍由本文件的 `type` 与业务状态规则负责。`accepts` 只能使用上方 `type` 表里的值；需要新类型时先在表中登记，再写入契约并同步模板。全库契约汇总见 [[00-系统/槽位总览]]。

**检查**：`/vault-lint`（脚本 `.claude/skills/vault-lint/vault_lint.py`）按契约和本文件检查全库。脚本在运行时直接解析本文件的 `type` 表、`status` 列表和业务状态表：新增类型或枚举值只需改这里；改动这几张表的格式（列顺序、反引号写法）时，要同步检查脚本能否解析。

## 其他按需字段

- **项目笔记**：`priority`、`start_date`、`due_date`——历史上写过 `"🔴 高"`、`P0`、`high`、`高` 等混用格式，新建时参考同目录最近笔记，暂无强制统一
- **阅读笔记**：`rating`（⭐⭐⭐⭐⭐）、`start_date`、`finish_date`
- **通用**：`title`（默认不需要引号，仅当标题含 `:` 等 YAML 特殊字符时才需要加引号——OKF spec §4.1 对 `title` 本身无格式要求，引号是 YAML 语法层面按需触发的，不是规范强制）、`created`/`updated`（YYYY-MM-DD）、`tags`（`[标签1, 标签2]`）
- **`visibility`**："🔒 私有"/"🌐 可公开"，不写默认私有，仅对确认可对外公开的内容显式标注，用于反向筛选 `30-输出/` 的候选素材
- **`stale_after`**（时效性内容，如财务规划、技术参考类笔记）：YYYY-MM-DD，预计失效/需复查的日期，配合 HOME 或 README 的过期提醒 Dataview 使用，仅对确实会过时的内容加

## Attested Computation：可执行、可校验的计算类笔记

当某个数值需要"每次都按同一套公式算，且要能查出这次算没算错"（而不是普通的一次性分析结论）时，用 `type: "Attested Computation"`：

```yaml
type: "Attested Computation"
runtime: "claude-agent-applescript-numbers"   # 必需，执行环境
parameters:
  - { name: numbers_file, type: string, required: true }
computation: ...        # 公式定义
executor:
  resource: "指向某个 skill，谁来跑这个计算"
attester:
  resource: "不依赖 LLM 的独立校验脚本路径"
```

`runtime` 是 spec 要求的必需字段，说明这个计算跑在什么执行环境里（spec 举例 bigquery/postgres/python 等，vault 场景通常是某个 skill 驱动的环境）；`parameters` 是入参列表，`{name, type, required}` 三元组。

示例：一篇每月按固定公式计算家庭财务指标的笔记，配一个 `attesters/finance-check.py` 校验脚本，由负责同步数据的 skill 每次运行后调用。

不要用于普通的一次性判断或分析——那些仍然是 `Finance Note`/`Reference` 等类型，不需要 `attester`。

## 参考

- [[00-系统/📖 使用手册]]
- [[00-系统/README-写作范式]]
- [[00-系统/🏠 HOME]]
- [OKF v0.2 规范](https://github.com/GoogleCloudPlatform/open-knowledge-format)
