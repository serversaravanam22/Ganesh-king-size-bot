
Navigation Menu
ironman-17
VJFILTER-TEST

Code
Pull requests
Actions
Projects
Wiki
Security
1
Insights
Settings
Commit a0d58df
Preview
Give feedback
kumarpk45
kumarpk45
authored
on Dec 1, 2024
Verified
Update commands.py
Tech_VJ
1 parent 
f0d60ea
 commit 
a0d58df
File tree
Filter files…
plugins
commands.py
1 file changed
+126
-2
lines changed
Search within code
 
‎plugins/commands.py
+126
-2
Original file line number	Diff line number	Diff line change
@@ -6,18 +6,20 @@
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import *
from database.ia_filterdb import col, sec_col, get_file_details, unpack_new_file_id, get_bad_files
from database.users_chats_db import db, delete_all_referal_users, get_referal_users_count, get_referal_all_users, referal_add_user
from database.join_reqs import JoinReqs
from info import CLONE_MODE, REACTIONS, CHANNELS, REQUEST_TO_JOIN_MODE, TRY_AGAIN_BTN, ADMINS, SHORTLINK_MODE, PREMIUM_AND_REFERAL_MODE, STREAM_MODE, AUTH_CHANNEL, OWNER_USERNAME, REFERAL_PREMEIUM_TIME, REFERAL_COUNT, PAYMENT_TEXT, PAYMENT_QR, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, CHNL_LNK, GRP_LNK, REQST_CHANNEL, SUPPORT_CHAT_ID, SUPPORT_CHAT, MAX_B_TN, VERIFY, SHORTLINK_API, SHORTLINK_URL, TUTORIAL, VERIFY_TUTORIAL, IS_TUTORIAL, URL
from utils import get_settings, pub_is_subscribed, get_size, is_subscribed, save_group_settings, temp, verify_user, check_token, check_verification, get_token, get_shortlink, get_tutorial, get_seconds
from info import CLONE_MODE, REACTIONS, CHANNELS, REQUEST_TO_JOIN_MODE, TRY_AGAIN_BTN, ADMINS, SHORTLINK_MODE, PREMIUM_AND_REFERAL_MODE, STREAM_MODE, AUTH_CHANNEL, OWNER_USERNAME, REFERAL_PREMEIUM_TIME, REFERAL_COUNT, PAYMENT_TEXT, PAYMENT_QR, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, CHNL_LNK, GRP_LNK, REQST_CHANNEL, SUPPORT_CHAT_ID, SUPPORT_CHAT, MAX_B_TN, VERIFY, SHORTLINK_API, SHORTLINK_URL, TUTORIAL, VERIFY_TUTORIAL, IS_TUTORIAL, URL, HOW_TO_POST_SHORT, ADMINS, DIRECT_GEN_DB
from utils import get_settings, pub_is_subscribed, get_size, is_subscribed, save_group_settings, temp, verify_user, check_token, check_verification, get_token, get_shortlink, get_tutorial, get_seconds, gen_link, clean_title, get_poster, temp, short_link
from database.connections_mdb import active_connection
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
logger = logging.getLogger(__name__)

BATCH_FILES = {}
user_states = {}
join_db = JoinReqs

@Client.on_message(filters.command("start") & filters.incoming)
@@ -1515,3 +1517,125 @@ async def purge_requests(client, message):
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
async def delete_previous_reply(chat_id):
    if chat_id in user_states and "last_reply" in user_states[chat_id]:
        try:
            await user_states[chat_id]["last_reply"].delete()
        except Exception as e:
            print(f"Failed to delete message: {e}")
@Client.on_message(filters.command("post") & filters.user(ADMINS))
async def post_command(client, message):
    try:
        await message.reply("**Wᴇʟᴄᴏᴍᴇ Tᴏ Usᴇ Oᴜʀ Rᴀʀᴇ Mᴏᴠɪᴇ Pᴏsᴛ Fᴇᴀᴛᴜʀᴇ:) Cᴏᴅᴇ ʙʏ [Hᴇᴀʀᴛ_Tʜɪᴇꜰ](https://t.me/HeartThieft_bot) 👨‍💻**\n\n**👉🏻Sᴇɴᴅ ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ ғɪʟᴇs ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴀᴅᴅ👈🏻**\n\n**‼️ ɴᴏᴛᴇ : Oɴʟʏ ɴᴜᴍʙᴇʀ**", disable_web_page_preview=True)
        user_states[message.chat.id] = {"state": "awaiting_num_files"}
    except Exception as e:
        await message.reply(f"Error occurred: {e}")
