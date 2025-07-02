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
        await ctx.send(
            f"🔄 Recreating messages (with attachments and threads) from {source_channel.mention} to {dest_channel.mention}..."
        )

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

            # ✅ Check for an associated thread
            for thread in source_channel.threads:
                if thread.message_id == msg.id:  # Instead of msg.has_thread
                    old_thread = thread
                    try:
                        new_thread = await new_msg.create_thread(
                            name=old_thread.name,
                            auto_archive_duration=old_thread.auto_archive_duration,
                            type=old_thread.type,
                        )
                    except Exception as e:
                        print(f"❌ Failed to create thread: {e}")
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

        await ctx.send("✅ Done copying channel with threads.")

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
