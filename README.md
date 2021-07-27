# nonebot-adapter-telegram
（施工中）自己用的非官方nonebot2 telegram adapter，代码全靠糊  
开发中代码没有经过清理和优化，不能与官方版本共存  
当前仅支持有限类型的消息解析和发送（接受私聊/群聊文字/图片，发送私聊/群聊文字/图片/语音，入群事件）  
需要公网ip或者frp  
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
host=127.0.0.1 # 配置 NoneBot 监听的 IP / 主机名  
port=xxxxx     # 配置 NoneBot 监听的端口  
webhook_host=your_domain # 配置telegram webhook域名，由于telegram要求webhook地址必须为https，我们需要在之后配置反向代理  
bot_token=your_bot_token  #telegram bot token
```
三、
将域名解析到本机，用你喜欢的方式配置反代将webhook域名的流量转发到nonebot2的监听端口  
四、
开始写机器人（摸鱼）

## 最简单的例子
bot.py
```python
import nonebot
from nonebot.adapters.telegram import Bot

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter("your_bot_token", Bot) #your_bot_token替换为bot的token
nonebot.load_plugin("plugins.echo")

if __name__ == "__main__":
    nonebot.run()   
```
plugins/echo.py
```python
from nonebot.plugin import on, on_command
from nonebot.adapters.telegram import Bot, MessageEvent, Message, MessageSegment
from nonebot.rule import to_me

echo = on_command("echo",to_me())

@echo.handle()
async def echo_escape(bot: Bot, event: MessageEvent):
    await bot.send(message=event.get_message(), event=event)

#await bot.send(message="114514", event=event) #发送文字
#await bot.send(message=MessageSegment.photo(pic_url)), event=event) #发送图片 支持file:///，base64://，file_id，url(由Telegram服务器下载)
```
运行机器人，向bot私聊发送/echo 123，bot会将消息原样重新发送


