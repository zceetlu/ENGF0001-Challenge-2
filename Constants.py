#constants
SCREENWIDTH = 1280
SCREENHEIGHT = 720

MENU = "#518cb8"
BLUE = "#55beeb"
GREEN = "#49a362"
YELLOW = "#e79f3c"
RED = "#cd5542"
GREY = "#edf0f5"

FONT = 'MonacoB'
FONT_BOLD = 'MonacoB2 Bold'
FONTSIZE = SCREENWIDTH//100
MEDIUM = SCREENWIDTH//128
LARGE = SCREENHEIGHT//28

#Splash screen constants
MAX_ANGLE = 360
MAX_INCREMENT = 5
FRAMES_PER_SECOND = 16
DELAY = 500

#Login constants
USERNAME = 'ADMIN'
PASSWORD = '12345'

#Serial read constants
PORT = '/dev/ttyACM1'
BAUD_RATE = 9600
SERIAL_DELAY = 100 #100 miliseconds
MAX_DATA_POINTS = 60
RETRY_DELAY = 1000

#graph constants
OPTIMAL_VALS = {'pH of yeast': (7, 7), 'Temperature of yeast': (29, 32),
                'Motor Speed': (1450, 1550), '': (0, 0)}
FREQUENCY = 20
FRAMES = 200
