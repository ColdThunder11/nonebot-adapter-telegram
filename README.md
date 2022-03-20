# nonebot-adapter-telegram
（施工中）自己用的非官方nonebot2 telegram adapter，代码全靠糊  
开发中代码没有经过清理和优化，不能与官方版本共存  
当前仅支持有限类型的消息解析和发送（接受私聊/群聊文字/图片，发送私聊/群聊文字/图片/语音，入群事件）  
如果使用webhook工作方式需要公网ip或者frp  
演示bot[@aya_od_bot](https://t.me/aya_od_bot)  
## 使用方法
如果要试毒的话  
真的要的话  
```shell
pip install nonebot-adapter-antelegram
```
## 上路
一、  
新建项目文件夹  
二、  
在nonebot2的配置文件中配置以下选项  
```shell
bot_token=your_bot_token  #telegram bot token，需要事先申请，参考https://core.telegram.org/bots#3-how-do-i-create-a-bot
telegram_bot_api_server_addr=https://api.telegram.org #可选，应该大概也可以替换为反代的域名，不设置默认官方
telegram_bot_api_proxy=proxy_server_addr #可选，代理服务器地址

#如果需要使用webhook方式接受消息，进行如下设置（推荐但是麻烦）
driver=~fastapi
host=127.0.0.1 # 配置 NoneBot 监听的 IP / 主机名  
port=xxxxx     # 配置 NoneBot 监听的端口  
webhook_host=https://your_domain # 配置telegram webhook域名，由于telegram要求webhook地址必须为https，需要自行配置反向代理，也可以参考telegram文档自建本地bot api，本地api无需https  

#如果需要长轮训方式接受消息，进行如下设置（推荐，长轮询比轮训接受消息更及时，资源占用更小）
driver=~httpx
telegram_polling_interval=0 #不使用轮训
telegram_long_polling_timeout=20 #长轮训超时时间

#如果需要轮训方式接受消息，进行如下设置（不推荐，仅建议调试网络时使用）
driver=~httpx
telegram_polling_interval=5 #轮训间隔
telegram_long_polling_timeout=0 #不使用长轮训

#注意：使用driver=~fastapi+~httpx时会使用httpx作为Driver并启动fastapi，用于需要轮训且同时启动fastapi服务器的情况

```
三、（仅使用webhook方式需要）  
将webhook域名解析到本机，用你喜欢的方式配置反代将webhook域名的流量转发到nonebot2的监听端口（如果不使用本地bot api）  
四、  
开始写机器人（摸鱼）  

## 已知问题（短时间内并不会解决）  
仅支持接受有限种类的消息  
仅支持发送有限种类的消息  
有亿点点小bug  
~~可能存在内存泄漏问题~~  

## 最简单的例子
bot.py
```python
import nonebot
from nonebot.adapters.telegram.adapter import Adapter

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(Adapter)
nonebot.load_plugin("plugins.echo")

if __name__ == "__main__":
    nonebot.run()   
```
plugins/echo.py
```python
from nonebot.plugin import on_command
from nonebot.adapters.telegram import Bot, MessageEvent, Message, MessageSegment
from nonebot.rule import to_me

echo = on_command("echo",to_me())

@echo.handle()
async def echo_escape(bot: Bot, event: MessageEvent):
    await bot.send(event, event.get_message())

#await bot.send(event, "114514") #发送文字
#await bot.send(event, MessageSegment.photo(pic_url)) #发送图片 支持file:///，base64://，bytes，file_id，url(由Telegram服务器下载)  
#
```
运行机器人，向bot私聊发送/echo 123，bot会将消息原样重新发送  


