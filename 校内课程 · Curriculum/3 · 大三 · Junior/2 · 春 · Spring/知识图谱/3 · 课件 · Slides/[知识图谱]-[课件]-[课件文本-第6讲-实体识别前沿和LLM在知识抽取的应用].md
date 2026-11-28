# 知识图谱 · 课件 · 课件文本 · 2026春 · 第6讲-实体识别前沿和LLM在知识抽取的应用

第三章 实体识别前沿和大模型在
     知识抽取的应用

  牛广林 <beihangngl@buaa.edu.cn>

  北京航空航天大学，人工智能学院
                                     目录
    • 定义：What is NER
    • NER常见任务
       – CoNLL 2003
       – CoNLL++
       – WNUT 2017
       – Ontonotes v5
       – FEW-NERD
    • NER衍生方向
       – Few/Zero Shot NER
       – Continual NER
       – Nested NER
       – Cross Domain/Domain specific NER
       – Multi-Modal NER
2
What is NER ?
 命名实体识别(Named Entity Recognition, NER)是标记出文本中预定义类型的 实
 体的任务，通常建模为序列标注任务。NER是NLP和知识图谱关键的上游任
 务，在医学、新闻和社交领域得到了广泛的应用。
 命名实体：一个恰当的名词，作为某物或某人的名称
NER数据集和现成工具：
基于深度学习的NER系统通常包含以下三个组件：

1. 分布式输入表征：分布式表征
     将单词用低维实值稠密向量表
     示，每个维度表示一个隐含的
     特征。分布式表征是从文本中
     自动学到的，它捕捉了单词的
     没有显式地呈现在NER输入中
     的语义和句法属性。
2. 上下文编码器：采用CNN,RNN
     等网络捕捉输入的上下文依赖
3. 标注解码器：预测输入序列中
     每个token的标签
NER常见任务
CoNLL 2003                   数据来源：<http://nlpprogress.com/english/named_entity_recognition.html>
CoNLL 2003 NER任务由来自Reuters RCV1语料库的新闻专线文本组成，并用
四种不同的实体类型(PER，LOC，ORG，MISC)标记。 测试集中利用基于跨
度的F1值来评估模型。
Model                         F1     Paper / Source                Code

                                     Automated Concatenation of

ACE + document-context
                             94.6    Embeddings for Structured     Official
(Wang et al., 2021)
                                     Prediction

                                     LUKE: Deep Contextualized
LUKE (Yamada et al., 2020)   94.3    Entity Representations with   Official
                                     Entity-aware Self-attention

                                     Improving Named Entity
                                     Recognition by External
CL-KL (Wang et al., 2021)    93.85                                 Official
                                     Context Retrieving and
                                     Cooperative Learning
ACE + document-context (Wang et al., 2021)
预训练上下文嵌入是结构化预测任务的强有力的词表示。最近研究表明，通过连接不
同类型的嵌入，可以获得更好的单词表示。然而，选择什么样的嵌入来形成最佳的串
接表示通常取决于任务和候选嵌入的集合，且嵌入类型的不断增加使问题变得更加困
难。本文基于神经结构搜索的最新进展，提出了自动化嵌入连接(ACE)，实现为结构
化预测任务寻找更好的嵌入连接的过程的自动化。具体来说，控制器根据当前对个体
嵌入类型在任务中的有效性的信念，交替地对一系列嵌入进行采样，并基于奖励更新
该信念。本文采用强化学习策略对控制器参数进行优化，并根据任务模型的精度计算
奖励，该任务模型以采样的串接为输入，在任务数据集上进行训练。在6个任务和21
个数据集上实现了SOTA的性能
ACE + document-context (Wang et al., 2021)

  上图解释了ACE的基本原理。在ACE中，一个任务模型和一个控制器相互
  重复地交互。任务模型预测任务输出，控制器搜索更好的嵌入连接作为任
  务模型的词表示，以达到更高的准确性。给定控制器生成的嵌入连接，任
  务模型通过任务数据进行训练，并返回奖励给控制器。控制器收到奖励来
  更新它的参数，并为任务模型采样一个新的嵌入连接。
LUKE(Yamada et al., 2020)
       论文提出了基于双向Transformer（Vaswani et al., 2017）的单词和实体的
   新的预训练上下文。
       模型将给定文本中的单词和实体视为独立的标记，并输出它们的上下文
   表示。在基于BERT (Devlin et al., 2018)的 掩 码 语言模型(Mask Language
   Models) 的基础上使用新的预训练任务对模型进行了训练。
       模型在五个著名的数据集上获得了SOTA的结果：
       Open Entity(Entity Type)， TACRED(Relation Classification)，
       CoNLL-2003(Named Entity Recognition)， ReCoRD(cloze-style question
   answering)， SQuAD 1.1(extractive question answering)。
