# NLP_final_project

### Brief Introduction
2018下学期自然语言处理期末大作业：
基于哈利波特英文原文进行词云，联系图生成，并进行关系特征学习

</br>

JK罗琳在其著作《哈利波特》中构建了一个奇幻而宏大的世界观，其中充斥着形形色色各有不同魅力的人物形象。这些人物又组成家庭，家族，部门，学院等等组织，彼此之间存在着复杂的人际关系。我们试图通过分析作者的英文原著，提取出人物在文本中的信息：包括观察人物在文本中的分布位置，在全文中的提及频数，名字包含的姓氏部分，与其他人物姓名同时出现的频率等等一系列参数来得到我们想要的信息，并以形象直观的文本、图标形式展现出来。

![WordCloud](https://github.com/KaLuLas/NLPproject/blob/master/word_cloud.png?raw=true)

![RelationGraph](https://github.com/KaLuLas/NLPproject/blob/master/relation_graph.png?raw=true)

</br>

### Contents

**./corpus: 存放原著语料**

​         /book(n).txt 对应第n册的英文原著

​         /book(n)_sent.txt 对应第n册英文原著分句后的结构

​         /input.txt & input_sent.txt 同上，为7册原文的整合

​         /PotterNameEnglish.txt 哈利波特出场人物介绍

​         /PotterNameEnglishOutput.txt 提取出的人物姓名

​         /PotterNameEnglishOutput_save.txt 提取并修改后的姓名语料

**./csv: 存放用于形成人物关系图的节点/边数据，以及用于训练分类器的标签关系对，分类器得分**

​         /book(n)_sent_node.csv 节点数据，权重为出现次数影响节点大小

​         /book(n)_sent_edge.csv 边数据，权重为两个人物出现在文章一定区间的次数，影响边的粗细

​         /…relation_label.csv 关系对与标注的关系，关系对来自input_sent.txt中

​         /…scores.csv 分类器得分根据输入特征集大小变化的记录（关系从少到多

**./errors: 分类器的评分使用交叉验证法，文件夹下记录每一次验证时判断错的记录**

​         /…iter(n).csv 交叉验证中第n次判断错的人物关系

​         /…join.csv 以上所有记录的并集

**./save: 构建姓名字典，人物关系字典，训练器用的特征集十分耗时，**

**目录下的这部分的pkl文件用于这些字典结构的快速重建** 

​         /…name_dict.pkl 保存与读取name_dict数据结构

​         /…relation_record.pkl 保存与读取 relation_record 数据结构

**others**

./pre_treatment.py 原文语料和姓名语料的预处理

./potter_more.py 主程序，设计了可选功能的命令行ui

./relation_predict.py 训练关系分类器并对分类效果进行评价

./name_extract_logic.png 在文本中匹配人名的逻辑图

./word_cloud.png 根据人名在文本中出现次数生成的人名词云

./relation_graph.png 利用gephi软件与csv文件生成的人物关系网络图

./PerformanceWithVaryingSize 分类器表现根据输入特征集大小变化的图表

</br>

**执行代码文件potter_more.py所需环境:**

​         python3.6及以上

​         拓展库安装：nltk / numpy / matplotlib / tqdm（进度条）/ wrodcloud（生成词云）/

</br>

### TODO

1. 文本预处理: 分句，去除大标题，空行，替换符号，Page，归一一下放到pre里面去 **finished**
2. 异常的省略号导致的分句问题 **finished**
3. 对异常姓名的一个处理：提及次数就一两次的其实在关系提取中也不重要，可以直接把出现次数少的都筛选掉，建议在构建家族字典树之前对姓名字典进行筛选。**存在问题：**小样本下一个出现次数少的也可能拥有重要信息，比如一个人的人名只出现了一次。**finished**
4. 在提取姓名的时候不仅记录初次出场，应该记录所有出场，根据这些出场信息整合一个“行数->出现人员”之后再投影成“段落（几行）->出现人员”的字典 **finished**
5. 出场顺序的序列输出利用pandas **finished**，姓名字典的输出 **finished**，提及占比的词云 **finished**
6. 打印信息做成一个整合的参数可选的函数，输入参数字典可能不同 **finished**
7. 创建姓名字典进度条 **finished**
8. 添加选择文件读取功能 **finished**
9. 利用**出现投影字典**人物间关系亲密疏远的一个图/ 直接用gephi画图 save csv **finished**
10. 应该用标准化 **finished**
11. 交互报错机制 **finished**
12. figure_selected，appear_dict_radius 需要调参 做曲线（后期
13. **（接下来往下的工作记得标注是哪基于个文本的内容，明天优先做input_sent）**把name-dict / relation-record-dict 保存并重新加载的机制（形成时间过长 尝试pickle）开始执行时先利用pkl文件对这两个字典初始化可以省掉大部分时间 **存档功能finished**
14. 把关系对导出进行标注 “关系-标签” **finished**
15. 读csv文件 -> 构建 **人物关系出现文本词频** 特征集 **finished**
16. 利用“关系-标签”训练关系分类器，预测的函数实现train和predict **finished**
17. 去掉了文本中的所有符号，人名，stopwords **finished**
18. 特征选取 / 调参开始 **finished** 按照line20的来
19. 在line20 基础上试着去掉stopword人名试试吧 **finished**
20. [重要]训练集和测试集的大小范围问题，交叉验证 **finished**
21. 可以看看判错的例子 **finished**
22. 标签根据判错例子修改一下 **finished**
23. 用pickle保存一下feature_set，已经确认是按顺序保存的了 **finished**
24. [最后做]把关系不是特别大的联系排除掉，通过特征集排序就不用每次都构建特征集，画个图表试试 **finished**

</br>

**随便乱记的分类器成长史**

| 特征                    | 映射区间大小 | 备注                                                  | 符号                                                   | 人名                                                   | 停止词                                                  | 准确率% | 交叉验证 |
| ----------------------- | ------------ | ------------------------------------------------------------ | ----------------- | ---- | ----------------------- | ----------------------- | ----------------------- |
| related_word_freq | ±4           |                                                  | 有                                                | 有                                                | 有                                                | 35.3              |               |
| (下同）                 | (下同）      |                                              | 无                                            | 有                                            | 有                                            | **36.5**          |           |
|                         |              |                                             | 无                                          | 有                                           | 无                                           | 23.2              |               |
|                         |              |                                         | 无                                       | 无                                       | 无                                       | 23.2              |               |
| 人物关系出现文本词袋all |              |                              | 无                                                    | 有                                                    | 有                                                    | 浮动过大          |           |
| 文本词袋30 or 200       |              |                                                              | 无 | 有 | 有 | 13.0 浮动大       |        |
| related_word_freq       | ±4           | **发现我一个标签标错了** | 无 | 有 | 有 | **55.9**       |        |
|                         | ±3选定      |  | 无 | 有 | 有 | **57.9**    |     |
|                         | ±2           |                                                              | 无 | 有 | 有 | 57.1              |               |
|                         | ±1           |                                                              | 无 | 有 | 有 | 57.0              |               |
|                         | ±0           |                                                              | 无 | 有 | 有 | 57.7             |              |
| 词袋 | ±3 | 词袋确实是没戏了 | 无 | 有 | 有 | 52.7 |  |
| related_word_freq       | ±3 | MAXENT 分类器没戏了 | 无 | 有 | 有 |  |  |
| hapax_words |  |  | 无 | 有 | 有 | 57.7 |  |
| hapax_words | ±0 |  | 无 | 有 | 有 | **59.0** |  |
| 同上 | 同上 | **训练集包含后五分之四** | 无 | 有 | 有 | 76.8 |  |
| related_word_freq | ±3 | **把人物关系记录字典改对了** | 无 | 有 | 有 | 70.37 |  |
|  | ±2 |  | 无 | 有 | 有 | 70.37 |  |
|  | ±1 |  | 无 | 有 | 有 | 70 |  |
|  | **±0** |  | 无 | 有 | 有 | **76.38** |  |
| hapax_words | ±0 |  | 无 | 有 | 有 | 76.38 |  |
|  | ±1 |  | 无 | 有 | 有 | 70 |  |
| 交叉验证之后的数据我放到excel里面了 |              |                              |      |      |        |             |          |

 </br>

---------人物关系部分--------

需要找到人物共同出场部分的话可能记录所有出现句子序号会有用，不需要再次遍历 **finished**

PART1 根据两个人物出现在同一句话或同一段对话中的次数多少来判断联系强弱 **finished**

PART2 根据关系找出人名实体对，再去找包含这个人名对的所有实例，利用这些实例来做关系提取

需要进行有监督学习，特征提取可以考虑使用**词袋**

进行文本分类的特征提取需不需要去掉上下引号 



<i>（见12/6课上CS224n内容）</i>

**参考：**

词云 http://www.cnblogs.com/Sinte-Beuve/p/7617517.html

关系可视化？http://www.cnblogs.com/Sinte-Beuve/p/7679392.html

</br>

### History

**2019/01/12【基本结项】**

调参工作和找特征都完成

也找到了分类器表现最好的特征集大小

AC 最高能达到88％

接下来完成论文就行啦

</br>

**2019/01/11**

调参前工作完成

接下来找更好的特征和更好的参数

目标AC 65-70％

</br>

**2019/01/10**

cmd交互完成

词云的生成以及人物联系图的生成

人物联系图生成需要软件Gephi

</br>

**2019/01/09**

异常姓名的筛选处理完毕

姓名字典name_dict改版

出场字典以及出场投影字典完成

交互cmd制作中

</br>

**2018/12/28**

现在pre_treatment.py可以做分句了，不过似乎需要修改（如省略号问题），book1.txt->book1_sent.txt

human_name_extraction.py现在输入输出格式为book1_sent.txt -> book1_sent_name_extract.txt

似乎分句后有得有失，具体表现还要自己检查

</br>

**2018/12/7**

Mr. Harry Potter / Miss Hermione Granger问题（在姓名提取中解决 **finished**

现在使用一个三元组来进行名字检测，具体判断逻辑见下方

现在名字识别已经几乎没有问题

![name_detect_logic](https://github.com/KaLuLas/NLPproject/blob/master/name_detect_logic.jpg?raw=true)

</br>

**2018/12/6  **

家族树建立 **finished**

human_name_extraction.py 

family_name_extract()根据name_dict得到所有可能的人物姓氏 代表家族

build_family_tree()根据name_dict与family_name_dict得到一个以 name:（mentioned, member）为成员的字典，其中member包含name_dict中信息，即初次登场，出场次数，以及名字

Mr/Mrs Ron Weasley处理（没在家族树里面）**finished**

</br>

需要记录出现的 名 / 姓 / 姓名 / Mr Mrs Miss敬称 记录出场行数，记录出场次数 **finished**

现在human_name_extraction.py extract_name() 得到人物的初次登场，出场次数，以及名字

（存在姓/名/姓名/敬称重复）

</br>

更新nltk语料库，自己添加语料不然无法复现（chap2载入自己语料库）**finished**

添加的姓名现在保存在HarryNameEnglishOutput_save.txt中，处理函数在PreTreatment.py中


