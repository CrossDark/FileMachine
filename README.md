本python程序提供了一些管理文件的小方法
## 归档
本方法可以切换一个文件夹下的内容
### 语法
```yaml
filing:
    <你想要显示在文件夹下的内容>
```
### 使用说明
1. 将内容分组放到不同的文件夹里,例如:
```
Big
|--small1
    |--file1
	|--flie2
|--small2
    |--file3
```
2. 将setting.yaml设置为你想要显示的那组文件,例如:
```yaml
filing:
    Big/small1
```
3. 运行FileMachine.py,效果如下
```
Folder
|--file1
|--file2
```
## 当前
本方法可以将正在进行的项目整理到一个文件夹里
### 语法
```yaml
working:
    <项目目录1>
    <……>
    <项目目录n>
```