LUKE(Yamada et al., 2020)

   LUKE的体系结构：使用输入语句“Beyoncélives in Los Angeles. ” LUKE为文本中
   的每个word和entity输出其上下文表示。训练模型以预测随机Mask的单词（e.g., live and
   Angeles）和实体(e.g., Los Angeles)。 下游任务利用LUKE的输出表示，使用线性分类器
   来解决task-specific问题。
CL-KL (Wang et al., 2021)
NER的最新进展表明，文档级上下文可以显著提高模型性能。然而，在许多应用程序场景中，这样的上
下文是不可用的。本文提出通过搜索引擎检索并选择一组语义相关的文本，以原句作为查询，从而找到
句子的外部上下文。研究发现，与仅基于句子的原始输入视图相比，基于检索输入视图(通过连接句子
及其外部上下文构造)计算的上下文表示可以获得显著的性能改善。此外可以通过合作学习(Cooperative
Learning)来改善两个输入视图的模型性能，这是一种鼓励两个输入视图产生类似上下文表示或输出标
签分布的训练方法。实验表明，该方法在跨越5个领域的8个NER数据集上达到SOTA性能
CL-KL (Wang et al., 2021)

本文的方法框架如上图。给定一个有n个token的句子x，输入句子作为查询输入到搜索引擎中。搜索引擎返回 top
𝑘个相关的文本。本文的框架将这些文本输入到一个重排名模型，然后将排名后的top 𝑙个文本作为外部上下文。
NER模型以原始输入视图或输入句子与外部文本的串接作为输入，然后基于CRF层输出每个位置的预测标签。并
采用合作学习训练一个在两种输入上都很擅长的统一模型来进一步提升模型性能。由于合作学习地约束，模型对
于两种输入视图还可以得到一致的内部表示和输出分布。
                                  数据来源：<http://nlpprogress.com/english/named_entity_recognition.html>
CoNLL ++
CoNLL 2003 NER任务的更清洁纯净的版本，其中由于标签错误而纠正了测试集中
约5％的实例，训练集保持不变。测试集中利用基于跨度的F1值来评估模型。

Model                                 F1     Paper / Source                    Code

                                             Improving Named Entity
                                             Recognition by External Context
CL-KL (Wang et al., 2021)            94.81                                     Official
                                             Retrieving and Cooperative
                                             Learning

                                             CrossWeigh: Training Named
CrossWeigh + Flair (Wang et al.,
                                     94.28   Entity Tagger from Imperfect      Official
2019)
                                             Annotations

Flair embeddings (Akbik et al.,              Contextual String Embeddings
                                     93.89                                     Flair framework
2018)                                        for Sequence Labeling
Flair embeddings (Akbik et al., 2018)

    当前SOTA的方法最多可concatenate三种不同的嵌入类型：
    1. Classical word embeddings (Mikolov et al., 2013; Pennington et al., 2014)，在
       非常大的语料库上预训练，并显示出潜在的句法和语义相似性。

    2. Character-level features (Ma and Hovy, 2016; Lample et al., 2016)， 尚未经过
       预先训练，而是针对任务数据进行了训练，得到特定于任务的字特征。

    3. Contextualized word embeddings (Peters et al., 2017; Peters et al., 2018)，在
       上下文中提取单词语义，以解决单词的多义性和上下文相关性。
Flair embeddings (Akbik et al., 2018)

    论文所提方法的整体结构：将句子作为字符序列输入到预训练的双向字符语言模型
    中。在LM中，该文为每个单词检索上下文嵌入，并将其传递到BiLSTM-CRF序列标
    记器中，从而在下游任务上获得可靠的 SOTA结果（图示NER任务）。
Flair embeddings (Akbik et al., 2018)

   在句子上下文中提取单词“Washington”的上下文字符串嵌入(Contextual String
   Embedding)：从正向语言模型（以红色显示）中，提取单词中最后一个字符之前的输出隐
   藏状态。因此，该隐藏状态包含从句子开头一直传播到这一点的信息。从后向语言模型（
   以蓝色显示）中，提取单词中第一个字符之后的输出隐藏状态。将两个输出隐藏状态连接
   起来以形成嵌入(Flair Embeddings)。
