# 🧚 PIXIE

> Photography Insights and eXIF Intelligence Engine

Transform photo metadata into actionable insights.

## Overview

PIXIE is a photography analytics and photo management platform that helps photographers organize large image collections, analyze shooting patterns, and extract meaningful insights from photo metadata.

Modern cameras generate thousands of images along with rich metadata such as camera settings, lens information, focal lengths, exposure parameters, timestamps, and geolocation data. While this information is invaluable, it often remains underutilized.

PIXIE unlocks the value hidden within photo metadata by providing tools for library organization, RAW/JPEG file management, photography analytics, and data-driven equipment insights.

## Key Features

### 🗂️ RAW File Management

Efficiently manage RAW and JPEG workflows.

* Detect RAW/JPEG file pairs
* Identify orphaned RAW files
* Generate cleanup reports
* Reduce unnecessary storage consumption
* Support for multiple camera manufacturers and RAW formats

---

### 📅 Metadata-Driven Timeline Organization

Automatically organize photo collections using EXIF metadata.

Organize by:

* Year
* Month
* Day
* Camera
* Lens

Example:

```text
Photos/
├── 2026/
│   ├── January/
│   ├── February/
│   └── March/
```

---

### 📊 Photography Analytics

Analyze how your camera equipment is actually being used.

Track:

* Camera bodies
* Lens usage
* Focal length distributions
* Aperture preferences
* Shutter speed distributions
* ISO behavior
* Shooting frequency over time

Sample questions:

* Which focal lengths do I use most frequently?
* What aperture range dominates my photography?
* Which lenses are underutilized?
* How has my shooting style evolved over time?

---

### 🎯 Equipment Insights

Leverage historical shooting data to make informed equipment decisions.

Examples:

* Most frequently used focal length ranges
* Lens utilization statistics
* Camera usage comparisons
* Photography style profiling

---

### 📈 Trip and Project Analytics

Generate summary reports for photography projects and travel collections.

Metrics include:

* Total images captured
* Shooting duration
* Most used equipment
* Exposure statistics
* Daily capture trends

## Roadmap

### Phase 1

* [ ] EXIF extraction engine
* [ ] RAW/JPEG relationship tracking
* [ ] Timeline generation
* [ ] Photography analytics dashboard

### Phase 2

* [ ] Duplicate image detection
* [ ] Near-duplicate burst analysis
* [ ] Interactive reporting
* [ ] Equipment recommendation engine

### Phase 3

* [ ] Geospatial photo visualization
* [ ] Image quality scoring
* [ ] Computer vision-based categorization
* [ ] AI-powered photography insights

## Technology Stack

* Python
* Pandas
* ExifTool
* Pillow
* OpenCV
* Plotly
* Streamlit

## Vision

PIXIE aims to become a photography intelligence platform that helps photographers better understand their images, workflows, and equipment through metadata-driven analytics.

---

**Organize. Analyze. Understand Your Photography.**


---

## Running PIXIE

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Application

```bash
uvicorn main:app --reload
```

You should see output similar to:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 3. Open PIXIE in Your Browser

Navigate to:

```text
http://127.0.0.1:8000
```

### Notes

* Ensure you are running the command from the project's root directory.
* The application supports Windows, macOS, and Linux file paths.
* For safety, PIXIE runs in **Dry Run** mode by default and will not move any files unless explicitly instructed.
