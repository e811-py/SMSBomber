from telethon.sync import TelegramClient, events, connection
from telethon.utils import resolve_inline_message_id
from time import sleep

api_id = 1520270
api_hash = "82bd7b4562a5cd24d182bdc39b2d9352"
admin = '820586182'
botId = 'vote'

# client = TelegramClient('Hadis', api_id, api_hash)
client = TelegramClient('VoteMaker', api_id, api_hash, connection=connection.ConnectionTcpMTProxyRandomizedIntermediate, proxy=('51.195.19.124', 8115, '65ea861534b172aa143ce1ee6fff257a'))


with client:
	# idd = client.get_messages('vote', 1)[0].id
	# print(client(resolve_inline_message_id(idd)))
	# client.send_message('e811_py', 'testButtons', buttons=[[Button.inline('left'), Button.inline('right')]])
	@client.on(events.NewMessage())
	async def handler(event):
		if bool(event.mentioned):
			print('okiff')
			print(event)
			if str(event.from_id.user_id) == admin:
				print('\n\nokifs')
				# print(event)
				count = int(str(event.message.message).split('@VoteMaker ')[1])
				group_id = int(event.original_update.message.peer_id.channel_id)
				#print(group_id,' ',count)
				for co in range(count):
					co+=1
					text = f'سوال{co}'
					await client.send_message(botId, '/start')
					sleep(1)
					await client.send_message(botId, 'Public')
					sleep(1)
					await client.send_message(botId, text)
					sleep(1)
					await client.send_message(botId, 'گزینه 1')
					sleep(1)
					await client.send_message(botId, 'گزینه 2')
					sleep(1)
					await client.send_message(botId, 'گزینه 3')
					sleep(1)
					await client.send_message(botId, 'گزینه 4')
					sleep(1)
					await client.send_message(botId, '/done')
					sleep(1)
					mes = await client.get_messages(botId, 1)
					res = await client.inline_query("@Vote", text)
					messs = await res[0].click(event.to_id)

	client.run_until_disconnected()

