"""Self-created exceptions"""

class ParticipantExistsException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    async def send_message(self, ctx):
        await ctx.send("Participant already exists.")

class ParticipantDoesntExistException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    async def send_message(self, ctx):
        await ctx.send("Participant doesn't exist.")

class CompetitionInactiveException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    async def send_message(self, ctx):
        await ctx.send("Competition is concluded. No modifications can be made.")
