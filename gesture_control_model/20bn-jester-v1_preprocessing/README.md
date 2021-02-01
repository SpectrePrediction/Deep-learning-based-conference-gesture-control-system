## jester数据集预处理模块：

|`jester数据集`|
|----|
|[官网下载](https://20bn.com/datasets/jester/)|
|[百度aistudio下载](https://aistudio.baidu.com/aistudio/datasetdetail/57932)|
 
### cat_20bn.py：
1. 用于在无法使用cat指令时：例如Windows环境下合并20bn文件
* 在有cat指令环境时可以使用cat指令合并，具体指令通过官网获取
 
### jester_collation.py：
1. 用于jester数据集整理成符合项目数据集格式
* 他会将对应类别的文件夹存放在一起
* 可以通过设置白名单来选择需要整理的标签
* 可以选择是复制还是移动

