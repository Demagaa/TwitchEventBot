import os
import telebot
import hashlib
import hmac
import json
import twitchio
from flask import Flask, request, jsonify
import secrets
import twitchio

from twitchio.ext import commands, eventsub

esbot = commands.Bot.from_client_credentials(client_id='...',
                                             client_secret='...')
esclient = eventsub.EventSubClient(esbot,
                                   webhook_secret='...',
                                   callback_route='https://your-url.here/callback')
stream_id = 1

broadcaster = {'broadcaster_user_id' : 106166322,
               'broadcaster_user_name' : 'Stubborn51',
               'id' : stream_id,
               'type' : '1',
               'started_at' : ''}
class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token='...', prefix='!', initial_channels=['channel'])

    async def __ainit__(self) -> None:
        self.loop.create_task(esclient.listen(port=4000))

        try:
            await esclient.subscribe_channel_stream_start(broadcaster=106166322)
        except twitchio.HTTPException:
            pass

    async def event_ready(self):
        print('Bot is ready!')


bot = Bot()
bot.loop.run_until_complete(bot.__ainit__())


@esbot.event()
async def event_notification_stream_start(payload: eventsub.StreamOnlineData) -> None:
    print('Received event!')
    channel = bot.get_channel('channel')
    await channel.send(f'{payload.data.user.name} started stream woohoo!')

bot.run()