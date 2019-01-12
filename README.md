# NLP_final_project

### Brief Introduction
2018下学期自然语言处理期末大作业：
基于哈利波特英文原文进行词云，联系图生成，并进行关系特征学习

![WordCloud](https://github.com/KaLuLas/NLPproject/blob/master/word_cloud.png?raw=true)

![RelationGraph](https://github.com/KaLuLas/NLPproject/blob/master/relation_graph.png?raw=true)



### Contents

**./half_done：**

filename.txt 未处理文本材料

filename_sent.txt 几何并处理，分句后的文本材料

</br>

**./csv:**

用于生成关系图

node.csv 人物与出场权重

edge.csv 人物关系与权重

</br>

**./pre_treatment.py:** 

text_pre_treat():

文本材料预处理，删去空行，标题，页注，并去除空行，进行分句

输入为filename.txt，输出为filename_sent.txt

name_pre_treat():

人名素材处理 （HarryNameEnglish.txt -> HarryNameEnglishOuptu.txt）

</br>

**./human_name_extraction.py:** 

**name_dict**结构：{姓名，出场行数列表[]}

**family_name_dict**结构：{姓，[家族出场次数，[各个成员信息(姓名，出场行数列表)]]}

**appearance_dict**结构：{行数 / 行数±radius 区间段落，出现的角色}

**threshold:** [需要调参] 出现次数小于等于此值的姓名信息键值对将被视为无效

**appear_dict_radius:**[需要调参] 出场字典的投影范围大小

extract_name():

人名提取，并记录初次登场行数

family_name_extract():

根据提取到的人名得到所有姓氏

build_family_tree():

根据前两个函数得到的结果将提取到的姓名整合到家族字典树中

build_appearance_dict():

先创建 行数 -> 出现角色 的映射 appearance_dict

再把 当前行数±radius（闭区间）的出现角色映射到当前行数上来形成 appearance_proj_dict



word_cloud.png 在七本书内容基础上生成的词云

relation_graph.png 在七本书基础上生成的人物联系图（不包含确切关系

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



### History

**2019/01/11**

调参前工作完成

接下来找更好的特征和更好的参数

目标AC 65-70％



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


