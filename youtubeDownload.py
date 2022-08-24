from telegram import ChatAction, Update
from telegram.ext import Updater, MessageHandler,Filters,CallbackContext,CommandHandler
from pytube import YouTube, exceptions
import os

TOKEN = '5618202461:AAEoa7ntmzoD0DbF7bNA4xQ72Agt-zLIzBw'

#Handlers
def startf(update: Update,context: CallbackContext):
    update.message.reply_text("Bienvenido, este bot puede ser utilizado para descargar videos y audio de youtube. Para mas información /help")

def helpf(update: Update,context: CallbackContext):
    update.message.reply_text("Utilice /mp4 [link] para descargar video.\nUtilice /mp3 [link] para descargar audio.")

def video(update: Update,context: CallbackContext):
    try:
        if len(context.args) != 1:
            update.message.reply_text("Perdona no veo claro el link")
        else:
            url = context.args[0]
            update.message.reply_chat_action(ChatAction.RECORD_VIDEO)
            yt = YouTube(str(url))
            out_file = yt.streams.get_highest_resolution().download('./')

            base,ext = os.path.splitext(out_file)
            update.message.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            update.message.reply_video(open(out_file,'rb'), caption='Tu video')
            os.remove(out_file)
    except exceptions.RegexMatchError:
        update.message.reply_text("Perdona no veo claro el link")
        

def audio(update: Update,context: CallbackContext):
    try: 
        if len(context.args) != 1:
            update.message.reply_text("Perdona no veo claro el link")
        else:
            url = context.args[0]
            update.message.reply_chat_action(ChatAction.RECORD_AUDIO)
            yt = YouTube(str(url))
            vid = yt.streams.filter(only_audio=True).first()
            out_file = vid.download(output_path='./')

            base,ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            #print(out_file)
            #print(new_file)
            os.rename(out_file,new_file)
            update.message.reply_chat_action(ChatAction.UPLOAD_AUDIO)
            update.message.reply_audio(open(new_file,'rb'), caption='Tu audio')
            os.remove(new_file)
    except exceptions.RegexMatchError:
        update.message.reply_text("Perdona no veo claro el link")


def run():
    
    updater = Updater(TOKEN)

    #Este es el que maneja eventos
    dispatcher = updater.dispatcher

    #Creando manejadores
    dispatcher.add_handler(CommandHandler("start",startf))
    dispatcher.add_handler(CommandHandler("help",helpf))
    dispatcher.add_handler(CommandHandler("mp4",video))
    dispatcher.add_handler(CommandHandler("mp3",audio))

    #Inicio del bot
    updater.start_polling()

    #Mantener el bot corriendo
    updater.idle()

if __name__=='__main__':
    run()