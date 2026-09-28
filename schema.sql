CREATE TABLE IF NOT EXISTS cameras (
    camera_id VARCHAR(50) PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    long DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS plate_detections (
    id SERIAL PRIMARY KEY,
    plate_number VARCHAR(20) NOT NULL,
    camera_id VARCHAR(50) REFERENCES cameras(camera_id),
    confidence FLOAT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    image_path VARCHAR(255) NOT NULL
);

INSERT INTO cameras (camera_id, location_name, lat, long) VALUES
('CAM_01', 'Connaught Place North', 28.6315, 77.2167),
('CAM_02', 'Mandi House Circle', 28.6258, 77.2343),
('CAM_03', 'India Gate Roundabout', 28.6129, 77.2295)
ON CONFLICT (camera_id) DO NOTHING;