Ontonotes 5.0 数据来源：<http://nlpprogress.com/english/named_entity_recognition.html>
Ontonotes v5语料库是一个注释丰富的语料库，具有多层注释，包括命名实体、
共引用、词性、词义、命题和句法解析树。这些注释包含大量的标记、广泛的
领域横截面和3种语言(英语、阿拉伯语和汉语)。NER数据集包括18个标记，由
11种类型(PERSON、ORGANIZATION等)和7个值(DATE、PERCENT等)组成，
并包含200万个token。
 Model                              F1     Paper / Source                 Code

                                           Improving Named Entity
                                           Recognition with Attentive
 BERT+KVMN (Nie et al., 2020)      90.32                                  Official
                                           Ensemble of Syntactic
                                           Information

 Flair embeddings (Akbik et al.,           Contextual String Embeddings
                                   89.71                                  Official
 2018)                                     for Sequence Labeling

                                           Semi-Supervised Sequence
 CVT + Multi-Task (Clark et al.,
                                   88.81   Modeling with Cross-View       Official
 2018)
                                           Training
CVT + Multi-Task (Clark et al., 2018)
如word2vec和ELMo等无监督表示学习算法提高了许多有监督NLP模型的准确性，主要是因为它们可以利用大量的无标 记
文本。然而，监督模型只在主要训练阶段从任务特定的标记数据中学习。本文因此提出交叉视图训练(CVT)，一种半监
督学习算法，使用带标签和未带标签的混合数据改进Bi-LSTM句子编码器的表示。对于有标记的例子，使用标准的监督
学习。在未标记的例子中，CVT则教看到输入的受限视图(例如，只看到一个句子的一部分)的辅助预测模块去匹配看到整
个输入的完整模型的预测。由于辅助模块和完整模型共享中间表示，这反过来改进了完整模型。此外还表明，当CVT与
多任务学习相结合时，它是特别有效的。在五个序列标记、机器翻译和依赖解析任务上评估了CVT，获得了SOTA结果
CVT + Multi-Task (Clark et al., 2018)
上图是CVT概览。该模型是用标准的监督学习
训练标记的例子。在未标记的例子中，训练具
有不同输入视图的辅助预测模块，使其与主预
测模块一致。这个例子展示了CVT在命名实体
识别中的应用。从标记的例子中，模型可以知
道Washington通常指的是一个位置。在未标记
的数据上，训练辅助预测模块在不看到输入的
情况下达到相同的预测，改善了模型产生的上
下文表示，例如，学习travel to通常会跟着一个
地点。
CVT + Multi-Task (Clark et al., 2018)

上图是序列标注模型的辅助预测模块。每一个都能看到输入的受限视图。例如，“forward”
预测模块在预测该token的标签时，不会看到当前令牌右侧的任何上下文。为了简单起见，
只显示了一个单层的Bi-LSTM编码器，并且只显示了单个时间步长的模型预测
NER衍生方向
Few/Zero-Shot NER
 少样本学习(FSL)在机器学习领域具有重要意义和挑战性。成功地从很少的样本中学
 习和归纳的能力是区分人工智能和人类智能的一个明显的界限，因为人类可以很容
 易地从一个或几个例子中建立他们对新颖性的认知，而机器学习算 法通常需要数百
 或数千个监督样本来保证泛化能力。从高层次上看，研究少样本学习的理论和现实
 意义主要来自三个方面。首先，FSL方法不依赖于大规模的训练样本，从而避免了在
 某些特定应用中数据准备的高昂成本。第二，FSL可以缩小人类智能和人工智能之间
 的差距，是发展通用人工智能的必要之旅。第三，FSL可以实现一个新兴任务的低成
 本和快速的模型部署，而这个任务只有几个暂时可用的样本，这有利于阐明任务早
 期的潜在规律。
Few-NERD                      数据来源：<http://nlpprogress.com/english/named_entity_recognition.html>
Few-NERD 是一个大规模、细粒度、手工标注的命名实体识别英文数据集，包含8
种粗粒度类型、66种细粒度类型、188,200个句子、491,711个实体和4,601,223个标
记。构建了三个基准测试任务:
• Few-NERD (SUP) ：标准的NER任务;
• Few-NERD (INTRA)是一个跨不同粗粒度类型的小样本NER任务;
• Few-NERD(INTER)是一个粗粒度类型的小样本NER任务

Model                              F1     Paper / Source               Code

                                          Few-NERD: A Few-shot Named
BERT-Tagger (Ding et al., 2021)   68.88                                Official
                                          Entity Recognition Dataset
ACL 2021: Leveraging Type Descriptions for Zero-
shot Named Entity Recognition and Classification

