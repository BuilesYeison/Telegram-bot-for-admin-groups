import os
import logging #report bot events   
import telegram
import sys
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
#Updater, receive messages from telegram to process that

#configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s," 
)
logger = logging.getLogger()

welcomeMessage = '\n\n[Establece un mensaje de bienvenida con el comando /changeMsg nuevo mensaje de bienvenida y será reemplazado aqui]'
rudeList = ['imbecil', 'Imbecil', 'Ignorante', 'ignorante', 'baboso', 'Baboso', 'Estupido', 'estupido', 'gay', 'Gay'
            ,'hpta', 'HPTA'
            ]

eventos = 'Eventos: \nAgéndate en este enlace: https://app.interacpedia.com/mass-events'

#agregar comando de eventos para que los administradores, agreguen los eventos disponibles con sus fechas y horarios
#datos como: el clima, noticias de tecnologia, o alguna informacion relevante

#request TOKEN
#this bot will be on the net and heroku, so for security, the token of the bot should be hidden 
#in the environment variable
TOKEN = os.getenv("TOKEN") #create an environment variable. pwershell = $env:TOKEN="token code", cmd = set TOKEN=token code
MODE = os.getenv('MODE') #for know if is running in cmd or in web heroku

if MODE == 'dev':#is running in cmd
    def run(updater):
        updater.start_polling()#constantly ask if there are messages
        print("BOT RUNNING")
        updater.idle()
elif MODE == 'prod': #is running on web, heroku
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443")) #assign a port for bot execution
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0", port= PORT, url_path=TOKEN)
        updater.bot.set_webhook(f'https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}')
else:
    logger.info('No se especificó el modo de ejecucion del bot')
    sys.exit()


def userisAdmin(bot, userId, chatId): #method for find and get the chat admins, identify if the new user is an admin
    try:
        groupAdmins = bot.get_chat_administrators(chatId)
    except Exception as e:
        print(e)

    isAdmin = False
    for admin in groupAdmins:
        if admin.user.id == userId:
            isAdmin = True
    
    return isAdmin

def changeMsg(update, context): #change default welcome message
    # ''' /changeMsg nuevo mensaje de bienvenida '''
    bot = context.bot
    args = context.args #get extra info from the command
    user_id = update.effective_user['id'] #get user id
    userName = update.effective_user['first_name'] #
    groupId = update.message.chat_id 
    global welcomeMessage

    if userisAdmin(bot, user_id, groupId) == True: #if the user that sent command is an admin
        if len(args) == 0: #if there is not extra info in command
            logger.info(f'{userName} no ha establecido correctamente un Mensaje de bienvenida')
            bot.sendMessage(
                chat_id=groupId,
                text=f'{userName}, no has establecido ningun mensaje, intentalo de nuevo por ej: /changeMsg este es un nuevo mensaje de bienvenida'
            )
        else: #there is extra info
            welcomeMessage = " ".join(args) #get all exra info and set in var
            welcomeMessage = "\n" + welcomeMessage   #change welcome message 
            bot.sendMessage(
                chat_id=groupId,
                text=f'Mensaje de bienvenida cambiado correctamente'
            )
    else: #is not admin
        logger.info(f'{userName} ha intentado cambiar el mensaje de bienvenida, pero no tiene permisos')    
        bot.sendMessage(
            chat_id=groupId,
            text=f'{userName}, no tienes permiso para cambiar el mensaje de bienvenida.'
        )

def addEvent(update, context):
    bot = context.bot
    global eventos
    args = context.args #get extra info from command sent
    groupId = update.message.chat_id
    user_id = update.effective_user['id']
    userName = update.effective_user['first_name']

    if userisAdmin(bot, user_id, groupId) == True: #user that sent command is admin
        if len(args) == 0: #there is not extra info: event
            logger.info(f'{userName} no ha establecido ningun evento')
            bot.sendMessage(
                chat_id=groupId,
                text=f'{userName} no has establecido ningun evento, ejemplo: /addEvent este es un evento de prueba'
            )
        else: #there is info
            evento = ' '.join(args)#create string with complete event
            eventos = eventos + "\n\n>> " + evento #add event to events            
            
            bot.sendMessage(
                chat_id=groupId,
                text=f'{userName} has establecido el evento correctamente'
            )
    else: #user that sent command is not admin
        logger.info(f'El usuario {userName} ha intentado agregar un evento pero no es admin')
        bot.sendMessage(
            chat_id=groupId,
            text=f'{userName} lo siento, pero no tienes permiso para realizar está accion'
        )

def getEvents(update, context): #send message to chat with events added
    bot = context.bot
    groupId = update.message.chat_id
    userName = update.effective_user['first_name']
    logger.info(f'El usuario {userName} ha solicitado los eventos')
    bot.sendMessage(
        chat_id=groupId,
        text= eventos
    )

