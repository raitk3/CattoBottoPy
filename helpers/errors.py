"""Self-created exceptions"""


class CompetitionInactiveException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    async def send_message(self, ctx):
        await ctx.send("Competition is concluded. No modifications can be made.", ephemeral=True)

class NotAHostException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    async def send_message(self, ctx):
        await ctx.send("You are not a host, sorry.", ephemeral=True)

class NotAModException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    async def send_message(self, ctx):
        await ctx.send("You are not a mod, sorry.", ephemeral=True)

class UnsupportedCompetitionTypeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    async def send_message(self, ctx):
        await ctx.send("Current competition type doesn't support this command, sorry.", ephemeral=True)

class InvalidValueException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    async def send_message(self, ctx):
        await ctx.send("The value you entered is invalid, sorry.", ephemeral=True)