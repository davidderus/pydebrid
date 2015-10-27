# -*- coding: utf-8 -*-

from babelfish import Language
import subliminal


class Subtitle:
    filepath = None
    langs = set([Language('eng')])
    isSingle = True

    def __init__(self, path):
        self.filepath = unicode(path, 'utf-8')

    def get(self):
        # scan for videos in the folder and their subtitles
        video = subliminal.scan_video(self.filepath)
        # download best subtitles
        subs = subliminal.download_best_subtitles([video], self.langs)
        return subliminal.save_subtitles(video, subs[video], self.isSingle)

    def get_langs(self):
        return self.langs

    def set_langs(self, langs):
        langs_set = set()
        for lang in langs:
            # Using a more flexible standard (ietf), allowing both fr et fra (e.g.)
            langs_set.add(Language.fromietf(lang))

        self.langs = langs_set

        if len(langs_set) > 1:
            self.isSingle = False

        return self
