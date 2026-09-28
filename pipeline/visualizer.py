from typing import List, Dict, Any, Optional
import numpy as np
import cv2


class Visualizer:
    """Draws visual annotations, bounding boxes, and HUD metrics on video frames."""

    # Colors in BGR
    COLOR_VEHICLE = (255, 178, 50)     # Vibrant Sky Blue / Cyan
    COLOR_PLATE = (0, 255, 128)        # Neon Spring Green
    COLOR_BG = (24, 24, 27)            # Dark slate background for text badges
    COLOR_WHITE = (255, 255, 255)
    COLOR_ACCENT = (0, 215, 255)       # Gold/Amber accent

    def __init__(self, show_plate_zoom: bool = True):
        self.show_plate_zoom = show_plate_zoom
        self.last_plate_crop: Optional[np.ndarray] = None

    def draw_badge(
        self,
        image: np.ndarray,
        text: str,
        origin: tuple,
        bg_color: tuple,
        text_color: tuple = (255, 255, 255),
        font_scale: float = 0.5,
        thickness: int = 1,
        padding: int = 4,
    ):
        """Draw a sleek rounded-like filled badge with text."""
        font = cv2.FONT_HERSHEY_SIMPLEX
        (tw, th), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        x, y = origin

        bx1 = x
        by1 = max(0, y - th - padding * 2)
        bx2 = x + tw + padding * 2
        by2 = y

        # Ensure inside frame
        h, w = image.shape[:2]
        bx2 = min(w - 1, bx2)
        by2 = min(h - 1, by2)

        cv2.rectangle(image, (bx1, by1), (bx2, by2), bg_color, -1)
        cv2.rectangle(image, (bx1, by1), (bx2, by2), text_color, 1)
        cv2.putText(
            image,
            text,
            (bx1 + padding, by2 - padding),
            font,
            font_scale,
            text_color,
            thickness,
            cv2.LINE_AA,
        )

    def annotate(
        self,
        frame: np.ndarray,
        vehicles: List[Dict[str, Any]],
        plates: List[Dict[str, Any]],
        fps: float = 0.0,
    ) -> np.ndarray:
        """
        Draw all vehicle boxes, license plate boxes, labels, and HUD on the frame.
        """
        annotated = frame.copy()
        h_frame, w_frame = annotated.shape[:2]

        # 1. Draw Vehicles
        for veh in vehicles:
            vx1, vy1, vx2, vy2 = veh["bbox"]
            cv2.rectangle(annotated, (vx1, vy1), (vx2, vy2), self.COLOR_VEHICLE, 2)

            label_parts = []
            if veh.get("track_id") is not None:
                label_parts.append(f"#{veh['track_id']}")
            label_parts.append(veh["cls_name"].capitalize())
            label_parts.append(f"{veh['conf']:.2f}")
            label = " ".join(label_parts)

            self.draw_badge(
                annotated,
                label,
                (vx1, vy1),
                bg_color=self.COLOR_BG,
                text_color=self.COLOR_VEHICLE,
                font_scale=0.45,
                thickness=1,
            )

        # 2. Draw Number Plates
        for plate in plates:
            px1, py1, px2, py2 = plate["bbox"]
            # Draw a thicker, vibrant neon box around plate
            cv2.rectangle(annotated, (px1, py1), (px2, py2), self.COLOR_PLATE, 2)

            p_label = f"Plate {plate['conf']:.2f}"
            if plate.get("vehicle_track_id") is not None:
                p_label = f"Plate #{plate['vehicle_track_id']} ({plate['conf']:.2f})"

            self.draw_badge(
                annotated,
                p_label,
                (px1, py1),
                bg_color=self.COLOR_BG,
                text_color=self.COLOR_PLATE,
                font_scale=0.45,
                thickness=1,
            )

            # Store the latest valid plate crop for thumbnail display
            crop = plate.get("plate_crop")
            if crop is not None and crop.size > 0:
                ch, cw = crop.shape[:2]
                if cw >= 40 and ch >= 12:
                    self.last_plate_crop = crop

        # 3. Draw Floating Pill HUD Badge
        hud_text = f"FPS: {fps:.1f} | Vehicles: {len(vehicles)} | Plates: {len(plates)}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.55
        thickness = 2
        (tw, th), _ = cv2.getTextSize(hud_text, font, font_scale, thickness)

        pill_pad_x = 14
        pill_pad_y = 8
        pill_x1 = 16
        pill_y1 = 14
        pill_x2 = pill_x1 + tw + (pill_pad_x * 2)
        pill_y2 = pill_y1 + th + (pill_pad_y * 2)

        hud_overlay = annotated.copy()
        cv2.rectangle(hud_overlay, (pill_x1, pill_y1), (pill_x2, pill_y2), (20, 20, 24), -1)
        cv2.rectangle(hud_overlay, (pill_x1, pill_y1), (pill_x2, pill_y2), (70, 70, 80), 1)
        cv2.addWeighted(hud_overlay, 0.85, annotated, 0.15, 0, annotated)

        cv2.putText(
            annotated,
            hud_text,
            (pill_x1 + pill_pad_x, pill_y2 - pill_pad_y),
            font,
            font_scale,
            self.COLOR_WHITE,
            thickness,
            cv2.LINE_AA,
        )

        # 4. Optional Plate Thumbnail Zoom in Top-Right
        if self.show_plate_zoom and self.last_plate_crop is not None:
            thumb_w = 210
            crop_h, crop_w = self.last_plate_crop.shape[:2]
            if crop_h > 0 and crop_w > 0:
                aspect = crop_h / float(crop_w)
                thumb_h = max(45, min(105, int(thumb_w * aspect)))
                resized_plate = cv2.resize(self.last_plate_crop, (thumb_w, thumb_h))

                tx1 = w_frame - thumb_w - 16
                ty1 = 14
                tx2 = tx1 + thumb_w
                ty2 = ty1 + thumb_h

                if tx1 >= 0 and ty2 < h_frame:
                    annotated[ty1:ty2, tx1:tx2] = resized_plate
                    cv2.rectangle(annotated, (tx1, ty1), (tx2, ty2), self.COLOR_PLATE, 2)
                    self.draw_badge(
                        annotated,
                        "Latest Detected Plate",
                        (tx1, ty1),
                        bg_color=self.COLOR_BG,
                        text_color=self.COLOR_PLATE,
                        font_scale=0.42,
                    )

        return annotated
