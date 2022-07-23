debug_enabled = False

async def msg(ctx, message, override=False):
    print(message)
    if debug_enabled or override:
        await ctx.send(message)