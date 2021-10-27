import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

FIO, AGE, CITY, PHONE, EMAIL, EDUCATION, KNOWLEDGE, EXPERIENCE, LINK, DAY, SOURCE, INCOME = range(12)

f = True

def start(update: Update, context: CallbackContext) -> int:

    user = update.message.from_user
    update.message.reply_text(
        'Здравствуйте, ответьте на несколько вопросов для рассмотрение Вас на должность дизайнера.:\n'
        'Нажмите /cancel, чтобы перестать общаться со мной'
    )

    update.message.reply_text('Укажите ФИО:')

    return FIO


def fio(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("ФИО: %s", update.message.text)
    update.message.reply_text('Укажите возраст:')

    return AGE


def age(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Возраст: %s", update.message.text)
    if int(update.message.text) > 70:
        global f
        f = False
    update.message.reply_text('Укажите город проживания:')

    return CITY


def city(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Город проживания: %s", update.message.text)
    update.message.reply_text('Укажите номер телефона:')
    return PHONE


def phone(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Номер телефона: %s", update.message.text)
    update.message.reply_text('Укажите Email:')
    return EMAIL


def email(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Электронная почта: %s", update.message.text)

    reply_keyboard = [['Да', 'Нет']]

    update.message.reply_text(
            'Есть ли у вас образование в сфере дизайна?',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Да или Нет?'
            ),
        )
    return EDUCATION


def education(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Образовние дизайна: %s", update.message.text)
    if update.message.text == 'Нет':
        global f
        f = False
    reply_keyboard = [['Да', 'Нет']]

    update.message.reply_text(
            'Умеете ли вы работать в Adobe Illustrator и Photoshop?',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Да или Нет?'
            ),
        )
    return KNOWLEDGE


def knowledge(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Навыки программ: %s", update.message.text)
    if update.message.text == 'Нет':
        global f
        f = False
    update.message.reply_text('Укажите стаж работы дизайнером:')
    return EXPERIENCE


def experience(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Стаж работы: %s", update.message.text)
    if int(update.message.text) < 12:
        global f
        f = False
    update.message.reply_text('Прикрепите ссылку на портфолио:')
    return LINK


def link(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Ссылка на портфолио: %s", update.message.text)
    reply_keyboard = [['Да', 'Нет']]

    update.message.reply_text(
            'Готовы ли вы к работе на полную занятость в нашей компании, 5-8ч/день?',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Да или Нет?'
            ),
        )

    return DAY


def day(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Полная занятость: %s", update.message.text)
    if update.message.text == 'Нет':
        global f
        f = False
    update.message.reply_text('Укажите предпочитаемый уровень зарплаты:')
    return SOURCE


def source(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Предпочитаемый уровень зарплаты: %s", update.message.text)
    if int(update.message.text) > 70000:
        global f
        f = False
    update.message.reply_text('Спасибо! Ответы обрабатываются')
    if f:
        update.message.reply_text('Скоро с вами свяжутся для назначения времени собеседования!')
    else:
        update.message.reply_text('К сожалению, вы нам не подходите')
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("2092638762:AAG6Q1Ecc6xe3tB2FMa7jAR69Ictw8LgzUI")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIO: [MessageHandler(Filters.text & ~Filters.command, fio)],
            AGE: [MessageHandler(Filters.text & ~Filters.command, age)],
            CITY: [MessageHandler(Filters.text & ~Filters.command, city)],
            PHONE: [MessageHandler(Filters.text & ~Filters.command, phone)],
            EMAIL: [MessageHandler(Filters.text & ~Filters.command, email)],
            EDUCATION: [MessageHandler(Filters.regex('^(Да|Нет)$'), education)],
            KNOWLEDGE: [MessageHandler(Filters.regex('^(Да|Нет)$'), knowledge)],
            EXPERIENCE: [MessageHandler(Filters.text & ~Filters.command, experience)],
            LINK: [MessageHandler(Filters.text & ~Filters.command, link)],
            DAY: [MessageHandler(Filters.regex('^(Да|Нет)$'), day)],
            SOURCE: [MessageHandler(Filters.text & ~Filters.command, source)],
            INCOME: [MessageHandler(Filters.text & ~Filters.command, income)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()