from dotenv import load_dotenv
from telethon.sync import TelegramClient, events
import os
import json
import asyncio

# Consigue la lista de grupos donde la cuenta está unida y lo retorna en un array
async def getListOfGroups(client):
    try:
        dialogs = await client.get_dialogs()
        groups_info = []
        for dialog in dialogs:
            if dialog.is_group or dialog.is_channel:
                entity = await client.get_entity(dialog.id)
                can_send_messages = entity.default_banned_rights is None or not entity.default_banned_rights.send_messages
                if can_send_messages:
                    group_info = {'group_id': dialog.id, 'group_name': dialog.title}
                    groups_info.append(group_info)

        return groups_info
    except Exception as e:
        print(e)
        return []
    
# Consigue la lista de mensajes a mandar
async def getMessagesFromGroup(client, group_id):
    try:
        all_messages = []
        async for message in client.iter_messages(group_id):
            # Verificar que el mensaje tenga texto o contenido multimedia
            if message.message or message.media:
                all_messages.append(message)
        return all_messages
    except Exception as e:
        print(f"Error obteniendo mensajes del grupo: {e}")
        return []



# Esto es para iniciar sesión del bot y manejar el spam
async def logUserBot():
    load_dotenv()
    api_id = int(29241873)
    api_hash = "73de6718cfc27e5665dfe05d336e2005"
    phone_number = "51990883049"
    session_name = "bot_spammer"
    client = TelegramClient(session_name, api_id, api_hash)
    await client.connect()
    
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        await client.sign_in(phone_number, input('Ingrese el código de verificación: '))
        
    await client.send_message("@VentasStreamingSpam", f'<b>Bot encendido</b>', parse_mode="HTML")
    
    # Detectar mensajes entrantes y responder automáticamente solo en chats privados
    @client.on(events.NewMessage(incoming=True))
    async def handler(event):
        sender = await event.get_sender()
        # Verificar si el mensaje viene de un chat privado
        if event.is_private and sender.bot is False:  # Asegurarse de que no sea un bot ni un grupo
            await client.send_message(sender.id, 
                                      "Hola, soy bot oficial de Spam de @VENTAS_STREAMING2 escribeme y te atendere al instante.\n@VENTAS_STREAMING2")
    
    spammer_group = int("-4678965284")

    while True:
        groups_info = await getListOfGroups(client)
        messages_list = await getMessagesFromGroup(client, spammer_group)
        
        try:
            await client.send_message("@VentasStreamingSpam", f"<b>CANTIDAD DE MENSAJES CONSEGUIDOS PARA PUBLICAR</b> <code>{len(messages_list)-1}</code>", parse_mode="HTML")
        except:
            pass
        
        try:
            for i in groups_info:
                if i['group_name'] not in ["Spam 2024", "RESPALDO🇵🇪BINS PERU", "➳𝒀𝑨𝑷𝑬 𝑫𝑬 𝑬𝑺𝑻𝑨𝑭𝑨𝑫𝑶𝑹𝑬𝑺 ✧", "QUEMANDO ESTAFADORES", "𝐏𝐄𝐑Ú 𝐀𝐘𝐔𝐃𝐀", "Referencias Elmer 💸", "🎭 CANAL MUNDO STREAMING PERÚ 🇵🇪", "TU MARKETPLACE", "⚫️𝙈𝙀𝙍𝘾𝘼𝘿𝙊 𝙉𝙀𝙂𝙍𝙊⚫️", "💻 BLAK PERU OFC COMUNITY 💻", "🇵🇪PRIMITOS BINS PERU🇵🇪"]:
                    j = 0
                    for message_spam in messages_list:
                        j += 1
                        try:
                            # Intentar enviar el mensaje completo (texto y multimedia)
                            await client.forward_messages(i["group_id"], message_spam)
                            await client.send_message("@VentasStreamingSpam", f'<b>Mensaje enviado a {i["group_id"]}</b> - <code>{i["group_name"]}</code>', parse_mode="HTML")
                        except Exception as error:
                            if "CHAT_SEND_PHOTOS_FORBIDDEN" in str(error):
                                # Si el grupo no permite multimedia, enviar solo el texto del mensaje
                                try:
                                    if message_spam.text:  # Verifica si el mensaje tiene texto
                                        await client.send_message(i["group_id"], message_spam.text)
                                        await client.send_message("@VentasStreamingSpam", f'<b>Multimedia no permitido en {i["group_name"]}. Se envió solo texto.</b>', parse_mode="HTML")
                                    else:
                                        await client.send_message("@VentasStreamingSpam", f'<b>No se pudo enviar a {i["group_name"]}: el mensaje no tiene texto válido.</b>', parse_mode="HTML")
                                except Exception as inner_error:
                                    await client.send_message("@VentasStreamingSpam", f'<b>Error enviando texto a {i["group_name"]}: {inner_error}</b>', parse_mode="HTML")
                            else:
                                # Manejar cualquier otro error
                                await client.send_message("@VentasStreamingSpam", f'<b>Error enviando a {i["group_name"]}: {error}</b>', parse_mode="HTML")

                        await asyncio.sleep(10)
                        if j == 3: break
            await client.send_message("@VentasStreamingSpam", f'<b>RONDA ACABADA</b>', parse_mode="HTML")
            await asyncio.sleep(600) 
        except:
            pass

if __name__ == "__main__":
    asyncio.run(logUserBot())