在命名实体识别和分类(NERC)的现实世界应用中，一个常见的问题是在训练期间缺乏目标实
体类的有标注 数据。零样本学习方法通过学习可以将训练数据中观察到的类的信息转移到未
见过的类的模型来解决这个 问题。本文介绍了第一种零样本NERC的方法，引入了一种全新
的体系结构，该体系结构利用了许多自然 出现的实体类的文本描述对应的事实。由于在训练
和测试中考虑了不同的实体类，因此本文的体系结构解 决了零样本NERC特定的挑战，即not-
an-entity类没有很好地定义。本文采用了两个数据集OntoNotes和 MedMentions进行评估，通过
在最罕见的实体类型上测试模型，模拟真实世界零样本学习的难度。该论文提出的方法优于
基于机器阅读理解和零样本文本分类的基线方法。
零样本NER图解

在测试期间，输入是一个句子和一组目标实体类型。每一个类型都有一个描述，学习目标是识别和分类这
些目标类型的实体。描述包含任务的关键信息。如图，给定输入“Shantou Harbour, a natural river seaport,
opens to the South China Sea.” 和使用一段描述“Names of human-made structures: infrastructure (streets,
bridges), [...]”的类别Facility ，就不需要在训练中看到有标注样本就可以建立Facility与Shantou Harbour之间
的连接。虽然使用描述可以让模型预测在训练中没见过的实体类，NERC提出了对负类(非实体token)建模
的额外挑战，因为它的定义包括训练和测试中的不同实体类和token。在训练过程中观察到的非实体单词可
能属于测试类之一，比如图中在训练期间的Huaqiao Park和在测试期间的Shantou Harbour 都是Facility类型
的实体，然而， Huaqiao Park在前者中被标记为非实体
 EMNLP 2021:Learning from Language Description: Low-
shot Named Entity Recognition via Decomposed Framework

 本工作研究了低资源场景下的命名实体识别(NER)问题，重点是少样本和零样本设置。在大规模预训练语
 言模型的基础上，本文提出了一种新的NER框架，即SpanNER，它可以从自然语言监督中学习，并能够
 在不使用域内标记数据的情况下识别从未见过的实体类。本文在5个基准数据集上进行了大量的实验，并
 在少样本学习、领域迁移和零样本学习设置方面对所提出的方法进行了评估。实验结果表明，该方法在少
 样本学习、领域迁移和零样本学习设置下，比最佳基线平均提高了10%、23%和26%
背景和动机
• 少样本NER关注的是仅用少量甚至不用新领域内的有标注样本来鉴定出新领域
  的定制实体。少样本NER的成功在于模型能够迁移学过的知识来识别新的实体
  类别。传统NER模型通常将每个类别视为一个独热向量来训练，因此训练出的
  模型不能捕捉标签的语义含义，实际上这么训练出的模型可能与已知类别高度
  相关联，很难迁移学过的知识到新的实体类别上

• 目前的工作采用基于原型的方法，用基于标注样本的原型表示每个类，使用最
  近邻方法实现NER。然而每个NER任务中的实体类别可能包括多个细粒度实体
  类别，并含有丰富的语义意义。相应地，属于同一实体类的token或实体不一定
  彼此接近，这让用基于少量样本得到的原型来代表类别具有挑战性，而且基于
  原型的方法最终可能会学到有噪声的原型表示，并不能获得令人满意的性能。
  此外，基于原型的方法不可避免地依赖于有标注的样本，从而使其无法扩展到
  零样本学习设置
方法

本文提出了一种简单而有效的方法，既能解决少样本又能解决零样本的NER。该方法直接从实体类的自然
语言描述中学习，而不是单纯地从几个带标签的例子中推导标签的表示。这样的选择为得到实体类的语义
提供了一种灵活而精确的方法，并使零样本学习成为可能。受机器阅读理解框架的启发，提出将NER任务
分解为两个过程：跨度检测和实体类推理，这两个过程可以联合训练。MRC框架通常需要大量的数据进行
培训，这在资源匮乏的场景下是不可用的。为了应对这些挑战，提出了一个类别无关的跨度检测模块，该
模块配备了token采样机制，以缓解不平衡的类别问题，并可以用有限的标记数据进行训练。此外，为了处
理在一个实体类中包含多个细粒度类的挑战，开发了一个实体类注意力模块，以关注给定实体类描述中与
提取的跨度相对应的最相关的信息。上图显示了所提出框架。跨度检测阶段的目标是识别文本的跨度，实
体类推理负责根据预定义实体类的自然语言描述对提取的跨度进行分类。
结果

不同模型在不同数据集上的F1对比       模型用5-shot监督以实现领域迁移的F1对比

