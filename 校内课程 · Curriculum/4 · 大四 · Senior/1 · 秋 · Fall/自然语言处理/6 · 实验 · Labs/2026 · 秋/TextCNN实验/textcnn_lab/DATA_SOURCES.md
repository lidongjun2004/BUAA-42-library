# 数据与代码来源

数据沿用去年实验的 Cornell sentence polarity dataset v1.0。
正面和负面影评各5331条，每行一条，按Windows-1252编码读取。

数据主页 https://www.cs.cornell.edu/people/pabo/movie-review-data/

下载地址 https://www.cs.cornell.edu/people/pabo/movie-review-data/rt-polaritydata.tar.gz

论文 Bo Pang and Lillian Lee. Seeing stars: Exploiting class relationships for sentiment categorization with respect to rating scales. ACL 2005.

数据原始说明保存在data/rt-polaritydata.README.1.0.txt。使用和引用按该说明执行。

代码以课程去年《基于MindSpore的TextCNN情感分类实验》手册与同名Notebook为基础整理。
保留英文影评二分类、Embedding40、3/4/5三支96通道卷积、最大池化、Dropout0.5、Adam和8轮训练。
整理时修正词编号越界，训练与验证共用固定词表，增加UNK编号、固定划分、预测截断和验证模式切换。
卷积按valid计算，再沿句长方向取最大值。学习率统一为1e-3。
对照组只把卷积核高度改成2/3/4，两组使用完全相同的数据划分。
