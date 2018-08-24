* [Sublime](#Sublime)
      * [1 使用Sublime Text 3进行Markdown 编辑+实时预览](#1-使用Sublime-Text-3进行Markdown-编辑+实时预览)


## Sublime
---
sublime 插件

### 1 使用Sublime Text 3进行Markdown 编辑+实时预览
---
1. 安装插件
	* 输入： Shift + Ctrl + P， 
	* 输入： pcip（也可以点击 Preferences --> 选择 Package Control: ，然后输入install），然后在插件库中分别选择安装Markdown Preview；
	* 输入： mmp  (选择:Markmon real-time markdown preview)
	* 输入： Markdown Preview

2. 自定义快捷键
	* 点击 Preferences --> Key Bindings User
	* 在[]中添加↓并保存，Alt + M 可以直接通过浏览器预览
	```
	{ "keys": ["alt+m"], "command": "markdown_preview", "args": {"target": "browser", "parser":"markdown"} },
	```


参考：https://jingyan.baidu.com/article/f006222838bac2fbd2f0c87d.html

### 2
