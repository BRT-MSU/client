import enum

AUTONOMY_ACTIVATION_MESSAGE = 'activate'
AUTONOMY_DEACTIVATION_MESSAGE = 'deactivate'


class ForwardingPrefix(enum.Enum):
    CLIENT = '-c'
    TANGO = '-t'
    MOTOR = '-m'
    CONTROLLER = '-p'
    DEBUG = '-d'
    STATUS = '-s'


class SubMessagePrefix(enum.Enum):
    LEFT_MOTOR = 'l'
    RIGHT_MOTOR = 'r'
    ACTUATOR = 'a'
    BUCKET = 'b'
    SERVO = 's'


class Message:
    def __init__(self, forwarding_prefix, sub_messages):
        sub_message_string = ''
        for sub_message_prefix, sub_message in sub_messages.items():
            sub_message_string += sub_message_prefix + str(sub_message) + '|'

        self.message = forwarding_prefix + sub_message_string
