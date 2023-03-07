
# from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
# from SETTINGS import tuple_admins_id
#
#
# # Это пример реализации класса, который может управлять доступом к боту
# class AccessManager:
#     def __init__(self):
#         self.allowed_users = set()
#
#     def allow_user(self, user_id):
#         self.allowed_users.add(user_id)
#
#     def deny_user(self, user_id):
#         self.allowed_users.remove(user_id)
#
#     def user_allowed(self, user_id):
#         return user_id in self.allowed_users
#
#
# class AccessMiddleware(LifetimeControllerMiddleware):
#     def __init__(self, access_manager):
#         super().__init__()
#         self.access_manager = access_manager
#
#     async def on_pre_process_message(self, message, data):
#         user_id = message.from_user.id
#         if not self.access_manager.user_allowed(user_id):
#             await message.answer("Вы не авторизованы для выполнения этой команды!")
#             return False
#         return True
#
#     access_manager = AccessManager()
#     access_manager.allow_user(tuple_admins_id)
#
#     # Создаем объект Dispatcher и добавляем middleware
#     from aiogram import Bot, Dispatcher, types
#     from aiogram.contrib.fsm_storage.memory import MemoryStorage
#
#     bot = Bot(token='<TOKEN>')
#     storage = MemoryStorage()
#     dp = Dispatcher(bot, storage=storage)
#
#     dp.middleware.setup(AccessMiddleware(access_manager))