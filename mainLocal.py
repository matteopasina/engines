from controller.get_data import *
from controller.mini_planner.message_selector import selectMessages

messages=getResourceMessages('Tr2')
for m in selectMessages(messages,3,['SMS']):
    print m.text
