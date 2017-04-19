from controller.get_data import *
from controller.mini_planner.message_selector import selectMessages

messages=getResourceMessages('Tr2')
print selectMessages(messages,3,['SMS','Messenger','Whatsapp'])
