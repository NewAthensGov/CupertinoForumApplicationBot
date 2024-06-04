#Created by Tyler Mullins of the Free Nation of the New Athens, for use in the Cupertino Forum.

import discord
from discord.ext import commands
import asyncio
import datetime

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
create_thread_lock = asyncio.Lock()

@bot.event
async def on_message(message):
    #print("message received")
    if message.content.startswith('!create_poll') and message.author.bot:
        print("bot invoked !create_poll")
        ctx = await bot.get_context(message)
        await bot.invoke(ctx)

# Command to create emoji reaction poll
@bot.command()
async def create_poll(ctx, nation: str, delegate: str):

    member_role = discord.utils.get(ctx.guild.roles, name="Member")
    applicant_role = discord.utils.get(ctx.guild.roles, name="Applicant") 
    guild = bot.get_guild(GuildIDRedacted)
    member = discord.utils.get(ctx.guild.members, name=delegate)
    channel_id = ChannelIDRedacted  # Replace this with your desired channel ID
    thread_name = nation
    thread_id = await create_thread(channel_id, thread_name)
    #await ctx.send(f"Thread '{thread_name}' created. ID: <#{thread_id}>")

    try:
        await ctx.send(f"<@&RoleIDRedacted>\nNew Applicant: {nation}, represented by <@{member.id}>. Discussion is open in <#{thread_id}> and will close <t:{unix_time_in_hours(72)}:R>, voting will automatically begin <t:{unix_time_in_hours(48)}:R>.")
        await member.add_roles(applicant_role)
    except:
        await ctx.send(f"<@&RoleIDRedacted>\nNew Applicant: {nation}, represented by {delegate} (who has not joined this server). Discussion is open in <#{thread_id}> and will close <t:{unix_time_in_hours(72)}:R>, voting will automatically begin <t:{unix_time_in_hours(48)}:R>.")
    # Wait for 48 hours before opening the poll
    await asyncio.sleep(48 * 60 * 60)

    # Create the poll embed
    embed = discord.Embed(title=f"Approve the following applicant: {nation}?", color=discord.Color.blue())
    embed.add_field(name="Options", value=":thumbsup: - Approve\n:thumbsdown: - Deny\n:raised_hand: - Abstain", inline=False)
    
    # Send the poll message and add reactions
    poll_msg = await ctx.send(embed=embed)
    await poll_msg.add_reaction('👍')
    await poll_msg.add_reaction('👎')
    await poll_msg.add_reaction('🤷‍♂️')

    try:
        await ctx.send(f"<@&RoleIDRedacted>\nVoting has opened on Applicant: {nation}, represented by <@{member.id}>. Voting will automatically end <t:{unix_time_in_hours(24)}:R>.")
    except:
        await ctx.send(f"<@&RoleIDRedacted>\nVoting has opened on Applicant: {nation}, represented by {delegate} (who has not joined this server). Voting will automatically end <t:{unix_time_in_hours(24)}:R>.")

    # Wait for 24 hours before announcing the winner
    await asyncio.sleep(24 * 60 * 60)

    # Get the poll message again to fetch reactions
    poll_msg = await ctx.channel.fetch_message(poll_msg.id)

    # Count reactions
    approve_count = deny_count = abstain_count = 0
    for reaction in poll_msg.reactions:
        if reaction.emoji == '👍':
            approve_count = reaction.count - 1  # Subtract bot's own reaction
        elif reaction.emoji == '👎':
            deny_count = reaction.count - 1
        elif reaction.emoji == '🤷‍♂️':
            abstain_count = reaction.count - 1

    # Announce the results
    if approve_count > deny_count:
        try:
            await ctx.send(f"<@&RoleIDRedacted>\nVoting has ended! The majority approves {nation}. Granting the Member role to <@{member.id}>.\nApprove: {approve_count}\nDeny: {deny_count}\nAbstain: {abstain_count}")
            await member.add_roles(member_role)
        except:
             await ctx.send(f"<@&RoleIDRedacted>\nVoting has ended! The majority approves {nation}. Delegate {delegate} has not joined this server. <@&RoleIDRedacted> Please find their delegate and manually give them the Member role.\nApprove: {approve_count}\nDeny: {deny_count}\nAbstain: {abstain_count}")
    else:
        await ctx.send(f"<@&RoleIDRedacted>\nVoting has ended! The majority denies {nation}. No action will be taken.\nApprove: {approve_count}\nDeny: {deny_count}\nAbstain: {abstain_count}")

#get unix time of +X hours
def unix_time_in_hours(hours):
    # Get current time
    current_time = datetime.datetime.now()
    # Add hours
    future_time = current_time + datetime.timedelta(hours=hours)
    # Convert to Unix time
    unix_time = int(future_time.timestamp())

    return unix_time

#create a thread
async def create_thread(channel_id, thread_name):
    async with create_thread_lock:  # Acquire the lock
        # Fetch the channel
        channel = bot.get_channel(channel_id)
        if not channel:
            print("Channel not found.")
            return
        
        # Create the thread
        thread = await channel.create_thread(name=thread_name, auto_archive_duration=259200, private=False)
        print(f"Thread '{thread_name}' created under channel '{channel.name}'.")
    
        return thread.id  # Return the ID of the created thread

# Run the bot
bot.run('REDACTED')
