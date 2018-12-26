# NLP_final_project

### Brief Introduction

half_done 存放预处理文本素材

pre_treatment.py 

文本材料预处理，删去空行，标题，页注，并去除空行，分句

人名素材处理 （HarryNameEnglish.txt -> HarryNameEnglishOuptu.txt）

human_name_extraction.py 人名提取，按分册进行，标记初次登场位置，人名~~，性别：~~之后添加人名唯一识别



**2018/12/6 **

更新nltk语料库，自己添加语料不然无法复现（chap2载入自己语料库）**finished**

添加的姓名现在保存在HarryNameEnglishOutput_save.txt中，处理函数在PreTreatment.py中



**2018/12/6**

需要记录出现的 名 / 姓 / 姓名 / Mr Mrs Miss敬称 记录出场行数，记录出场次数 **finished**

现在human_name_extraction.py extract_name() 得到人物的初次登场，出场次数，以及名字

（存在姓/名/姓名/敬称重复）



**2018/12/6 **

家族树建立 **finished**

human_name_extraction.py 

family_name_extract()根据name_dict得到所有可能的人物姓氏 代表家族

build_family_tree()根据name_dict与family_name_dict得到一个以 name:（mentioned, member）为成员的字典，其中member包含name_dict中信息，即初次登场，出场次数，以及名字

Mr/Mrs Ron Weasley处理（没在家族树里面）**finished**



**2018/12/7**

Mr. Harry Potter / Miss Hermione Granger问题（在姓名提取中解决 **finished**

现在使用一个三元组来进行名字检测，具体判断逻辑见下方

现在名字识别已经几乎没有问题

![name_detect_logic](D:\QQPCmgr\Desktop\Courses\大三\能量炮\NLPproject\name_detect_logic.jpg)



**2018/12/28**

现在pre_treatment.py可以做分句了，不过似乎需要修改（如省略号问题），book1.txt->book1_sent.txt

human_name_extraction.py现在输入输出格式为book1_sent.txt -> book1_sent_name_extract.txt

似乎分句后有得有失，具体表现还要自己检查



**TODO**

文本预处理: 分句chap3/ 去除大标题，空行，替换符号，Page，归一一下放到pre里面去

姓名字典的图形化，出场顺序的一个数轴，提及占比的一个饼状图

家族字典树的图形化，每个家族姓氏作为一个树



---------人物关系部分--------

需要找到人物共同出场部分的话可能记录所有出现句子序号会有用，不需要再次遍历

PART1 根据两个人物出现在同一句话或同一段对话中的次数多少来判断联系强弱

PART2 根据关系找出人名实体对，再去找包含这个人名对的所有实例，利用这些实例来做关系提取

需要进行有监督学习，特征提取可以考虑使用词袋

<i>（见12/6课上CS224n内容）</i>
