# NEXTRA ANPR System - Cloud Architecture Workflow

This document outlines the final end-to-end data pipeline of the NEXTRA project, utilizing Cloud storage tiers (Hot & Archive) to massively reduce costs while maintaining real-time dashboard performance.

> [!TIP] The **15-Day Data Lifecycle**
> By automating the transition from **Hot Storage** (expensive, fast access) to **Cold Archive** (cheap, slow access), you reduce your cloud storage costs by over 90% without losing legal compliance records.

## Complete Workflow Diagram

```mermaid
flowchart TD
    %% Styling
    classDef edge fill:#1e1e2f,stroke:#4f46e5,stroke-width:2px,color:#fff;
    classDef cloud fill:#0f172a,stroke:#06b6d4,stroke-width:2px,color:#fff;
    classDef ai fill:#312e81,stroke:#a855f7,stroke-width:2px,color:#fff;
    classDef db fill:#022c22,stroke:#10b981,stroke-width:2px,color:#fff;
    classDef ui fill:#4c1d95,stroke:#f43f5e,stroke-width:2px,color:#fff;

    %% Components
    subgraph EdgeNode [1. Edge Capture (Streets)]
        C1[Traffic Camera 01]:::edge
        C2[Traffic Camera 02]:::edge
        Chunk[Video Chunking\n(10-min MP4 Files)]:::edge
        
        C1 --> Chunk
        C2 --> Chunk
    end

    subgraph Cloud [2. Cloud Storage Lifecycle]
        Hot[(Standard Hot Storage\nAWS S3 / Cloudflare R2)]:::cloud
        Archive[(Cold Archive Storage\nAWS Glacier)]:::cloud
        
        Hot -- "Automated Lifecycle Rule\n(Moves video after 15 days)" --> Archive
    end

    subgraph Pipeline [3. NEXTRA AI Engine (Backend)]
        YOLO[YOLOv11 Tracking\nVehicle Detection]:::ai
        Crop[Crop Extraction\nImage Sharpness Check]:::ai
        OCR[PaddleOCR Engine\nText Recognition]:::ai
        Guard[Data Guard Filter\n(Regex & >85% Confidence)]:::ai
        
        YOLO --> Crop --> OCR --> Guard
    end

    subgraph DB [4. Structured Metadata]
        Postgres[(PostgreSQL Database\nocr_db)]:::db
        Alerts[Blacklist Engine\nAnomaly Detection]:::db
        
        Postgres <--> Alerts
    end

    subgraph Frontend [5. Nextra Command Center]
        Dashboard[React Dashboard\nLive Map, Split Screen, Alerts]:::ui
    end

    %% Connections
    Chunk -- "Upload via API" --> Hot
    Hot -- "Triggers Inference" --> YOLO
    Guard -- "Insert Valid Plates" --> Postgres
    
    %% Dashboard Feeds
    Postgres -- "Serve Analytics\n(API Polling)" --> Dashboard
    Hot -- "Stream Recent Video\n(Instant Playback)" --> Dashboard
    Archive -. "Legal Retrieval Request\n(12-48 Hr Delay)" .-> Dashboard
```

## How It Works

1. **Edge Capture:** High-definition cameras on the streets capture live traffic. To prevent massive file corruption and upload failures, the video is chunked into 10-minute MP4 clips.
2. **Hot Cloud Upload:** The chunks are uploaded instantly to an S3-compatible cloud bucket (Standard Storage). This allows the Nextra Dashboard to stream the videos back to the user instantly with zero delay.
3. **AI Inference:** The arrival of a new video triggers the Python FastAPI backend. The YOLO model tracks vehicles, extracts the sharpest license plate crop, and sends it to PaddleOCR. The **Data Guard** heavily filters the results to ensure only perfect reads enter the database.
4. **Metadata Storage:** The raw text (plate numbers, timestamps, coordinates) is saved in PostgreSQL. Because text is extremely lightweight, it can be kept locally (or on Supabase) forever without significant cost.
5. **The Archival Process:** To save money, an automated Cloud Lifecycle Rule watches the video bucket. Exactly 15 days after a video was uploaded, the cloud provider automatically moves it to the "Glacier" Archive tier, dropping its storage cost to $0.99/TB. The video is no longer instantly playable on the dashboard, but remains securely backed up for legal compliance.
