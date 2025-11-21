

# GTFS Interactive Analytics Dashboard

## Overview

This project is an interactive **GTFS Analytics Dashboard** designed to explore, analyze, and visualize transit operations using static GTFS data.
It supports planners, researchers, and transit enthusiasts in understanding the structure, operations, and service characteristics of a transit network over time.

Instead of treating GTFS as just a scheduling format, this project treats it as a **planning and performance dataset** and builds an interface for extracting meaningful network metrics and insights.

The dashboard transforms raw GTFS feeds into:

* Network-level indicators
* Route- and block-level statistics
* Temporal service patterns
* Visual network representations

---

## Project Goals

This dashboard was developed with four main goals:

### 1. Make GTFS Data Interpretable

GTFS files are powerful but complex. This project makes them **human-readable and explorable** by providing:

* Interactive tables for all major GTFS feeds
* Network-wide summaries
* Contextual explanations of each dataset

---

### 2. Enable Daily Service Analysis

Transit supply changes day-to-day due to service calendars, exceptions, and special schedules.

This dashboard allows users to:

* Pick any date in a service period
* Identify which services are active
* Analyze what the network actually looks like *on that specific day*
* Compute network metrics dynamically for that date

This is especially useful for:

* Holiday scheduling comparisons
* Weekday vs weekend analysis
* Special event or disruption studies

---

### 3. Visualize Multi-Modal Transit Networks

The dashboard supports multiple modes (e.g., Bus, Subway, Streetcar) and visualizes them on an interactive map.

It helps answer questions like:

* How does the physical network vary by mode?
* Which mode dominates specific areas?
* How dense is the spatial distribution of service?

The map supports:

* Mode filtering
* Color-coded network layers
* Transparent base map overlay

---

### 4. Support Transit Planning Research

While useful for operations, this project is also designed as a **research tool** for:

* Transit planning studies
* Comparative city analysis
* Network structure modeling
* Policy evaluation
* Data-driven transit strategy research

It is especially relevant for studies involving:

* Service frequency modeling
* Temporal demand patterns
* Transit electrification planning
* Infrastructure prioritization
* Pattern-based service modeling (TPFS-related research)

---

## Key Features

### Network Overview

Provides high-level system indicators such as:

* Total number of active routes
* Total stops
* Total trips
* Block usage
* Daily variation of network scale

All metrics are date-sensitive and reflect actual active services.

---

### GTFS Feed Explorer

Interactive exploration of:

* agency
* routes
* trips
* stops
* stop_times
* calendars
* calendar_dates
* shapes

This helps users understand how the system is structured at a data level.

---

### Top Route Identification

Identifies:

* Most active routes by number of trips
* Most resource-intensive routes by number of blocks
* Mode distribution of top-performing routes

This is valuable for resource allocation studies and service planning.

---

### Temporal Service Distribution (Day Period Analysis)

The dashboard segments the day into major operational periods such as:

* Early Morning
* Morning Peak
* Midday
* Afternoon Peak
* Evening
* Late Night

For each period, it calculates:

* Trips per hour
* Peak service periods
* Service intensity patterns

This helps reveal:

* Scheduling concentration
* Demand-oriented supply patterns
* Peak load distributions

---

### Trip Frequency Distribution

A statistical view of:

* How trip counts vary across routes
* Distribution of service intensity
* Outlier detection (very high or very low service routes)

This is crucial for:

* Network equity analysis
* High-frequency corridor identification
* Strategic investment studies

---

## Target Users

This dashboard is designed for:

* Transit planners
* Academic researchers
* Graduate students in transportation engineering
* Transit agencies
* Data scientists working with GTFS
* Urban mobility analysts

It can be used in:

* Planning reports
* Academic studies
* Service optimization projects
* Demonstrations and policy analysis

---

## Data Sources

The project is built using static GTFS feeds provided by public transit agencies.
It supports local GTFS imports and is adaptable to multiple agencies.

Case studies currently supported or planned include:

* Toronto
* Dallas
* Chicago
* New Jersey
* San Diego
* Washington
* Winnipeg

---

## Future Direction

Planned improvements include:

* Integration of real-time GTFS feeds
* Performance metrics (headway regularity, service reliability)
* Passenger demand proxies
* Vehicle occupancy layer
* Pattern-based TPFS extension support
* Multi-city benchmarking tools

