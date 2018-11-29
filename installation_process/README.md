
#### Linux安装Anaconda
---
- 下载Anaconda： wget https://repo.continuum.io/archive/Anaconda3-5.3.0-Linux-x86_64.sh
- 输入安装命令： bash Anaconda3-5.2.0-Linux-x86_64.sh
- 根据提示按：ENTER yes 默认路径 写入环境变量
- 生效.bashrc文件： source ~/.bashrc
- 


#### Linux下载rz sz
- yum install -y lrzsz
- apt-get install lrzsz


#### Linux下载火狐浏览器
- 命令下载：
	- yum install firefox
	- apt-get install firefox
- 驱动下载地址： https://github.com/mozilla/geckodriver/releases/
- geckodriver移动到：/usr/bin or /usr/local/bin

- ERROR:
	- ERROR:...wrong permissions. 解决：chmod 777 geckodriver
	- ERROR:...can't kill an exited proces. 解决：驱动版本不符
	- ERROR:...newSession.  解决：驱动版本不符
	- ERROR:...Process unexpectedly closed with status 1
		- 无头设置：```python
		from selenium import webdriver
		from selenium.webdriver import FirefoxOptions
		opts = FirefoxOptions()
		opts.add_argument("--headless")
		browser = webdriver.Firefox(firefox_options=opts)
		```
- 参考：
	- https://stackoverflow.com/questions/46809135/webdriver-exceptionprocess-unexpectedly-closed-with-status-1
	- http://www.seleniumhq.org/
	- https://pypi.org/project/selenium/
	- http://ftp.mozilla.org/pub/firefox/releases/

- 注意：
	- 有的命令需要加：sudo
	- 更新源： sudo apt-get update


#### Ubuntu下载phantomjs
- 更新源：sudo apt-get update
- 下载：sudo apt-get install phantomjs
- 查看版本： phantomjs --version

- ERROR:
	- ...Could not connect to display...Aborted...
		- 打开： vi /etc/profile.d/aliases.sh
		- 添加： 
			- #!/bin/bash  
			- alias phantomjs="xvfb-run phantomjs"
		- 执行： source /etc/profile && phantomjs
	- Service phantomjs unexpectedly exited. Status code was: -6
		- ```python
			from selenium import webdriver  
			from pyvirtualdisplay import Display  
			display = Display(visible=0, size=(800,600))  
			display.start()  
			driver = webdriver.PhantomJS()  
			driver.get("http://www.baidu.com")  
			```

- 注意：
	- 依赖包： sudo apt install xvfb

# 未成功
#### 谷歌
- 下载网站： https://www.google.com/chrome/
	- wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
- 依赖： sudo apt-get -f install
- 安装： sudo dpkg -i 文件
- ChromeDriver下载地址： https://sites.google.com/a/chromium.org/chromedriver/downloads
	- 例： wget https://chromedriver.storage.googleapis.com/2.44/chromedriver_win32.zip
- 解压： unzip 文件
- 移动到： /usr/bin

- chrome的chromedriver网址：
	- http://npm.taobao.org/mirrors/chromedriver/
	- http://chromedriver.storage.googleapis.com/index.html