import asyncio

from loguru import logger

from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from Uprove_TG_Bot.TG_bot.setup import user_router
from Uprove_TG_Bot.TG_bot.src.telegram.buttons.user_btn import main_btn
from Uprove_TG_Bot.TG_bot.src.telegram.messages.user_msg import MESSAGES
from Uprove_TG_Bot.TG_bot.work_PROCESS import run_process_and_reply_after, RunBotStates, StructData


@user_router.message(F.text == MESSAGES['btn_reset'])
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.reply(MESSAGES['reset_msg'], reply_markup=main_btn)


@user_router.message(RunBotStates.reddit_link)
async def answer_link(message: Message, state: FSMContext):
    await state.set_state(RunBotStates.upvote_int)
    await state.update_data(reddit_link=message.text)

    await message.reply(MESSAGES['upvote_int'])


@user_router.message(RunBotStates.upvote_int)
async def answer_vote(message: Message, state: FSMContext):
    try:
        await state.update_data(upvote_int=int(message.text))
    except ValueError:
        await state.clear()
        await message.reply(MESSAGES['error_vote_int'],
                            reply_markup=main_btn)
        return

    data = await state.get_data()
    struct_data = StructData(**data)

    logger.info(struct_data.reddit_link)
    logger.info(struct_data.upvote_int)

    run_process = asyncio.create_task(run_process_and_reply_after(message, struct_data))

    await state.clear()
    await message.answer(str(MESSAGES['notif_browser_run'] + data["reddit_link"]), reply_markup=main_btn)

    await run_process



# @user_router.message(RunBotStates.upvote_int)
# async def answer_vote(message: Message, state: FSMContext):
#     try:
#         await state.update_data(upvote_int=int(message.text))
#         await state.set_state(RunBotStates.comments_int)
#         await message.reply(MESSAGES['comments_int'])
#     except ValueError:
#         await state.clear()
#         await message.reply(MESSAGES['error_vote_int'],
#                             reply_markup=main_btn)
#
#
# # catch user's upvote integer
# @user_router.message(RunBotStates.comments_int)
# async def answer_comment(message: Message, state: FSMContext):
#     try:
#         await state.update_data(comments_int=int(message.text))
#     except ValueError:
#         await state.clear()
#         await message.reply(MESSAGES['error_comments_int'],
#                             reply_markup=main_btn)
#         return
#
#     data = await state.get_data()
#     struct_data = StructData(**data)
#
#     logger.info(struct_data.reddit_link)
#     logger.info(struct_data.upvote_int)
#     logger.info(struct_data.comments_int)
#
#     run_process = asyncio.create_task(run_process_and_reply_after(message, struct_data))
#
#     await state.clear()
#     await message.answer(
#         f'Браузер запустився для опрацювання вашого посилання {data["reddit_link"]}.', reply_markup=main_btn
#     )
#
#     await run_process
