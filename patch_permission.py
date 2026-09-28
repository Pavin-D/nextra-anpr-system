import re

with open("yolo_tracker.py", "r", encoding="utf-8") as f:
    content = f.read()

bad_block = """        if frame_count % 5 == 0:
            tmp_path = f"data/live_frame_{args.camera_id}_tmp.jpg"
            final_path = f"data/live_frame_{args.camera_id}.jpg"
            cv2.imwrite(tmp_path, frame)
            os.replace(tmp_path, final_path)"""

good_block = """        if frame_count % 5 == 0:
            tmp_path = f"data/live_frame_{args.camera_id}_tmp.jpg"
            final_path = f"data/live_frame_{args.camera_id}.jpg"
            cv2.imwrite(tmp_path, frame)
            try:
                os.replace(tmp_path, final_path)
            except PermissionError:
                pass  # Windows locks the file when the browser is actively downloading it. Skip this frame update."""

content = content.replace(bad_block, good_block)

with open("yolo_tracker.py", "w", encoding="utf-8") as f:
    f.write(content)
