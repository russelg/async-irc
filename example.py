import asyncio
import bottom
from dispatcher import Dispatcher, connector, cooldown

host = 'chat.freenode.net'
port = 6697
ssl = True

NICK = "russel-test"
CHANNEL = ["#pigbenis", "#fuccboi"]
PASSWORD = None

loop = asyncio.get_event_loop()
loop.set_debug(True)

# create the irc client
bot = bottom.Client(host=host, port=port, ssl=ssl, loop=loop)


async def autoupdate_or_some_shit():
    await bot.wait("client_connect")
    while not bot.protocol.closed:
        # bot.send("privmsg", target=CHANNEL, message="sent this test message")
        await asyncio.sleep(3, loop=bot.loop)


# this is the command dispatcher
class IrcBot(Dispatcher):
    # nick, message and channel are always supplied
    # command and args come from the regex named capture groups
    # (in this case: r'^!(?P<command>.*?)\s(?P<args>.*)')
    @cooldown(5)
    def command(self, nick, message, channel, command, args):
        # return 'Command: %s, arguments: %s' % (command, args)
        self.respond('Command: %s, arguments: %s' % (command, args), channel=channel)

    def command_patterns(self):
        return (
            (r'^!(?P<command>.*?)\s(?P<args>.*)', self.command),
        )

# this creates the dispatcher for use in the connector
dispatcher = IrcBot(bot)

# this handles what to do on connection, and
# handles commands for the dispatcher
connector(bot, dispatcher, NICK, CHANNEL, PASSWORD)

# creates the async task and run forever
# bot.loop.create_task(autoupdate_or_some_shit())
bot.loop.create_task(bot.connect())
bot.loop.run_forever()
