# -*- coding: utf-8 -*-
"""
    pySplash – Wallpaper for your Mac
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ver: 0.1.1
    url: http://egregors.com/lab/pySplash
    source: https://github.com/Egregors/pySplash

    img source: https://unsplash.it/

        Unbelievable simple app to set the desktop random picture from
    https://unsplash.com

    Required:
    - PyObjC
    - Python 2.6+
    - rumps

    To build mac bundle use:
    ```python setup.py py2app```
"""
import os
import shutil
import urllib
import datetime

import rumps

from AppKit import NSScreen, NSWorkspace
from Foundation import NSURL


class SplshApp(rumps.App):
    def __init__(self):
        super(SplshApp, self).__init__('Splsh')
        self.icon = 'img/icon.png'

        try:
            self.screen_width = int(NSScreen.mainScreen().frame().size.width)
            self.screen_height = int(NSScreen.mainScreen().frame().size.height)
        except:
            self.screen_width = 1024
            self.screen_height = 768

        self.menu = [
            'x'.join([str(self.screen_width), str(self.screen_height)]),
            None,
            rumps.MenuItem('Next', key='n'),
            None,
            rumps.MenuItem('Gray Mood'),
            rumps.MenuItem('Blur'),
            rumps.MenuItem('Clear Cache', key='c'),
            None,
        ]

        # Path to directory for downloaded images
        self.media_dir = 'media/'
        # Extra url parameters
        self.gray_mood = False
        self.blur = False

        print('Current resolution: {} x {}'.format(self.screen_width, self.screen_height))

    @rumps.clicked('Next')
    def next_image(self, _):

        if not os.path.exists(self.media_dir):
            print('Creating MEDIA_DIR...')
            os.makedirs(self.media_dir)

        url = 'https://unsplash.it/'

        if self.gray_mood:
            url += 'g/'

        url += '{w}/{h}/?random'

        if self.blur:
            url += '&blur'

        url = url.format(w=self.screen_width, h=self.screen_height)

        file_name = self.media_dir + datetime.datetime.now().strftime("%H:%M:%S.%f") + '.jpg'

        try:
            self.icon = 'img/wait.png'
            urllib.urlretrieve(url, file_name)
            file_url = NSURL.fileURLWithPath_(file_name)

            # Get shared workspace
            ws = NSWorkspace.sharedWorkspace()

            # Iterate over all screens
            for screen in NSScreen.screens():
                # Tell the workspace to set the desktop picture
                (result, error) = ws.setDesktopImageURL_forScreen_options_error_(
                    file_url, screen, {}, None)
            self.icon = 'img/icon.png'
        except IOError:
            print('Service unavailable, check your internet connection.')
            rumps.alert(title='Connection Error', message='Service unavailable\n'
                                                          'Please, check your internet connection')

    @rumps.clicked('Gray Mood')
    def is_gray_mood(self, sender):
        self.gray_mood = not self.gray_mood
        sender.state = not sender.state

    @rumps.clicked('Blur')
    def is_blur(self, sender):
        self.blur = not self.blur
        sender.state = not sender.state

    @rumps.clicked('Clear Cache')
    def clear_cache(self, _):
        """ Remove directory with all downloaded images.
        :param _:
        :return:
        """
        if os.path.exists(self.media_dir):
            print('Removing MEDIA_DIR...')
            shutil.rmtree(self.media_dir)


if __name__ == '__main__':
    app = SplshApp().run()
