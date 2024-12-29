from imdb import IMDb
from pyrogram import Client, filters

# Function to get movie details
def get_movie_details(movie_name):
    ia = IMDb()
    search_results = ia.search_movie(movie_name)
    if not search_results:
        return "❌ Movie not found."

    movie = search_results[0]
    ia.update(movie)

    title = movie.get('title', 'N/A')
    year = movie.get('year', 'N/A')
    rating = movie.get('rating', 'N/A')
    genres = ', '.join(movie.get('genres', []))
    plot = movie.get('plot outline', 'No plot available.')
    runtime = movie.get('runtime', ['N/A'])[0]
    imdb_url = f"https://www.imdb.com/title/{movie.movieID}/"
    poster = movie.get('cover url', None)

    message = f"""
<b>🎥 {title} ({year})</b>

<b>✅ IMDb Rating:</b> {rating}/10  
<b>✅ Genre:</b> {genres}

<b>📖 Plot:</b> {plot}

🔗 <a href="{imdb_url}">View on IMDb</a>

<b>✅ Runtime:</b> {runtime} Minutes  
❤️‍🔥 <b>Uploaded By:</b> <a href="https://t.me/Hinata_Developer">@Hinata_Developer</a>

⬆️ <b>Direct Files / Online Watching / Fast Download Links ⚡️</b>

<b>🗂️ 480p:</b> <a href="https://modijiurl.com/iSFEDe">Click Here</a>  
<b>🗂️ 720p:</b> <a href="https://modijiurl.com/PbsMMf">Click Here</a>  
<b>🗂️ 1080p:</b> <a href="https://modijiurl.com/AQEK5L">Click Here</a>

✔️ <b>Note:</b> How to open the links.  
📱 <b>Share with friends 📌</b>
"""

    return poster, message

# Command handler to fetch movie details
@Client.on_message(filters.command("post", prefixes="/"))
async def movie_post(client, message):
    # Extract the movie name from the message
    movie_name = message.text.split(' ', 1)[1] if len(message.text.split(' ', 1)) > 1 else None

    if movie_name:
        poster, movie_message = get_movie_details(movie_name)
        # Send the message with the poster (if exists)
        if poster:
            await message.reply_photo(poster, caption=movie_message)
        else:
            await message.reply_text(movie_message)
    else:
        await message.reply_text("❌ Please provide a movie name after the command.")
