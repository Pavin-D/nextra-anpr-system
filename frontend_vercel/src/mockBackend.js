export function initMockBackend() {
    const originalFetch = window.fetch;
    window.fetch = async (url, options) => {
        if (typeof url === 'string' && url.startsWith('/api/v1/')) {
            console.log("Mocking API:", url);
            await new Promise(r => setTimeout(r, 300)); // Simulate network delay

            if (url === '/api/v1/telemetry') return new Response(JSON.stringify({ total_vehicles: 14205, total_alerts: 12, system_health: "Optimal", recent_alerts: [{ id: 101, plate: "KA02MN1828", type: "Stolen Vehicle", time: "Just now" }, { id: 102, plate: "DL4CAB4421", type: "Speeding", time: "2m ago" }] }), { status: 200, headers: { 'Content-Type': 'application/json' } });
            
            if (url === '/api/v1/analytics/heatmap') return new Response(JSON.stringify([{ location: "CAM_01", count: 120 }, { location: "CAM_02", count: 340 }]), { status: 200, headers: { 'Content-Type': 'application/json' } });
            
            if (url === '/api/v1/progress') return new Response(JSON.stringify({ status: 'processing', progress: 68 }), { status: 200, headers: { 'Content-Type': 'application/json' } });
            
            if (url === '/api/v1/database/tables') return new Response(JSON.stringify([{ name: 'plate_detections', row_count: 14205, size_bytes: 4096000 }, { name: 'blacklist', row_count: 5, size_bytes: 10240 }, { name: 'alerts', row_count: 12, size_bytes: 20480 }]), { status: 200, headers: { 'Content-Type': 'application/json' } });
            
            if (url.startsWith('/api/v1/database/data/plate_detections')) return new Response(JSON.stringify({ columns: ['id', 'plate_number', 'camera_id', 'timestamp', 'confidence'], rows: [[1, 'KA02MN1828', 'CAM_01', '2026-09-28 14:30', 0.98], [2, 'DL4CAB4421', 'CAM_02', '2026-09-28 14:31', 0.95], [3, 'MH12RN4398', 'CAM_01', '2026-09-28 14:32', 0.89], [4, 'UP32EZ1029', 'CAM_03', '2026-09-28 14:33', 0.99]] }), { status: 200, headers: { 'Content-Type': 'application/json' } });
            
            if (url.startsWith('/api/v1/database/data/blacklist')) return new Response(JSON.stringify({ columns: ['plate_number', 'reason', 'added_by', 'date'], rows: [['KA02MN1828', 'Stolen Vehicle', 'Admin', '2026-09-20'], ['DL8CX1234', 'Amber Alert', 'System', '2026-09-25']] }), { status: 200, headers: { 'Content-Type': 'application/json' } });
            
            if (url.startsWith('/api/v1/database/data/alerts')) return new Response(JSON.stringify({ columns: ['id', 'plate_number', 'alert_type', 'camera', 'time'], rows: [[101, 'KA02MN1828', 'Stolen Vehicle', 'CAM_01', '2026-09-28 14:30']] }), { status: 200, headers: { 'Content-Type': 'application/json' } });
            
            if (url === '/api/v1/blacklist' && (!options || options.method === 'GET' || !options.method)) return new Response(JSON.stringify([{ plate_number: 'KA02MN1828', reason: 'Stolen', added_date: '2026-09-20' }, { plate_number: 'DL8CX1234', reason: 'Amber Alert', added_date: '2026-09-25' }]), { status: 200, headers: { 'Content-Type': 'application/json' } });
            if (url === '/api/v1/blacklist' && options && options.method === 'POST') return new Response(JSON.stringify({ success: true }), { status: 200, headers: { 'Content-Type': 'application/json' } });
            
            if (url === '/api/v1/alerts') return new Response(JSON.stringify([{ id: 101, plate_number: 'KA02MN1828', alert_type: 'Stolen', timestamp: '2026-09-28 14:30', camera_id: 'CAM_01', resolved: false }, { id: 102, plate_number: 'DL8CX1234', alert_type: 'Amber Alert', timestamp: '2026-09-28 10:15', camera_id: 'CAM_02', resolved: true }]), { status: 200, headers: { 'Content-Type': 'application/json' } });
            
            if (url === '/api/v1/videos') return new Response(JSON.stringify(["CAM_01_morning_traffic.mp4", "CAM_02_highway_accident.mp4", "CAM_03_city_center.mp4"]), { status: 200, headers: { 'Content-Type': 'application/json' } });
            
            if (url === '/api/v1/plates') return new Response(JSON.stringify([{ plate_number: 'KA02MN1828', last_seen: '2026-09-28 14:30', total_detections: 4 }, { plate_number: 'DL4CAB4421', last_seen: '2026-09-28 14:31', total_detections: 1 }]), { status: 200, headers: { 'Content-Type': 'application/json' } });
            
            if (url.startsWith('/api/v1/trajectory')) return new Response(JSON.stringify([{ camera_id: 'CAM_01', timestamp: '2026-09-28 14:30:00', lat: 12.9716, lng: 77.5946 }, { camera_id: 'CAM_02', timestamp: '2026-09-28 14:35:00', lat: 12.9750, lng: 77.6000 }]), { status: 200, headers: { 'Content-Type': 'application/json' } });
            
            if (url === '/api/v1/geofence-search') return new Response(JSON.stringify([{ plate_number: 'MH12RN4398', camera_id: 'CAM_03', timestamp: '2026-09-28 14:32:00', lat: 12.9716, lng: 77.5946 }]), { status: 200, headers: { 'Content-Type': 'application/json' } });
            
            if (url === '/api/v1/chat') return new Response(JSON.stringify({ response: "System is operating normally. I have monitored 14,205 vehicles today across 3 active cameras." }), { status: 200, headers: { 'Content-Type': 'application/json' } });

            return new Response(JSON.stringify({ success: true }), { status: 200, headers: { 'Content-Type': 'application/json' } });
        }
        return originalFetch(url, options);
    };
}