模型在全监督和零样本设置下的F1对比   消融实验：是否引入基于类别描述的注意力的对比
Continual NER
 持续学习(Continual Learning)目标：模型可以不断学习新任务，实现通用智能
 让模型能够胜任多个任务的方法：
 •   多任务学习/联合训练：在新旧任务的数据的并集上重新训练一个模型
 •   微调：用一个相对很小的学习率在新任务的数据集上更新模型的参数，可以更新全部参数也
     可以只更新部分参数
 •   迁移学习/特征抽取：复用在大数据集上训练好的预训练模型的特征提取模块，训练一个以
     输出特征作为输入的任务模块，如分类器
 上述方法的局限性
 • 重新训练一个模型的时间成本会随着要学任务的增多变得越来越高，且过去任务的数据往往
   并不能轻易得到
 •   简单的微调会影响在之前学习任务上的性能，因为会改变用于过去任务的参数
 •   简单的迁移学习在新任务上通常较差，因为特征抽取无法覆盖到新任务中特定的信息，只能
     抽取通用的特征

51
 AAAI 2021: Continual Learning for Named
           Entity Recognition

现实场景中会不断地出现新的命名实体类型。为这些新类型重新标注原始的训练数
据常常受到存储和安全的限制导致代价较高或不可能实现，并且随着类型数量的增
加，为所有实体标注新数据集不切实际且容易出错。为解决此问题，本文提出了一
个NER持续学习方法，仅用新的实体类型标注的新训练数据即可满足训练要求；采
用知识蒸馏框架巩固已学到的知识。实验证明该方法可以让学生模型在不忘记之前
学习类型的情况下有效地鉴定出新的类型。
背景知识：知识蒸馏介绍
• 定义：通过一个叫蒸馏的过程实现模型间的知识迁移的技术，
  最初提出是用于将知识从一个笨重的模型迁移到一个更小更有
  效地模型，目前已被成功地用于压缩大规模的语言模型，如
  BERT
• 实现：首先训练一个教师模型，然后通过迁移教师的输出分布
  在一个迁移数据集上训练一个学生模型。学生模型是通过计算
  教师的概率分布𝑝𝑇 与学生的输出概率分布𝑝𝑆 的KL散度来训练的
• 在图像领域，有研究者通过更新一个图片分类器来支持新的类
  型的同时防止灾难性遗忘(Li and Hoiem 2018)
结果：ExtendNER学生模型的各实体类型随步骤变化
的F1得分图
 ACL 2021:Nested Named Entity Recognition via
Explicitly Excluding the Influence of the Best Path

提出了一种新的嵌套命名实体识别方法。作为一种分层方法，通过明确排除最优路径的影响，扩展了之前的次优路径识
别方法。在每个步骤中维护一组隐藏状态，并有选择地利用它们来构建不同的潜在函数，以便在每个级别上进行识。此
外，该文还证明了内部实体优先识别方案比传统的外部实体优先识别方案具有更好的性能。该文在ACE2004, ACE2005
和GENIA数据集上提供了大量的实验结果，以显示该文提出的方法的有效性和效率。
为了解决嵌套的NER问题，将这种序列标记方法扩展为多级编码方案。在该编码方案中，根据实体的深度将其划分
为若干层，并逐层采用序列标记方法对所有实体进行识别。
编码模式：
该文发现从最内部的实体进行检测可以得到更好的性能。
如果从外部开始。比如：“Former Hogwarts headmaster Albus Dumbledore”，第一层全认为是PER，第四层才辨认 “霍
格沃兹” 和 “校长”

如果从内部开始。在这个编码方案中，最内部 的 实 体 “ 霍 格 沃 茨 ” 、 “ 校 长 ” 和 “ 阿 不 思 ·邓 布 利 多 ” 出 现
在第一层。
用词向量和字符级词向量来表示

3层BiLSTM来编码，CRF来解码
实验：
数据集：ACE2004，ACE2005，GENIA
AAAI 2021:CrossNER: Evaluating Cross-Domain
         Named Entity Recognition

跨领域实体识别模型能够解决目标领域内实体识别样本的稀缺性问题。然而，大多数现有的NER基准缺乏 特 定 领域的
实体类型，或者不关注某个领域，导致跨领域评估的效率较低。为了解决这些 问题，该文引入了一个跨域的NER数据
集(CrossNER)，这是一个全标记的NER数据集合，跨越五个不同的领域，具有不同领域的专门实体类别。此外， 该 文
还提供了一个领域相关的语料库，因为使用它来预训练语言模型(领域自适应预训练)对领域自适应是有效的 。 然 后 ，
该 文 进行了综合实验，探讨了利用不同层次的领域语料库和预训练策略对跨领域任务进行领域自适应预训练的有效性
。研究结果表明，专注于包含领域专业实体的分数语料库，并在领域自适应预训练中采用更具挑战性的预训练策略，
有利于NER领域的适应，并且该文提出的方法可以持续优于现有的跨领域NER基线。然而，实验也说明了跨域NER任
务的挑战。
动机：目前的NER数据集有2个问题：
a)目标数据集要么和源数据集过于相近
b)源数据集和目标数据集的实体类别差距过大

