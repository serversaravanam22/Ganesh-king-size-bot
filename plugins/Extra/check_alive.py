import time
import random
from pyrogram import Client, filters

CMD = ["/", "."]

@Client.on_message(filters.command("alive", CMD))
async def check_alive(_, message):
    await message.reply_text("you very luck 🤞 iam alive ❤️ press /start use me")


@Client.on_message(filters.command("ping", CMD))
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Pong!\n{time_taken_s:.3f} ms")

































































































# this line is for copy-pasters...
#         ...while you are removing my credit and calling yourself a developerr... 
#         _____ just imagine, At that time i am fucking your mom and sis at same time, harder & too harder...
#
# Credit @user_is_leo.
# Please Don't remove credit.
# Born to make history @LazyDeveloper !
# for any error please contact me -> telegram@leotgadmin_bot
