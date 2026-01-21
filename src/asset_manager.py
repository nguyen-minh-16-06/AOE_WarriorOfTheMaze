import pygame
import os
from src.config import ASSET_CONFIG, TILE_WIDTH, TILE_HEIGHT

class AssetManager:
    def __init__(self):
        self.assets = {k: [] for k in ASSET_CONFIG.keys()}
        self.agent_image = None
        self.goal_image = None
        self._load_all_assets()

    def _load_all_assets(self):
        valid_ext = ('.png', '.webp', '.jpg')

        for key, path in ASSET_CONFIG.items():
            if not os.path.exists(path):
                print(f"Warning: Path not found {path}")
                continue

            files = []
            for root, _, filenames in os.walk(path):
                for f in filenames:
                    if f.lower().endswith(valid_ext):
                        files.append(os.path.join(root, f))
            files.sort()

            # ===== AGENT & GOAL =====
            if key in ['agent', 'goal']:
                target_file = next((f for f in files if 'idle' in f.lower()), files[0] if files else None)
                if target_file:
                    try:
                        img = pygame.image.load(target_file).convert_alpha()

                        cw = min(128, img.get_width())
                        ch = min(128, img.get_height())
                        img = img.subsurface((0, 0, cw, ch))
                        final_img = self._scale_proportional(img, 60)

                        if key == 'agent':
                            self.agent_image = final_img
                        else:
                            self.goal_image = final_img
                    except Exception as e:
                        print(f"Error loading {key}: {e}")

                if key == 'agent' and not self.agent_image:
                    self.agent_image = self._create_fallback((200, 50, 50))
                elif key == 'goal' and not self.goal_image:
                    self.goal_image = self._create_fallback((50, 50, 200))
                continue

            # ===== OTHER ASSETS =====
            for f in files:
                try:
                    img = pygame.image.load(f).convert_alpha()
                    if key == 'floor':
                        img = pygame.transform.scale(img, (TILE_WIDTH, TILE_HEIGHT * 2))
                    elif key == 'wall':
                        img = self._scale_proportional(img, 80)
                    else:
                        img = self._scale_proportional(img, 50)
                    self.assets[key].append(img)
                except:
                    pass

    # ===== HELPER METHODS =====
    def _create_fallback(self, color):
        s = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (20, 20), 15)
        return s

    def _scale_proportional(self, img, target_h):
        w, h = img.get_size()
        if h == 0: return img
        scale = target_h / h
        return pygame.transform.scale(img, (int(w * scale), int(h * scale)))

    def get_image(self, key, seed=0):
        imgs = self.assets.get(key, [])
        if not imgs: return None
        return imgs[seed % len(imgs)]