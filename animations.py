import pygame as pg
import os

class Explosion:
    #Класс для анимации взрыва при смерти танка
    
    def __init__(self):
        self.frame_index = 0
        # Загрузка кадров с автоматизацией
        self.frames = self._load_frames()
        
    def _load_frames(self):
        #Загружает кадры анимации из папки
        frames = []
        folder = 'images/animations/explosion/'
        # Автоматическая загрузка кадров
        for i in range(33):  # 0-32 кадры
            frame_num = str(i).zfill(2)  # Форматирование в 01, 02 и т.д.
            filename = f'frame_{frame_num}_delay-0.05s.png'
            try:
                frame = pg.image.load(folder + filename)
                # Добавляем каждый кадр дважды для замедления анимации
                frames.extend([frame, frame.copy()])
            except FileNotFoundError:
                print(f"Предупреждение: отсутствует кадр {filename}")
                # Если кадр отсутствует, используем последний доступный
                if frames:
                    frames.extend([frames[-1], frames[-1].copy()])
        
        return frames

    def boom(self, screen, x, y):
        #Отрисовывает текущий кадр взрыва
        if self.frame_index < len(self.frames):
            screen.blit(self.frames[self.frame_index], (x - 30, y - 30))
            self.frame_index += 1
            return True  # Анимация продолжается
        return False  # Анимация завершена