新的数据集CrossNER：
包含5个领域politics, natural science, music, literature和artificial intelligence

制作数据集的方法：
a)收集无标签的wiki数据集
b)用DBpedia Ontology进行预标记
c)用2个训练好的NER标记器和一个专家进行标记
ACL2021:Explicitly Capturing Relations between
 Entity Mentions via Graph Neural Networks for
  Domain-specific Named Entity Recognition

命名实体识别(NER)在通用领域得到了很好的研究，最近的系统在识别通用实体类型方面已经达到了人类水平的性能。
然而，对于倾向于以复杂上下文和术语实体类型为特征的专门化领域，NER性能仍然是中等的。为了应对这些挑战，
该文基于全局共引用关系和局部依赖关系明确地连接实体提及，以构建更好的实体提及表示。在该文的实验中，该文将
实体提及关系加入到图神经网络中，结果表明该文的系统在两个不同领域的数据集上显著地提高了NER的性能。进一步
表明，所提出的轻量级系统可以有效地将NER性能提高到一个更高的水平，即使只有少量的标记数据可用。
实验
数据集：AnatEM(生物医学领域)，Mars(行星科学领域)

该文可以看到，在全局实体共引用和局部依赖关系下，该文的系统在所有系统中表现最好。与在AnatEM上的
BioBERT相比，它提高了平均F1得分0.88，与在Mars上的SciBERT相比，它提高了平均F1得 分0.62分
   ACL2021:TEBNER: Domain Specific Named Entity
Recognition with Type Expanded Boundary-aware Network

 为 解 决 命名实体识别中的标签稀缺问题，远程监督的命名实体识别方法被广泛应用于数据的自
 动标注和实体识别。虽然减少了人工工作量，但生成的不完整和有噪声的标注对学习有效模型
 提出了新的挑战。本文提出了一种新的字典扩展方法，通过类型扩展模型提取新的实体。此外，
 设计了一个多粒度的边界感知网络，从局部和全局的角度检测实体的边界 ， 在不同类型的数据
 集上进行了实验，结果表明，该文的模型优于以往最先进的远程监督系统。
动机：专业领域有标记的数据集很少
采用远程监督方法，根据给定的字典自动给数据打标签，并辨认实体。
但是这样打标签有2个问题：
a) 不完整标注，dictionary覆盖不全面(50%)
b) 对新的实体毫无办法

TEBNER (Type Expanded Boundary-aware NER)：
Dictionary Extender扩展字典：
   扩展原始字典，从未标注数据集提取高质量的(AutoPhrase)短语作为潜在实体
   用entity typing model实体类别模型(在标记数据集上训练)辨认这些潜在实体后，将其加入字典
Entity Recognizer辨认实体：boundary detector+ entity classifier
   "Break or Tie" Tagging Schema：辨认2个相邻的token是不是属于同一个实体mention，在词级别检测实体
   "BIO" Tagging Schema：在句子级别检测实体
   "Phrase Matching" Tagging Schema：提供全文级别的特征
实验：
数据集：BC5CDR（化学，疾病），NCBI-Disease（疾病），LaptopReview（评论）
Multi-modal NER
   多模态命名实体识别(MNER)已成为命名实体识别(NER)的重要研究方向，
   因为其在多模态深度学习和广泛应用中的研究意义 ，例如从大量媒体新闻
   和网络产品信息中提取结构。通过将图像作为附加输入，它大大扩展了传统
   的基于文本的NER。其背后的假设是，由于视觉上下文有助于解决歧义的多
   义词，因此预期结构化提取比纯粹基于文本的NER更准确。
Multi-modal NER
 AAAI 2021:Multi-modal Graph Fusion for Named
 Entity Recognition with Targeted Visual Guidance

    多模态命名实体识别（MNER）旨在以自由文本形式显示命名实体，并将其分类为带有图像的预定义类型。
    但是，主要的MNER模型不能完全利用不同模态的语义单元之间的细粒度语义信息，这有可能改善多模态表
    示学习。为了解决这个问题，该文为MNER提出了统一的多模态图融合(UMGF)方法。具体来说，该文首先使
    用统一的多模态图表示输入的句子和图像，该图捕捉了多模态语义单元（单词和视觉对象）之间的各种语义
    关系。然后，该文堆叠多个基于图的多模式融合层，这些层迭代执行语义交互以学习节点表示。最后，为每
    个单词实现了基于注意力的多模态表示，并使用CRF解码器执行命名实体标记。在两个基准数据集上进行的
    实验证明了MNER模型的优越性。
