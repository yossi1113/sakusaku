#bot tokenはenvにDISCORD_BOT_TOKENとして設定するか390行らへんにハードコードしてね
import discord
from discord import app_commands
from discord.ext import commands
import os
import random
import aiohttp
import json
import sys
import asyncio
from datetime import datetime, timezone, timedelta
import logging
from collections import defaultdict
import pytz
import ast

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#intents = discord.Intents.all()
intents = discord.Intents.default()
intents.message_content = True  # 必要最小限の特権インテントのみ有効化
client = discord.Client(intents=intents)
# 枕(プレフィックス)がデカすぎます！
prefix = os.getenv('prefix')
logch = int(os.getenv('logch'))
nausaba = os.getenv('nausaba')
# アップロード先のチャンネルID（ここを変更してください）
UPLOAD_CHANNEL_ID = int(os.getenv('upload')) # 実際のチャンネルIDに変更
sttime = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M:%S")
bot4 = commands.Bot(command_prefix={prefix}, intents=intents, help_command=None)

kyonotenpura = []
last_reset_date = None
kyononeta = []
susikaiten = None

def tench():
    """メッセージ受信時などに呼び出して、日付が変わっていたらリセット"""
    global kyonotenpura, last_reset_date
    
    jst = pytz.timezone('Asia/Tokyo')
    now = datetime.now(jst)
    current_date = now.date()
    
    # 初回実行または日付が変わった場合
    if last_reset_date is None:
        last_reset_date = current_date
    elif current_date != last_reset_date:
        kyonotenpura = []
        last_reset_date = current_date
        print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} JST - kyonotenpuraをリセットしました")

def netach():
    """メッセージ受信時などに呼び出して、日付が変わっていたらリセット"""
    global kyononeta, susikaiten
    
    jst = pytz.timezone('Asia/Tokyo')
    now = datetime.now(jst)
    current_date = now.date()
    
    # 初回実行または日付が変わった場合
    if susikaiten is None:
        susikaiten = current_date
    elif current_date != susikaiten:
        kyononeta = []
        susikaiten = current_date
        print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} JST - kyononetaをリセットしました")

# 許可されたユーザーのIDリスト（実際のDiscord User IDに置き換えてください）
ALLOWED_USER_IDS = ast.literal_eval(os.getenv('allow'))

# 権限チェック関数
# @is_authorized_user()
def is_authorized_user():
    def predicate(ctx):
        return ctx.author.id in ALLOWED_USER_IDS
    return commands.check(predicate)

@bot4.event
async def on_ready():
    print(f'{bot4.user} has connected to Discord!')
    try:
        synced = await bot4.tree.sync()  # bot → bot4 に修正
        print(f'{len(synced)}個のコマンドを同期しました')
    except Exception as e:
        print(f'コマンドの同期に失敗: {e}')

#--------------------------------------------------
@bot4.command()
async def しがちゃ(ctx):
    dotti = ["さくさく","ほくほく"]
    osume = random.choice(dotti)
    await ctx.reply(f"調理方法は{osume}だよ！\n鍋を用意しよう！")
#--------------------------------------------------
@bot4.command()
@is_authorized_user()
async def reset(ctx):
    global kyonotenpura, kyononeta
    kyonotenpura = []
    kyononeta = []
    await ctx.reply("リセットしたよ！")
#--------------------------------------------------
@bot4.command()
async def てんぷら(ctx):
    tench()
    global kyonotenpura
    if ctx.author.id in kyonotenpura:
        await ctx.reply("今日はもう天ぷらを作ってるよ！\n油ものは一日一回！")
        return
    else:
        dotti = ["さつまいも","かぼちゃ","しいたけ","ししとう","いんげん","おくら","あすぱら","えび"]
        site = ["https://www.sirogohan.com/recipe/tenpurasatumaimo/","https://www.sirogohan.com/recipe/tenpurakabocha/","https://www.sirogohan.com/recipe/tenpurasiitake/","https://www.sirogohan.com/recipe/tenpurasisitou/","https://www.sirogohan.com/recipe/tenpuraingen/","https://www.sirogohan.com/recipe/tenpurasapara/","https://www.sirogohan.com/recipe/tenpuraasupara/","https://www.nissui.co.jp/recipe/00874.html"]
        nan = [0,1,2,3,4,5,6,7]
        osume = random.choice(nan)
        k1 = dotti[osume]
        k2 = site[osume]
        await ctx.reply(f"今日作るべき天ぷらは{k1}だよ！\nレシピ:{k2}")
        kyonotenpura.append(ctx.author.id)
