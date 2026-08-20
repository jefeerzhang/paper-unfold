# 示例：统一文献展开（节选）

> 以下输出由 `paper-unfold` 在真实论文上生成，**导读（含知识族谱图）与研究空白写在同一份文件**。仅保留结构框架和关键内容。学术检索走 SciVerse（`list_catalog` / `search_papers` / `semantic_search` / `read_content` / `list_paper_relations`）。

## 📋 文献 DNA 扫描

- **标题**：Attention Is All You Need
- **作者**：Vaswani et al.
- **年份**：2017
- **研究类型**：理论 + 实证
- **核心三问**：
  1. 研究想解决什么问题？序列模型依赖循环/卷积结构，训练慢、并行度低。
  2. 用了什么方法？完全抛弃 RNN/CNN，只用自注意力机制构建 Transformer。
  3. 发现了什么？在机器翻译任务上达到 SOTA，且训练速度显著更快。

## 🎓 四层渐进理解

### 🟢 Layer 1：直觉层

想象你在听一场多人会议。RNN 像你逐字记录，必须等上一个人说完才能写下一句；Transformer 像你同时扫视所有人的名牌和表情，一眼判断谁和谁相关。

### 🔵 Layer 2：概念层

- **自注意力（Self-Attention）**：让句子里的每个词直接和其他词计算相关性，而不是按顺序传递信息。
- **多头注意力（Multi-Head Attention）**：并行做多组注意力计算，捕捉不同类型的依赖关系。

### 🟡 Layer 3：技术层

1. 输入词向量 + 位置编码
2. 经过 N 个 Encoder 层（每层 = 多头自注意力 + 前馈网络 + 残差连接 + LayerNorm）
3. Decoder 同样堆叠，但增加 Encoder-Decoder Attention
4. 输出 Softmax 预测下一个词

关键公式：

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

### 🔴 Layer 4：批判层

- 位置编码是手工设计的，是否能学得更好？
- 长序列上注意力复杂度是 $O(n^2)$，后续工作（Linformer、Longformer、FlashAttention）都在解决这个问题。
- 论文未充分讨论小数据集上的表现。

## 🗺️ 知识族谱图

```text
RNN/LSTM
   ↓
Seq2Seq + Attention (Bahdanau 2014)
   ↓
Transformer (本文, 2017) ──→ BERT (2018) ──→ GPT 系列
   ↓
Vision Transformer (2020)
```

## 📚 推荐阅读

- **Attention Is All You Need** 是开创性贡献，后续推荐阅读以下文献（示例 `doc_id`，实际运行时以 SciVerse 实时检索结果为准）：

- **[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — `doc_id: paper:10.48550/arXiv.1810.04805`
  理由：与本文同方法族（Transformer encoder），是双向预训练的开创性工作，用于横向比较架构变体。
- **[FlashAttention: Fast and Memory-Efficient Exact Attention](https://arxiv.org/abs/2205.14135)** — `doc_id: paper:10.48550/arXiv.2205.14135`
  理由：解决本文 Layer 4 提到的 $O(n^2)$ 复杂度问题，体现后续算法演进。
- **[Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752)** — `doc_id: paper:10.48550/arXiv.2312.00752`
  理由：挑战 Transformer 范式的代表性后续工作，展示对该领域的不同替代路径。
- **[A Survey on Transformers](https://arxiv.org/abs/2106.01254)** — `doc_id: paper:10.48550/arXiv.2106.01254`
  理由：综述类，提供本文在更大学术谱系中的位置。

> 检索方法：`mcp__sciverse__semantic_search(query="Transformer attention mechanism")` 取 top 10，按相关性 + 引用数过滤。

---

## 📝 自测清单

- [ ] 能向朋友解释为什么 Transformer 比 RNN 快
- [ ] 能写出 Attention 公式并解释每个符号
- [ ] 能说出 Transformer 在长序列上的两个局限

## 🔍 研究空白识别

> ⚠️ 以下分析基于单篇论文的信号提取 + 有限外部检索（SciVerse/WebSearch），不保证穷尽所有空白。检索覆盖范围受限于数据库收录和检索时间窗口。建议结合自身领域知识做最终判断。

分类依据：Miles (2017) 七分法（见 `研究空白.md`）。族谱图中的「长序列 $O(n^2)$ / 位置编码」对应方法空白。

### ① 证据空白（Evidence Gap）
- **判断**：⚠️ 不确定
- **证据**：WMT 2014 英德/英法上达到当时 SOTA，但是单一翻译基准；小数据设定作者讨论不足。
- **置信度**：中

### ② 知识空白（Knowledge Gap）
- **判断**：❌ 不存在（就「纯注意力能否替代循环」这一问题，本文本身是填补而非留下）
- **证据**：标题命题已被后续大量工作承接（BERT、GPT、ViT）。
- **置信度**：高

### ③ 实践-知识冲突空白
- **判断**：⚠️ 不确定
- **证据**：工业界迅速采用 Transformer，但推理成本与论文强调的训练并行优势并不等同。
- **置信度**：中

### ④ 方法空白（Methodological Gap）
- **判断**：✅ 存在
- **证据**：自注意力 $O(n^2)$ 与手工位置编码是文内已知局限，催生 Linformer / Longformer / FlashAttention / 相对位置编码等后续。
- **置信度**：高

### ⑤–⑦
（完整报告须七项全扫；此处节选。）

## 📊 空白地图

| # | 空白类型 | 是否存在 | 交叉验证 |
|---|----------|----------|----------|
| ④ | 方法空白 | ✅ | 部分已填补（FlashAttention 等，SciVerse 须给 `doc_id`） |

## 🎯 高价值空白建议

（完整报告 ≤3 个方向。本节选略。）

---

**完整报告保存到 `./文献导读/<论文简称>_文献展开.md`（一份文件，禁止再写 `./研究空白/`）**
