from os import curdir

WORK_DIR = f'{curdir}/'

COGS_DIR_NAME = 'cogs'
COGS_DIR = f'{WORK_DIR}{COGS_DIR_NAME}/'

CONFIG_DIR_NAME = 'conf'
CONFIG_DIR = f'{WORK_DIR}{CONFIG_DIR_NAME}/'
BOT_CONFIG = f'{CONFIG_DIR}bot.json'

DATA_DIR_NAME = 'data'
DATA_DIR = f'{WORK_DIR}{DATA_DIR_NAME}/'
CHAR_INFO_DATA = f'{DATA_DIR}char_info.json'

LOGS_DIR_NAME = 'logs'
LOGS_DIR = f'{WORK_DIR}{LOGS_DIR_NAME}/'
BOT_LOG = f'{LOGS_DIR}bot.log'