#--------------------------------------------------
@bot4.command()
async def すしねたがちゃ(ctx):
    netach()
    global kyononeta
    if ctx.author.id in kyononeta:
        await ctx.reply("みんなにおごってたら回転寿司で破産したので今日はもうやめて")
        return
    else:
        dotti = ["まぐろ","かつお","サーモン","えび","いか","たこ","たまご","生ハム","鴨","なす","生えび","あなご","チキン","ハンバーグ","はまち","たい","あじ","いわし","数の子","貝","うなぎ","とろ","ほたて","かに","たらこ","ミートボール","なっとう","きゅうり","いなり","たくあん"]
        k1 = random.choice(dotti)
        await ctx.reply(f"あなたが食うべき寿司ネタは{k1}だよ！\nさぁかいてんずしに行ってこい")
        kyononeta.append(ctx.author.id)
#--------------------------------------------------

@bot4.command(name='wl')
@is_authorized_user()
async def wl_command(ctx):
    await ctx.reply('もーまんたい\nhttps://www.youtube.com/watch?v=GWAtnzcbfFQ', mention_author=False)
#--------------------------------------------------
@bot4.command(name='ping')
async def ping(ctx):
    raw_ping = bot4.latency
    ping_ms = round(raw_ping * 1000)
    await ctx.reply(f'Pong!:ping_pong:\nBotのPing値は{ping_ms}msです。\n現在は{nausaba}サーバーで動作しています。\n起動時刻は{sttime}です!\nPythonのバージョン: {sys.version}\n', mention_author=False)
    # await bot4.change_presence(
    #     activity=discord.Game(f'{len(bot4.guilds)}サーバーで稼働中、、、起動時刻は{sttime}です!')
    # )
#--------------------------------------------------
@bot4.command(name='time')
async def current_time(ctx):
    """現在の日本時刻を表示"""
    japan_time = datetime.now(timezone(timedelta(hours=9)))
    await ctx.reply(f'今は{japan_time}です', mention_author=False)
#--------------------------------------------------
@bot4.command()
async def http(ctx, cag):
    cag = f"https://http.cat/{cag}"
    embed = discord.Embed(title="cute cat!",description="meow!",url=cag)
    embed.set_image(url=f"{cag}.jpg")
    await ctx.reply(embed=embed,mention_author=False)
#--------------------------------------------------
@bot4.command()
async def feed(ctx, etti):
	tenis = os.getenv('webhookhayada')
	bail = bot4.get_channel(tenis)
	embed = discord.Embed(title="問い合わせが来たよ!",description=etti,color=discord.Colour.from_rgb(102,250,184))
	A = ctx.author.display_name
	B = ctx.author.name
	C = ctx.author.id
	embed.add_field(name="送った人の表示名",value=A)
	embed.add_field(name="送った人のユーザー名",value=B)
	embed.add_field(name="送った人のID",value=C)
	await ctx.reply("お問い合わせを送信しました!\nこのご意見はbot開発に役立たせていただきます!")
	await bail.send("<@1376164344651321587>",embed=embed)