将整个图像编码为全局特征向量(a)，可用于增强每个单词表示，或指导单词学习视觉感知表示，
将整个图像平均分割成多个区域(b)，并基于变换框架与文本序列交互。但是并没有充分利用输入
句子-图像对中语义单元之间的细粒度语义对应。所以用(c)，将目标对象区域作为线索来指导
多模态的图：
2种顶点：
表征词的顶点：文本中的每个词都对应一个顶点，先将文本输入BERT编码器得到词的隐藏层，用于构造词对
应的顶点
表征图片的顶点：为得到图片中对NER针对性更强的信息，需要先进行目标检测，截取图片中包含目标的小
块，用于视觉信息抽取。这就产生了两个问题：文本目标检测、图片目标检测。
前者，使用斯坦福语法解析器（Stanford parser）对文本进行处理，取出所有的名词性短语。
后者，图片中的实体目标可能含两种，一种是对应于文本中的名词性短语的，一种没有出现在文本当中。
比如：文本目标检测出的结果是: Photo of Helmut Kohl(赫尔穆特•科尔) 、the brandenburg gate(勃兰登 堡门)
图片目标检测的结果：
多模态的图：
2种边：
模态内的边：任意两个表征文本的顶点间都有边、任意两个表征图片的顶点间都有边，即同一
模态内任意两个节点都有边连接
模态间的边：通用词提取的视觉对象对应的顶点和所有的文本顶点都有边连接，使用文本中名
词性短语提取到的视觉顶点只和名词性短语对应的那些文本顶点有边
实验：
数据集：Twitter-2015 ，Twitter-2017

1   BERT-CRF优于BiLSTM-CRF，因为预训练的模型可以一定程度上解决未标注实体等问题
2   BERT-CRF优于BERT，虽然差的不多，但也说明了CRF的有效性
3   多模态的方法总体上优于纯文本的方法，说明了视觉信息的有效性
4   UMT明显优于单模态和其他多模态的baseline，因为其除了使用交叉transformer来融合文本和图片外，
使用了辅助任务。
5   本文的方法优于UMT，因为加入了足够的visual guidance
         大模型在知识抽取的应用

Large Language Model Is Not a Good Few-shot Information
    Extractor, but a Good Reranker for Hard Samples!
                   动机

•   大语言模型在多种任务上取得了显著的进步，通过in-context   learning，
    在许多应用上展现了惊人的涌现能力 （记忆和推理能力）

•   最近有研究对比了LLMs使用小语言模型（SLMs）和使用传统微调技术
    在多种任务上的能力。在信息抽取领域，对于LLMs是否是好的few-shot
    信息抽取器的观点不一。

下面将系统性地评估LLMs在多种few-shot信息抽取任务中是否具有有竞争性
的能力。
                     提出问题

1) 在few-shot IE任务中，LLMs是否能真正超过SLMs？
2) 更多的标注数据能否提升LLMs和SLMs的能力？
3) 在经济和时间代价方面，哪类模型更好？
4) 是否LLMs和SLMs分别适合于处理不同类型的样本？

     在三个IE任务的八个数据集上对LLM和SMLs进行评估，通过k-shot采样策略
     构建少样本数据集
                   小模型

评估小模型执行few-shot IE任务的能力

本文采用的小模型为RoBERTa- large（基于抽取的方法）和T5- large（生成
式），使用以下4种有监督方法：

1   微调 (FT)：在SLMs添加一个分类头用于预测每个句子/词的标签
2   FSLS [1]：少样本NER和ED的基于抽取的SOTA模型
3   KnowPrompt [2]：执行少样本RE最佳的基于抽取的模型
4   UIE[3]：生成式的少样本信息抽取模型
                                大语言模型

评估大语言模型执行few-shot IE任务的能力
采用CODEX模型（调用免费，ICL能力强），在四种ICL设置下进行实验

•In-context learning （ICL）由instruction,
demonstrations, questions组成，随机选择
少样本训练集中的样本作demonstrations
• ICL + Auto COT
先使用原始的样本生成rational，再将生成的rational加入demonstration。
• ICL + demo筛选 (DS)
从训练集中选取和测试样本embedding相似的训练样本作为demonstrations。

• ICL + Self-ensemble (SE)
对每个测试样本预测多次，取出现次数最多的预测结果作为最终答案。
        结论：LLMs不是一个好的少样本信息抽取工具

•   1-shot下LLMs比SLMs表现好，
•   5-10 shot下LLMs和SLMs差不多，使用更多的训练数据后，SLMs比LLMs 好，
    因为SLMs可以基于训练数据微调。
   结论：LLMs不是一个好的少样本信息抽取工具

