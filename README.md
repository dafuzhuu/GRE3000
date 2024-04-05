# GRE3000

将《再要你命3000》第二版按单词、释义、例句整理成若干个文档（数量自定义），用于导入专用背单词app：[生词本](https://apps.apple.com/cn/app/%E7%94%9F%E8%AF%8D%E6%9C%AC-%E6%99%BA%E8%83%BD%E8%83%8C%E8%AF%B5%E6%8F%90%E9%86%92/id1120027237)

<img width="1000" alt="image" src="https://github.com/ultimate233/GRE3000/assets/156023557/c8c0dd9e-4271-4115-933d-ad66778c8bd0">

选择这款app理由如下：

1. 不拘泥于单词书，可随时增加/减少单词，自由度高
2. 对于每个单词，可以随意自定义释义和例句，自由度高（这很有必要因为释义并不是展示的越多越好，而是要记住关键的）
3. 采用新东方背词法，每个单词从记录时刻起分8个记忆周期，分别为5分钟、30分钟、12小时、1天、2天、4天、7天、15天。八个周期结束后开启长期记忆周期，每15天复习一次，防止遗忘。相较于普通的艾宾浩斯曲线更加科学有效
4. 排序随机。不背单词、扇贝等软件都存在的问题是排序不随机，即假如两个单词在录入时相邻，且未来的记忆数据完全相同，则这两个单词永远相邻。长期来看容易出现“一同出现时记得、分开出现不记得”的情况

<img width="1000" alt="image" src="https://github.com/ultimate233/GRE3000/assets/156023557/e045a3c6-092e-4907-b65c-df936192039a">

在python导出excel文件后，仍需“获取模版”，将导出的excel单词复制粘贴进模版，以确保格式正确。接着点击“导入文件”将修改后的模版导入app

参数解释：

- `filename`：txt文件名
- `start_word`：输入一个单词，只导出从这个单词起后面的所有词
- `num`：定义等分成多少个excel

其中，单词书的txt文档来自[网站](http://www.downcc.com/soft/334837.html)

excel效果

<img width="1000" alt="image" src="https://github.com/ultimate233/GRE3000/assets/156023557/754f39bc-8cbb-4b47-a14f-bd31535cdbe5">

导入进app的效果

<img width="1000" alt="image" src="https://github.com/ultimate233/GRE3000/assets/156023557/f9cef52a-1a8d-420e-8908-43c768176377">

