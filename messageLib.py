import enum

AUTONOMOY_ACTIVATION_MESSAGE = 'activate'
AUTONOMY_DEACTIVATION_MESSAGE = 'deactivate'

class forwardingPrefix(enum.Enum):
    CLIENT = '-c'
    TANGO = '-t'
    MOTOR = '-m'
    CONTROLLER = '-p'
    DEBUG = '-d'
    STATUS = '-s'

class subMessagePrefix(enum.Enum):
    LEFT_MOTOR = 'l'
    RIGHT_MOTOR = 'r'
    ACTUATOR = 'a'
    BUCKET = 'b'
    SERVO = 's'

class Message():
    # Constructor expects a receiver and a submessage dictionary.
    # Submessage dictionary format
    def __init__(self, forwardingPrefix, subMessages):
        subMessageString = ''
        for subMessagePrefix, subMessage in subMessages.items():
            subMessageString += subMessagePrefix + str(subMessage) + '|'

        self.message = forwardingPrefix + subMessageString
