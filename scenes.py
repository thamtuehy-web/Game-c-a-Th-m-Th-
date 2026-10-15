"""
scenes.py - Quản lý các phân cảnh tương tác và nhiệm vụ của Thắm & Thơ
Tương tác trực quan, dễ chơi, âm thanh sống động, phù hợp tuyệt đối cho trẻ 6-8 tuổi.
"""

import math
import random
import pygame
import graphics

class BaseScene:
    def __init__(self, game):
        self.game = game
        self.tick = 0
        self.message = ""
        self.message_timer = 0

    def show_toast(self, text, duration=150):
        self.message = text
        self.message_timer = duration

    def draw_hud_message(self, surface):
        if self.message_timer > 0:
            self.message_timer -= 1
            font = pygame.font.SysFont('Segoe UI', 20, bold=True)
            text_surf = font.render(self.message, True, (255, 255, 255))
            tw, th = text_surf.get_size()
            rect = pygame.Rect(self.game.width // 2 - tw // 2 - 16, 75, tw + 32, th + 12)
            pygame.draw.rect(surface, (40, 160, 60), rect, border_radius=12)
            pygame.draw.rect(surface, (255, 255, 255), rect, width=2, border_radius=12)
            surface.blit(text_surf, (self.game.width // 2 - tw // 2, 80))


# ==========================================================
# CẢNH 1: NGOÀI SÂN XE Ô TÔ (Nhiệm vụ 1 & 2)
# ==========================================================
class SceneCar(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.door_closed = False
        self.door_anim_progress = 0.0  # 0: Mở toang, 1: Đóng sập
        self.blink_lights = 0
        self.auto_advance_timer = 0
        
        # 2 Cặp sách trong xe
        self.tham_backpack_taken = False
        self.tho_backpack_taken = False
        
        # Vị trí các vùng bấm tương tác
        self.car_rect = pygame.Rect(180, 200, 480, 260)
        self.door_btn_rect = pygame.Rect(400, 240, 160, 180)
        self.bp_tham_rect = pygame.Rect(320, 270, 55, 65)
        self.bp_tho_rect = pygame.Rect(385, 275, 55, 65)
        self.btn_next = pygame.Rect(780, 550, 190, 55)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            
            # Nếu đã xong cả 2 việc thì bấm bất kỳ đâu để qua cảnh cất giày
            if self.game.is_task_done(1) and self.game.is_task_done(2):
                self.game.switch_scene("shoes")
                return

            # 1. Đóng cửa xe BYD Sealion 6
            if not self.door_closed and self.door_btn_rect.collidepoint(mx, my):
                self.door_closed = True
                self.door_anim_progress = 1.0
                self.blink_lights = 40
                self.game.sound_mgr.play('door_close')
                self.game.complete_task(1, "Bé giỏi lắm! Đã đóng cửa xe BYD Sealion 6 màu đen an toàn! (+1 điểm ⭐)")
                return

            # 2. Lấy cặp sách của Thắm
            if not self.tham_backpack_taken and self.bp_tham_rect.collidepoint(mx, my):
                self.tham_backpack_taken = True
                self.game.sound_mgr.play('backpack')
                self.show_toast("Bé Thắm đã nhận được chiếc cặp hồng dâu tây xinh xắn!")
                self._check_task2()
                return

            # 3. Lấy cặp sách của Thơ
            if not self.tho_backpack_taken and self.bp_tho_rect.collidepoint(mx, my):
                self.tho_backpack_taken = True
                self.game.sound_mgr.play('backpack')
                self.show_toast("Bé Thơ đã nhận được chiếc cặp vàng ngôi sao rực rỡ!")
                self._check_task2()
                return

    def _check_task2(self):
        if self.tham_backpack_taken and self.tho_backpack_taken and not self.game.is_task_done(2):
            self.game.complete_task(2, "Tuyệt vời! Hai bé đã lấy đủ cặp sách xuống xe! (+1 điểm ⭐)")
            self.auto_advance_timer = 90  # Tự động chuyển cảnh sau 1.5s

    def update(self):
        self.tick += 1
        if self.blink_lights > 0:
            self.blink_lights -= 1
        # Tự động chuyển cảnh nếu đã hoàn thành nhiệm vụ 1 & 2
        if self.game.is_task_done(1) and self.game.is_task_done(2):
            if self.auto_advance_timer > 0:
                self.auto_advance_timer -= 1
                if self.auto_advance_timer == 0:
                    self.game.switch_scene("shoes")


    def draw(self, surface):
        w, h = self.game.width, self.game.height

        # Nền trời, cỏ, đường và nhà
        surface.fill(graphics.COLOR_BG_SKY)
        # Mặt trời & mây
        pygame.draw.circle(surface, (255, 235, 100), (880, 90), 45)
        pygame.draw.circle(surface, (255, 245, 180), (880, 90), 38)
        # Mây bồng bềnh
        for cx, cy in [(150, 110), (220, 105), (550, 130), (620, 125)]:
            pygame.draw.circle(surface, (255, 255, 255), (cx, cy), 32)
        # Bãi cỏ & lối vào nhà
        pygame.draw.rect(surface, graphics.COLOR_GRASS, (0, 360, w, h - 360))
        # Đường bê tông đỗ xe
        pygame.draw.rect(surface, graphics.COLOR_ROAD, (100, 420, 720, 190), border_radius=16)

        # Ngôi nhà ở phía sau
        pygame.draw.rect(surface, (255, 245, 225), (700, 180, 260, 240))
        pygame.draw.polygon(surface, (230, 80, 70), [(680, 180), (830, 100), (980, 180)]) # Mái ngói đỏ
        pygame.draw.rect(surface, (140, 85, 45), (740, 280, 60, 140)) # Cửa ra vào

        # BÓNG XE Ô TÔ
        graphics.draw_shadow(surface, 420, 480, 460, 45)

        # THÂN XE Ô TÔ ĐIỆN BYD MÀU ĐEN SANG TRỌNG
        cx, cy = 180, 240
        
        # Mui xe cong màu đen bóng
        car_polygon = [
            (cx + 80, cy + 30), (cx + 170, cy - 40), (cx + 340, cy - 40),
            (cx + 420, cy + 30), (cx + 475, cy + 80), (cx + 475, cy + 160),
            (cx, cy + 160), (cx, cy + 80)
        ]
        pygame.draw.polygon(surface, (30, 32, 38), car_polygon) # Đen bóng
        pygame.draw.polygon(surface, (15, 16, 20), car_polygon, width=3)

        # Đường viền kim loại ánh bạc chrome trên mui xe
        pygame.draw.lines(surface, (180, 195, 215), False, [
            (cx + 90, cy + 28), (cx + 170, cy - 36), (cx + 340, cy - 36), (cx + 415, cy + 28)
        ], 3)

        # Kính cửa sổ ô tô màu xanh khói hiện đại
        pygame.draw.polygon(surface, (190, 215, 235), [
            (cx + 100, cy + 30), (cx + 180, cy - 30), (cx + 330, cy - 30),
            (cx + 400, cy + 30)
        ])
        # Cột chia kính đen
        pygame.draw.line(surface, (20, 22, 26), (cx + 255, cy - 30), (cx + 255, cy + 30), 5)

        # Dải đèn LED ban ngày của BYD (trắng xanh hiện đại)
        pygame.draw.line(surface, (220, 245, 255), (cx + 2, cy + 90), (cx + 65, cy + 90), 4)
        pygame.draw.circle(surface, (180, 240, 255), (cx + 15, cy + 90), 5)

        # LOGO THƯƠNG HIỆU BYD NỔI BẬT TRÊN ĐẦU VÀ THÂN XE
        # Huy hiệu BYD mạ bạc trên đầu xe
        byd_badge_rect = pygame.Rect(cx + 15, cy + 115, 48, 22)
        pygame.draw.rect(surface, (220, 225, 235), byd_badge_rect, border_radius=6)
        pygame.draw.rect(surface, (120, 130, 145), byd_badge_rect, width=2, border_radius=6)
        font_byd = pygame.font.SysFont('Segoe UI', 13, bold=True)
        txt_byd = font_byd.render("BYD", True, (20, 25, 35))
        surface.blit(txt_byd, (byd_badge_rect.centerx - txt_byd.get_width() // 2, byd_badge_rect.centery - txt_byd.get_height() // 2))

        # Dải chữ thương hiệu sườn xe: BYD SEALION 6
        font_byd_side = pygame.font.SysFont('Segoe UI', 15, bold=True)
        txt_byd_side = font_byd_side.render("✦ BYD SEALION 6 ✦", True, (190, 205, 225))
        surface.blit(txt_byd_side, (cx + 105, cy + 120))

        # CẶP SÁCH SIÊU XINH BÊN TRONG XE (dùng draw_cute_backpack)
        if not self.tham_backpack_taken:
            graphics.draw_cute_backpack(surface, self.bp_tham_rect.centerx, self.bp_tham_rect.centery, 50, 60, theme="tham", tick=self.tick)
            pygame.draw.rect(surface, (255, 255, 120), self.bp_tham_rect.inflate(6, 6), width=2, border_radius=12)

        if not self.tho_backpack_taken:
            graphics.draw_cute_backpack(surface, self.bp_tho_rect.centerx, self.bp_tho_rect.centery, 50, 60, theme="tho", tick=self.tick + 10)
            pygame.draw.rect(surface, (255, 255, 120), self.bp_tho_rect.inflate(6, 6), width=2, border_radius=12)

        # MÔ PHỎNG CÁNH CỬA XE Ô TÔ BYD SEALION 6
        if not self.door_closed:
            # Cửa mở nghiêng ra ngoài (màu đen ánh kim)
            door_points = [
                (cx + 255, cy + 30),
                (cx + 395, cy + 50),
                (cx + 385, cy + 180),
                (cx + 255, cy + 160)
            ]
            pygame.draw.polygon(surface, (45, 48, 56), door_points) # Màu đen cửa mở
            pygame.draw.polygon(surface, (20, 22, 28), door_points, width=3)
            # Kính trên cánh cửa mở
            pygame.draw.polygon(surface, (205, 225, 245), [
                (cx + 265, cy + 35), (cx + 385, cy + 52), (cx + 380, cy + 100), (cx + 265, cy + 95)
            ])
            # Tay nắm cửa mạ crom bạc sáng bóng
            pygame.draw.rect(surface, (245, 245, 250), (cx + 350, cy + 115, 28, 9), border_radius=4)
            pygame.draw.rect(surface, (120, 130, 140), (cx + 350, cy + 115, 28, 9), width=1, border_radius=4)
            
            # Hướng dẫn nhấp nháy bấm đóng cửa
            tip_x = cx + 400
            tip_y = cy + 105
            pygame.draw.circle(surface, (255, 230, 0), (tip_x, tip_y), 16 + int(math.sin(self.tick * 0.15) * 3))
            font_tip = pygame.font.SysFont('Segoe UI', 13, bold=True)
            tip_surf = font_tip.render("👉 Đóng cửa xe BYD Sealion 6!", True, (20, 20, 20))
            surface.blit(tip_surf, (tip_x + 18, tip_y - 10))
        else:
            # Cửa đã đóng kín khít vào thân xe màu đen bóng
            door_rect = pygame.Rect(cx + 255, cy + 30, 140, 130)
            pygame.draw.rect(surface, (26, 28, 34), door_rect)
            pygame.draw.rect(surface, (15, 16, 20), door_rect, width=2)
            # Kính xe khớp
            pygame.draw.rect(surface, (190, 215, 235), (cx + 260, cy + 35, 130, 55))
            # Tay nắm cửa crom
            pygame.draw.rect(surface, (245, 245, 250), (cx + 360, cy + 105, 26, 8), border_radius=4)
            # Đèn xe nhấp nháy báo khóa cửa an toàn
            if self.blink_lights > 0 and (self.blink_lights // 6) % 2 == 0:
                pygame.draw.circle(surface, (255, 220, 0), (cx + 470, cy + 100), 16)
                pygame.draw.circle(surface, (255, 255, 180), (cx + 470, cy + 100), 10)


        # Bánh xe ô tô vành đúc thể thao
        for wx in [cx + 100, cx + 380]:
            pygame.draw.circle(surface, (30, 32, 36), (wx, cy + 160), 38)
            pygame.draw.circle(surface, (210, 215, 225), (wx, cy + 160), 22) # Vành nhôm bạc
            pygame.draw.circle(surface, (50, 55, 65), (wx, cy + 160), 10)
            # Nan hoa vành đúc
            for ang_deg in [0, 60, 120, 180, 240, 300]:
                rad = math.radians(ang_deg)
                pygame.draw.line(surface, (140, 145, 155), (wx, cy + 160), (wx + int(math.cos(rad) * 20), cy + 160 + int(math.sin(rad) * 20)), 2)


        # VẼ 2 NHÂN VẬT THẮM & THƠ ĐỨNG NGOÀI SÂN
        # Thắm
        graphics.draw_character(surface, 100, 420, "Tham", scale=1.1,
                                is_cheering=self.tham_backpack_taken, tick=self.tick)
        # Thơ
        graphics.draw_character(surface, 180, 435, "Tho", scale=1.1,
                                is_cheering=self.tho_backpack_taken, tick=self.tick + 15)

        # Nút chuyển cảnh khi xong
        if self.game.is_task_done(1) and self.game.is_task_done(2):
            pulse = int(math.sin(self.tick * 0.15) * 4)
            r = self.btn_next.inflate(pulse, pulse)
            pygame.draw.rect(surface, (255, 130, 0), r, border_radius=16)
            pygame.draw.rect(surface, (255, 255, 255), r, width=3, border_radius=16)
            f_btn = pygame.font.SysFont('Segoe UI', 18, bold=True)
            txt = f_btn.render("Đi Vào Nhà Nào ➔", True, (255, 255, 255))
            surface.blit(txt, (r.centerx - txt.get_width() // 2, r.centery - txt.get_height() // 2))

        self.draw_hud_message(surface)


# ==========================================================
# CẢNH 2: TIỀN SẢNH - CẤT GIÀY DÉP LÊN KỆ (Nhiệm vụ 3)
# ==========================================================
class SceneShoes(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.tham_shoe_on_rack = False
        self.tho_shoe_on_rack = False
        self.auto_advance_timer = 0
        
        # Vị trí giày dưới sàn
        self.shoe_tham_rect = pygame.Rect(230, 470, 140, 75)
        self.shoe_tho_rect = pygame.Rect(400, 470, 140, 75)
        self.rack_rect = pygame.Rect(630, 230, 320, 280)
        self.btn_next = pygame.Rect(game.width // 2 - 160, 560, 320, 58)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            
            # Nếu đã xếp xong cả 2 đôi thì chạm bất kỳ đâu để qua cảnh cất cặp vào tủ
            if self.game.is_task_done(3):
                self.game.switch_scene("study")
                return

            # Nếu cả hai chưa cất
            if not self.tham_shoe_on_rack and not self.tho_shoe_on_rack:
                if self.shoe_tham_rect.collidepoint(mx, my) or mx < 350:
                    self.tham_shoe_on_rack = True
                    self.game.sound_mgr.play('shoe')
                    self.show_toast("Giày hồng xinh của Thắm đã xếp ngay ngắn lên tầng 1!")
                    self._check_task()
                    return
                else:
                    self.tho_shoe_on_rack = True
                    self.game.sound_mgr.play('shoe')
                    self.show_toast("Giày vàng xinh của Thơ đã xếp ngay ngắn lên tầng 2!")
                    self._check_task()
                    return

            # Nếu Thắm chưa cất, bấm bất kỳ đâu để cất nốt
            if not self.tham_shoe_on_rack:
                self.tham_shoe_on_rack = True
                self.game.sound_mgr.play('shoe')
                self.show_toast("Giày hồng xinh của Thắm đã xếp ngay ngắn lên tầng 1!")
                self._check_task()
                return

            # Nếu Thơ chưa cất, bấm bất kỳ đâu để cất nốt
            if not self.tho_shoe_on_rack:
                self.tho_shoe_on_rack = True
                self.game.sound_mgr.play('shoe')
                self.show_toast("Giày vàng xinh của Thơ đã xếp ngay ngắn lên tầng 2!")
                self._check_task()
                return

    def _check_task(self):
        if self.tham_shoe_on_rack and self.tho_shoe_on_rack and not self.game.is_task_done(3):
            self.game.complete_task(3, "Bé giỏi quá! Giày dép đã cất gọn gàng lên kệ sắc màu! (+1 điểm ⭐)")
            self.auto_advance_timer = 90  # Tự động chuyển cảnh sau 1.5s

    def update(self):
        self.tick += 1
        if self.game.is_task_done(3):
            if self.auto_advance_timer > 0:
                self.auto_advance_timer -= 1
                if self.auto_advance_timer == 0:
                    self.game.switch_scene("study")

    def draw(self, surface):
        w, h = self.game.width, self.game.height

        # Nền tường ấm áp & Sàn gỗ tiền sảnh
        surface.fill(graphics.COLOR_WALL_CREAM)
        # Đường chân tường
        pygame.draw.rect(surface, (215, 175, 130), (0, 380, w, 25))
        # Sàn gỗ sọc ấm cúng
        pygame.draw.rect(surface, (230, 190, 140), (0, 405, w, h - 405))
        for gy in range(435, h, 35):
            pygame.draw.line(surface, (205, 165, 115), (0, gy), (w, gy), 2)

        # Thảm đón khách hình đám mây xinh xắn
        mat_rect = pygame.Rect(200, 465, 380, 105)
        pygame.draw.rect(surface, (170, 220, 240), mat_rect, border_radius=25)
        pygame.draw.rect(surface, (120, 185, 215), mat_rect, width=3, border_radius=25)
        f_mat = pygame.font.SysFont('Segoe UI', 15, bold=True)
        txt_mat = f_mat.render("★ Chào Mừng Về Nhà ★", True, (70, 120, 150))
        surface.blit(txt_mat, (mat_rect.centerx - txt_mat.get_width() // 2, mat_rect.y + 10))

        # KỆ ĐỂ GIÀY DÉP MÀU SẮC DỄ THƯƠNG CHO BÉ
        rack_x, rack_y = 630, 230
        rack_w, rack_h = 320, 280
        
        # Biển hiệu trên cùng của kệ giày: Dải cầu vồng xinh xắn
        header_rect = pygame.Rect(rack_x + 10, rack_y - 25, rack_w - 20, 34)
        pygame.draw.rect(surface, (255, 140, 180), header_rect, border_radius=12)
        pygame.draw.rect(surface, (255, 255, 255), header_rect, width=2, border_radius=12)
        f_top = pygame.font.SysFont('Segoe UI', 14, bold=True)
        t_top = f_top.render("🌈 KỆ GIÀY SẮC MÀU 🌈", True, (255, 255, 255))
        surface.blit(t_top, (header_rect.centerx - t_top.get_width() // 2, header_rect.centery - t_top.get_height() // 2))

        # Khung kệ chính: Màu tím pastel dịu ngọt
        pygame.draw.rect(surface, (195, 185, 245), (rack_x, rack_y, rack_w, rack_h), border_radius=16)
        pygame.draw.rect(surface, (255, 255, 255), (rack_x, rack_y, rack_w, rack_h), width=4, border_radius=16)
        
        # Tầng 1 (Trên): Dành cho Thắm - Màu hồng dâu tây xinh xắn
        t1_y = rack_y + 35
        pygame.draw.rect(surface, (255, 205, 222), (rack_x + 15, t1_y, rack_w - 30, 95), border_radius=12)
        pygame.draw.rect(surface, (255, 120, 160), (rack_x + 15, t1_y, rack_w - 30, 95), width=3, border_radius=12)
        f_lbl = pygame.font.SysFont('Segoe UI', 13, bold=True)
        surface.blit(f_lbl.render("🌸 Ngăn Bé Thắm (Tầng 1)", True, (200, 40, 90)), (rack_x + 25, t1_y + 8))
        # Ảnh thật bé Thắm cạnh tên ngăn
        av_t1 = graphics.get_avatar("Tham", 40)
        if av_t1:
            surface.blit(av_t1, (rack_x + rack_w - 60, t1_y + 5))
            pygame.draw.circle(surface, (255, 215, 0), (rack_x + rack_w - 40, t1_y + 25), 22, 2)

        # Tầng 2 (Dưới): Dành cho Thơ - Màu vàng chanh & cam rực rỡ
        t2_y = rack_y + 145
        pygame.draw.rect(surface, (255, 242, 160), (rack_x + 15, t2_y, rack_w - 30, 95), border_radius=12)
        pygame.draw.rect(surface, (245, 180, 30), (rack_x + 15, t2_y, rack_w - 30, 95), width=3, border_radius=12)
        surface.blit(f_lbl.render("⭐ Ngăn Bé Thơ (Tầng 2)", True, (180, 110, 0)), (rack_x + 25, t2_y + 8))
        # Ảnh thật bé Thơ cạnh tên ngăn
        av_t2 = graphics.get_avatar("Tho", 40)
        if av_t2:
            surface.blit(av_t2, (rack_x + rack_w - 60, t2_y + 5))
            pygame.draw.circle(surface, (255, 215, 0), (rack_x + rack_w - 40, t2_y + 25), 22, 2)

        # ĐÔI GIÀY CỦA THẮM (Dùng hàm vector draw_cute_shoes)
        if self.tham_shoe_on_rack:
            # Đã cất trên kệ
            graphics.draw_cute_shoes(surface, rack_x + 130, t1_y + 55, theme="tham", tick=0)
        else:
            # Còn trên thảm
            graphics.draw_cute_shoes(surface, self.shoe_tham_rect.centerx, self.shoe_tham_rect.centery, theme="tham", tick=self.tick)
            f_hint = pygame.font.SysFont('Segoe UI', 12, bold=True)
            hint = f_hint.render("👉 Giày Thắm", True, (220, 50, 100))
            surface.blit(hint, (self.shoe_tham_rect.centerx - hint.get_width() // 2, self.shoe_tham_rect.y - 18))

        # ĐÔI GIÀY CỦA THƠ (Dùng hàm vector draw_cute_shoes)
        if self.tho_shoe_on_rack:
            # Đã cất trên kệ
            graphics.draw_cute_shoes(surface, rack_x + 130, t2_y + 55, theme="tho", tick=0)
        else:
            # Còn trên thảm
            graphics.draw_cute_shoes(surface, self.shoe_tho_rect.centerx, self.shoe_tho_rect.centery, theme="tho", tick=self.tick + 10)
            f_hint = pygame.font.SysFont('Segoe UI', 12, bold=True)
            hint = f_hint.render("👉 Giày Thơ", True, (190, 130, 0))
            surface.blit(hint, (self.shoe_tho_rect.centerx - hint.get_width() // 2, self.shoe_tho_rect.y - 18))

        # VẼ THẮM & THƠ ĐỨNG CƯỜI Ở TIỀN SẢNH
        graphics.draw_character(surface, 110, 390, "Tham", scale=1.1,
                                is_cheering=self.tham_shoe_on_rack, tick=self.tick)
        graphics.draw_character(surface, 190, 405, "Tho", scale=1.1,
                                is_cheering=self.tho_shoe_on_rack, tick=self.tick + 10)

        # Nút chuyển tiếp (Nổi bật, rực rỡ)
        if self.game.is_task_done(3):
            pulse = int(math.sin(self.tick * 0.15) * 4)
            r = self.btn_next.inflate(pulse, pulse)
            pygame.draw.rect(surface, (255, 120, 0), r, border_radius=18)
            pygame.draw.rect(surface, (255, 255, 255), r, width=3, border_radius=18)
            f_btn = pygame.font.SysFont('Segoe UI', 19, bold=True)
            txt = f_btn.render("🚪 Cất Cặp Sách Vào Tủ ➔", True, (255, 255, 255))
            surface.blit(txt, (r.centerx - txt.get_width() // 2, r.centery - txt.get_height() // 2))

        self.draw_hud_message(surface)


# ==========================================================
# CẢNH 3: PHÒNG NGỦ - CẤT CẶP SÁCH VÀO TỦ 2 NGĂN (Nhiệm vụ 4)
# ==========================================================
class SceneStudy(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.tham_bp_placed = False
        self.tho_bp_placed = False
        self.auto_advance_timer = 0
        
        # Vị trí click tương tác
        self.bp_click_tham = pygame.Rect(100, 310, 180, 200)
        self.bp_click_tho = pygame.Rect(260, 320, 180, 200)
        self.cabinet_tham_rect = pygame.Rect(470, 150, 230, 370)
        self.cabinet_tho_rect = pygame.Rect(710, 150, 230, 370)
        self.btn_next = pygame.Rect(game.width // 2 - 160, 560, 320, 58)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            
            # Nếu đã cất xong cả 2 cặp thì bấm bất kỳ đâu trên màn hình để đến giờ ăn cơm!
            if self.game.is_task_done(4):
                self.game.switch_scene("dining")
                return

            # Cả hai cặp chưa cất
            if not self.tham_bp_placed and not self.tho_bp_placed:
                if self.bp_click_tham.collidepoint(mx, my) or self.cabinet_tham_rect.collidepoint(mx, my) or mx < 590:
                    self.tham_bp_placed = True
                    self.game.sound_mgr.play('backpack')
                    self.show_toast("Đã cất chiếc cặp hồng dâu tây của Thắm vào Ngăn tủ 1!")
                    self._check_task()
                    return
                else:
                    self.tho_bp_placed = True
                    self.game.sound_mgr.play('backpack')
                    self.show_toast("Đã cất chiếc cặp vàng ngôi sao của Thơ vào Ngăn tủ 2!")
                    self._check_task()
                    return

            # Chỉ còn cặp Thắm chưa cất: Bấm bất kỳ đâu để cất nốt
            if not self.tham_bp_placed:
                self.tham_bp_placed = True
                self.game.sound_mgr.play('backpack')
                self.show_toast("Đã cất chiếc cặp hồng dâu tây của Thắm vào Ngăn tủ 1!")
                self._check_task()
                return

            # Chỉ còn cặp Thơ chưa cất: Bấm bất kỳ đâu để cất nốt
            if not self.tho_bp_placed:
                self.tho_bp_placed = True
                self.game.sound_mgr.play('backpack')
                self.show_toast("Đã cất chiếc cặp vàng ngôi sao của Thơ vào Ngăn tủ 2!")
                self._check_task()
                return

    def _check_task(self):
        if self.tham_bp_placed and self.tho_bp_placed and not self.game.is_task_done(4):
            self.game.complete_task(4, "Xuất sắc! Cặp sách đã được cất gọn gàng vào tủ 2 ngăn! (+1 điểm ⭐)")
            self.auto_advance_timer = 90  # Tự động chuyển cảnh sau 1.5s sang phòng ăn

    def update(self):
        self.tick += 1
        if self.game.is_task_done(4):
            if self.auto_advance_timer > 0:
                self.auto_advance_timer -= 1
                if self.auto_advance_timer == 0:
                    self.game.switch_scene("dining")

    def draw(self, surface):
        w, h = self.game.width, self.game.height

        # Nền phòng ngủ pastel ấm áp, dễ thương
        surface.fill((255, 245, 240))
        pygame.draw.rect(surface, (245, 220, 215), (0, 390, w, 20))
        pygame.draw.rect(surface, (240, 215, 185), (0, 410, w, h - 410))

        # Cửa sổ ngập nắng nhìn ra vườn hoa
        win_rect = pygame.Rect(60, 110, 220, 170)
        pygame.draw.rect(surface, (180, 225, 255), win_rect)
        pygame.draw.rect(surface, (255, 255, 255), win_rect, width=8)
        pygame.draw.line(surface, (255, 255, 255), (170, 110), (170, 280), 5)
        pygame.draw.line(surface, (255, 255, 255), (60, 195), (280, 195), 5)

        # CHIẾC TỦ ĐỒ 2 NGĂN ĐỨNG TO ĐẸP CỦA HAI BÉ
        cab_x, cab_y = 460, 130
        cab_w, cab_h = 490, 400

        # Mái vòm / Biển hiệu trên nóc tủ
        roof_rect = pygame.Rect(cab_x + 20, cab_y - 25, cab_w - 40, 36)
        pygame.draw.rect(surface, (255, 150, 180), roof_rect, border_radius=14)
        pygame.draw.rect(surface, (255, 255, 255), roof_rect, width=2, border_radius=14)
        f_top = pygame.font.SysFont('Segoe UI', 15, bold=True)
        txt_cab = f_top.render("🚪 TỦ CẤT CẶP 2 NGĂN CỦA HAI BÉ", True, (255, 255, 255))
        surface.blit(txt_cab, (roof_rect.centerx - txt_cab.get_width() // 2, roof_rect.centery - txt_cab.get_height() // 2))

        # Khung thân tủ màu kem sữa viền bo tròn
        pygame.draw.rect(surface, (250, 240, 230), (cab_x, cab_y, cab_w, cab_h), border_radius=18)
        pygame.draw.rect(surface, (220, 190, 175), (cab_x, cab_y, cab_w, cab_h), width=5, border_radius=18)
        # Vách ngăn giữa 2 cánh tủ
        pygame.draw.line(surface, (200, 170, 155), (cab_x + cab_w // 2, cab_y + 15), (cab_x + cab_w // 2, cab_y + cab_h - 15), 6)

        # ---------------- NGĂN 1: TỦ BÉ THẮM (BÊN TRÁI) ----------------
        t1_x, t1_y = cab_x + 18, cab_y + 25
        t1_w, t1_h = 215, cab_h - 45
        
        # Lòng ngăn tủ màu hồng phấn nhạt
        pygame.draw.rect(surface, (255, 235, 242), (t1_x, t1_y, t1_w, t1_h), border_radius=12)
        pygame.draw.rect(surface, (255, 180, 205), (t1_x, t1_y, t1_w, t1_h), width=3, border_radius=12)
        
        # Bảng tên ngăn Thắm + Chân dung thật
        name_t1 = pygame.Rect(t1_x + 12, t1_y + 10, t1_w - 24, 32)
        pygame.draw.rect(surface, (255, 110, 155), name_t1, border_radius=8)
        f_lbl = pygame.font.SysFont('Segoe UI', 12, bold=True)
        surface.blit(f_lbl.render("🌸 Ngăn Bé Thắm (Ngăn 1)", True, (255, 255, 255)), (name_t1.x + 8, name_t1.y + 6))
        
        # Ảnh chân dung thật bé Thắm
        av_t1 = graphics.get_avatar("Tham", 44)
        if av_t1:
            surface.blit(av_t1, (t1_x + t1_w - 52, t1_y + 5))
            pygame.draw.circle(surface, (255, 215, 0), (t1_x + t1_w - 30, t1_y + 27), 24, 2)

        # Giá để cặp bên trong ngăn 1
        shelf_t1_y = t1_y + t1_h - 100
        pygame.draw.rect(surface, (255, 195, 215), (t1_x + 10, shelf_t1_y, t1_w - 20, 14), border_radius=5)

        if self.tham_bp_placed:
            # Cặp Thắm cất ngay ngắn trên giá tủ (hình vẽ vector xinh xắn)
            graphics.draw_cute_backpack(surface, t1_x + t1_w // 2, shelf_t1_y - 45, 74, 84, theme="tham", tick=0)
            graphics.draw_star(surface, (t1_x + 35, shelf_t1_y - 65), 10, (255, 215, 0))
            graphics.draw_star(surface, (t1_x + t1_w - 35, shelf_t1_y - 65), 10, (255, 215, 0))
        else:
            # Ô đứt nét nhấp nháy đón cặp
            pulse = math.sin(self.tick * 0.15) * 3
            spot_r = pygame.Rect(t1_x + t1_w // 2 - 42, shelf_t1_y - 92, 84, 90)
            pygame.draw.rect(surface, (255, 140, 175), spot_r.inflate(pulse, pulse), width=2, border_radius=12)
            f_pl = pygame.font.SysFont('Segoe UI', 12, bold=True)
            surface.blit(f_pl.render("👉 Đặt Cặp Thắm", True, (220, 60, 100)), (spot_r.x + 2, spot_r.y + 36))

        # Tay nắm mạ vàng của ngăn 1
        pygame.draw.circle(surface, (255, 215, 0), (t1_x + t1_w - 15, t1_y + t1_h // 2), 10)
        pygame.draw.circle(surface, (200, 150, 0), (t1_x + t1_w - 15, t1_y + t1_h // 2), 10, width=2)

        # ---------------- NGĂN 2: TỦ BÉ THƠ (BÊN PHẢI) ----------------
        t2_x, t2_y = cab_x + cab_w // 2 + 8, cab_y + 25
        t2_w, t2_h = 215, cab_h - 45
        
        # Lòng ngăn tủ màu vàng chanh nhạt
        pygame.draw.rect(surface, (255, 252, 230), (t2_x, t2_y, t2_w, t2_h), border_radius=12)
        pygame.draw.rect(surface, (250, 210, 80), (t2_x, t2_y, t2_w, t2_h), width=3, border_radius=12)
        
        # Bảng tên ngăn Thơ + Chân dung thật
        name_t2 = pygame.Rect(t2_x + 12, t2_y + 10, t2_w - 24, 32)
        pygame.draw.rect(surface, (245, 175, 20), name_t2, border_radius=8)
        surface.blit(f_lbl.render("⭐ Ngăn Bé Thơ (Ngăn 2)", True, (255, 255, 255)), (name_t2.x + 8, name_t2.y + 6))
        
        # Ảnh chân dung thật bé Thơ
        av_t2 = graphics.get_avatar("Tho", 44)
        if av_t2:
            surface.blit(av_t2, (t2_x + t2_w - 52, t2_y + 5))
            pygame.draw.circle(surface, (255, 215, 0), (t2_x + t2_w - 30, t2_y + 27), 24, 2)

        # Giá để cặp bên trong ngăn 2
        shelf_t2_y = t2_y + t2_h - 100
        pygame.draw.rect(surface, (255, 230, 150), (t2_x + 10, shelf_t2_y, t2_w - 20, 14), border_radius=5)

        if self.tho_bp_placed:
            # Cặp Thơ cất ngay ngắn trên giá tủ (hình vẽ vector xinh xắn)
            graphics.draw_cute_backpack(surface, t2_x + t2_w // 2, shelf_t2_y - 45, 74, 84, theme="tho", tick=0)
            graphics.draw_star(surface, (t2_x + 35, shelf_t2_y - 65), 10, (255, 200, 20))
            graphics.draw_star(surface, (t2_x + t2_w - 35, shelf_t2_y - 65), 10, (255, 200, 20))
        else:
            # Ô đứt nét nhấp nháy đón cặp
            pulse = math.cos(self.tick * 0.15) * 3
            spot_r2 = pygame.Rect(t2_x + t2_w // 2 - 42, shelf_t2_y - 92, 84, 90)
            pygame.draw.rect(surface, (240, 175, 20), spot_r2.inflate(pulse, pulse), width=2, border_radius=12)
            f_pl = pygame.font.SysFont('Segoe UI', 12, bold=True)
            surface.blit(f_pl.render("👉 Đặt Cặp Thơ", True, (180, 120, 0)), (spot_r2.x + 4, spot_r2.y + 36))

        # Tay nắm mạ vàng của ngăn 2
        pygame.draw.circle(surface, (255, 215, 0), (t2_x + 15, t2_y + t2_h // 2), 10)
        pygame.draw.circle(surface, (200, 150, 0), (t2_x + 15, t2_y + t2_h // 2), 10, width=2)

        # ---------------- VẼ 2 BÉ THẮM & THƠ ĐỨNG BÊN TRÁI ----------------
        graphics.draw_character(surface, 170, 400, "Tham", scale=1.1,
                                is_cheering=self.tham_bp_placed, tick=self.tick)
        graphics.draw_character(surface, 320, 415, "Tho", scale=1.1,
                                is_cheering=self.tho_bp_placed, tick=self.tick + 10)

        # Cặp sách của Thắm bên cạnh bé nếu chưa cất
        if not self.tham_bp_placed:
            graphics.draw_cute_backpack(surface, 225, 415, 62, 72, theme="tham", tick=self.tick)
            f_b = pygame.font.SysFont('Segoe UI', 12, bold=True)
            t_b = f_b.render("👉 Bấm cất cặp", True, (220, 50, 100))
            surface.blit(t_b, (225 - t_b.get_width() // 2, 455))

        # Cặp sách của Thơ bên cạnh bé nếu chưa cất
        if not self.tho_bp_placed:
            graphics.draw_cute_backpack(surface, 375, 430, 62, 72, theme="tho", tick=self.tick + 10)
            f_b = pygame.font.SysFont('Segoe UI', 12, bold=True)
            t_b = f_b.render("👉 Bấm cất cặp", True, (180, 120, 0))
            surface.blit(t_b, (375 - t_b.get_width() // 2, 470))

        # NÚT CHUYỂN TIẾP TO RỰC RỠ Ở GIỮA
        if self.game.is_task_done(4):
            pulse = int(math.sin(self.tick * 0.15) * 4)
            r = self.btn_next.inflate(pulse, pulse)
            pygame.draw.rect(surface, (255, 120, 0), r, border_radius=18)
            pygame.draw.rect(surface, (255, 255, 255), r, width=3, border_radius=18)
            f_btn = pygame.font.SysFont('Segoe UI', 19, bold=True)
            txt = f_btn.render("🍽️ Đến Giờ Ăn Cơm Nào ➔", True, (255, 255, 255))
            surface.blit(txt, (r.centerx - txt.get_width() // 2, r.centery - txt.get_height() // 2))

        self.draw_hud_message(surface)


# ==========================================================
# CẢNH 4: PHÒNG ĂN - NGỒI ĂN CƠM (Nhiệm vụ 5)
# ==========================================================
class SceneDining(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.bites_count = 0  # Cần ăn 4 món: cơm, thịt sườn, rau xanh, canh
        self.food_eaten = [False, False, False, False]
        self.auto_advance_timer = 0
        
        # 4 Món ăn trên bàn
        self.food_rects = [
            pygame.Rect(400, 340, 70, 60),  # Bát cơm Thắm
            pygame.Rect(475, 335, 75, 55),  # Đĩa thịt sườn ram
            pygame.Rect(555, 335, 75, 55),  # Đĩa rau củ luộc
            pygame.Rect(635, 340, 70, 60),  # Bát canh súp thơm
        ]
        self.table_rect = pygame.Rect(320, 310, 440, 190)
        self.btn_next = pygame.Rect(game.width // 2 - 160, 560, 320, 58)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            
            # Nếu đã ăn xong, bấm bất kỳ đâu để qua cảnh rửa bát
            if self.game.is_task_done(5):
                self.game.switch_scene("dishes")
                return
            
            # Bấm vào món ăn cụ thể
            for i, r in enumerate(self.food_rects):
                if not self.food_eaten[i] and r.collidepoint(mx, my):
                    self.food_eaten[i] = True
                    self.bites_count += 1
                    self.game.sound_mgr.play('eat')
                    names = ["Bát cơm dẻo", "Món sườn rim thơm phức", "Rau củ ngọt mát", "Bát canh nóng ấm"]
                    self.show_toast(f"Hai bé ăn {names[i]} ngon tuyệt! Măm măm!")
                    self._check_task()
                    return

            # Nếu bấm vào vùng bàn ăn bất kỳ mà còn món chưa ăn -> tự động ăn món tiếp theo
            if self.table_rect.collidepoint(mx, my):
                for i in range(4):
                    if not self.food_eaten[i]:
                        self.food_eaten[i] = True
                        self.bites_count += 1
                        self.game.sound_mgr.play('eat')
                        names = ["Bát cơm dẻo", "Món sườn rim thơm phức", "Rau củ ngọt mát", "Bát canh nóng ấm"]
                        self.show_toast(f"Hai bé ăn {names[i]} ngon tuyệt! Măm măm!")
                        self._check_task()
                        return

    def _check_task(self):
        if self.bites_count >= 4 and not self.game.is_task_done(5):
            self.game.complete_task(5, "Tuyệt vời! Thắm & Thơ đã ăn cơm thật ngoan và no bụng! (+1 điểm ⭐)")
            self.auto_advance_timer = 90  # Tự động chuyển cảnh sau 1.5s sang cảnh rửa bát

    def update(self):
        self.tick += 1
        if self.game.is_task_done(5):
            if self.auto_advance_timer > 0:
                self.auto_advance_timer -= 1
                if self.auto_advance_timer == 0:
                    self.game.switch_scene("dishes")

    def draw(self, surface):
        w, h = self.game.width, self.game.height

        # Nền phòng ăn ấm áp
        surface.fill((255, 248, 235))
        pygame.draw.rect(surface, (230, 200, 170), (0, 420, w, h - 420))

        # Tranh treo tường gia đình hạnh phúc (Có ảnh thật của 2 bé!)
        pic_rect = pygame.Rect(350, 100, 300, 160)
        pygame.draw.rect(surface, (255, 255, 255), pic_rect, border_radius=12)
        pygame.draw.rect(surface, graphics.COLOR_WOOD, pic_rect, width=6, border_radius=12)
        f_pic = pygame.font.SysFont('Segoe UI', 14, bold=True)
        txt = f_pic.render("❤ GIA ĐÌNH HẠNH PHÚC ❤", True, (200, 60, 80))
        surface.blit(txt, (pic_rect.centerx - txt.get_width() // 2, pic_rect.y + 10))
        
        # Vẽ chân dung thật của 2 bé lồng trong khung ảnh gia đình
        graphics.draw_avatar_portrait(surface, pic_rect.x + 80, pic_rect.y + 88, "Tham", size=65)
        graphics.draw_avatar_portrait(surface, pic_rect.right - 80, pic_rect.y + 88, "Tho", size=65)

        # BÀN ĂN TRÒN ẤM CÚNG
        pygame.draw.ellipse(surface, (250, 225, 195), self.table_rect)
        pygame.draw.ellipse(surface, (220, 175, 135), self.table_rect, width=5)
        # Khăn trải bàn sọc caro
        cloth_rect = pygame.Rect(370, 330, 340, 130)
        pygame.draw.ellipse(surface, (255, 255, 255), cloth_rect)
        pygame.draw.ellipse(surface, (255, 190, 200), cloth_rect, width=2)

        # CÁC MÓN ĂN TRÊN BÀN
        # 1. Bát cơm
        r0 = self.food_rects[0]
        if not self.food_eaten[0]:
            pygame.draw.ellipse(surface, (240, 240, 245), r0)
            pygame.draw.ellipse(surface, (255, 255, 255), (r0.x + 8, r0.y + 6, 54, 38))
            f_f = pygame.font.SysFont('Segoe UI', 11, bold=True)
            surface.blit(f_f.render("Bát Cơm", True, (80, 80, 90)), (r0.x + 12, r0.y + 18))
        else:
            pygame.draw.ellipse(surface, (220, 220, 225), r0, width=2)
            f_f = pygame.font.SysFont('Segoe UI', 10, bold=True)
            surface.blit(f_f.render("Hết rồi!", True, (150, 150, 160)), (r0.x + 15, r0.y + 18))

        # 2. Đĩa sườn
        r1 = self.food_rects[1]
        if not self.food_eaten[1]:
            pygame.draw.ellipse(surface, (255, 245, 230), r1)
            pygame.draw.ellipse(surface, (190, 80, 40), (r1.x + 12, r1.y + 10, 50, 32))
            f_f = pygame.font.SysFont('Segoe UI', 11, bold=True)
            surface.blit(f_f.render("Thịt Sườn", True, (255, 255, 255)), (r1.x + 14, r1.y + 18))
        else:
            pygame.draw.ellipse(surface, (220, 220, 225), r1, width=2)

        # 3. Đĩa rau
        r2 = self.food_rects[2]
        if not self.food_eaten[2]:
            pygame.draw.ellipse(surface, (255, 245, 230), r2)
            pygame.draw.ellipse(surface, (80, 185, 90), (r2.x + 12, r2.y + 10, 50, 32))
            f_f = pygame.font.SysFont('Segoe UI', 11, bold=True)
            surface.blit(f_f.render("Rau Xanh", True, (255, 255, 255)), (r2.x + 13, r2.y + 18))
        else:
            pygame.draw.ellipse(surface, (220, 220, 225), r2, width=2)

        # 4. Bát canh
        r3 = self.food_rects[3]
        if not self.food_eaten[3]:
            pygame.draw.ellipse(surface, (255, 225, 210), r3)
            pygame.draw.ellipse(surface, (255, 170, 70), (r3.x + 8, r3.y + 6, 54, 38))
            f_f = pygame.font.SysFont('Segoe UI', 11, bold=True)
            surface.blit(f_f.render("Bát Canh", True, (255, 255, 255)), (r3.x + 12, r3.y + 18))
        else:
            pygame.draw.ellipse(surface, (220, 220, 225), r3, width=2)

        # VẼ 2 BÉ NGỒI 2 BÊN BÀN ĂN
        # Thắm ngồi ghế bên trái
        graphics.draw_character(surface, 230, 370, "Tham", scale=1.1,
                                is_cheering=self.game.is_task_done(5), tick=self.tick)
        # Thơ ngồi ghế bên phải
        graphics.draw_character(surface, 830, 370, "Tho", scale=1.1,
                                is_cheering=self.game.is_task_done(5), tick=self.tick + 10)

        # Hướng dẫn bấm thức ăn
        if not self.game.is_task_done(5):
            pulse = math.sin(self.tick * 0.15) * 4
            f_g = pygame.font.SysFont('Segoe UI', 15, bold=True)
            g_txt = f_g.render("👉 Bé hãy bấm vào các món ăn trên bàn để Thắm & Thơ măm măm nhé!", True, (180, 70, 20))
            surface.blit(g_txt, (w // 2 - g_txt.get_width() // 2, 275 + pulse))

        # Nút chuyển tiếp to rực rỡ ở giữa
        if self.game.is_task_done(5):
            pulse = int(math.sin(self.tick * 0.15) * 4)
            r = self.btn_next.inflate(pulse, pulse)
            pygame.draw.rect(surface, (255, 120, 0), r, border_radius=18)
            pygame.draw.rect(surface, (255, 255, 255), r, width=3, border_radius=18)
            f_btn = pygame.font.SysFont('Segoe UI', 19, bold=True)
            txt = f_btn.render("🧽 Đi Rửa Bát Nào ➔", True, (255, 255, 255))
            surface.blit(txt, (r.centerx - txt.get_width() // 2, r.centery - txt.get_height() // 2))

        self.draw_hud_message(surface)


# ==========================================================
# CẢNH 5: BỒN RỬA BÁT - RỬA BÁT (Nhiệm vụ 6)
# ==========================================================
class SceneDishes(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.step = 0  # 0: Bật vòi nước, 1: Dùng xà phòng tạo bọt, 2: Tráng nước sạch bong
        self.water_running = False
        self.bubbles = []
        self.auto_advance_timer = 0
        
        self.tap_rect = pygame.Rect(480, 180, 80, 100)
        self.sponge_rect = pygame.Rect(680, 340, 80, 60)
        self.sink_bowl_rect = pygame.Rect(380, 310, 280, 160)
        self.btn_next = pygame.Rect(game.width // 2 - 160, 560, 320, 58)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            
            # Nếu đã rửa bát xong, bấm bất kỳ đâu để sang phòng khách
            if self.game.is_task_done(6):
                self.game.switch_scene("living_room")
                return

            # Bước 1: Mở vòi nước
            if self.step == 0 and (self.tap_rect.collidepoint(mx, my) or my < 290):
                self.step = 1
                self.water_running = True
                self.game.sound_mgr.play('wash')
                self.show_toast("Đã mở vòi nước! Giờ hãy lấy bọt biển xà phòng chùi bát nhé!")
                return

            # Bước 2: Dùng bọt biển
            if self.step == 1 and (self.sponge_rect.collidepoint(mx, my) or mx > 640):
                self.step = 2
                self.game.sound_mgr.play('wash')
                # Tạo hàng chục bong bóng
                for _ in range(25):
                    self.bubbles.append([random.randint(400, 620), random.randint(330, 420), random.randint(6, 16)])
                self.show_toast("Bọt xà phòng trắng xoá! Bấm vào bồn để xả nước tráng sạch!")
                return

            # Bước 3: Tráng nước sạch
            if self.step == 2:
                self.step = 3
                self.water_running = False
                self.game.sound_mgr.play('point')
                self.game.complete_task(6, "Bé thật chăm chỉ! Bát đĩa đã sạch bóng kin kít! (+1 điểm ⭐)")
                self.auto_advance_timer = 90  # Tự động chuyển cảnh sau 1.5s
                return

    def update(self):
        self.tick += 1
        if self.game.is_task_done(6):
            if self.auto_advance_timer > 0:
                self.auto_advance_timer -= 1
                if self.auto_advance_timer == 0:
                    self.game.switch_scene("living_room")

    def draw(self, surface):
        w, h = self.game.width, self.game.height

        # Nền gạch men nhà bếp sạch bong
        surface.fill((240, 248, 255))
        for gy in range(80, 340, 40):
            pygame.draw.line(surface, (220, 235, 245), (0, gy), (w, gy), 2)
        for gx in range(0, w, 40):
            pygame.draw.line(surface, (220, 235, 245), (gx, 80), (gx, 340), 2)

        # Bàn bếp đá hoa cương
        pygame.draw.rect(surface, (225, 230, 235), (0, 340, w, h - 340))
        pygame.draw.rect(surface, (180, 190, 200), (0, 340, w, 15))

        # BỒN RỬA INOX SÁNG LOÁNG
        sink_x, sink_y = 350, 300
        pygame.draw.rect(surface, (200, 205, 215), (sink_x, sink_y, 340, 210), border_radius=20)
        pygame.draw.rect(surface, (150, 160, 175), (sink_x + 15, sink_y + 15, 310, 180), border_radius=16)

        # VÒI NƯỚC CỔ NGỖNG SÁNG BÓNG
        tap_x, tap_y = 500, 200
        pygame.draw.arc(surface, (140, 150, 160), (tap_x - 30, tap_y, 60, 90), 0, math.pi, 12)
        pygame.draw.line(surface, (140, 150, 160), (tap_x + 30, tap_y + 45), (tap_x + 30, tap_y + 90), 12)
        pygame.draw.circle(surface, (100, 110, 120), (tap_x + 30, tap_y + 90), 8)

        # DÒNG NƯỚC CHẢY (Nếu đang mở vòi)
        if self.water_running:
            for i in range(5):
                wave_off = math.sin(self.tick * 0.3 + i) * 3
                pygame.draw.line(surface, (130, 210, 255), (tap_x - 30 + wave_off, tap_y + 45), (tap_x - 30 + wave_off, sink_y + 110), 4)

        # BÁT ĐĨA TRONG BỒN
        if self.step < 3:
            # Bát dơ / đang rửa
            pygame.draw.ellipse(surface, (245, 245, 250), (420, 370, 90, 50))
            pygame.draw.ellipse(surface, (245, 245, 250), (510, 380, 95, 55))
        else:
            # Bát đĩa sạch bóng sáng loáng phát ra tia lấp lánh
            pygame.draw.ellipse(surface, (255, 255, 255), (420, 370, 90, 50))
            pygame.draw.ellipse(surface, (255, 255, 255), (510, 380, 95, 55))
            # Tia sao sáng
            graphics.draw_star(surface, (450, 360), 10, (255, 240, 100))
            graphics.draw_star(surface, (560, 370), 12, (255, 240, 100))

        # BỌT XÀ PHÒNG
        for bx, by, br in self.bubbles:
            pygame.draw.circle(surface, (255, 255, 255), (bx, by), br)
            pygame.draw.circle(surface, (200, 235, 255), (bx, by), br, 1)

        # MIẾNG BỌT BIỂN RỬA BÁT MÀU VÀNG
        pygame.draw.rect(surface, (255, 215, 60), self.sponge_rect, border_radius=10)
        pygame.draw.rect(surface, (220, 170, 20), self.sponge_rect, width=2, border_radius=10)
        f_sp = pygame.font.SysFont('Segoe UI', 12, bold=True)
        surface.blit(f_sp.render("Bọt Biển", True, (120, 80, 0)), (self.sponge_rect.x + 12, self.sponge_rect.y + 20))

        # GIÁ ÚP BÁT BÊN CẠNH
        pygame.draw.rect(surface, (210, 215, 225), (710, 240, 160, 110), border_radius=8)
        for i in range(5):
            pygame.draw.line(surface, (180, 185, 195), (730 + i * 25, 250), (730 + i * 25, 335), 3)

        # THẮM & THƠ ĐỨNG CẠNH PHỤ RỬA BÁT
        graphics.draw_character(surface, 180, 390, "Tham", scale=1.1,
                                is_cheering=self.game.is_task_done(6), tick=self.tick)
        graphics.draw_character(surface, 260, 405, "Tho", scale=1.1,
                                is_cheering=self.game.is_task_done(6), tick=self.tick + 10)

        # Hướng dẫn thao tác theo từng bước
        f_inst = pygame.font.SysFont('Segoe UI', 15, bold=True)
        if self.step == 0:
            pulse = math.sin(self.tick * 0.15) * 4
            t = f_inst.render("👉 Bước 1: Bé hãy bấm vào vòi nước để mở nước chảy nhé!", True, (20, 100, 200))
            surface.blit(t, (w // 2 - t.get_width() // 2, 130 + pulse))
        elif self.step == 1:
            pulse = math.sin(self.tick * 0.15) * 4
            t = f_inst.render("👉 Bước 2: Bấm vào miếng bọt biển vàng để xoa xà phòng!", True, (200, 120, 0))
            surface.blit(t, (w // 2 - t.get_width() // 2, 130 + pulse))
        elif self.step == 2:
            pulse = math.sin(self.tick * 0.15) * 4
            t = f_inst.render("👉 Bước 3: Bấm vào bồn nước để tráng sạch bóng kin kít!", True, (40, 160, 60))
            surface.blit(t, (w // 2 - t.get_width() // 2, 130 + pulse))

        # Nút chuyển tiếp to rực rỡ ở giữa
        if self.game.is_task_done(6):
            pulse = int(math.sin(self.tick * 0.15) * 4)
            r = self.btn_next.inflate(pulse, pulse)
            pygame.draw.rect(surface, (255, 120, 0), r, border_radius=18)
            pygame.draw.rect(surface, (255, 255, 255), r, width=3, border_radius=18)
            f_btn = pygame.font.SysFont('Segoe UI', 19, bold=True)
            txt = f_btn.render("🧹 Ra Phòng Khách Dọn Dẹp ➔", True, (255, 255, 255))
            surface.blit(txt, (r.centerx - txt.get_width() // 2, r.centery - txt.get_height() // 2))

        self.draw_hud_message(surface)


# ==========================================================
# CẢNH 6: PHÒNG KHÁCH - QUÉT NHÀ & DỌN ĐỒ CHƠI (Nhiệm vụ 7 & 8)
# ==========================================================
class SceneLivingRoom(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        
        # NHIỆM VỤ 7: QUÉT NHÀ (5 mẩu bụi/rác)
        self.dust_items = [
            {'x': 180, 'y': 490, 'cleaned': False, 'type': 'leaf'},
            {'x': 260, 'y': 530, 'cleaned': False, 'type': 'paper'},
            {'x': 340, 'y': 480, 'cleaned': False, 'type': 'dust'},
            {'x': 420, 'y': 540, 'cleaned': False, 'type': 'paper'},
            {'x': 500, 'y': 500, 'cleaned': False, 'type': 'leaf'},
        ]
        
        # NHIỆM VỤ 8: DỌN ĐỒ CHƠI (4 món đồ chơi)
        self.toys = [
            {'name': 'Gấu Teddy', 'x': 620, 'y': 480, 'w': 50, 'h': 50, 'stored': False, 'color': (180, 120, 80)},
            {'name': 'Ô tô mini', 'x': 700, 'y': 510, 'w': 55, 'h': 40, 'stored': False, 'color': (240, 60, 60)},
            {'name': 'Lego khối', 'x': 780, 'y': 480, 'w': 45, 'h': 45, 'stored': False, 'color': (60, 180, 240)},
            {'name': 'Bóng tròn', 'x': 850, 'y': 505, 'w': 45, 'h': 45, 'stored': False, 'color': (255, 200, 40)},
        ]
        
        # Thùng đồ chơi
        self.toy_box_rect = pygame.Rect(720, 340, 180, 120)
        self.btn_next = pygame.Rect(game.width // 2 - 170, 560, 340, 58)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            
            # Nếu cả 2 nhiệm vụ đã xong, bấm bất kỳ đâu để sang màn CHIẾN THẮNG
            if self.game.is_task_done(7) and self.game.is_task_done(8):
                self.game.switch_scene("victory")
                return

            # 1. Quét nhà (Bấm vào mẩu rác bất kỳ)
            for d in self.dust_items:
                if not d['cleaned']:
                    dist = math.hypot(mx - d['x'], my - d['y'])
                    if dist <= 32:
                        d['cleaned'] = True
                        self.game.sound_mgr.play('sweep')
                        self.show_toast("Soạt soạt! Bé quét sạch mẩu rác rồi!")
                        self._check_sweep()
                        return

            # 2. Dọn đồ chơi (Bấm vào món đồ chơi)
            for t in self.toys:
                if not t['stored']:
                    r = pygame.Rect(t['x'] - t['w']//2, t['y'] - t['h']//2, t['w'], t['h'])
                    if r.collidepoint(mx, my):
                        t['stored'] = True
                        self.game.sound_mgr.play('toy')
                        self.show_toast(f"Bính boong! Đã cất {t['name']} vào thùng đồ chơi!")
                        self._check_toys()
                        return

    def _check_sweep(self):
        if all(d['cleaned'] for d in self.dust_items) and not self.game.is_task_done(7):
            self.game.complete_task(7, "Tuyệt cú mèo! Sàn nhà đã quét sạch bóng loáng! (+1 điểm ⭐)")

    def _check_toys(self):
        if all(t['stored'] for t in self.toys) and not self.game.is_task_done(8):
            self.game.complete_task(8, "Hoan hô! Tất cả đồ chơi đã được cất ngăn nắp! (+1 điểm ⭐)")

    def update(self):
        self.tick += 1

    def draw(self, surface):
        w, h = self.game.width, self.game.height

        # Nền phòng khách ấm cúng
        surface.fill((255, 245, 230))
        # Sàn gạch gỗ sáng
        pygame.draw.rect(surface, (240, 205, 160), (0, 420, w, h - 420))
        for gy in range(450, h, 35):
            pygame.draw.line(surface, (215, 180, 135), (0, gy), (w, gy), 2)

        # Ghế sofa màu cam êm ái
        sofa_rect = pygame.Rect(120, 240, 320, 160)
        pygame.draw.rect(surface, (255, 140, 70), sofa_rect, border_radius=20)
        pygame.draw.rect(surface, (230, 110, 40), sofa_rect, width=4, border_radius=20)
        # Đệm ngồi
        pygame.draw.rect(surface, (255, 170, 110), (145, 310, 270, 70), border_radius=12)

        # Cây chổi quét nhà xinh xắn tựa vào tường
        broom_x = 80
        pygame.draw.line(surface, (180, 120, 70), (broom_x, 480), (broom_x + 15, 360), 6) # Cán chổi
        pygame.draw.polygon(surface, (240, 200, 80), [(broom_x - 15, 480), (broom_x + 15, 480), (broom_x, 440)]) # Lông chổi

        # VẼ CÁC MẨU BỤI / RÁC CẦN QUÉT
        for d in self.dust_items:
            if not d['cleaned']:
                # Vòng tròn chỉ thị nhẹ
                pulse = math.sin(self.tick * 0.15 + d['x']) * 2
                pygame.draw.circle(surface, (255, 255, 200), (d['x'], d['y']), 16 + int(pulse))
                if d['type'] == 'leaf':
                    pygame.draw.ellipse(surface, (100, 160, 60), (d['x'] - 10, d['y'] - 6, 20, 12))
                elif d['type'] == 'paper':
                    pygame.draw.rect(surface, (255, 255, 255), (d['x'] - 8, d['y'] - 8, 16, 16))
                    pygame.draw.rect(surface, (180, 180, 180), (d['x'] - 8, d['y'] - 8, 16, 16), 1)
                else:
                    pygame.draw.circle(surface, (150, 130, 110), (d['x'], d['y']), 6)

        # THÙNG ĐỒ CHƠI MÀU XANH NGỌC BÍCH
        bx, by, bw, bh = self.toy_box_rect.x, self.toy_box_rect.y, self.toy_box_rect.w, self.toy_box_rect.h
        pygame.draw.rect(surface, (60, 195, 175), (bx, by + 20, bw, bh - 20), border_radius=14)
        pygame.draw.rect(surface, (40, 160, 140), (bx, by + 20, bw, bh - 20), width=4, border_radius=14)
        # Nắp thùng
        pygame.draw.rect(surface, (255, 215, 60), (bx - 8, by + 8, bw + 16, 24), border_radius=8)
        f_box = pygame.font.SysFont('Segoe UI', 15, bold=True)
        txt_b = f_box.render("Thùng Đồ Chơi 🧸", True, (255, 255, 255))
        surface.blit(txt_b, (bx + bw // 2 - txt_b.get_width() // 2, by + 45))

        # CÁC MÓN ĐỒ CHƠI DƯỚI THẢM
        for t in self.toys:
            if not t['stored']:
                pulse = math.sin(self.tick * 0.12 + t['x']) * 3
                ty = t['y'] + pulse
                # Vòng sáng bao quanh
                pygame.draw.circle(surface, (255, 255, 150), (t['x'], int(ty)), 26)
                if t['name'] == 'Gấu Teddy':
                    # Vẽ gấu bông mini
                    pygame.draw.circle(surface, t['color'], (t['x'], int(ty)), 16) # Đầu
                    pygame.draw.circle(surface, t['color'], (t['x'] - 12, int(ty) - 12), 6) # Tai
                    pygame.draw.circle(surface, t['color'], (t['x'] + 12, int(ty) - 12), 6)
                    pygame.draw.circle(surface, (255, 255, 255), (t['x'], int(ty) + 4), 6) # Mõm
                elif t['name'] == 'Ô tô mini':
                    pygame.draw.rect(surface, t['color'], (t['x'] - 18, int(ty) - 10, 36, 20), border_radius=4)
                    pygame.draw.circle(surface, (30, 30, 30), (t['x'] - 10, int(ty) + 10), 5)
                    pygame.draw.circle(surface, (30, 30, 30), (t['x'] + 10, int(ty) + 10), 5)
                elif t['name'] == 'Lego khối':
                    pygame.draw.rect(surface, (255, 60, 60), (t['x'] - 14, int(ty) - 14, 28, 10))
                    pygame.draw.rect(surface, (255, 215, 0), (t['x'] - 14, int(ty) - 4, 28, 10))
                    pygame.draw.rect(surface, (40, 160, 240), (t['x'] - 14, int(ty) + 6, 28, 10))
                else: # Quả bóng sọc
                    pygame.draw.circle(surface, t['color'], (t['x'], int(ty)), 16)
                    pygame.draw.line(surface, (255, 70, 70), (t['x'] - 16, int(ty)), (t['x'] + 16, int(ty)), 5)

                # Tên món đồ
                f_tn = pygame.font.SysFont('Segoe UI', 11, bold=True)
                lbl = f_tn.render(t['name'], True, (70, 70, 80))
                surface.blit(lbl, (t['x'] - lbl.get_width() // 2, int(ty) + 20))

        # VẼ THẮM & THƠ ĐỨNG CỔ VŨ
        graphics.draw_character(surface, 510, 370, "Tham", scale=1.1,
                                is_cheering=self.game.is_task_done(7) and self.game.is_task_done(8), tick=self.tick)
        graphics.draw_character(surface, 580, 385, "Tho", scale=1.1,
                                is_cheering=self.game.is_task_done(7) and self.game.is_task_done(8), tick=self.tick + 10)

        # Hướng dẫn nhiệm vụ trên màn hình
        f_hint = pygame.font.SysFont('Segoe UI', 14, bold=True)
        if not self.game.is_task_done(7):
            t = f_hint.render("👉 Nhiệm vụ 7: Bấm vào các mẩu bụi/rác trên sàn để quét nhà nhé!", True, (160, 80, 20))
            surface.blit(t, (140, 190))
        if not self.game.is_task_done(8):
            t = f_hint.render("👉 Nhiệm vụ 8: Bấm vào các món đồ chơi để cất gọn vào thùng!", True, (20, 130, 120))
            surface.blit(t, (140, 215))

        # Nút chuyển tiếp tới màn Chiến Thắng
        if self.game.is_task_done(7) and self.game.is_task_done(8):
            pulse = int(math.sin(self.tick * 0.15) * 4)
            r = self.btn_next.inflate(pulse, pulse)
            pygame.draw.rect(surface, (255, 120, 0), r, border_radius=18)
            pygame.draw.rect(surface, (255, 255, 255), r, width=3, border_radius=18)
            f_btn = pygame.font.SysFont('Segoe UI', 19, bold=True)
            txt = f_btn.render("🎆 Xem Chiến Thắng & Pháo Hoa ➔", True, (255, 255, 255))
            surface.blit(txt, (r.centerx - txt.get_width() // 2, r.centery - txt.get_height() // 2))

        self.draw_hud_message(surface)


# ==========================================================
# CẢNH 7: MÀN HÌNH CHIẾN THẮNG & PHÁO HOA RỰC RỠ
# ==========================================================
class SceneVictory(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.fireworks = graphics.FireworksEngine(game.width, game.height, game.sound_mgr)
        self.btn_replay = pygame.Rect(game.width // 2 - 135, 570, 270, 54)
        
        # Nút nghe lại giọng nói ngọt ngào của mẹ / lời chúc
        self.btn_voice1 = pygame.Rect(game.width // 2 - 250, 508, 240, 46)
        self.btn_voice2 = pygame.Rect(game.width // 2 + 10, 508, 240, 46)
        
        self.fanfare_played = False
        self.voice_played = False
        self.voice_delay = 45  # Chờ 0.75s sau tiếng kèn fanfare thì giọng nữ cất lên

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if self.btn_replay.collidepoint(mx, my):
                self.game.reset_game()
            elif self.btn_voice1.collidepoint(mx, my):
                self.game.sound_mgr.play('voice_yeu_tham_tho')
                self.show_toast("❤ Yêu Thắm Thơ! ❤", 90)
            elif self.btn_voice2.collidepoint(mx, my):
                self.game.sound_mgr.play('voice_bo_me')
                self.show_toast("👨‍👩‍👧‍👧 Bố mẹ yêu hai em bé! 👨‍👩‍👧‍👧", 120)

    def update(self):
        self.tick += 1
        self.fireworks.update()
        
        # Phát nhạc kèn fanfare
        if not self.fanfare_played:
            self.fanfare_played = True
            self.game.sound_mgr.play('victory')
        
        # Tự động phát giọng nữ tiếng Việt "Yêu Thắm Thơ"
        if not self.voice_played:
            if self.voice_delay > 0:
                self.voice_delay -= 1
            else:
                self.voice_played = True
                self.game.sound_mgr.play('voice_yeu_tham_tho')

    def draw(self, surface):
        w, h = self.game.width, self.game.height

        # Nền bầu trời đêm ăn mừng lung linh ánh sao
        surface.fill((18, 20, 38))
        for i in range(40):
            sx = (i * 97 + self.tick) % w
            sy = (i * 53) % (h - 150)
            pygame.draw.circle(surface, (255, 255, 220), (sx, sy), 2)

        # Hiệu ứng pháo hoa và hoa giấy rực rỡ
        self.fireworks.draw(surface)

        # BẢNG TỔNG KẾT ĐIỂM SỐ 8/8 SAO
        star_y = 50
        for i in range(8):
            sx = w // 2 - 210 + i * 60
            pulse = math.sin(self.tick * 0.15 + i) * 3
            graphics.draw_star(surface, (sx, star_y + pulse), 20, (255, 225, 30), filled=True)

        # DÒNG CHỮ "CHIẾN THẮNG!" 3D RỰC RỠ KHỔNG LỒ
        font_big = pygame.font.SysFont('Segoe UI', 58, bold=True)
        txt_word = "CHIẾN THẮNG!"
        for off in range(5, 0, -1):
            s_sh = font_big.render(txt_word, True, (160, 40, 10))
            surface.blit(s_sh, (w // 2 - s_sh.get_width() // 2 + off, 95 + off))
        s_fg = font_big.render(txt_word, True, (255, 235, 60))
        surface.blit(s_fg, (w // 2 - s_fg.get_width() // 2, 95))

        # DÒNG CHỮ 1: "Bé Thắm, Bé Thơ giỏi quá!"
        font_praise = pygame.font.SysFont('Segoe UI', 32, bold=True)
        praise_txt = "Bé Thắm, Bé Thơ giỏi quá!"
        # Đổ bóng chữ
        surface.blit(font_praise.render(praise_txt, True, (180, 80, 0)), (w // 2 - font_praise.size(praise_txt)[0] // 2 + 2, 175))
        surface.blit(font_praise.render(praise_txt, True, (255, 240, 100)), (w // 2 - font_praise.size(praise_txt)[0] // 2, 173))

        # DÒNG CHỮ 2: "❤ Bố mẹ yêu hai em bé ❤"
        font_love = pygame.font.SysFont('Segoe UI', 28, bold=True)
        love_txt = "❤ Bố mẹ yêu hai em bé ❤"
        heart_pulse = int(math.sin(self.tick * 0.15) * 4)
        # Nền banner tình yêu bo tròn
        bw, bh = font_love.size(love_txt)[0] + 40, font_love.size(love_txt)[1] + 12
        bg_love = pygame.Rect(w // 2 - bw // 2, 222, bw, bh)
        pygame.draw.rect(surface, (230, 60, 110), bg_love.inflate(heart_pulse, heart_pulse), border_radius=18)
        pygame.draw.rect(surface, (255, 255, 255), bg_love.inflate(heart_pulse, heart_pulse), width=2, border_radius=18)
        surface.blit(font_love.render(love_txt, True, (255, 255, 255)), (w // 2 - font_love.size(love_txt)[0] // 2, 228))

        # CHÂN DUNG THẬT CỦA 2 BÉ TRONG KHUNG VÀNG LẤP LÁNH (2 BÊN)
        cx1, cx2 = w // 2 - 105, w // 2 + 105
        cy_char = 385
        
        # Ảnh thật chân dung 2 bé có khung vàng hoàng gia
        graphics.draw_avatar_portrait(surface, cx1 - 145, 360, "Tham", size=95)
        graphics.draw_avatar_portrait(surface, cx2 + 145, 360, "Tho", size=95)

        # VẼ 2 NHÂN VẬT THẮM & THƠ NHẢY MÚA VUI SƯỚNG VỚI VƯƠNG MIỆN Ở GIỮA
        graphics.draw_character(surface, cx1, cy_char, "Tham", scale=1.2, is_cheering=True, tick=self.tick)
        graphics.draw_character(surface, cx2, cy_char + 8, "Tho", scale=1.2, is_cheering=True, tick=self.tick + 10)
        
        # Vương miện vàng lấp lánh trên đầu Thắm & Thơ
        self._draw_crown(surface, cx1, cy_char - 38)
        self._draw_crown(surface, cx2, cy_char - 28)

        # Trái tim bay bổng xung quanh hai bé
        for hi, (hx, hy) in enumerate([(cx1 - 60, cy_char - 30), (cx2 + 60, cy_char - 30), (w // 2, cy_char - 40)]):
            hp = int(math.sin(self.tick * 0.12 + hi) * 5)
            self._draw_heart(surface, hx, hy + hp, 12)

        # HAI NÚT BẤM NGHE GIỌNG NÓI NỮ TIẾNG VIỆT
        f_voice = pygame.font.SysFont('Segoe UI', 15, bold=True)
        
        # Nút 1: Yêu Thắm Thơ
        p1 = int(math.sin(self.tick * 0.15) * 3)
        r_v1 = self.btn_voice1.inflate(p1, p1)
        pygame.draw.rect(surface, (255, 105, 180), r_v1, border_radius=14)
        pygame.draw.rect(surface, (255, 255, 255), r_v1, width=2, border_radius=14)
        t_v1 = f_voice.render("🔊 Nghe: \"Yêu Thắm Thơ\" ❤", True, (255, 255, 255))
        surface.blit(t_v1, (r_v1.centerx - t_v1.get_width() // 2, r_v1.centery - t_v1.get_height() // 2))

        # Nút 2: Lời chúc bố mẹ
        r_v2 = self.btn_voice2.inflate(p1, p1)
        pygame.draw.rect(surface, (70, 160, 240), r_v2, border_radius=14)
        pygame.draw.rect(surface, (255, 255, 255), r_v2, width=2, border_radius=14)
        t_v2 = f_voice.render("🔊 Lời Bố Mẹ Yêu Thương 👨‍👩‍👧‍👧", True, (255, 255, 255))
        surface.blit(t_v2, (r_v2.centerx - t_v2.get_width() // 2, r_v2.centery - t_v2.get_height() // 2))

        # NÚT CHƠI LẠI TỪ ĐẦU
        pulse_btn = int(math.sin(self.tick * 0.15) * 4)
        btn_r = self.btn_replay.inflate(pulse_btn, pulse_btn)
        pygame.draw.rect(surface, (255, 110, 0), btn_r, border_radius=18)
        pygame.draw.rect(surface, (255, 255, 255), btn_r, width=3, border_radius=18)
        f_btn = pygame.font.SysFont('Segoe UI', 21, bold=True)
        t_btn = f_btn.render("🔄 CHƠI LẠI TỪ ĐẦU", True, (255, 255, 255))
        surface.blit(t_btn, (btn_r.centerx - t_btn.get_width() // 2, btn_r.centery - t_btn.get_height() // 2))

        self.draw_hud_message(surface)

    def _draw_crown(self, surface, x, y):
        points = [
            (x - 18, y + 10), (x - 22, y - 6), (x - 9, y),
            (x, y - 10), (x + 9, y), (x + 22, y - 6), (x + 18, y + 10)
        ]
        pygame.draw.polygon(surface, (255, 215, 0), points)
        pygame.draw.polygon(surface, (230, 160, 0), points, width=2)
        pygame.draw.circle(surface, (255, 50, 50), (x, y - 10), 3)

    def _draw_heart(self, surface, x, y, size):
        """Vẽ biểu tượng trái tim tình yêu nhỏ xinh."""
        r = size // 2
        pygame.draw.circle(surface, (255, 80, 120), (x - r // 2, y - r // 2), r)
        pygame.draw.circle(surface, (255, 80, 120), (x + r // 2, y - r // 2), r)
        pygame.draw.polygon(surface, (255, 80, 120), [
            (x - r, y - r // 4), (x + r, y - r // 4), (x, y + r)
        ])