#--------------------------------------------------
@bot4.command(name='timer')
@is_authorized_user()
async def timer(ctx, minutes: int):
    try:
        if minutes <= 0:
            await ctx.reply("❌ 1以上の数字を入力してください！")
            return

        if minutes > 1440:
            await ctx.reply("❌ 1440分（24時間）以下で設定してください！")
            return

        await ctx.reply(f"⏰ わかった！{minutes}分後にお知らせするね！", mention_author=False)
        await asyncio.sleep(minutes * 60)
        await ctx.reply(f"## ⏰ {minutes}分が経ったよ！\n{ctx.author.mention}")

    except Exception as e:
        await ctx.reply(f"❌ エラーが発生しました: {e}")

@timer.error
async def timer_error(ctx, error):
    """timerコマンドのエラーハンドリング"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("❌ 使い方: `y.timer [分数]`\n例: `y.timer 5`")
    elif isinstance(error, commands.BadArgument):
        await ctx.reply("❌ 正しい数字を入力してください！\n例: `y.timer 5`")
#--------------------------------------------------
@bot4.command(name='say')
@is_authorized_user()
async def say(ctx, *, content: str = None):
    if not content:
        await ctx.reply("お前は何を言いたいんだっていう")
        return

    sender_name = ctx.author.name
    embed = discord.Embed(description=f"{content}")
    await ctx.channel.send(embed=embed)

    japan_time = datetime.now(timezone(timedelta(hours=9)))
    message_link = f'https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}'
    
    logembed = discord.Embed(
        title="脅迫されて強引に喋らされました。",
        description=f"{content}"
    )
    logembed.add_field(name="時刻", value=f"{japan_time}")
    logembed.add_field(name="脅迫ニキ", value=f"<@{ctx.author.id}>({sender_name})")
    logembed.add_field(name="喋ったとこ", value=f"<#{ctx.channel.id}>({message_link})")
    
    await ctx.message.delete()
    await asyncio.sleep(1)
    
    try:
        channel = await bot4.fetch_channel(logch)
        await channel.send(embed=logembed)
    except Exception as e:
        logger.error(f"Log channel error: {e}")
#--------------------------------------------------
@bot4.command(name='purge')
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    """指定した数のメッセージを削除
    
    使い方: y.purge [削除数]
    例: y.purge 10
    """
    if amount <= 0:
        embed = discord.Embed(
            title="❌ エラー",
            description="削除するメッセージ数は1以上である必要があります",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=5)
        return

    if amount > 100:
        embed = discord.Embed(
            title="❌ エラー",
            description="一度に削除できるメッセージは最大100件です\n大量削除は複数回に分けて実行してください",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=8)
        return

    try:
        amount = amount + 1
        embed = discord.Embed(
            title="🗑️ メッセージ削除中...",
            description=f"最大{amount}件のメッセージを削除しています...",
            color=discord.Color.orange()
        )
        status_msg = await ctx.send(embed=embed)

        messages_to_delete = []
        now = discord.utils.utcnow()

        async for msg in ctx.channel.history(limit=amount + 100):
            if msg != ctx.message and len(messages_to_delete) < amount:
                if (now - msg.created_at) < timedelta(days=14):
                    messages_to_delete.append(msg)

        if (now - ctx.message.created_at) < timedelta(days=14):
            messages_to_delete.append(ctx.message)

        if not messages_to_delete:
            embed = discord.Embed(
                title="⚠️ 警告",
                description="削除可能なメッセージが見つかりませんでした\n（14日以上古いメッセージは削除できません）",
                color=discord.Color.yellow()
            )
            await status_msg.edit(embed=embed)
            await asyncio.sleep(5)
            await status_msg.delete()
            return

        deleted_messages = await ctx.channel.delete_messages(messages_to_delete)
        deleted_count = len(deleted_messages)

        embed = discord.Embed(
            title="✅ 削除完了",
            description=f"**{deleted_count}件**のメッセージを正常に削除しました",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="👤 実行者", value=ctx.author.mention, inline=True)
        embed.add_field(name="📍 チャンネル", value=ctx.channel.mention, inline=True)
        embed.add_field(name="📊 要求数", value=f"{amount}件", inline=True)
        embed.set_footer(text=f"実行者ID: {ctx.author.id}")

        await status_msg.edit(embed=embed)
        logger.info(f"Purge executed: {deleted_count} messages deleted by {ctx.author} in {ctx.channel}")

        await asyncio.sleep(10)
        try:
            await status_msg.delete()
        except discord.NotFound:
            pass

    except discord.Forbidden:
        embed = discord.Embed(
            title="❌ 権限エラー",
            description="メッセージを削除する権限がありません\nボットに「メッセージの管理」権限を付与してください",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=10)

    except discord.HTTPException as e:
        embed = discord.Embed(
            title="❌ 削除エラー",
            description=f"メッセージの削除中にエラーが発生しました\n```{str(e)}```",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=10)
        logger.error(f"Purge error: {e}")

    except Exception as e:
        embed = discord.Embed(
            title="❌ 予期しないエラー",
            description="予期しないエラーが発生しました\n管理者に報告してください",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=10)
        logger.error(f"Unexpected purge error: {e}")
@purge.error
async def purge_error(ctx, error):
    """purgeコマンドのエラーハンドリング"""
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="❌ 権限不足",
            description="このコマンドを使用するには **メッセージの管理** 権限が必要です",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=8)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="❌ 引数不足",
            description="削除するメッセージ数を指定してください\n使用方法: `y.purge 10`",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=8)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            title="❌ 不正な引数",
            description="数字を正しく入力してください\n例: `y.purge 10`",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=8)
#--------------------------------------------------
def mizikaku(text):
    # 1. そもそも中身が空なら空で返す
    if not text:
        return ""

    # 2. 「。」で分割する（最大3つまで取り出す）
    # .strip() で末尾の余計な空白を消しておくのがコツ
    sentences = text.strip().split('。')

    # 3. 最初の3つ分だけ取り出し、空の要素（末尾の分割分など）を除去
    summary_list = [s for s in sentences[:3] if s]

    # 4. 「。」で繋ぎ直し、最後に必ず「。」を一つ添える
    summary = "。".join(summary_list) + "。"

    return summary
@bot4.command()
async def wiki(ctx, data, ser=None):
    url = 'https://ja.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        "prop": "extracts|pageprops",
        "exintro": "true",
        "explaintext": "true",
        "redirects": "1",
        "utf8": "1",
        "titles": f"{data}"
    }
    headers = {'User-Agent': "Raspberry Pi 4 Model B/Python"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as r:
            pagesdata = (await r.json())['query']["pages"]

            if list(pagesdata.keys())[0] == "-1" or ser == "1" or ser == "true" or ser == "1" or ser == "るえ":
                url = 'https://ja.wikipedia.org/w/api.php'
                params = {
                    'action': 'query',
                    'format': 'json',
                    "prop": "extracts|pageprops",
                    "exintro": "true",
                    "explaintext": "true",
                    "generator": "search",
                    "gsrlimit": "1",
                    "utf8": "1",
                    "gsrsearch": f"{data}"
                }

                async with session.get(url, params=params, headers=headers) as r2:
                    pagesdata = await r2.json()

                    if list(pagesdata.keys()) == ['batchcomplete']:
                        await ctx.reply("なんと!何も見つからなかった!")
                    else:
                        pagesdata = pagesdata.get("query", {}).get("pages", {})
                        page_id = list(pagesdata.keys())[0]
                        page = pagesdata[page_id]
                        pagestitle = page.get("title", "タイトル不明")
                        
                        # URLエンコード
                        import urllib.parse
                        encoded_title = urllib.parse.quote(pagestitle)
                        
                        embed = discord.Embed(
                            title=pagestitle,
                            color=4360181,
                            description=mizikaku(page.get("extract", "説明なし")),
                            url=f"https://ja.wikipedia.org/wiki/{encoded_title}"
                        )
                        embed.set_footer(text="タイトル直打ちでヒットしなかったため検索にフォールバックしました。")
                        embed.set_author(name=page.get("pageprops", {}).get("defaultsort", "エラーのため値ないよ"))
                        await ctx.reply(embed=embed)
            else:
                page = pagesdata[list(pagesdata.keys())[0]]
                pagestitle = page.get("title", "タイトル不明")
                
                # URLエンコード
                import urllib.parse
                encoded_title = urllib.parse.quote(pagestitle)
                
                print(page)
                embed = discord.Embed(
                    title=pagestitle,
                    color=4360181,
                    description=mizikaku(page.get("extract", "説明なし")),
                    url=f"https://ja.wikipedia.org/wiki/{encoded_title}"
                )
                embed.set_author(name=page.get("pageprops", {}).get("defaultsort", "エラーのため値ないよ"))

                await ctx.reply(embed=embed)
#--------------------------------------------------
@bot4.command()
async def gazou(ctx):
    # コマンドの名前とライブラリの名前は一致させないほうがいいよ！
    # バグってchoice呼び出せなくなるよ！
    sou = ["呼び方:https://www.pixiv.net/artworks/120872174","デカホシノサクサク:https://www.pixiv.net/artworks/120990590","ホシノサクサク:https://www.pixiv.net/artworks/128414689","最悪の場合遺体が1つ増えることになるユメ！:https://www.pixiv.net/artworks/138133128","ヤンデレとメンヘラの個人的な違い:https://www.pixiv.net/artworks/133399362","強いヤンデレ女が好き:https://www.pixiv.net/artworks/133399386","メンヘラ男も好き:https://www.pixiv.net/artworks/133399427","水族館:https://www.pixiv.net/artworks/137916731","暗記科目:https://www.pixiv.net/artworks/139216446","何でもお願い聞いてくれる米倉くん:https://www.pixiv.net/artworks/103687785","もう頑張りたくないよ:https://www.pixiv.net/artworks/108700483","近くのコンビニ店員さんの様子がおかしい:https://www.pixiv.net/artworks/126279647","全肯定後輩と死体を埋めに行く話:https://www.pixiv.net/artworks/134157548"]
    osusume = random.choice(sou)
    tintin = osusume.rsplit(':', 2)
    tintin1 = tintin[1]
    tintin2 = tintin[2]
    tintin = f"{tintin1}"":"f"{tintin2}"
    susumebed = discord.Embed( # Embedを定義する
        title="ぽまえにおすすめなのは",# タイトル
        color=12343551, # フレーム色指定(今回は緑)
        description=f"{osusume}\nなのだ！",
        url=tintin)
    susumebed.set_footer(text="embedは画像が半分までなのでりんくひらけ！")
    await ctx.reply(embed=susumebed)
#--------------------------------------------------
@bot4.command()
async def ramdom(ctx):
    await ctx.reply("ramdomじゃないよrandomだよ。")
#--------------------------------------------------
@bot4.command()
async def coin(ctx):
    okanemawasita = random.choice(["1","2"])
    if okanemawasita == "1":
        await ctx.reply("表だったよ！")
    elif okanemawasita == "2":
        await ctx.reply("裏だったよ！")
    else:
        ctx.reply("バグって停止したので作者を殺しに行きましょう！:sparkles:")
#--------------------------------------------------
@bot4.command()
async def help(ctx):
    await ctx.reply("[Web版のhelpです。(通信料は自己負担)](https://sakusaku.static.jp/help )\n[Web版のお問い合わせ先です。(通信料は自己負担)](https://sakusaku.static.jp/toi )\n[プライバシーポリシーです。(通信量は自己負担)](https://sakusaku.static.jp/privacy/ )\nbotはMPL2.0でオープンソースです。\nhttps://github.com/yoshihisa11132/sakusaku/tree/main")

    
# インポート時は実行せず、直接実行時のみbotを起動
if __name__ == "__main__":
    token = os.getenv("token")
    if not token:
        print("DISCORD_BOT_TOKEN環境変数が設定されていません。")
        print("Secretsタブでトークンを設定してください。")
    else:
        bot4.run(token)
