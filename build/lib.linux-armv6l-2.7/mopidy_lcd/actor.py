import pykka
import pylirc
import logging
import tempfile

from time import sleep

from mopidy.core import PlaybackState
from mopidy.utils import process
from mopidy.core import CoreListener
from Adafruit_CharLCD import Adafruit_CharLCD


logger = logging.getLogger('mopidy_lCD')

class LCDFrontend(pykka.ThreadingActor, CoreListener):
    def __init__(self, config, core):
        super(LCDFrontend, self).__init__()
        self.core = core
	self.config = config

    def on_start(self):
        try:
            logger.debug('LCD starting')
            self.lcd = Adafruit_CharLCD()
            self.lcd.begin(16, 1)
            self.lcd.clear()
            self.lcd.message("Mopidy started")
            logger.debug('LCD started')
        except Exception as e:
            logger.warning('LCD has not started: ' + str(e))
            self.stop()

    def on_stop(self):
        logger.info('LCD stopped')
        self.lcd.begin(16, 1)
        self.lcd.clear()
        self.lcd.message("Mopidy stopped")

    def on_failure(self):
        logger.warning('LCD failing')

    def track_playback_started(self,tl_track):
        logger.info('LCD: Track has changed')
	track = tl_track.track
	song = track.name
	artists = ', '.join([a.name for a in track.artists])
	album = track.album.name
        self.lcd.clear()
        self.lcd.message(artists + "\n" + song)
	

