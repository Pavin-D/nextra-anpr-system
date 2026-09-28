from typing import List, Dict, Any, Optional
import numpy as np
from ultralytics import YOLO


class VehicleDetector:
    """Detects and tracks vehicles using YOLO11."""

    # Default COCO vehicle classes: car (2), motorcycle (3), bus (5), truck (7)
    DEFAULT_VEHICLE_CLASSES = [2, 3, 5, 7]

    def __init__(
        self,
        model_path: str = "yolo11n.pt",
        vehicle_classes: Optional[List[int]] = None,
        conf_threshold: float = 0.35,
        device: Optional[str] = None,
    ):
        """
        Initialize the vehicle detector.

        Args:
            model_path: Path to YOLO11 weights (e.g., 'yolo11n.pt')
            vehicle_classes: List of COCO class indices to filter for vehicles.
            conf_threshold: Confidence threshold for vehicle detections.
            device: 'cpu', 'cuda', '0', etc. Defaults to auto.
        """
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.vehicle_classes = vehicle_classes or self.DEFAULT_VEHICLE_CLASSES
        self.device = device
        self.class_names = self.model.names

    def detect(self, frame: np.ndarray, track: bool = True) -> List[Dict[str, Any]]:
        """
        Run detection or tracking on a single video frame.

        Args:
            frame: BGR numpy image from cv2.VideoCapture.
            track: Whether to enable persistent vehicle tracking (ByteTrack).

        Returns:
            List of detected vehicle dictionaries containing:
            'bbox': [x1, y1, x2, y2]
            'conf': float
            'cls_id': int
            'cls_name': str
            'track_id': Optional[int]
        """
        if track:
            results = self.model.track(
                source=frame,
                persist=True,
                classes=self.vehicle_classes,
                conf=self.conf_threshold,
                device=self.device,
                tracker="bytetrack.yaml",
                verbose=False,
            )
        else:
            results = self.model.predict(
                source=frame,
                classes=self.vehicle_classes,
                conf=self.conf_threshold,
                device=self.device,
                verbose=False,
            )

        detections: List[Dict[str, Any]] = []
        if not results or len(results) == 0:
            return detections

        res = results[0]
        if res.boxes is None or len(res.boxes) == 0:
            return detections

        boxes = res.boxes.xyxy.cpu().numpy()
        confs = res.boxes.conf.cpu().numpy()
        classes = res.boxes.cls.cpu().numpy().astype(int)
        track_ids = (
            res.boxes.id.cpu().numpy().astype(int)
            if (res.boxes.id is not None)
            else [None] * len(boxes)
        )

        for bbox, conf, cls_id, track_id in zip(boxes, confs, classes, track_ids):
            x1, y1, x2, y2 = [int(v) for v in bbox]
            cls_name = self.class_names.get(cls_id, str(cls_id))
            detections.append({
                "bbox": [x1, y1, x2, y2],
                "conf": float(conf),
                "cls_id": cls_id,
                "cls_name": cls_name,
                "track_id": int(track_id) if track_id is not None else None,
            })

        return detections
