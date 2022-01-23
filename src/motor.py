import pyb
class MotorDriver:
    '''! 
    This class implements a motor driver for an ME405 kit. 
    '''

    def __init__ (self, en_pin, in1pin, in2pin, timer):
        '''! 
        Creates a motor driver by initializing GPIO
        pins and turning the motor off for safety. 
        @param en_pin (There will be several of these)
        '''
        print ('Creating a motor driver')
        self.en_pin = pyb.Pin(en_pin, pyb.Pin.OUT_PP)
        self.in1pin = pyb.Pin(in1pin)
        self.in2pin = pyb.Pin(in2pin)
        self.timer = timer
        
        self.ch1 = self.timer.channel(1, pyb.Timer.PWM, pin=in1pin)
        self.ch2 = self.timer.channel(2, pyb.Timer.PWM, pin=in2pin)

    def set_duty_cycle (self, level):
        '''!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        '''
        print ('Setting duty cycle to ' + str (level))
        if level < 0 and level >= -100:
            ch1_level = 0
            ch2_level = level
        elif level == 0:
            ch1_level = 0
            ch2_level = 0
        elif level > 0 and level <= 100:
            ch1_level = level
            ch2_level = 0
        else:
            raise ValueError("level must be between -100 and 100")
        self.en_pin.high()
        print("ch1: ", ch1_level, "ch2: ", ch2_level)
        self.ch1.pulse_width_percent(ch1_level)
        self.ch2.pulse_width_percent(ch2_level)


if __name__ == "__main__":
    ena_pin = pyb.Pin.board.PA10
    in1a_pin = pyb.Pin.board.PB4
    in2a_pin = pyb.Pin.board.PB5
    tim3 = pyb.Timer(3, freq=20000)
    moe = MotorDriver(ena_pin, in1a_pin, in2a_pin, tim3)
    moe.set_duty_cycle(70)
