import serial, time, Utilities
from Constants import *

"""
What happens if user disconnects board during reading
User wants to connect board after logging in
"""

#to optimise: may need to run in a different thread
class SerialPort(serial.Serial):
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600,**kwargs):
        super().__init__(port, baudrate=baud_rate, **kwargs)
        self.running, self.reading_value = True, False
        self.start_time = time.time()
        self.time_elapsed = 0
    
    def convert(self, value):
        try:
            value = float(value)
            return value, True
        except ValueError:
            error_msg('Conversion error',
                      'Could not convert "{}" into float.'.format(value))
            return value, False

    def read_data(self):
        '''
        A message from the board is of the format: <subsystem,value>
        with <, > indicating the start and end of data
        '''
        buffer = ""
        first_char = self.read(1) #read first byte
        #chosen character to mark start of data
        if first_char == b'<' and not self.reading_value:
            self.reading_value = True
            while self.in_waiting and self.reading_value: #while there is data to be read
                one_byte = self.read(1)
                if one_byte == b'>':
                    self.reading_value = False
                    return buffer
                #rare occurence when two messages read as one
                elif one_byte == b'<':
                    self.reading_value = False
                    return buffer
                else:
                    buffer += one_byte.decode('utf-8')
            #if it exits while loop w/o returning not all data was read
        if len(buffer) > 0: pass#print(buffer) #if not all data was read
        self.reading_value = False
        return None

    '''
    Somtimes the first few characters aren't sent so we do not start reading
    until the marker (<) is read first - end of data is marked by '>'
    With the builtin read functions, sometimes not all of the data is read,
    causing errors instead read one byte until undesirable character is found
    Test by continually running
    '''

    def read_value(self):
        try:
            msg_digest, datatype, value = None, None, None
            msg_digest = self.read_data()
            if msg_digest is not None:
                split_msg = msg_digest.split(',')
                if len(split_msg) == 2:
                    datatype, value = split_msg
                    value, converted = self.convert(value)
                    if converted:
                        elapsed_time = time.time() - self.start_time
                        return datatype, round(value, 1), elapsed_time
            return None, None, None
        except serial.serialutil.SerialException:
            Utilities.error_msg('Disconnected', 'The MSP board was disconnected')
            return False, False, False

    def close(self):
        #send message to board to stop while loop in energia sketch
        self.write(bytes(b'<stop>'))
        self.close()

