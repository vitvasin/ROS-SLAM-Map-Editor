# ROS SLAM Map Editor (Modified Version)

A web-based map editor for quick editing of ROS and ROS2 SLAM maps. This is a modified version of the original tool by Dominick Lee, enhanced with additional features for local robotic workflows.

## Overview
This repository provides a web-based map editor designed specifically for quick and convenient editing of ROS and ROS2 SLAM maps, such as those created in the popular [`slam_toolbox`](https://github.com/SteveMacenski/slam_toolbox). 

![Screenshot](img/screenshot-main.png)

## Modifications & Enhancements
This version includes the following improvements over the [original repository](https://github.com/GyroPalm/ROS-SLAM-Map-Editor):

- **Map Rotation**: Ability to rotate the map for better alignment.
- **Fit-to-Screen**: One-click zoom to fit the map to the current viewport.
- **Enhanced UI & Touch Support**: Improved responsiveness and touch interactions for tablets and mobile devices.
- **Offline Mode**: Includes local `vendor` assets (CSS/JS) to work without an internet connection.
- **Local Server Integration**: A Python-based backend (`server.py`) for automatic loading and saving of maps from local directories.

## Features
- [x] Completely Browser-based Self-Hosted Solution
- [x] Responsive Map Editing for Touchscreen Devices and Computers
- [x] Drag and Drop Map PGM and YAML files
- [x] Drag and Drop Keepout PGM and YAML files
- [x] Uses Font Awesome for sleek UI icons
- [x] Convenient Zoom In, Zoom Out, and Auto-Fit buttons
- [x] Map Rotation Tool
- [x] Invert and Auto-level options
- [x] Paint or Erase Walls/Keep-out zones
- [x] Un-Scan Area (Mark area as unknown)
- [x] Multi-level Undo and Redo Capabilities
- [x] Measurement Tool (Meters and Feet)
- [x] Integrated Local Saving (via Python Server)

## Usage

### 1. Online / Static Usage
You can still use the editor as a static tool by opening `editor.html` in any modern browser.
*Note: In static mode, you must manually drag and drop map files and download changes.*

### 2. Local Integrated Usage (Recommended for Robots)
If you are running this on a robot or local machine with Python, you can use the integrated server to auto-load and save maps.

1. **Launch the Editor**:
   ```bash
   ./run_editor.sh
   ```
   This will start a local server on port `7070` and attempt to open the editor in Chromium.

2. **Server Configuration**:
   The `server.py` is configured to look for maps in `../mini_amr/amrROS2_ws/maps`. You can modify `MAPS_DIR` in `server.py` to point to your specific maps directory.

3. **Auto Loading/Saving**:
   When using the server, you can trigger loads and saves via the API endpoints, allowing for a more seamless integration with ROS workflows.

## Credits & License
This tool is based on the [original ROS-SLAM-Map-Editor](https://github.com/GyroPalm/ROS-SLAM-Map-Editor) created by **Dominick Lee** as part of GyroPalm's OmniBot V2 AMR product.

### Attribution
If you use this tool in your work, please cite the original author:
> Lee, Dominick. (2025). ROS SLAM Map Editor [Computer software]. GyroPalm, LLC. https://github.com/GyroPalm/ROS-SLAM-Map-Editor

### License
Modified code and original assets are provided under the **MIT License**. See the `LICENSE` file for details.