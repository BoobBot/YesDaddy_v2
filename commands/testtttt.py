import discord
from discord.ext import commands
import aiohttp
import io


class RecreateWithAllThreads(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="recreate")
    async def recreate(self, ctx, source_channel: discord.TextChannel, dest_channel: discord.TextChannel):
        await ctx.send(f"🔄 Recreating from {source_channel.mention} to {dest_channel.mention}...")

        # Step 1: Recreate base messages
        async for msg in source_channel.history(limit=None, oldest_first=True):
            if msg.type != discord.MessageType.default:
                continue

            files = await self.download_attachments(msg.attachments)
            try:
                await dest_channel.send(content=msg.content or None, files=files if files else None)
            except Exception as e:
                print(f"❌ Failed to send message: {e}")

        # Step 2: Recreate ALL threads from source_channel, even manual ones
        for thread in source_channel.threads:
            print(f"🧵 Creating thread: {thread.name}")
            try:
                # Send a parent message so we can attach the new thread to it
                placeholder = await dest_channel.send(f"🧵 **Thread recreated:** {thread.name}")
                new_thread = await placeholder.create_thread(
                    name=thread.name,
                    auto_archive_duration=thread.auto_archive_duration,
                    type=thread.type,
                )
            except Exception as e:
                print(f"❌ Failed to create thread {thread.name}: {e}")
                continue

            # Copy messages in thread
            async for tmsg in thread.history(limit=None, oldest_first=True):
                if tmsg.type != discord.MessageType.default:
                    continue
                t_files = await self.download_attachments(tmsg.attachments)
                try:
                    await new_thread.send(
                        content=tmsg.content or None,
                        files=t_files if t_files else None,
                    )
                except Exception as e:
                    print(f"❌ Failed to send in thread {thread.name}: {e}")

        await ctx.send("✅ All messages and threads copied.")

    async def download_attachments(self, attachments):
        files = []
        for attachment in attachments:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as resp:
                        if resp.status == 200:
                            data = await resp.read()
                            fp = io.BytesIO(data)
                            files.append(discord.File(fp, filename=attachment.filename))
            except Exception as e:
                print(f"⚠️ Failed to download attachment {attachment.url}: {e}")
        return files


async def setup(bot):
    await bot.add_cog(RecreateWithAllThreads(bot))
