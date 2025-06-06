import os
import aiohttp
import asyncio

token = "MTM4MDM0MDE2ODM5NzAyOTQ3OA.GXFEiE.AcTro7HPaWYITYVFPAPBWYDjjqLg5u-USyrveo" #token
hook = "https://discord.com/api/webhooks/1380340642433073183/J1uaOG_LzxM99m4iK6JiyvQbUyfx8kBiRSBxu2NS9aFziO1GvlBY3GMzLQ_8umqfmMC9" #webhook link
guild = "9191373839292920"
vanity_list = ["botancxn"]
delay = 0.1 
claimed = False

async def notify_start(vanity_code):
    embed = {
        "title": "Vanity Sniper Started",
        "description": f"Target Vanity Code: {vanity_code}",
        "color": 0000
    }
    payload = {
        "content": "@everyone",
        "embeds": [embed]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(hook, json=payload) as response:
            print(f"Sent start notification, status: {response.status}")

async def notify_vanity_claimed(vanity_code):
    vanity_url = f"[{vanity_code}](https://discord.gg/{vanity_code})"
    embed = {
        "title": "Vanity Claimed",
        "description": f"Vanity Code: {vanity_url}\nGuild ID: {guild}",
        "color": 0000
    }
    payload = {
        "content": "@everyone",
        "embeds": [embed]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(hook, json=payload) as response:
            print(f"Sent claimed notification, status: {response.status}")

async def claim(session, url, json):
    global claimed
    if claimed:
        return
    claimed = True
    async with session.patch(url, json=json, headers={
        "Authorization": token,
        "X-Audit-Log-Reason": "slapped by console",
        "Content-Type": "application/json"
    }) as response:
        print(response.status)
        if response.status in [200, 201]:
            print(f"[+] Vanity claimed: {json['code']}")
            await notify_vanity_claimed(json['code'])
        else:
            print(f"[-] Failed to claim vanity: {json['code']} | status: {response.status}")

async def fetchVanity(session, vanity, x):
    if not vanity:
        return
    try:
        async with session.get(f"https://canary.discord.com/api/v10/invites/{vanity}", headers={"Authorization": token}) as response:
            status = response.status
            if status == 404:
                await claim(session, f"https://canary.discord.com/api/v9/guilds/{guild}/vanity-url", {"code": vanity})
            elif status == 200:
                print(f"[+] Attempt: {x} | Vanity: {vanity}")
            elif status == 429:
                print("[-] | Rate Limited")
                os.system("kill 1")
                raise SystemExit
            else:
              print("[-] Unknown Error")
              raise SystemExit
    except Exception as error:
      print(f"[-] | Error: {error}")
      await asyncio.sleep(delay)

async def threadExecutor(vanity, x):
    async with aiohttp.ClientSession() as session:
        while not claimed:
            try:
                await fetchVanity(session, vanity, x)
                break
            except Exception as error:
                print(f"[-] | Thread suspended, Thread ID: {x}")
                continue

async def main():
    print("Starting...")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("https://canary.discord.com/api/v9/users/@me", headers={"Authorization": token}) as response:
                if response.status in [200, 201, 204]:
                    user = await response.json()
                    id = user["id"]
                    username = user["username"]
                    print(f"Logged in as {username} | {id}")
                else:
                    print("[!] | Bad Auth")
                    raise SystemExit
                for vanity in vanity_list:
                    if claimed:
                        raise SystemExit
                    await notify_start(vanity)
                    for x in range(100000000):
                        if claimed:
                            break
                        await threadExecutor(vanity, x)
                        await asyncio.sleep(delay)
                print("[+] | Execution Completed")
        except Exception as error:
          print(f"[-] | Error: {error}")

asyncio.run(main())
