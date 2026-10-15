"""
graphics.py - Hệ thống đồ họa hoạt hình đáng yêu & Hiệu ứng pháo hoa
Dành riêng cho các bé 6-8 tuổi: Màu sắc tươi sáng, hình khối tròn trịa, biểu cảm sinh động.
"""

import math
import random
import pygame

# Bảng màu thân thiện với trẻ nhỏ
COLOR_BG_SKY = (175, 218, 252)
COLOR_GRASS = (130, 204, 102)
COLOR_ROAD = (120, 130, 145)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (35, 35, 45)
COLOR_PINK_THAM = (255, 120, 160)
COLOR_PINK_DARK = (230, 70, 120)
COLOR_YELLOW_THO = (255, 210, 60)
COLOR_YELLOW_DARK = (230, 170, 20)
COLOR_SKIN = (255, 224, 196)
COLOR_SKIN_BLUSH = (255, 170, 180)
COLOR_HAIR_BROWN = (90, 50, 30)
COLOR_HAIR_DARK = (60, 35, 20)
COLOR_CAR_BODY = (28, 30, 34)
COLOR_CAR_DARK = (14, 15, 18)
COLOR_CAR_SHINE = (70, 76, 88)
COLOR_CAR_WINDOW = (195, 220, 240)
COLOR_STAR_GOLD = (255, 215, 0)
COLOR_WOOD = (195, 140, 90)
COLOR_WOOD_DARK = (160, 105, 60)
COLOR_WALL_CREAM = (255, 248, 230)
COLOR_FLOOR_TILE = (245, 235, 220)

def draw_aa_circle(surface, color, center, radius):
    """Vẽ hình tròn mượt mà."""
    x, y = int(center[0]), int(center[1])
    r = int(radius)
    pygame.draw.circle(surface, color, (x, y), r)

