from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import cv2
from ultralytics import YOLO


class PlateDetector:
    """Detects number / license plates using a fine-tuned YOLO model."""

    def __init__(
        self,
        model_path: str = "plate_model_v11n.pt",
        conf_threshold: float = 0.25,
        device: Optional[str] = None,
    ):
        """
        Initialize the license plate detector.

        Args:
            model_path: Path to license plate YOLO weights.
            conf_threshold: Confidence threshold for plate detections.
            device: 'cpu', 'cuda', etc.
        """
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.device = device
        self.class_names = self.model.names

    def _pad_bbox(
        self,
        bbox: List[int],
        frame_shape: Tuple[int, int],
        pad_ratio: float = 0.05,
    ) -> Tuple[int, int, int, int]:
        """Expand bbox slightly with padding clamped to frame bounds."""
        h_frame, w_frame = frame_shape[:2]
        x1, y1, x2, y2 = bbox
        bw = x2 - x1
        bh = y2 - y1

        pad_w = int(bw * pad_ratio)
        pad_h = int(bh * pad_ratio)

        px1 = max(0, x1 - pad_w)
        py1 = max(0, y1 - pad_h)
        px2 = min(w_frame, x2 + pad_w)
        py2 = min(h_frame, y2 + pad_h)

        return px1, py1, px2, py2

    def detect_in_vehicle_crops(
        self,
        frame: np.ndarray,
        vehicles: List[Dict[str, Any]],
        pad_ratio: float = 0.05,
        min_vehicle_size: int = 30,
    ) -> List[Dict[str, Any]]:
        """
        Detect plates by cropping each detected vehicle region.
        Greatly suppresses background false positives (signs, shop boards, etc.).

        Args:
            frame: Full BGR video frame.
            vehicles: Detected vehicles from VehicleDetector.
            pad_ratio: Padding around vehicle bounding box.
            min_vehicle_size: Minimum width/height for vehicle crop.

        Returns:
            List of detected plate dictionaries with coordinates mapped to original frame.
        """
        plate_detections: List[Dict[str, Any]] = []
        frame_h, frame_w = frame.shape[:2]

        for veh in vehicles:
            vx1, vy1, vx2, vy2 = veh["bbox"]
            if (vx2 - vx1) < min_vehicle_size or (vy2 - vy1) < min_vehicle_size:
                continue

            cx1, cy1, cx2, cy2 = self._pad_bbox([vx1, vy1, vx2, vy2], (frame_h, frame_w), pad_ratio)
            crop = frame[cy1:cy2, cx1:cx2]
            if crop.size == 0:
                continue

            results = self.model.predict(
                source=crop,
                conf=self.conf_threshold,
                device=self.device,
                verbose=False,
            )

            if not results or len(results) == 0:
                continue

            res = results[0]
            if res.boxes is None or len(res.boxes) == 0:
                continue

            boxes = res.boxes.xyxy.cpu().numpy()
            confs = res.boxes.conf.cpu().numpy()

            for p_bbox, p_conf in zip(boxes, confs):
                # Map relative coordinates back to full frame coordinates
                px1 = int(cx1 + p_bbox[0])
                py1 = int(cy1 + p_bbox[1])
                px2 = int(cx1 + p_bbox[2])
                py2 = int(cy1 + p_bbox[3])

                # Clamp to frame
                px1 = max(0, min(frame_w - 1, px1))
                py1 = max(0, min(frame_h - 1, py1))
                px2 = max(0, min(frame_w, px2))
                py2 = max(0, min(frame_h, py2))

                # Validate plate geometry and filter edge slivers/false positives
                if not self.is_valid_plate(
                    [px1, py1, px2, py2],
                    float(p_conf),
                    (frame_h, frame_w),
                    vehicle_bbox=veh.get("bbox"),
                    min_conf=self.conf_threshold,
                ):
                    continue

                pw = px2 - px1
                ph = py2 - py1
                pad_x = int(pw * 0.10)
                pad_y = int(ph * 0.05)
                
                c_px1 = max(0, px1 - pad_x)
                c_py1 = max(0, py1 - pad_y)
                c_px2 = min(frame_w, px2 + pad_x)
                c_py2 = min(frame_h, py2 + pad_y)

                if c_px2 > c_px1 and c_py2 > c_py1:
                    plate_crop = frame[c_py1:c_py2, c_px1:c_px2].copy()
                    # Enhance clarity: Denoise, upscale, and mild sharpen
                    h, w = plate_crop.shape[:2]
                    plate_crop = cv2.bilateralFilter(plate_crop, 5, 50, 50)
                    plate_crop = cv2.resize(plate_crop, (w * 2, h * 2), interpolation=cv2.INTER_LANCZOS4)
                    kernel = np.array([[0, -0.5, 0], [-0.5, 3.0, -0.5], [0, -0.5, 0]])
                    plate_crop = cv2.filter2D(plate_crop, -1, kernel)
                else:
                    plate_crop = None

                plate_detections.append({
                    "bbox": [px1, py1, px2, py2],
                    "conf": float(p_conf),
                    "vehicle_track_id": veh.get("track_id"),
                    "vehicle_type": veh.get("cls_name"),
                    "vehicle_bbox": veh.get("bbox"),
                    "plate_crop": plate_crop,
                })

        return plate_detections

    def detect_in_full_frame(
        self,
        frame: np.ndarray,
        vehicles: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Run plate detection over the entire frame, then match plates to vehicles.

        Args:
            frame: Full BGR video frame.
            vehicles: Optional list of detected vehicles to associate.

        Returns:
            List of detected plate dictionaries.
        """
        results = self.model.predict(
            source=frame,
            conf=self.conf_threshold,
            device=self.device,
            verbose=False,
        )

        plate_detections: List[Dict[str, Any]] = []
        if not results or len(results) == 0:
            return plate_detections

        res = results[0]
        if res.boxes is None or len(res.boxes) == 0:
            return plate_detections

        frame_h, frame_w = frame.shape[:2]
        boxes = res.boxes.xyxy.cpu().numpy()
        confs = res.boxes.conf.cpu().numpy()

        for p_bbox, p_conf in zip(boxes, confs):
            px1, py1, px2, py2 = [int(v) for v in p_bbox]
            px1 = max(0, min(frame_w - 1, px1))
            py1 = max(0, min(frame_h - 1, py1))
            px2 = max(0, min(frame_w, px2))
            py2 = max(0, min(frame_h, py2))

            # Associate plate with vehicle containing it
            matched_vehicle = None
            if vehicles:
                for veh in vehicles:
                    vx1, vy1, vx2, vy2 = veh["bbox"]
                    pcx = (px1 + px2) / 2.0
                    pcy = (py1 + py2) / 2.0
                    if vx1 <= pcx <= vx2 and vy1 <= pcy <= vy2:
                        matched_vehicle = veh
                        break

            # Validate plate geometry
            veh_bbox = matched_vehicle.get("bbox") if matched_vehicle else None
            if not self.is_valid_plate(
                [px1, py1, px2, py2],
                float(p_conf),
                (frame_h, frame_w),
                vehicle_bbox=veh_bbox,
                min_conf=self.conf_threshold,
            ):
                continue

            pw = px2 - px1
            ph = py2 - py1
            pad_x = int(pw * 0.10)
            pad_y = int(ph * 0.05)
            
            c_px1 = max(0, px1 - pad_x)
            c_py1 = max(0, py1 - pad_y)
            c_px2 = min(frame_w, px2 + pad_x)
            c_py2 = min(frame_h, py2 + pad_y)

            if c_px2 > c_px1 and c_py2 > c_py1:
                plate_crop = frame[c_py1:c_py2, c_px1:c_px2].copy()
                # Enhance clarity: Denoise, upscale, and mild sharpen
                h, w = plate_crop.shape[:2]
                plate_crop = cv2.bilateralFilter(plate_crop, 5, 50, 50)
                plate_crop = cv2.resize(plate_crop, (w * 2, h * 2), interpolation=cv2.INTER_LANCZOS4)
                kernel = np.array([[0, -0.5, 0], [-0.5, 3.0, -0.5], [0, -0.5, 0]])
                plate_crop = cv2.filter2D(plate_crop, -1, kernel)
            else:
                plate_crop = None

            plate_detections.append({
                "bbox": [px1, py1, px2, py2],
                "conf": float(p_conf),
                "vehicle_track_id": matched_vehicle.get("track_id") if matched_vehicle else None,
                "vehicle_type": matched_vehicle.get("cls_name") if matched_vehicle else None,
                "vehicle_bbox": matched_vehicle.get("bbox") if matched_vehicle else None,
                "plate_crop": plate_crop,
            })

        return plate_detections

    @staticmethod
    def is_valid_plate(
        bbox: List[int],
        conf: float,
        frame_shape: Tuple[int, int],
        vehicle_bbox: Optional[List[int]] = None,
        min_conf: float = 0.35,
    ) -> bool:
        """
        Filter out edge slivers, door/window false positives, and micro-noise.
        """
        if conf < min_conf:
            return False

        frame_h, frame_w = frame_shape[:2]
        x1, y1, x2, y2 = bbox
        bw = x2 - x1
        bh = y2 - y1

        # Minimum dimension bounds
        # Lowered back slightly to ensure we don't miss smaller/distant plates
        if bw < 25 or bh < 9:
            return False

        # Maximum dimension sanity check
        if bw > 350 or bh > 140:
            return False

        aspect = bw / float(bh)

        # Frame edge tolerance: if touching left/right frame boundary
        is_touching_edge = (x1 <= 1 or x2 >= frame_w - 2)
        if is_touching_edge:
            if bw < 35 or aspect < 1.0:
                return False
            return aspect <= 4.5

        # Standard Indian plates aspect bounds
        # Tightened upper bound to 4.5 to reject "INNOVA" and "TRAVELS" which are usually > 4.8
        if aspect < 1.3 or aspect > 4.5:
            return False

        # Relative vehicle size check: plate shouldn't be taller than 40% of parent vehicle
        if vehicle_bbox:
            vx1, vy1, vx2, vy2 = vehicle_bbox
            veh_h = vy2 - vy1
            veh_w = vx2 - vx1
            if veh_h > 0 and (bh / float(veh_h)) > 0.40:
                return False
            if veh_w > 0 and (bw / float(veh_w)) > 0.90:
                return False

            # Position heuristic: Real license plates are almost always in the lower 60% of a vehicle.
            # This filters out false positives like "TRAVELS" text painted on upper windows/roofs.
            if veh_h > 0:
                plate_cy = y1 + (bh / 2.0)
                relative_y = (plate_cy - vy1) / float(veh_h)
                if relative_y < 0.40:
                    return False

        return True

    @staticmethod
    def compute_iou(boxA: List[int], boxB: List[int]) -> float:
        """Compute Intersection over Union (IoU) of two bounding boxes."""
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        inter_w = max(0, xB - xA)
        inter_h = max(0, yB - yA)
        inter_area = inter_w * inter_h

        boxAArea = max(0, boxA[2] - boxA[0]) * max(0, boxA[3] - boxA[1])
        boxBArea = max(0, boxB[2] - boxB[0]) * max(0, boxB[3] - boxB[1])

        union_area = float(boxAArea + boxBArea - inter_area)
        return (inter_area / union_area) if union_area > 0 else 0.0

    def merge_detections(
        self,
        primary_plates: List[Dict[str, Any]],
        secondary_plates: List[Dict[str, Any]],
        iou_thresh: float = 0.35,
    ) -> List[Dict[str, Any]]:
        """
        Merge two detection lists, eliminating duplicates based on IoU overlap.
        """
        merged = list(primary_plates)
        for s_plate in secondary_plates:
            s_box = s_plate["bbox"]
            is_dup = False
            for m_plate in merged:
                if self.compute_iou(s_box, m_plate["bbox"]) > iou_thresh:
                    is_dup = True
                    break
            if not is_dup:
                merged.append(s_plate)
        return merged

