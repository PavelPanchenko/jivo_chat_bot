from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
HOST = env.str("HOST")
DATABASE_NAME = env.str("DATABASE_NAME")
PORT = env.int('PORT') or 5000

SEND_URL = env.str("SEND_URL")

