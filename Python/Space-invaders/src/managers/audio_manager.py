from pathlib import Path

import arcade


class AudioManager:
    def __init__(self):
        self.background_music = None
        self.shoot_sound = None
        self.hit_sound = None
        self._music_player = None

    def load_audio(self, path: Path):
        if path.exists():
            return arcade.load_sound(path)
        return None
    
    def load(self, background_music: Path, shoot_sound: Path, hit_sound: Path):
        self.background_music = self.load_audio(background_music)
        self.shoot_sound = self.load_audio(shoot_sound)
        self.hit_sound = self.load_audio(hit_sound)

    def play_background(self, volume: float = 0.3):
        if self.background_music and self._music_player is None:
            self._music_player = self.background_music.play(volume=volume, loop=True)

    def play_shoot(self):
        if self.shoot_sound:
            self.shoot_sound.play()

    def play_hit(self):
        if self.hit_sound:
            self.hit_sound.play()