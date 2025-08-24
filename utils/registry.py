from typing import List, Callable, Any, Dict
from interactions import ActionRow, Button, ButtonStyle
from classes.embed import Embed

class Registry:
    def __init__(self):
        self.commands = {} 
        self.components = {}

    def command(self, name, description="No description", options=None):
        def decorator(func):
            self.commands[name] = {
                "callback": func,
                "description": description,
                "options": options or []
            }
            return func
        return decorator

    def to_payload(self):
        return [
            {
                "name": name,
                "description": meta["description"],
                "type": 1,  # CHAT_INPUT
                "options": meta["options"]
            }
            for name, meta in self.commands.items()
        ]

    def component(self, custom_id):
        def decorator(func):
            self.components[custom_id] = func
            return func
        return decorator

    async def dispatch(self, bot, data):
        interaction_type = data.get("type")
        d = data.get("data", {})
        
        if interaction_type == 2:  # Application Command
            name = d.get("name")
            cmd = self.commands.get(name)
            if cmd:
                return await cmd["callback"](bot, data)
                
        elif interaction_type == 3:  # Message Component
            custom_id = d.get("custom_id")
            cb = self.components.get(custom_id)
            if cb:
                return await cb(bot, data)
        
        # Default response for unknown interactions
        return {
            "type": 4,
            "data": {"content": "Unknown interaction.", "flags": 64},
        }

class InteractionResponse:
    def __init__(
        self,
        content: str = None,
        embeds: List[Embed] = None,
        components: List[ActionRow] = None,
        ephemeral: bool = False,
        type_: int = 4,  # CHANNEL_MESSAGE_WITH_SOURCE
    ):
        self.type = type_
        self.content = content
        self.embeds = embeds or []
        self.components = components or []
        self.ephemeral = ephemeral

    def to_dict(self):
        data = {}
        if self.content:
            data["content"] = self.content
        if self.embeds:
            data["embeds"] = [e.to_dict() for e in self.embeds]
        if self.components:
            data["components"] = [c.to_dict() for c in self.components]
        if self.ephemeral:
            data["flags"] = 64
        return {"type": self.type, "data": data}

registry = Registry()

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