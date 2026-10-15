"""
sound_effects.py - Hệ thống âm thanh tự sinh (Synthesized Sound Engine)
Tạo âm thanh chân thực, vui nhộn cho trẻ em bằng Pygame & NumPy mà không cần tải file âm thanh ngoài.
"""

import os
import math
import numpy as np
import pygame

class SoundManager:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.enabled = True
        self.sounds = {}
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=sample_rate, size=-16, channels=2, buffer=1024)
            self._generate_all_sounds()
            self._load_voice_sounds()
        except Exception as e:
            print(f"[SoundManager] Cảnh báo khởi tạo âm thanh: {e}")
            self.enabled = False

    def _load_voice_sounds(self):
        """Nạp các file giọng đọc nữ tiếng Việt."""
        voice_files = {
            'voice_yeu_tham_tho': 'yeu_tham_tho.mp3',
            'voice_bo_me': 'chuc_mung_bo_me.mp3'
        }
        for name, filename in voice_files.items():
            path = os.path.join(self.base_dir, filename)
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                except Exception as e:
                    print(f"[SoundManager] Không thể tải giọng nói {name}: {e}")


    def _to_stereo_sound(self, mono_wave):
        """Chuyển mảng mono float (-1.0 đến 1.0) thành Pygame Sound stereo 16-bit."""
        if not self.enabled:
            return None
        mono_int16 = np.clip(mono_wave * 30000, -32767, 32767).astype(np.int16)
        stereo = np.column_stack((mono_int16, mono_int16))
        return pygame.sndarray.make_sound(stereo)

    def _generate_all_sounds(self):
        sr = self.sample_rate

        # 1. Đóng cửa ô tô: Tiếng thịch trầm chắc chắn + tiếng lẫy khóa kim loại 'Cạch!'
        dur_door = 0.35
        t = np.linspace(0, dur_door, int(sr * dur_door), False)
        # Tiếng thịch thân xe trầm
        thump = np.sin(2 * np.pi * 95 * (1 - 0.5 * t / dur_door) * t) * np.exp(-t * 18)
        # Tiếng lẫy kim loại "cạch" xảy ra ở t = 0.05
        click = np.zeros_like(t)
        click_idx = int(sr * 0.04)
        click_dur = int(sr * 0.03)
        if click_idx + click_dur < len(t):
            tc = np.linspace(0, 0.03, click_dur, False)
            metal = (np.sin(2 * np.pi * 1800 * tc) + 0.6 * np.sin(2 * np.pi * 3200 * tc)) * np.exp(-tc * 120)
            click[click_idx:click_idx + click_dur] = metal
        door_wave = thump * 0.85 + click * 0.7
        self.sounds['door_close'] = self._to_stereo_sound(door_wave)

        # 2. Lấy cặp sách: Tiếng xột xoạt êm nhẹ (khóa kéo vải)
        dur_bp = 0.25
        t = np.linspace(0, dur_bp, int(sr * dur_bp), False)
        noise = (np.random.rand(len(t)) * 2 - 1) * np.exp(-t * 12)
        tone = np.sin(2 * np.pi * 480 * t) * np.exp(-t * 20) * 0.4
        self.sounds['backpack'] = self._to_stereo_sound(noise * 0.4 + tone)

        # 3. Cất giày lên kệ: Tiếng 'cộp' gỗ ấm áp vui tươi
        dur_shoe = 0.22
        t = np.linspace(0, dur_shoe, int(sr * dur_shoe), False)
        wood = (np.sin(2 * np.pi * 320 * t) + 0.3 * np.sin(2 * np.pi * 640 * t)) * np.exp(-t * 25)
        self.sounds['shoe'] = self._to_stereo_sound(wood)

        # 4. Ăn cơm: Tiếng nhai giòn vui 'Ngoạm ngoạm!'
        dur_eat = 0.18
        t = np.linspace(0, dur_eat, int(sr * dur_eat), False)
        munch = (np.sin(2 * np.pi * (600 - 300 * t / dur_eat) * t) * 0.6 +
                 (np.random.rand(len(t)) * 2 - 1) * 0.3) * np.exp(-t * 22)
        self.sounds['eat'] = self._to_stereo_sound(munch)

        # 5. Rửa bát: Tiếng bong bóng xà phòng & dòng nước 'róc rách'
        dur_wash = 0.3
        t = np.linspace(0, dur_wash, int(sr * dur_wash), False)
        bubble = np.sin(2 * np.pi * (700 + 400 * np.sin(2 * np.pi * 30 * t)) * t) * np.exp(-t * 8) * 0.4
        water_noise = (np.random.rand(len(t)) * 2 - 1) * 0.3 * np.exp(-t * 5)
        self.sounds['wash'] = self._to_stereo_sound(bubble + water_noise)

        # 6. Quét nhà: Tiếng chổi quét sàn 'Soạt soạt'
        dur_sweep = 0.25
        t = np.linspace(0, dur_sweep, int(sr * dur_sweep), False)
        sweep_noise = (np.random.rand(len(t)) * 2 - 1) * np.sin(np.pi * t / dur_sweep) * 0.5
        self.sounds['sweep'] = self._to_stereo_sound(sweep_noise)

        # 7. Dọn đồ chơi: Tiếng 'Bính boong' rộn ràng
        dur_toy = 0.28
        t = np.linspace(0, dur_toy, int(sr * dur_toy), False)
        toy = (np.sin(2 * np.pi * 659 * t) + 0.4 * np.sin(2 * np.pi * 987 * t)) * np.exp(-t * 14)
        self.sounds['toy'] = self._to_stereo_sound(toy)

        # 8. Hoàn thành 1 nhiệm vụ: Tiếng chuông sao lấp lánh (Arpeggio: Đô - Mi - Sol - Đố)
        dur_star = 0.45
        t = np.linspace(0, dur_star, int(sr * dur_star), False)
        star_wave = np.zeros_like(t)
        freqs = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
        note_len = int(sr * 0.1)
        for i, f in enumerate(freqs):
            start = i * int(sr * 0.08)
            end = min(start + note_len * 2, len(t))
            tn = t[start:end] - t[start]
            note = (np.sin(2 * np.pi * f * tn) + 0.3 * np.sin(2 * np.pi * 2 * f * tn)) * np.exp(-tn * 16)
            star_wave[start:end] += note * 0.5
        self.sounds['point'] = self._to_stereo_sound(star_wave)

        # 9. Pháo hoa bắn lên (Whistle) & Pháo hoa nổ (Boom!)
        dur_fw_up = 0.35
        t = np.linspace(0, dur_fw_up, int(sr * dur_fw_up), False)
        f_up = 350 + 1200 * (t / dur_fw_up)**2
        fw_up = np.sin(2 * np.pi * f_up * t) * (t / dur_fw_up) * 0.4
        self.sounds['firework_up'] = self._to_stereo_sound(fw_up)

        dur_boom = 0.5
        t = np.linspace(0, dur_boom, int(sr * dur_boom), False)
        boom = (np.sin(2 * np.pi * 70 * np.exp(-t * 5) * t) * 0.7 +
                (np.random.rand(len(t)) * 2 - 1) * 0.5) * np.exp(-t * 7)
        self.sounds['firework_boom'] = self._to_stereo_sound(boom)

        # 10. Giai điệu CHIẾN THẮNG hoành tráng (Fanfare)
        dur_vic = 1.8
        t = np.linspace(0, dur_vic, int(sr * dur_vic), False)
        vic_wave = np.zeros_like(t)
        # Giai điệu: Sol - Sol - Sol - Đố! Mi! Sol!
        melody = [
            (523.25, 0.0, 0.15),   # Đô
            (659.25, 0.18, 0.15),  # Mi
            (783.99, 0.36, 0.15),  # Sol
            (1046.50, 0.54, 0.5),  # Đố kéo dài
            (880.00, 1.10, 0.18),  # La
            (1046.50, 1.30, 0.45)  # Đố kết thúc
        ]
        for f, start_sec, dur_sec in melody:
            st = int(start_sec * sr)
            en = min(st + int(dur_sec * sr * 1.5), len(t))
            if st < len(t):
                tn = t[st:en] - t[st]
                harmonic = (np.sin(2 * np.pi * f * tn) +
                            0.4 * np.sin(2 * np.pi * 2 * f * tn) +
                            0.2 * np.sin(2 * np.pi * 3 * f * tn)) * np.exp(-tn * 5)
                vic_wave[st:en] += harmonic * 0.45
        self.sounds['victory'] = self._to_stereo_sound(vic_wave)

    def play(self, sound_name):
        if not self.enabled:
            return
        snd = self.sounds.get(sound_name)
        if snd:
            try:
                snd.play()
            except Exception:
                pass
