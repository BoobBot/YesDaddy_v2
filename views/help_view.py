import datetime

import discord


class Help(discord.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx
        options = [
            # add more options here
            discord.SelectOption(label="Core", emoji="<a:core:1158418275559022674>", description="Core Commands"),
            discord.SelectOption(label="Currency", emoji="<:currency:1158418293879754833>", description="Currency Commands"),
            discord.SelectOption(label="Gambling", emoji="<:Gambling:1158418665209864212>", description="Gambling Commands"),
            discord.SelectOption(label="Profile", emoji="<:Profile1:1158418933221695608>", description="Profile Commands"),
            discord.SelectOption(label="Inventory", emoji="<:inventory:1187049990804213830>", description="Inventory Commands"),
            discord.SelectOption(label="Transactions", emoji="<a:transaction:1158419857138778142>", description="Transactions Commands"),
            discord.SelectOption(label="Leaderboard", emoji="<:leaderboard:1186917831657406484>", description="Leaderboard Commands"),
            discord.SelectOption(label="Miscellaneous", emoji="<:misc:1186928407548801055>", description="Miscellaneous Commands"),
            discord.SelectOption(label="Shop", emoji="<:shop:1187028991333380156>", description="Shop Commands"),
            discord.SelectOption(label="Waifu", emoji="<:waifu:1187029479726534668>", description="Waifu Commands"),
            discord.SelectOption(label="Configuration", emoji="<:settings:1186920164172763166>", description="Configuration Commands"),
            discord.SelectOption(label="Moderation", emoji="<:Moderator:1158420095136190506>", description="Moderation Commands"),
        ]
        super().__init__(placeholder="Select an Category", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # set the embed
        em = discord.Embed(title="Commands List", colour=discord.Colour.blue())
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_author(
            name="Help Command",
            icon_url=self.ctx.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tomgames")
        em.set_footer(
            text=f"Command ran by {self.ctx.author.display_name} at {timestamp}",
            icon_url=self.ctx.author.display_avatar.with_static_format("png"))

        if self.values[0] == "Core":
            # overwrite the embed
            em.description = "</github:1146802715511492670>: view the bots github repo\n</invite:1146802715511492668>: invite the bot to your server\n</ping:1145445177092231339>: show bot and API latency\n</support:1146802715511492669>: join the support server\n"
            em.title = "<a:core:1158418275559022674> Core Commands"
            await interaction.response.edit_message(embed=em)

        elif self.values[0] == "Currency":
            em.description = "</adventure:1146773955642937375>: go on an adventure\n</chop:1146110870632530063>: chop some wood\n</fish:1146100979532570694>: go fishing\n</mine:1146109054154977373>: go mining\n</daily:1145445177092231343>: get your daily free coins\n</weekly:1145445177092231344>: get your weekly free coins\n</work:1145445177092231345>: slave away for capitalism\n</challenge:1186691561174609980>: solve a daily challenge for a reward\n"
            em.title = "<:currency:1158418293879754833> Currency Commands"
            await interaction.response.edit_message(embed=em)

        elif self.values[0] == "Gambling":
            em.description = "</blackjack:1146852161481883779>: play blackjack\n</coinflip:1146775189732987011>: play coinflip\n</dice:1146842135736356886>: roll some dice\n</slots:1145445177092231340>: play slots\n</roulette:1146842135736356887>: play roulette\n</rps:1146842135736356884>: play rock paper scissors\n</rpsls:1146842135736356885>: play rock paper scissors lizard spock\n</highlow:1153770798050459838>: play a game of highlow\n</wheel:1146879853321269348>: spin the wheel of fortune\n</crime:1145445177092231346>: do some crime\n</rob:1145445177092231347>: rob someone\n</race start:1169321390407688223>: start a race\n</race enter:1169321390407688223>: join a race\n</race bet:1169321390407688223>: bet on a race and fuel your addiction\n"
            em.title = "<:Gambling:1158418665209864212> Gambling Commands"
            await interaction.response.edit_message(embed=em)

        elif self.values[0] == "Profile":
            em.description = "</avatar:1145798060560089088>: look at yours or somebody elses avatar\n</profile:1145445177092231342>: look at yours or somebody elses profile\n</rank:1155848810157850738>: generate yours or somebody elses rank card\n</bail:1145445177092231341>: release you or someone else from jail\n</stats:1186787637885939752>: see your bot usage stats\n</race stats:1169321390407688223>: your raceing stats\n"
            em.title = "<:Profile1:1158418933221695608> Profile Commands"
            await interaction.response.edit_message(embed=em)

        elif self.values[0] == "Inventory":
            em.description = "</inventory role view:1163486147650003065>: view your role inventory\n</inventory role toggle:1163486147650003065>: toggle a role from your inventory\n</inventory role give:1163486147650003065>: gift a role from your inventory\n</inventory items view:1163486147650003065>: view your items inventory\n</inventory items use:1163486147650003065>: use an item from your inventory\n</inventory items equip:1163486147650003065>: equip an item from you inventory\n</inventory gifts view:1163486147650003065>: view your gifts inventory\n</inventory gifts give:1163486147650003065>: give a gift from your inventory\n"
            em.title = "<:inventory:1187049990804213830> Inventory Commands"
            await interaction.response.edit_message(embed=em)

        elif self.values[0] == "Transactions":
            em.description = "</transactions balance:1145445177092231348>: check your balance\n</transactions pay:1145445177092231348>: pay someone money\n</transactions deposit:1145445177092231348>: deposit money into your bank\n</transactions depall:1145445177092231348>: deposit all your money into the bank\n</transactions withdraw:1145445177092231348>: withdraw money from your bank\n</transactions withall:1145445177092231348>: withdraw all your money from the bank\n"
            em.title = "<a:transaction:1158419857138778142> Transactions Commands"
            await interaction.response.edit_message(embed=em)

        elif self.values[0] == "Leaderboard":
            em.description = "</leaderboard summary:1145503523652517968>: the name kind of explains it, doesnt it\n</leaderboard level:1145503523652517968>: check the level leaderboard\n</leaderboard balance:1145503523652517968>: check the cash balance leaderboard\n</leaderboard bank:1145503523652517968>: check the bank balance leaderboard\n</leaderboard total:1145503523652517968>: check the total balance leaderboard\n</leaderboard waifu:1145503523652517968>: check the waifu leaderboard\n"
            em.title = "<:leaderboard:1186917831657406484> Leaderboard Commands"
            await interaction.response.edit_message(embed=em)

        elif self.values[0] == "Miscellaneous":
            em.description = "</urban:1163281362963410964>: search the urban dictionary\n</penis:1170469859113578586>: detects user's penis length, this is 100% accurate\n</ban_chart:1163145353994965032>: display a chart of the moderators with the most bans\n"
            em.title = "<:misc:1186928407548801055> Miscellaneous Commands"
            await interaction.response.edit_message(embed=em)

        elif self.values[0] == "Shop":
            em.description = "</shop gift buy:1158410919387336724>: buy a gift from the shop\n</shop gift list:1158410919387336724>: list all gifts in the shop\n</shop roles buy:1158410919387336724>: buy a role from the shop\n</shop roles list:1158410919387336724>: list all roles in the shop\n</shop items buy:1158410919387336724>: buy an item from the shop\n</shop items list:1158410919387336724>: list all items in the shop\n"
            em.title = "<:shop:1187028991333380156> Shop Commands"
            await interaction.response.edit_message(embed=em)

        elif self.values[0] == "Waifu":
            em.description = "</waifu claim:1163610274251690014>: claim a waifu\n</waifu divorce:1163610274251690014>: divorce a waifu\n</waifu info:1163610274251690014>: get info about a waifu\n</waifu set_affinity:1163610274251690014>: set your affinity\n"
            em.title = "<:waifu:1187029479726534668> Waifu Commands"
            await interaction.response.edit_message(embed=em)

        elif self.values[0] == "Configuration":
            em.description = "</settings lvlroles add:1163163800841748536>: add level roles\n</settings lvlroles remove:1163163800841748536>: remove level roles\n</settings lvlroles list:1163163800841748536>: list the current level roles\n</settings lvl_up_channel set_lvl_channel:1163163800841748536>: set a level up channel\n</settings lvl_up_channel remove_lvl_channel:1163163800841748536>: remove the level up channel\n</settings lvl_up_channel view_lvl_channel:1163163800841748536>: view which channel is set as the level up channel\n</settings bonus_roles add:1163163800841748536>: add a bonus role\n</settings bonus_roles remove:1163163800841748536>: remove a bonus role\n</settings bonus_roles list:1163163800841748536>: list all bonus roles\n</settings bonus_cash_roles add_cash_role:1163163800841748536>: add a role to cash roles\n</settings bonus_cash_roles remove_cash_role:1163163800841748536>: remove a role to cash roles\n</settings bonus_cash_roles list_cash_roles:1163163800841748536>: list all cash roles\n</settings shop_admin add_gift:1163163800841748536>: add a gift item to the shop\n</settings shop_admin remove_gift:1163163800841748536>: remove a gift item from the shop\n</settings shop_admin add_role:1163163800841748536>: add a role item to the shop\n</settings shop_admin remove_role:1163163800841748536>: remove a role item from the shop\n</settings shop_admin list_gifts:1163163800841748536>: list all gift items in the shop\n</settings shop_admin list_roles:1163163800841748536>: list all role items in the shop\n</settings text_reactions add:1163163800841748536>: add a text reaction\n</settings text_reactions remove:1163163800841748536>: remove a text reaction\n</settings text_reactions list:1163163800841748536>: list all text reactions\n</settings pings add:1163163800841748536>: add a ping role\n</settings pings remove:1163163800841748536>: remove a ping role\n</settings pings list:1163163800841748536>: list all ping roles\n"
            em.title = "<:settings:1186920164172763166> Configuration Commands"
            await interaction.response.edit_message(embed=em)

        elif self.values[0] == "Moderation":
            em.description = "</pings:1168982695464927403>: role pings\n</massnick start:1154508740482052186>: run a massnick\n</massnick cancel:1154508740482052186>: cancel your currently running massnick\n</massnick reset:1154508740482052186>: clear a massnick and reset everyones names\n</idiot set:1155875939079700581>: set an idiots nickname\n</idiot clear:1155875939079700581>: clear an idiots nickname\n</idiot list:1155875939079700581>: list all idiots\n</idiot check:1155875939079700581>: check if a user is an idiot\n</ratio:1155206383986298900>: check the ratio of nsfw to sfw channels\n</new_ticket:1156219459011358750>: create a new ticket\n</new_verify:1170458219353751582>: create a new verification ticket\n</kick:1158392520284327937>: kick a user from the server\n</ban:1158392520284327938>: ban a user from the server\n</purge:1158392520284327936>: purge messages from a channel\n"
            em.title = "<:Moderator:1158420095136190506> Moderation Commands"
            await interaction.response.edit_message(embed=em)


class HelpView(discord.ui.View):
    def __init__(self, ctx, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(Help(ctx=ctx))
