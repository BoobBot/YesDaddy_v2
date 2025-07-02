import discord
from discord.ext import commands
import aiohttp
import io


class RecreateWithAttachments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="recreate")
    async def recreate(
        self,
        ctx,
        source_channel: discord.TextChannel,
        dest_channel: discord.TextChannel,
    ):
        await ctx.send(f"🔄 Recreating from {source_channel.mention} to {dest_channel.mention}...")

        # Fetch all threads (active + archived)
        threads = await source_channel.guild.fetch_active_threads()
        archived = await source_channel.guild.fetch_archived_threads(source_channel)
        all_threads = {t.id: t for t in (*threads.threads, *archived.threads)}

        print(f"Found {len(all_threads)} threads total")

        async for msg in source_channel.history(limit=None, oldest_first=True):
            if msg.type != discord.MessageType.default:
                continue

            files = await self.download_attachments(msg.attachments)
            try:
                new_msg = await dest_channel.send(
                    content=msg.content or None,
                    files=files if files else None,
                )
            except Exception as e:
                print(f"❌ Failed to send message: {e}")
                continue

            # Check if a thread exists with id == msg.id (meaning the thread was created from this message)
            old_thread = all_threads.get(msg.id)
            if old_thread:
                print(f"🧵 Creating thread: {old_thread.name}")
                try:
                    new_thread = await new_msg.create_thread(
                        name=old_thread.name,
                        auto_archive_duration=old_thread.auto_archive_duration,
                        type=old_thread.type,
                    )
                except Exception as e:
                    print(f"❌ Failed to create thread {old_thread.name}: {e}")
                    continue

                async for tmsg in old_thread.history(limit=None, oldest_first=True):
                    if tmsg.type != discord.MessageType.default:
                        continue
                    t_files = await self.download_attachments(tmsg.attachments)
                    try:
                        await new_thread.send(
                            content=tmsg.content or None,
                            files=t_files if t_files else None,
                        )
                    except Exception as e:
                        print(f"❌ Failed to send in thread: {e}")

        await ctx.send("✅ Re-creation complete.")

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
    await bot.add_cog(RecreateWithAttachments(bot))
