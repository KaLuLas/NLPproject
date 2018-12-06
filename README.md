# NLP_final_project

### Brief Introduction

half_done 存放预处理文本素材

pre_treatment.py 

文本材料预处理，删去空行，标题，页注，并去除空行（raw_book\*.txt -> book\*.txt）

人名素材处理 （HarryNameEnglish.txt -> HarryNameEnglishOuptu.txt）

human_name_extraction.py 人名提取，按分册进行，标记初次登场位置，人名~~，性别：~~之后添加人名唯一识别



**2018/12/6 **

更新nltk语料库，自己添加语料不然无法复现（chap2载入自己语料库）**finished**

添加的姓名现在保存在HarryNameEnglishOutput_save.txt中，处理函数在PreTreatment.py中



**2018/12/6**

需要记录出现的 名 / 姓 / 姓名 / Mr Mrs Miss？敬称 记录出场行数，记录出场次数 **finished**

现在human_name_extraction.py extract_name() 得到人物的初次登场，出场次数，以及名字

（存在姓/名/姓名/敬称重复）



**2018/12/6 **

家族树建立 **finished**

human_name_extraction.py 

family_name_extract()根据name_dict得到所有可能的人物姓氏 代表家族

build_family_tree()根据name_dict与family_name_dict得到一个以 name:（mentioned, member）为成员的字典，其中member包含name_dict中信息，即初次登场，出场次数，以及名字

Mr/Mrs Ron Weasley处理（没在家族树里面）**finished**



**TODO**

Miss 处理（加入到名字字典中）

文本预处理的功能（可以利用chap3的分句）归一一下放到pre里面去

姓名字典的图形化，出场顺序的一个数轴，提及占比的一个饼状图

家族字典树的图形化，每个成员作为一个树

---------人物关系部分--------

根据关系找出人名实体对，再去找包含这个人名对的所有实例，利用这些实例来做关系提取

<i>（见12/6课上CS224n内容）</i>