def draw_shadow(surface, x, y, width, height):
    """Bóng mờ êm dưới chân nhân vật / đồ vật."""
    shadow_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surf, (0, 0, 0, 45), (0, 0, width, height))
    surface.blit(shadow_surf, (x - width // 2, y - height // 2))

def draw_star(surface, center, size, color=COLOR_STAR_GOLD, filled=True):
    """Vẽ ngôi sao 5 cánh lấp lánh."""
    cx, cy = center
    points = []
    for i in range(10):
        r = size if i % 2 == 0 else size * 0.45
        angle = i * math.pi / 5 - math.pi / 2
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        points.append((px, py))
    if filled:
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, (255, 245, 150), points, width=2)
    else:
        pygame.draw.polygon(surface, (180, 180, 190), points, width=2)

# Nạp ảnh chân dung thật của 2 bé Thắm & Thơ
AVATAR_THAM_IMG = None
AVATAR_THO_IMG = None

def get_avatar(name="Tham", size=48):
    """Nạp và co giãn ảnh thật của bé Thắm & Thơ."""
    global AVATAR_THAM_IMG, AVATAR_THO_IMG
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        if name == "Tham":
            if AVATAR_THAM_IMG is None:
                p = os.path.join(base_dir, 'assets', 'avatar_tham.png')
                if not os.path.exists(p):
                    p = os.path.join(base_dir, 'avatar_tham.png')
                if os.path.exists(p):
                    AVATAR_THAM_IMG = pygame.image.load(p).convert_alpha()
            if AVATAR_THAM_IMG:
                return pygame.transform.smoothscale(AVATAR_THAM_IMG, (size, size))
        else:
            if AVATAR_THO_IMG is None:
                p = os.path.join(base_dir, 'assets', 'avatar_tho.png')
                if not os.path.exists(p):
                    p = os.path.join(base_dir, 'avatar_tho.png')
                if os.path.exists(p):
                    AVATAR_THO_IMG = pygame.image.load(p).convert_alpha()
            if AVATAR_THO_IMG:
                return pygame.transform.smoothscale(AVATAR_THO_IMG, (size, size))
    except Exception as e:
        pass
    return None

def draw_avatar_portrait(surface, cx, cy, name="Tham", size=90):
    """Vẽ ảnh chân dung thật của bé có khung vàng và nơ trang trí lộng lẫy."""
    av = get_avatar(name, size)
    if av:
        # Bóng đổ
        draw_shadow(surface, cx, cy + size // 2 + 5, size + 10, 16)
        # Khung viền vàng lấp lánh
        pygame.draw.circle(surface, (255, 215, 0), (cx, cy), size // 2 + 5)
        pygame.draw.circle(surface, (255, 255, 255), (cx, cy), size // 2 + 3, 2)
        surface.blit(av, (cx - size // 2, cy - size // 2))
        # Bảng tên phía dưới
        tag_color = (255, 105, 180) if name == "Tham" else (255, 195, 20)
        font = pygame.font.SysFont('Segoe UI', 13, bold=True)
        txt = font.render("Bé Thắm" if name == "Tham" else "Bé Thơ", True, (255, 255, 255))
        tw, th = txt.get_size()
        tag_r = pygame.Rect(cx - tw // 2 - 8, cy + size // 2 - 4, tw + 16, th + 2)
        pygame.draw.rect(surface, tag_color, tag_r, border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), tag_r, width=1, border_radius=8)
        surface.blit(txt, (cx - tw // 2, cy + size // 2 - 3))

def draw_cute_backpack(surface, cx, cy, w=68, h=78, theme="tham", tick=0):
    """
    Vẽ chiếc cặp sách học sinh siêu xinh xắn, đáng yêu:
    - Quai xách đệm êm, khóa kéo kim loại, túi trước 3D, bình nước bên hông, huy hiệu dâu tây/ngôi sao.
    """
    pulse = math.sin(tick * 0.1) * 2 if tick > 0 else 0
    y = cy + pulse

    # Bóng dưới đáy cặp
    draw_shadow(surface, cx, int(y + h // 2 + 4), w + 12, 14)

    # Bảng màu cặp
    if theme == "tham":
        col_main = (255, 110, 160)     # Hồng dâu tây tươi tắn
        col_dark = (220, 60, 110)
        col_pouch = (255, 170, 200)
        col_zipper = (255, 240, 245)
        badge_name = "Tham"
    else:
        col_main = (255, 200, 25)      # Vàng chanh rực rỡ
        col_dark = (220, 150, 0)
        col_pouch = (255, 230, 120)
        col_zipper = (255, 250, 220)
        badge_name = "Tho"

    # 1. Quai xách trên đỉnh cặp
    handle_rect = pygame.Rect(cx - 16, int(y - h // 2 - 8), 32, 16)
    pygame.draw.arc(surface, col_dark, handle_rect, 0, math.pi, 5)

    # 2. Hai quai đeo sau lưng (thò nhẹ sang 2 bên)
    pygame.draw.rect(surface, col_dark, (cx - w // 2 - 4, int(y - h // 2 + 10), 8, h - 20), border_radius=4)
    pygame.draw.rect(surface, col_dark, (cx + w // 2 - 4, int(y - h // 2 + 10), 8, h - 20), border_radius=4)

    # 3. Thân cặp chính (Bo góc tròn trịa 3D)
    main_rect = pygame.Rect(cx - w // 2, int(y - h // 2), w, h)
    pygame.draw.rect(surface, col_main, main_rect, border_radius=16)
    pygame.draw.rect(surface, col_dark, main_rect, width=3, border_radius=16)

    # Đường viền phản quang trắng sáng ngang trên
    pygame.draw.line(surface, col_zipper, (cx - w // 2 + 8, int(y - h // 2 + 18)), (cx + w // 2 - 8, int(y - h // 2 + 18)), 3)

    # 4. Túi phụ mặt trước cặp
    pouch_w = w - 16
    pouch_h = int(h * 0.48)
    pouch_rect = pygame.Rect(cx - pouch_w // 2, int(y + h // 2 - pouch_h - 6), pouch_w, pouch_h)
    pygame.draw.rect(surface, col_pouch, pouch_rect, border_radius=12)
    pygame.draw.rect(surface, col_dark, pouch_rect, width=2, border_radius=12)

    # Khóa kéo túi trước
    pygame.draw.line(surface, (230, 230, 240), (pouch_rect.x + 8, pouch_rect.y + 8), (pouch_rect.right - 8, pouch_rect.y + 8), 2)
    # Tay kéo khóa
    pygame.draw.rect(surface, (255, 220, 0), (cx - 3, pouch_rect.y + 5, 6, 8), border_radius=2)

    # 5. Huy hiệu hoạt hình dễ thương ở giữa túi
    if theme == "tham":
        # Quả dâu tây / hoa hồng xinh
        pygame.draw.circle(surface, (255, 50, 80), (cx, int(pouch_rect.centery + 4)), 10)
        pygame.draw.circle(surface, (100, 220, 80), (cx, int(pouch_rect.centery - 5)), 4)
    else:
        # Ngôi sao lấp lánh
        draw_star(surface, (cx, int(pouch_rect.centery + 4)), 11, (255, 230, 40))

    # 6. Bình nước mini xinh xắn cài bên hông
    bottle_rect = pygame.Rect(cx + w // 2 - 3, int(y - 5), 8, 22)
    pygame.draw.rect(surface, (120, 215, 255), bottle_rect, border_radius=4)
    pygame.draw.rect(surface, (255, 255, 255), (cx + w // 2 - 2, int(y - 8), 6, 5), border_radius=2)

    # Tên bé in xinh xắn
    font_b = pygame.font.SysFont('Segoe UI', 11, bold=True)
    t_name = font_b.render("Thắm" if theme == "tham" else "Thơ", True, (60, 60, 70))
    surface.blit(t_name, (cx - t_name.get_width() // 2, int(y - h // 2 + 5)))

def draw_cute_shoes(surface, cx, cy, theme="tham", tick=0):
    """
    Vẽ đôi giày thể thao học sinh xinh xắn có nơ buộc dây:
    - Đế cao su trắng viền rãnh, mũi giày trắng, thân giày màu pastel, nơ dây giày xinh xắn.
    """
    pulse = math.sin(tick * 0.12) * 2 if tick > 0 else 0
    y = cy + pulse

    # Bóng dưới đôi giày
    draw_shadow(surface, cx, int(y + 12), 80, 16)

    if theme == "tham":
        col_shoe = (255, 120, 160)     # Giày hồng Thắm
        col_dark = (220, 60, 110)
        badge_col = (255, 230, 240)
    else:
        col_shoe = (255, 210, 45)      # Giày vàng Thơ
        col_dark = (220, 160, 10)
        badge_col = (255, 255, 220)

    # Vẽ lần lượt Chiếc Trái và Chiếc Phải
    for sign, off_x in [(-1, cx - 22), (1, cx + 22)]:
        # 1. Thân giày uốn lượn
        shoe_rect = pygame.Rect(off_x - 18, int(y - 12), 36, 22)
        pygame.draw.ellipse(surface, col_shoe, shoe_rect)
        pygame.draw.ellipse(surface, col_dark, shoe_rect, width=2)

        # 2. Mũi giày cao su màu trắng
        toe_x = off_x - 17 if sign == -1 else off_x + 3
        pygame.draw.ellipse(surface, (255, 255, 255), (toe_x, int(y - 8), 14, 16))

        # 3. Đế giày cao su trắng dày
        pygame.draw.rect(surface, (255, 255, 255), (off_x - 17, int(y + 2), 34, 7), border_radius=3)
        pygame.draw.line(surface, (180, 185, 195), (off_x - 16, int(y + 5)), (off_x + 16, int(y + 5)), 2)

        # 4. Dây giày đan chéo trắng & Nơ bướm xinh xắn 🎀
        pygame.draw.line(surface, (255, 255, 255), (off_x - 6, int(y - 6)), (off_x + 6, int(y - 2)), 2)
        pygame.draw.line(surface, (255, 255, 255), (off_x + 6, int(y - 6)), (off_x - 6, int(y - 2)), 2)
        # Nơ nhỏ trên lưỡi gà
        pygame.draw.circle(surface, (255, 255, 255), (off_x, int(y - 8)), 3)
        pygame.draw.circle(surface, badge_col, (off_x - 4, int(y - 8)), 3)
        pygame.draw.circle(surface, badge_col, (off_x + 4, int(y - 8)), 3)

def draw_character(surface, x, y, name="Tham", scale=1.0, is_walking=False, is_cheering=False, tick=0):
    """
    Vẽ 2 bé gái Thắm & Thơ:
    - Tự động nạp và hiển thị khuôn mặt thật từ ảnh chụp của 2 bé!
    - Váy áo xinh xắn, cử chỉ vẫy tay, nhảy múa ăn mừng sinh động.
    """
    bob = int(math.sin(tick * 0.1) * 3) if is_cheering or is_walking else 0
    
    # Bóng chân
    draw_shadow(surface, x, y + int(75 * scale), int(60 * scale), int(16 * scale))
    
    cy = y + bob
    
    if name == "Tham":
        dress_color = COLOR_PINK_THAM
        dress_border = COLOR_PINK_DARK
        bow_color = (255, 80, 120)
        hair_color = COLOR_HAIR_BROWN
        shoe_color = (255, 100, 140)
    else:
        dress_color = COLOR_YELLOW_THO
        dress_border = COLOR_YELLOW_DARK
        bow_color = (255, 140, 0)
        hair_color = COLOR_HAIR_DARK
        shoe_color = (255, 180, 20)
        scale *= 0.94

    # 1. Chân & Giày
    leg_l_x = x - int(12 * scale)
    leg_r_x = x + int(12 * scale)
    leg_y = cy + int(45 * scale)
    leg_h = int(25 * scale)
    
    pygame.draw.rect(surface, COLOR_SKIN, (leg_l_x - int(4 * scale), leg_y, int(8 * scale), leg_h), border_radius=4)
    pygame.draw.rect(surface, COLOR_SKIN, (leg_r_x - int(4 * scale), leg_y, int(8 * scale), leg_h), border_radius=4)
    pygame.draw.ellipse(surface, shoe_color, (leg_l_x - int(8 * scale), leg_y + leg_h - int(6 * scale), int(16 * scale), int(10 * scale)))
    pygame.draw.ellipse(surface, shoe_color, (leg_r_x - int(8 * scale), leg_y + leg_h - int(6 * scale), int(16 * scale), int(10 * scale)))

    # 2. Váy áo xoè
    body_y = cy + int(15 * scale)
    skirt_points = [
        (x - int(14 * scale), body_y),
        (x + int(14 * scale), body_y),
        (x + int(26 * scale), body_y + int(36 * scale)),
        (x - int(26 * scale), body_y + int(36 * scale))
    ]
    pygame.draw.polygon(surface, dress_color, skirt_points)
    pygame.draw.polygon(surface, dress_border, skirt_points, width=2)
    # Cổ áo trắng
    pygame.draw.polygon(surface, COLOR_WHITE, [
        (x - int(8 * scale), body_y),
        (x, body_y + int(8 * scale)),
        (x + int(8 * scale), body_y)
    ])

    # 3. Cánh tay
    hand_y = body_y + int(10 * scale)
    if is_cheering:
        pygame.draw.line(surface, COLOR_SKIN, (x - int(14 * scale), hand_y), (x - int(26 * scale), hand_y - int(18 * scale)), int(6 * scale))
        pygame.draw.line(surface, COLOR_SKIN, (x + int(14 * scale), hand_y), (x + int(26 * scale), hand_y - int(18 * scale)), int(6 * scale))
        draw_aa_circle(surface, COLOR_SKIN, (x - int(26 * scale), hand_y - int(18 * scale)), int(4 * scale))
        draw_aa_circle(surface, COLOR_SKIN, (x + int(26 * scale), hand_y - int(18 * scale)), int(4 * scale))
    else:
        pygame.draw.line(surface, COLOR_SKIN, (x - int(14 * scale), hand_y), (x - int(20 * scale), hand_y + int(15 * scale)), int(6 * scale))
        pygame.draw.line(surface, COLOR_SKIN, (x + int(14 * scale), hand_y), (x + int(20 * scale), hand_y + int(15 * scale)), int(6 * scale))
        draw_aa_circle(surface, COLOR_SKIN, (x - int(20 * scale), hand_y + int(15 * scale)), int(4 * scale))
        draw_aa_circle(surface, COLOR_SKIN, (x + int(20 * scale), hand_y + int(15 * scale)), int(4 * scale))

    # 4. Khuôn mặt nhân vật: DÙNG ẢNH THẬT CỦA BÉ NẾU CÓ!
    head_y = cy - int(8 * scale)
    head_size = int(52 * scale)
    
    avatar_img = get_avatar(name, head_size)
    if avatar_img:
        # Hiển thị mặt thật của bé
        surface.blit(avatar_img, (x - head_size // 2, head_y - head_size // 2))
        # Nơ hoa kẹp tóc xinh xắn trên ảnh thật
        if name == "Tham":
            draw_aa_circle(surface, bow_color, (x - int(20 * scale), head_y - int(22 * scale)), int(6 * scale))
            draw_aa_circle(surface, (255, 255, 255), (x - int(20 * scale), head_y - int(22 * scale)), int(3 * scale))
        else:
            draw_aa_circle(surface, bow_color, (x + int(18 * scale), head_y - int(22 * scale)), int(6 * scale))
            draw_aa_circle(surface, (255, 255, 255), (x + int(18 * scale), head_y - int(22 * scale)), int(3 * scale))
    else:
        # Fallback vẽ hoạt hình nếu chưa nạp được ảnh
        head_r = int(22 * scale)
        if name == "Tham":
            draw_aa_circle(surface, hair_color, (x - int(24 * scale), head_y - int(6 * scale)), int(12 * scale))
            draw_aa_circle(surface, hair_color, (x + int(24 * scale), head_y - int(6 * scale)), int(12 * scale))
            draw_aa_circle(surface, bow_color, (x - int(20 * scale), head_y - int(12 * scale)), int(6 * scale))
            draw_aa_circle(surface, bow_color, (x + int(20 * scale), head_y - int(12 * scale)), int(6 * scale))
        else:
            draw_aa_circle(surface, hair_color, (x, head_y - int(24 * scale)), int(14 * scale))
            draw_aa_circle(surface, bow_color, (x, head_y - int(16 * scale)), int(7 * scale))

        draw_aa_circle(surface, COLOR_SKIN, (x, head_y), head_r)
        pygame.draw.arc(surface, hair_color, (x - head_r, head_y - head_r, head_r * 2, head_r * 1.5), 0, math.pi, int(10 * scale))
        eye_offset = int(7 * scale)
        eye_r = int(4 * scale)
        draw_aa_circle(surface, COLOR_BLACK, (x - eye_offset, head_y - int(2 * scale)), eye_r)
        draw_aa_circle(surface, COLOR_WHITE, (x - eye_offset - 1, head_y - int(3 * scale)), int(1.5 * scale))
        draw_aa_circle(surface, COLOR_BLACK, (x + eye_offset, head_y - int(2 * scale)), eye_r)
        draw_aa_circle(surface, COLOR_WHITE, (x + eye_offset - 1, head_y - int(3 * scale)), int(1.5 * scale))
        draw_aa_circle(surface, COLOR_SKIN_BLUSH, (x - int(12 * scale), head_y + int(5 * scale)), int(4.5 * scale))
        draw_aa_circle(surface, COLOR_SKIN_BLUSH, (x + int(12 * scale), head_y + int(5 * scale)), int(4.5 * scale))
        pygame.draw.arc(surface, (220, 70, 70), (x - int(5 * scale), head_y + int(3 * scale), int(10 * scale), int(7 * scale)), math.pi, 2 * math.pi, 2)

    # 5. Bảng tên nhân vật bên dưới
    font = pygame.font.SysFont('Segoe UI', int(15 * scale), bold=True)
    tag = "Bé Thắm" if name == "Tham" else "Bé Thơ"
    tag_surf = font.render(tag, True, (50, 50, 60))
    tw, th = tag_surf.get_size()
    bg_tag = pygame.Rect(x - tw//2 - 6, cy + int(76 * scale), tw + 12, th + 2)
    pygame.draw.rect(surface, COLOR_WHITE, bg_tag, border_radius=8)
    pygame.draw.rect(surface, dress_color, bg_tag, width=2, border_radius=8)
    surface.blit(tag_surf, (x - tw//2, cy + int(77 * scale)))



class FireworkParticle:
    """Hạt tia lửa của pháo hoa rực rỡ."""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2.0, 9.0)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.gravity = 0.12
        self.alpha = 255
        self.fade = random.uniform(3.0, 6.0)
        self.radius = random.uniform(2.5, 4.5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= 0.98
        self.alpha -= self.fade
        return self.alpha > 0

    def draw(self, surface):
        if self.alpha <= 0:
            return
        surf = pygame.Surface((int(self.radius * 2 + 2), int(self.radius * 2 + 2)), pygame.SRCALPHA)
        c = (*self.color[:3], int(max(0, min(255, self.alpha))))
        pygame.draw.circle(surf, c, (surf.get_width() // 2, surf.get_height() // 2), int(self.radius))
        surface.blit(surf, (self.x - surf.get_width() // 2, self.y - surf.get_height() // 2))


class FireworkRocket:
    """Tên lửa pháo hoa bay vút lên trời rồi bung nổ."""
    def __init__(self, start_x, target_y, color, sound_mgr=None):
        self.x = start_x
        self.y = 650
        self.target_y = target_y
        self.vy = random.uniform(-13.0, -10.0)
        self.color = color
        self.exploded = False
        self.sound_mgr = sound_mgr
        if self.sound_mgr:
            self.sound_mgr.play('firework_up')

    def update(self):
        self.y += self.vy
        self.vy += 0.08  # Giảm tốc nhẹ
        if self.y <= self.target_y or self.vy >= -1.0:
            self.exploded = True
            if self.sound_mgr:
                self.sound_mgr.play('firework_boom')
            return True
        return False

    def draw(self, surface):
        # Tia sáng vút lên
        pygame.draw.line(surface, (255, 255, 200), (self.x, self.y), (self.x, self.y + 12), 3)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 4)


class ConfettiPiece:
    """Mảnh giấy kim tuyến ăn mừng rơi lả tả."""
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.x = random.randint(20, w - 20)
        self.y = random.randint(-100, 0)
        self.color = random.choice([
            (255, 75, 75), (255, 215, 0), (75, 205, 255),
            (100, 230, 100), (255, 130, 200), (180, 100, 255)
        ])
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(2.0, 5.0)
        self.size = random.randint(6, 11)
        self.rot = random.uniform(0, 360)
        self.rot_speed = random.uniform(-6, 6)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rot += self.rot_speed
        if self.y > self.h:
            self.y = -10
            self.x = random.randint(20, self.w - 20)

    def draw(self, surface):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, self.size, self.size))
        rotated = pygame.transform.rotate(surf, self.rot)
        surface.blit(rotated, (self.x, self.y))


class FireworksEngine:
    """Bộ xử lý pháo hoa và hoa giấy rực rỡ chào mừng CHIẾN THẮNG."""
    def __init__(self, width, height, sound_mgr=None):
        self.width = width
        self.height = height
        self.sound_mgr = sound_mgr
        self.rockets = []
        self.particles = []
        self.confetti = [ConfettiPiece(width, height) for _ in range(70)]
        self.timer = 0
        self.colors = [
            (255, 50, 80), (255, 220, 40), (40, 200, 255),
            (80, 255, 120), (255, 120, 220), (255, 160, 40),
            (180, 100, 255), (255, 255, 255)
        ]

    def launch_random(self):
        x = random.randint(120, self.width - 120)
        y = random.randint(80, 260)
        col = random.choice(self.colors)
        self.rockets.append(FireworkRocket(x, y, col, self.sound_mgr))

    def update(self):
        self.timer += 1
        if self.timer % 30 == 0:
            self.launch_random()

        # Cập nhật tên lửa
        for r in self.rockets[:]:
            if r.update():
                # Nổ ra các hạt
                for _ in range(random.randint(60, 90)):
                    self.particles.append(FireworkParticle(r.x, r.y, r.color))
                self.rockets.remove(r)

        # Cập nhật hạt pháo hoa
        for p in self.particles[:]:
            if not p.update():
                self.particles.remove(p)

        # Cập nhật hoa giấy
        for c in self.confetti:
            c.update()

    def draw(self, surface):
        for r in self.rockets:
            r.draw(surface)
        for p in self.particles:
            p.draw(surface)
        for c in self.confetti:
            c.draw(surface)
