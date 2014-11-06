
## ChessQ
ChessQ是一个中国象棋程序。目前功能还很简单，目标是做个跨平台版的“象棋巫师”，希望在棋谱管理方面有自己独到的特色。

原作者仓库：https://github.com/walker8088/ChessQ


## ChessQ_Magic
个人修改的版本
<br>

## **一、工程目录结构** ##
根目录<br>
>├ doc --相关文档 <br>
>├ harmless --harmless引擎 <br>
>├ source --源代码 <br>
>├ LICENCE.txt --开源协议 <br>
>├ README.md --项目信息 <br>

<br>
## **二、源代码目录结构** ##
source<br>
>├ _eric4project  <br>
>├ cchess --界面操作<br>
>├ images --图片资源文件<br>
>├ sounds --声音<br>

<br>
## **三、引擎** ##
### harmless引擎
https://github.com/timebug/harmless

### 协议
[中国象棋通用引擎协议v3.0](https://github.com/haogefeifei/ChessQ_Magic/blob/master/doc/%E4%B8%AD%E5%9B%BD%E8%B1%A1%E6%A3%8B%E9%80%9A%E7%94%A8%E5%BC%95%E6%93%8E%E5%8D%8F%E8%AE%AEv3.0.md)

<br>
## **四、使用** ##

先编译引擎

    $ cd ChessQ_Magic/harmless
    $ make

运行

    $ cd ChessQ_Magic/source
    $ python ChessQ.py




