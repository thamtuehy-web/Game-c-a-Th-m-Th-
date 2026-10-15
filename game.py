"""
game.py - Game "Thắm & Thơ đi học về"
Dành cho trẻ em 6-8 tuổi trên nền tảng Python & Pygame.
"""

import sys
import pygame
import sound_effects
import graphics
import scenes

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        self.width = 1000
        self.height = 650
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Thắm & Thơ đi học về - Game Giáo Dục Dành Cho Trẻ Em")
        
        self.clock = pygame.time.Clock()
        self.sound_mgr = sound_effects.SoundManager()
        
        # Danh sách 8 nhiệm vụ chính
        self.task_names = [
            "Đóng cửa xe BYD",
            "Lấy cặp sách từ ô tô",
            "Cất giày dép lên kệ",
            "Cất cặp sách vào tủ 2 ngăn",
            "Ngồi ăn cơm",
            "Rửa bát",
            "Quét nhà",
            "Dọn đồ chơi"
        ]
        
        self.tasks_done = [False] * 8
        self.points = 0
        self.sound_muted = False
        
        # Cảnh hiện tại
        self.scenes = {}
        self.current_scene_name = "car"
        self.current_scene = None
        self.scene_order = ["car", "shoes", "study", "dining", "dishes", "living_room", "victory"]
        
        self.reset_game()

    def reset_game(self):
        """Khởi động lại toàn bộ game và điểm số."""
        self.tasks_done = [False] * 8
        self.points = 0
        
        self.scenes = {
            "car": scenes.SceneCar(self),
            "shoes": scenes.SceneShoes(self),
            "study": scenes.SceneStudy(self),
            "dining": scenes.SceneDining(self),
            "dishes": scenes.SceneDishes(self),
            "living_room": scenes.SceneLivingRoom(self),
            "victory": scenes.SceneVictory(self)
        }
        self.current_scene_name = "car"
        self.current_scene = self.scenes["car"]

    def complete_task(self, task_id, toast_message=None):
        """
        Đánh dấu hoàn thành nhiệm vụ task_id (1-indexed: 1 đến 8).
        Tăng điểm số tương ứng (+1 điểm cho mỗi công việc).
        """
        idx = task_id - 1
        if 0 <= idx < 8 and not self.tasks_done[idx]:
            self.tasks_done[idx] = True
            self.points = sum(self.tasks_done)
            self.sound_mgr.play('point')
            if toast_message and self.current_scene:
                self.current_scene.show_toast(toast_message)
            
            # Kiểm tra hoàn thành tất cả 8 nhiệm vụ -> Chuyển sang Màn hình CHIẾN THẮNG
            if self.points >= 8:
                self.switch_scene("victory")

    def is_task_done(self, task_id):
        idx = task_id - 1
        return self.tasks_done[idx] if 0 <= idx < 8 else False

    def switch_scene(self, scene_name):
        if scene_name in self.scenes:
            self.current_scene_name = scene_name
            self.current_scene = self.scenes[scene_name]

    def prev_scene(self):
        try:
            curr_idx = self.scene_order.index(self.current_scene_name)
            if curr_idx > 0:
                self.switch_scene(self.scene_order[curr_idx - 1])
        except ValueError:
            pass

    def next_scene(self):
        try:
            curr_idx = self.scene_order.index(self.current_scene_name)
            if curr_idx < len(self.scene_order) - 2:  # Không tự chuyển sang victory trừ khi đủ điểm
                self.switch_scene(self.scene_order[curr_idx + 1])
        except ValueError:
            pass

    def draw_hud(self, surface):
        """Vẽ thanh thông tin ở đầu màn hình (Tên game, 8 sao điểm số, nút âm thanh, nút đổi phòng)."""
        # Thanh nền HUD bo góc
        hud_rect = pygame.Rect(10, 8, self.width - 20, 56)
        pygame.draw.rect(surface, (255, 255, 255), hud_rect, border_radius=16)
        pygame.draw.rect(surface, (255, 180, 200), hud_rect, width=2, border_radius=16)

        # 1. Ảnh chân dung thật của 2 bé Thắm & Thơ trên thanh HUD
        av_tham = graphics.get_avatar("Tham", 38)
        if av_tham:
            surface.blit(av_tham, (20, 17))
            pygame.draw.circle(surface, (255, 120, 160), (39, 36), 20, 2)
            
        av_tho = graphics.get_avatar("Tho", 38)
        if av_tho:
            surface.blit(av_tho, (62, 17))
            pygame.draw.circle(surface, (255, 195, 20), (81, 36), 20, 2)

        # Tên Game
        font_title = pygame.font.SysFont('Segoe UI', 17, bold=True)
        txt_title = font_title.render("🎒 Thắm & Thơ Đi Học Về", True, (210, 60, 100))
        surface.blit(txt_title, (110, 23))

        # 2. Thanh 8 Ngôi Sao Điểm Số
        start_x = 340
        for i in range(8):
            sx = start_x + i * 32
            sy = 36
            done = self.tasks_done[i]
            if done:
                graphics.draw_star(surface, (sx, sy), 12, (255, 200, 20), filled=True)
            else:
                graphics.draw_star(surface, (sx, sy), 10, (190, 190, 200), filled=False)
            
            # Số thứ tự sao
            font_num = pygame.font.SysFont('Segoe UI', 9, bold=True)
            col = (110, 80, 0) if done else (150, 150, 160)
            n_txt = font_num.render(str(i + 1), True, col)
            surface.blit(n_txt, (sx - n_txt.get_width() // 2, sy - 5))

        # 3. Điểm số tổng kết
        font_score = pygame.font.SysFont('Segoe UI', 16, bold=True)
        txt_pts = font_score.render(f"⭐ {self.points}/8", True, (230, 120, 0))
        surface.blit(txt_pts, (605, 24))

        # 4. Nút Chuyển phòng (Lui / Tới) để bé dễ dàng xem các cảnh
        btn_font = pygame.font.SysFont('Segoe UI', 13, bold=True)
        
        # Nút Quay lại
        self.btn_back_rect = pygame.Rect(720, 18, 75, 36)
        pygame.draw.rect(surface, (245, 245, 250), self.btn_back_rect, border_radius=8)
        pygame.draw.rect(surface, (200, 200, 210), self.btn_back_rect, width=1, border_radius=8)
        b_txt = btn_font.render("◄ Trước", True, (80, 80, 90))
        surface.blit(b_txt, (self.btn_back_rect.centerx - b_txt.get_width() // 2, 26))

        # Nút Tiếp theo
        self.btn_fwd_rect = pygame.Rect(805, 18, 75, 36)
        pygame.draw.rect(surface, (245, 245, 250), self.btn_fwd_rect, border_radius=8)
        pygame.draw.rect(surface, (200, 200, 210), self.btn_fwd_rect, width=1, border_radius=8)
        f_txt = btn_font.render("Sau ►", True, (80, 80, 90))
        surface.blit(f_txt, (self.btn_fwd_rect.centerx - f_txt.get_width() // 2, 26))

        # 5. Nút Bật/Tắt Âm thanh
        self.btn_snd_rect = pygame.Rect(895, 18, 85, 36)
        bg_snd = (230, 245, 230) if not self.sound_muted else (255, 230, 230)
        pygame.draw.rect(surface, bg_snd, self.btn_snd_rect, border_radius=8)
        pygame.draw.rect(surface, (180, 210, 180), self.btn_snd_rect, width=1, border_radius=8)
        s_icon = "🔊 Bật" if not self.sound_muted else "🔇 Tắt"
        s_txt = btn_font.render(s_icon, True, (40, 120, 50) if not self.sound_muted else (180, 40, 40))
        surface.blit(s_txt, (self.btn_snd_rect.centerx - s_txt.get_width() // 2, 26))

    def run(self):
        running = True
        while running:
            # 1. Xử lý sự kiện (Events)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    # Bấm nút âm thanh
                    if hasattr(self, 'btn_snd_rect') and self.btn_snd_rect.collidepoint(mx, my):
                        self.sound_muted = not self.sound_muted
                        self.sound_mgr.enabled = not self.sound_muted
                        continue
                    # Bấm nút lùi cảnh
                    if hasattr(self, 'btn_back_rect') and self.btn_back_rect.collidepoint(mx, my):
                        self.prev_scene()
                        continue
                    # Bấm nút tiến cảnh
                    if hasattr(self, 'btn_fwd_rect') and self.btn_fwd_rect.collidepoint(mx, my):
                        self.next_scene()
                        continue
                
                # Chuyển sự kiện cho Cảnh hiện tại
                if self.current_scene:
                    self.current_scene.handle_event(event)

            # 2. Cập nhật logic (Update)
            if self.current_scene:
                self.current_scene.update()

            # 3. Vẽ hình (Draw)
            if self.current_scene:
                self.current_scene.draw(self.screen)

            # Vẽ HUD bar trên cùng (trừ màn hình victory để pháo hoa bung tỏa toàn màn hình)
            if self.current_scene_name != "victory":
                self.draw_hud(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
