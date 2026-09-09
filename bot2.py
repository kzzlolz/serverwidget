import os
import threading
from flask import Flask, jsonify
import discord

app = Flask(__name__)

# Built-in CORS handler for Flask
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    return response

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)

GUILD_ID = 1508402330913996841
BOT_TOKEN = os.getenv("DISCORD_TOKEN")

@app.route('/api/guild-data', methods=['GET'])
def get_guild_data():
    guild = client.get_guild(GUILD_ID)
    if not guild:
        return jsonify({"error": "Guild not found"}), 404

    members_data = []
    for member in guild.members:
        role_ids = [str(role.id) for role in member.roles]
        
        members_data.append({
            "id": str(member.id),
            "username": member.name,
            "display_name": member.display_name,
            "avatar_url": str(member.display_avatar.url),
            "status": str(member.status),
            "bot": member.bot,
            "roles": role_ids
        })

    return jsonify({
        "total_members": guild.member_count,
        "members": members_data
    })

def run_flask():
    # Render assigns dynamic ports via the PORT environment variable
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    guild = client.get_guild(GUILD_ID)
    if guild:
        await guild.chunk()
        print("Member cache successfully updated!")

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    if BOT_TOKEN:
        client.run(BOT_TOKEN)
    else:
        print("ERROR: No DISCORD_TOKEN found in environment variables!")
