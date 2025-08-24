from typing import List, Callable, Any, Dict
from interactions import ActionRow, Button, ButtonStyle
from classes.embed import Embed
from utils.registry import registry, InteractionResponse

@registry.command("ping", "Check latency")
async def ping(bot, interaction):
    return InteractionResponse(content="🏓 Pong!", ephemeral=True).to_dict()

@registry.command("hello", "Say hello")
async def hello(bot, interaction):
    user = interaction["member"]["user"]["username"]
    embed = Embed("Hello!", f"👋 Hey {user}, nice to meet you.")

    button = Button(
        style=ButtonStyle.SUCCESS,
        label="Click Me",
        custom_id="hello_button"
    )
    row = ActionRow(button) 

    return InteractionResponse(
        embeds=[embed],
        components=[row],
    ).to_dict()

@registry.component("hello_button")
async def hello_button(bot, interaction):
    return InteractionResponse(
        content="👋 You clicked Hello!",
        ephemeral=True
    ).to_dict()
