#導入 Discord.py
import discord
from PicImageSearch.sync import SauceNAO
from PicImageSearch.model import SauceNAOResponse


async def send_image(message, imagename):
    with open('{}'.format(imagename), 'rb') as f:
        picture = discord.File(f)
        await message.channel.send(file=picture)
async def mowmi(message):
    out = ""
    for i in message:
        if i == "咪":
            out = out + "卯"
        elif i == "卯":
            out = out + "咪"
        elif i == " ":
            out = out + " "
        else:
            pass
    return out
async def ismowmi(message):
    out = ""
    for i in message:
        if i == "咪":
            out = out + i
        elif i == "卯":
            out = out + i
        elif i == " ":
            pass
        else:
            return False
    if len(out) == 0:
        return False
    else:
        return True
        


#client 是我們與 Discord 連結的橋樑
client = discord.Client()
    
#調用 event 函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)

@client.event
#當有訊息時
async def on_message(message):
    #排除自己的訊息，避免陷入無限循環
    pic_ext = ['.jpg','.png','.jpeg']
    if message.author == client.user:
        return
    
    if message.content.startswith("說"):
        tmp = message.content.split(" ")
        if len(tmp) == 1:
            await message.channel.send("你要我說甚麼啦?")
        else:
            await message.channel.send(tmp[1])
    if message.content== "測試測試":
        tmp = message.content.split(" ")
        if len(tmp) == 1:
            await message.channel.send("測三小 測你媽有沒有確診嗎owo?")
    if message.content.startswith("poi"):
        tmp = message.content.split(" ")
        if len(tmp) == 1:
            await message.channel.send("poi?")
        elif len(tmp) == 2:
            if tmp[1] == "poi":
                await message.channel.send("https://cdn.discordapp.com/attachments/1084827679737532427/1086183202567225445/content2F96C5FBDAFF350F4859A202044AA31D2735B622FC.gif")
    if message.content == "龍神の剣を喰らえ":
        tmp = message.content.split(" ")
        if len(tmp) == 1:
            await message.channel.send("https://cdn.discordapp.com/attachments/1084827679737532427/1086183379713671188/content2F1e06d0001558749348174.gif")
    if message.content == "竜が我が敵を喰らう":
        tmp = message.content.split(" ")
        if len(tmp) == 1:
            await message.channel.send("https://cdn.discordapp.com/attachments/1084827679737532427/1086183508105494588/content2F999.gif")
    if message.content == "貓咪":
        tmp = message.content.split(" ")
        if len(tmp) == 1:
            await message.channel.send("https://cdn.discordapp.com/attachments/1084827679737532427/1086163580820402216/content2Fscratching-cat-head.gif")
    if message.content == "瑀寧":
        tmp = message.content.split(" ")
        if len(tmp) == 1:
            await message.channel.send("https://cdn.discordapp.com/attachments/1084827679737532427/1086163538642477106/content2Fning.jpg")
            await message.channel.send("看三小 沒看到我在抽菸逆?")
    if message.content.startswith("卯") or message.content.startswith("咪"):
        Ismowmi = await ismowmi(message.content)
        
        if(Ismowmi):
            out = await mowmi(message.content)
            await message.channel.send(out)
    if message.content == "ㄐㄐ":
        await message.channel.send("好ㄘ<3")
    filter01 = ["艸", "肏", "耖"]
    for i in filter01:
        if i in message.content:
            await message.channel.send("https://media.discordapp.net/attachments/1073513935539535934/1086181288395931699/content2FIMG_6833.gif?width=515&height=528")
    
    if len(message.attachments) > 0: #Checks if there are attachments
        for file in message.attachments:
            for ext in pic_ext:
                if file.filename.endswith(ext) and message.content == "!ps":
                    await message.channel.send("偵測到圖片，搜尋中...")
                    await message.channel.send("-" * 30)
                    proxies = None
                    url = message.attachments[0].url
                    api_key = "4d1599814732b3f9c260c69d516392926c2d5bad" # SauceNao API KEY
                    saucenao = SauceNAO(api_key=api_key)
                    resp = await saucenao.search(url)
                    if resp.raw[0].similarity < 80.00:
                        await message.channel.send("此非pixiv上的圖片或者圖片不完全，結束搜尋。")
                        await message.channel.send("相似度:{}%".format(resp.raw[0].similarity))
                        await message.channel.send("-" * 30)
                    else:
                        await message.channel.send("搜尋結果如下")
                        await message.channel.send("相似度:{}%".format(resp.raw[0].similarity))
                        await message.channel.send("作品名稱:{}".format(resp.raw[0].title))
                        if(resp.raw[0].pixiv_id != 0):
                            await message.channel.send("pixivid:{}".format(resp.raw[0].pixiv_id))
                            await message.channel.send("作者:{}".format(resp.raw[0].author))
                        if(resp.raw[0].url != ""):
                            await message.channel.send("連結:{}".format(resp.raw[0].url))
                        await message.channel.send("-" * 30)


client.run('NzM5NTA0MDQ4MzgxNjI0MzIw.GcAOaN.JtxrJ_EXYIh204S3IZigDCFdIeoD9Ek94Lm9BQ') #TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面