@Client.on_message(filters.private & (filters.text | filters.media) & ~filters.command("post"))
async def handle_message(client, message):
    try:
        chat_id = message.chat.id
        
        await delete_previous_reply(chat_id)
        
        if chat_id in user_states:
            current_state = user_states[chat_id]["state"]
            if current_state == "awaiting_num_files":
                try:
                    num_files = int(message.text.strip())
                    if num_files <= 0:
                        rply = await message.reply("⏩ Fᴏʀᴡᴀʀᴅ ᴛʜᴇ ғɪʟᴇ")
                        user_states[chat_id]["last_reply"] = rply
                        return
                    user_states[chat_id] = {
                        "state": "awaiting_files",
                        "num_files": num_files,
                        "files_received": 0,
                        "file_ids": [],
                        "file_sizes": [],
                        "stream_links": []
                    }
                    reply_message = await message.reply("**⏩ Fᴏʀᴡᴀʀᴅ ᴛʜᴇ ɴᴏ: 1 ғɪʟᴇ**")
                    user_states[chat_id]["last_reply"] = reply_message
                        
                except ValueError:
                    await message.reply("Invalid input. Please enter a valid number.")
            elif current_state == "awaiting_files":
                if message.media:
                    file_type = message.media
                    forwarded_message = await message.copy(chat_id=DIRECT_GEN_DB)
                    file_id = unpack_new_file_id(getattr(message, file_type.value).file_id)
                    log_msg = await message.copy(chat_id=DIRECT_GEN_DB)
                    stream_link = await gen_link(log_msg)
                    
                    size = get_size(getattr(message, file_type.value).file_size)
                    await message.delete()
                else:
                    forwarded_message = await message.forward(chat_id=DIRECT_GEN_DB)
                    file_id = forwarded_message.message_id
                user_states[chat_id]["file_ids"].append(file_id)
                user_states[chat_id]["file_sizes"].append(size)
                user_states[chat_id]["stream_links"].append(stream_link)
                user_states[chat_id]["files_received"] += 1
                files_received = user_states[chat_id]["files_received"]
                num_files_left = user_states[chat_id]["num_files"] - files_received
                if num_files_left > 0:
                    files_text = "ғɪʟᴇ" if files_received == 1 else "ғɪʟᴇs"
                    reply_message = await message.reply(f"**⏩ Fᴏʀᴡᴀʀᴅ ᴛʜᴇ ɴᴏ: {files_received + 1} {files_text}**")
                    user_states[chat_id]["last_reply"] = reply_message                     
                else:
                    reply_message = await message.reply("**ɴᴏᴡ sᴇɴᴅ ᴛʜᴇ ɴᴀᴍᴇ ᴏғ ᴛʜᴇ ᴍᴏᴠɪᴇ (ᴏʀ) ᴛɪᴛʟᴇ **\n\n**ᴇx : ʟᴏᴠᴇʀ 𝟸𝟶𝟸𝟺 ᴛᴀᴍɪʟ ᴡᴇʙᴅʟ**")                    
                    user_states[chat_id]["state"] = "awaiting_title"
                    user_states[chat_id]["last_reply"] = reply_message
                    
            elif current_state == "awaiting_title":
                title = message.text.strip()
                title_clean = re.sub(r"[()\[\]{}:;'!]", "", title)
                cleaned_title = clean_title(title_clean)
                imdb_data = await get_poster(cleaned_title) if imdb_info else None
                poster_url = imdb_data.get('poster') if imdb_data else 'https://telegra.ph/file/74707bb075903640ed3f6.jpg'
                file_info = []
                for i, file_id in enumerate(user_states[chat_id]["file_ids"]):
                    long_url = f"https://t.me/{temp.U_NAME}?start=aNsH_{file_id[0]}"
                    short_link_url = await short_link(long_url)
                    file_info.append(f"》{user_states[chat_id]['file_sizes'][i]} : {short_link_url}")
                
                file_info_text = "\n\n".join(file_info)
                stream_links_info = []
                for i, stream_link in enumerate(user_states[chat_id]["stream_links"]):
                    long_stream_url = stream_link[0]
                    short_stream_link_url = await short_link(long_stream_url)
                    stream_links_info.append(f"》{user_states[chat_id]['file_sizes'][i]} : {short_stream_link_url}")
                
                stream_links_text = "\n\n".join(stream_links_info)                
                summary_message = f"**🎬{title} Tamil HDRip**\n\n**[ 𝟹𝟼𝟶ᴘ☆𝟺𝟾𝟶ᴘ☆Hᴇᴠᴄ☆𝟽𝟸𝟶ᴘ☆𝟷𝟶𝟾𝟶ᴘ ]✌**\n\n**𓆩🔻𓆪 Dɪʀᴇᴄᴛ Tᴇʟᴇɢʀᴀᴍ Fɪʟᴇs Oɴʟʏ👇**\n\n**{file_info_text}**\n\n**✅ Note : [Hᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ]({HOW_TO_POST_SHORT})👀**\n\n**𓆩🔻𓆪 Sᴛʀᴇᴀᴍ/Fᴀsᴛ ᴅᴏᴡɴʟᴏᴀᴅ 👇**\n\n**{stream_links_text}**\n\n**✅ Note : [Hᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ]({HOW_TO_POST_SHORT})👀**\n\n**⚡ 𝐉𝐨𝐢𝐧 ➟ : <a href="https://t.me/Movieprovidergroups"><b>Mᴏᴠɪᴇs Rᴇǫᴜᴇsᴛ 𝟸𝟺×𝟽</b></a>**\n\n**❤️‍🔥ー𖤍 𓆩 Sʜᴀʀᴇ Wɪᴛʜ Fʀɪᴇɴᴅs 𓆪 𖤍ー❤️‍🔥**"
                summary_messages = f"{title_clean}, {cleaned_title}"
                if poster:
                    await message.reply_photo(poster, caption=summary_message)
                else:
                    await message.reply(summary_messages)
                    
                await message.delete()
                del user_states[chat_id]
        else:
            return
    except Exception as e:
        await message.reply(f"Error occurred: {e}")
