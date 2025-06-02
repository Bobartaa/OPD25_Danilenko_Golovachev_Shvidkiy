"""Централизованное управление звуками для игры"""
import pygame as pg
import os

# Глобальная инициализация микшера
pg.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

class SoundManager:
    """Класс для централизованного управления всеми звуками в игре"""
    
    def __init__(self):
        # Флаги состояния звуков
        self.menu_music_playing = False
        self.drone_sounds_playing = {}  # Словарь для отслеживания звуков дронов по их ID
        
        menu_music_path = 'sounds/menu_music.mp3.mp3'
          
        shot_sound_path = 'sounds/tank_shot.mp3'
            
        box_break_sound_path = 'sounds/box_break.mp3'
        
        drone_sound_path = 'sounds/drone.mp3'
            
        # Загрузка звуков меню
        self.menu_music = pg.mixer.Sound(menu_music_path)
            
        # Загрузка звука выстрела
        self.shot_sound = pg.mixer.Sound(shot_sound_path)
 
        # Звук дрона
        self.drone_sound = pg.mixer.Sound(drone_sound_path)
        
        # Звук разбивания ящика
        self.box_break_sound = pg.mixer.Sound(box_break_sound_path)
    
    def play_menu_music(self):
        """Воспроизведение музыки меню"""
        # Останавливаем все звуки, кроме музыки меню
        self.stop_game_sounds()
        
        # Затем запускаем музыку меню
        if self.menu_music is not None:
            self.menu_music.play(-1)  # -1 означает бесконечное повторение
            self.menu_music.set_volume(0.5)  # Установка громкости
            self.menu_music_playing = True
    
    def play_shot_sound(self):
        """Воспроизведение звука выстрела танка"""
        if self.shot_sound is not None:
            self.shot_sound.play()
                
    def play_box_break_sound(self):
        """Воспроизведение звука разбивания ящика"""
        #self.box_break_sound = pg.mixer.Sound(self.box_break_sound_path)
        # Воспроизводим звук, если он загружен
        if self.box_break_sound is not None:
            # Используем отдельный канал для звука разбивания ящика
            channel = pg.mixer.find_channel()
            if channel:
                channel.play(self.box_break_sound)
            else:
                # Если свободный канал не найден, воспроизводим напрямую
                self.box_break_sound.play()

                
    def play_drone_sound(self, drone_id):
        """Воспроизведение звука дрона с отслеживанием по ID"""
        
        # Воспроизводим звук, если он загружен и еще не воспроизводится для этого дрона
        if self.drone_sound is not None and drone_id not in self.drone_sounds_playing:
             # Создаем новый канал для этого дрона
            channel = pg.mixer.find_channel()
            if channel:
                channel.play(self.drone_sound, -1)  # -1 означает бесконечное повторение
                self.drone_sounds_playing[drone_id] = channel
                
    def stop_drone_sound(self, drone_id):
        """Остановка звука дрона по его ID"""
        if drone_id in self.drone_sounds_playing:
            channel = self.drone_sounds_playing[drone_id]
            channel.stop()
            del self.drone_sounds_playing[drone_id]
    
    def stop_menu_music(self):
        """Остановка музыки меню"""
        if self.menu_music is not None:
            self.menu_music.stop()
            self.menu_music_playing = False

    
    def stop_game_sounds(self):
        """Останавливает все игровые звуки, кроме музыки меню"""
        # Останавливаем все каналы микшера, кроме канала с музыкой меню
        for i in range(pg.mixer.get_num_channels()):
            if i != 0:  # Предполагаем, что музыка меню на канале 0
                pg.mixer.Channel(i).stop()
        
        # Очищаем словарь отслеживания звуков дронов
        self.drone_sounds_playing.clear()
    
    def stop_all_sounds(self):
        """Останавливает все звуки в игре, включая музыку меню"""
        # Останавливаем музыку меню
        self.stop_menu_music()
        
        # Останавливаем все каналы микшера
        pg.mixer.stop()
        
        # Очищаем словарь отслеживания звуков дронов
        self.drone_sounds_playing.clear()

# Создаем глобальный экземпляр менеджера звуков
sound_manager = SoundManager()