对于复杂的ED任务，SLMs总是比LLMs好。

在1shot下SLMs超过了LLMs
         结论：LLMs不是一个好的少样本信息抽取工具

LLMs的推理速度有限：

500个句子下的推理速度（秒）

B: RoBERTa/T5-base.
L: RoBERTa/T5-large.
C: code-davinci-002.
T: t e x t - d a v i n c i - 0 0 3 .
           LLMs是好的少样本重排工具

虽然在信息抽取任务中表现不好，但其记忆和推理能力对于解决IE任务仍然
具有关键优势

提出Filter-then-rerank范式，使得LLMs和SLMs在处理不同难度的样本时具
有互补性的结果

•   SMLs作为过滤器，移除不可能标签，保留Top-N个候选集
•   LLM重排这N个标签，输出最终的答案

        SLMs处理简单样本，LLMs处理复杂样本
         LLMs是好的少样本重排工具

对于需要外部知识或者复杂推理能力的复杂样本，SLMs由于不具备这些知
识或能力，处理困难。

SLMs有限的模型能力和数据量无法处理复杂样本，但可以通过更新参数，
从更多样本中学习到处理简单样本的能力。

以所有标签的最大概率为自信分数，衡量样本的困难程度。

     代表样本x具有标签y的概率，将自信分数低的样本分为困难样本
                       LLMs是好的少样本重排工具

    选出Top-n个预测，然后使用LLMs进行重排
    将重排过程重新构建成一个多项选择题的形式。
    将N个候选标签改写成选项，表明头实体<h ent>和尾实体<h ent>具有<label>
    关系。

 Sentence：Charles lives in the city
 Abidjan.
 T：(cities_of_residence, Charles,
Abidjan)

    优势：很大程度上减少了标签范围，以LLMs熟悉的形式执行IE任务，降低其
    执行IE任务的难度。
LLMs更擅长处理需要外部知识或者复杂推理的困难样本

适应性的过滤再重排：
设定一个confidence score阈值，高于阈值的用SLMs的预测作为最终结
果。低于阈值的选top- N个predictions作为多项选择输入给LLMs重排
                      实验结果

分别三个IE任务的数据集上进行实验 ：
NER： FewNERD K=（5, 10, 20）
RE: TACREV   K = (20, 50, 100)
ED: ACE05.   K= (5, 10, 20)

选取了基于LLM的ICL方法和基于小模型的FSLS微调方法作为基线模型，进
行比较
                   实验结果

• filter-then-rerank 方法在3个数据集上的9个实验设置下都取得了大的提升
• 在没有Ensemble时，rerank方法取得了2.4%的F1分数提升（3和5行），加入了
  ensemble后，rerank方法取得了2.1%的提升（4和6行）。表明rerank方法有效，
  且ensemble和rerank两种方法效果不同且互补。
总结：

•   因为任务形式和受限的demo数量，LLMs并不擅长少样本信息抽取

• 与SLMs相比，LLMs有较高时间和金钱开销

• LLMs可以通过filter-then-rerank范式帮助SLMs处理困难样本
行业知识图谱构建综述：
h t t p s : / / m p . w e i x i n . q q . c o m/ s / i V I o a Z x h S 1 E y C 2 e t R n B f 4 Q
知识增强的开源语言大模型框架KnowLM：
h t t p s : / / g i t h u b . c o m / z j u n l p / K n o w L M / b l o b / ma i n / R E A D M E _ Z H . md

InstructionKGC-指令驱动的自适应知识图谱构建
DeepKE/example/llm/InstructKGC/README_CN.md
编程练习：

◼ 数据集说明：本实验使用的是Resume命名实体识别数据集，实验共提供了三个数
  据集，分别是训练集train.txt，验证集dev.txt以及测试集test.txt。
◼ 其中，一共包含8种实体类型，它们分别是国籍(CONT)、教育背景(EDU)、地名
  (LOC)、人名(NAME)、组织名(ORG)、专业(PRO)、民族(RACE)、职称(TITLE)。
◼ 对于实体类型，这里我们使用的是BIO标注方式，即Beginning、Inside、Outside。
  对于一个实体的第一个字符，标注为B-实体类型，实体其他位置的字符标注为I-实
  体类型，不属于任何实体的字符标注为O。
◼ 数据格式采用conll标准，数据分为两列，第一列是输入句中的词划分，第二列是每
  个词对应的命名实体类型。
◼ 建议采用BiLSTM+CRF模型，也可以采用其它模型或对BiLSTM+CRF模型进行改进。
谢谢
