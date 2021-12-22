## C Y B Ξ R Assistant Modules

## Example plugin for C Y B Ξ R Assistant.

```python
from telethon import events
from . import tgbot
# <-- Let's note the imports

@tgbot.on(events.NewMessage(pattern="^/example_command"))
async def example(event):
    await tgbot.send_message(event.chat_id, "C Y B Ξ R is working..")

```

### All rights reserved