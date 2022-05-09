from components.drawable.gauge import Gauge
from components.drawable.drawable import Drawable
from components.variable.demo_variables import *
from components.variable.canbus_variable import *

class DemoGaugeConfig:
    GAUGE_OFFX_INNER = 125
    GAUGE_OFFX_OUTER = 380
    GAUGE_OFFY_TOP = 500
    GAUGE_OFFY_BTM = 700

    BIGGAUGE_OFFX = 200
    BIGGAUGE_OFFY = 200

    SMALL_GAUGE_SIZE = 75
    SMALL_GAUGE_HINTS = 5

    def get_drawables(self, window: (int, int)) -> list[Drawable]:
        (window_width, window_height) = window

        variable_speed = DemoLoopingVariable(0, 0, 240, 0.25)
        variable_dummy = DemoStaticVariable(40, 0, 100)
        variable_motorspeed = DemoLoopingVariable(0, 0, 60)
        variable_temp = DemoLoopingVariable(50, 50, 240)

        return [
            Gauge(variable_speed, window_width/2 - self.BIGGAUGE_OFFX,window_height-self.BIGGAUGE_OFFY,0,display_description="SPEED",display_unit="km/h",hint_range=13),
            Gauge(variable_motorspeed, window_width/2 + self.BIGGAUGE_OFFX,window_height-self.BIGGAUGE_OFFY,1,display_description="MOTOR SPEED",display_unit="rpm"),
            Gauge(variable_temp, window_width/2 - self.GAUGE_OFFX_INNER,window_height-self.GAUGE_OFFY_TOP,0,display_description="TEMP",size=self.SMALL_GAUGE_SIZE,hint_range=self.SMALL_GAUGE_HINTS),
            # dummys
            Gauge(variable_dummy, window_width/2 - self.GAUGE_OFFX_OUTER,window_height-self.GAUGE_OFFY_TOP,0,display_description="dummy",size=self.SMALL_GAUGE_SIZE,hint_range=self.SMALL_GAUGE_HINTS),
            Gauge(variable_dummy, window_width/2 - self.GAUGE_OFFX_INNER,window_height-self.GAUGE_OFFY_BTM,0,display_description="dummy",size=self.SMALL_GAUGE_SIZE,hint_range=self.SMALL_GAUGE_HINTS),
            Gauge(variable_dummy, window_width/2 - self.GAUGE_OFFX_OUTER,window_height-self.GAUGE_OFFY_BTM,0,display_description="dummy",size=self.SMALL_GAUGE_SIZE,hint_range=self.SMALL_GAUGE_HINTS),
            Gauge(variable_dummy, window_width/2 + self.GAUGE_OFFX_OUTER,window_height-self.GAUGE_OFFY_TOP,0,display_description="dummy",size=self.SMALL_GAUGE_SIZE,hint_range=self.SMALL_GAUGE_HINTS),
            Gauge(variable_dummy, window_width/2 + self.GAUGE_OFFX_OUTER,window_height-self.GAUGE_OFFY_BTM,0,display_description="dummy",size=self.SMALL_GAUGE_SIZE,hint_range=self.SMALL_GAUGE_HINTS),
            Gauge(variable_dummy, window_width/2 + self.GAUGE_OFFX_INNER,window_height-self.GAUGE_OFFY_TOP,0,display_description="dummy",size=self.SMALL_GAUGE_SIZE,hint_range=self.SMALL_GAUGE_HINTS),
            Gauge(variable_dummy, window_width/2 + self.GAUGE_OFFX_INNER,window_height-self.GAUGE_OFFY_BTM,0,display_description="dummy",size=self.SMALL_GAUGE_SIZE,hint_range=self.SMALL_GAUGE_HINTS),
        ]