def clearEvents(update, context):
    bot = context.bot
    userName = update.effective_user['first_name']
    user_id = update.effective_user['id']
    groupId = update.message.chat_id    
    global eventos

    if userisAdmin(bot, user_id, groupId) == True:
        eventos = 'Eventos: \nAgéndate en este enlace: https://app.interacpedia.com/mass-events'
        logger.info(f'El usuario {userName} ha eliminado los eventos')
        bot.sendMessage(
            chat_id=groupId,
            text=f'{userName} has eliminado los eventos existentes correctamente'
        )
    else:
        logger.info(f'El usuario {userName} ha intentado eliminar los eventos pero no es admin')
        bot.sendMessage(
            chat_id=groupId,
            text=f'Lo siento {userName} pero no tienes permisos para eliminar los eventos'
        )
    

def deleteMessage(bot, chatId, messageId, userName): #delete messages
    try:
        bot.delete_message(chatId, messageId)
        logger.info(f'El mensaje de {userName} ha sido eliminado porque tenia palabras ofensivas')
    except Exception as e:
        print(e)

def echo(update, context):
    #print(update)
    bot = context.bot
    update_msg = getattr(update, "message", None) #get info of message
    msg_id = update_msg.message_id #get recently message id
    groupId = update.message.chat_id
    userName = update.effective_user['first_name']
    user_id = update.effective_user['id'] #get user id
    logger.info(f"El usuario {userName}, ha enviado un mensaje de texto.")
    text = update.message.text #get message sent to the bot    

    if 'conquistar el mundo' in text and 'TecDataBot' in text:        
        bot.sendMessage( #send message to telegram chat
        chat_id=groupId,
        parse_mode="HTML",
        text = f'Claro que si {userName}, ese es el objetivo con el que mi creador me trajo al mundo muajajajaja'
        )
    elif 'TecDataBot' in text and 'buena suerte' in text:
        bot.sendMessage(
            chat_id=groupId,
            text= f'Muchas Gracias {userName}, aunque creo que no la necesito!!!'
        )
    else:
        for rude in rudeList: #delete message if there is bad word there
            if rude in str(text):
                deleteMessage(bot, groupId, msg_id, userName)
                bot.sendMessage(
                    chat_id=groupId,
                    parse_mode="HTML",
                    text = f'El mensaje de <b>{userName}</b> ha sido eliminado porque tenia palabras ofensivas o caracteres desconocidos.'
            )    
        
def botInfo(update, context): #get group id
    bot = context.bot
    groupId = update.message.chat_id
    logger.info(f"Obteniendo info del bot {groupId}")
    bot.sendMessage(chat_id=groupId, 
    parse_mode= "HTML", 
    text=f'<b>¡¡Hola, mi nombre es TecDataBot!!</b>\n\nDoy la bienvenida a nuevos usuarios que entran a nuestra comunidad, comunico eventos y elimino mensajes con lenguaje inapropiado. Estas son mis funcionalidades:\n\n<b>Comandos si eres administrador:</b>\n<b>1.</b> /changeMsg para cambio de mensaje bienvenida.\n<b>2.</b> /addEvent para agregar eventos próximos.\n<b>3.</b> /clearEvents para borrar eventos.\n\n<b>Comandos si eres miembro:</b>\n<b>1.</b> /events para visualizar eventos.\n<b>2.</b> /TecDataInfo para ver mi información'
    )

def newUsers(update, context):
    #print(update)
    groupId = update.message.chat_id #get group id
    update_msg = getattr(update, "message", None) #get all attributes of json message update
    for user in update_msg.new_chat_members:#get userName of new Member
        userName=user.first_name    

    logger.info(f"Se ha unido un nuevo miembro: {userName}")

    context.bot.sendMessage(chat_id=groupId,
        parse_mode="HTML",
        text=f"<b>¡Bienvenid@ a la comunidad de Tecnología y Data {userName}!</b>. {welcomeMessage}")

if __name__ == "__main__":
    #obtain bot info
    myBot = telegram.Bot(token= TOKEN)       
    #print(myBot.getMe())

#connect Updater with our bot
updater = Updater(myBot.token, use_context=True)

#create a receive and transmit info, dispatcher
dp = updater.dispatcher

#create handler
dp.add_handler(CommandHandler("TecDataInfo", botInfo))
dp.add_handler(CommandHandler("events", getEvents))
dp.add_handler(CommandHandler("clearEvents", clearEvents))
dp.add_handler(CommandHandler("changeMsg", changeMsg, pass_args=True))
dp.add_handler(CommandHandler("addEvent", addEvent, pass_args=True))
dp.add_handler(MessageHandler(Filters.text, echo)) #waiting for text input in chat
dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, newUsers)) #getting new members

run(updater)