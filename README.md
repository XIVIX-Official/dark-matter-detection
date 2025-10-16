# Dark Matter Detection Simulation

A sophisticated Monte Carlo simulation for detecting dark matter particles (WIMPs) based on particle physics interactions. This project features a modern, real-time, web-based UI built with React, TypeScript, and Tailwind CSS.

## 🌌 Features

-   **Advanced Physics Engine**: Simulates WIMP (Weakly Interacting Massive Particle) interactions within different detector materials.
-   **Monte Carlo Simulation**: Employs statistical modeling to generate realistic detector events based on configurable parameters.
-   **Real-time Analysis**: Live visualization of particle hits in the detector chamber and a dynamic energy spectrum histogram.
-   **Multiple Detector Types**: Switch between four common detector types: Superfluid Helium, Liquid Xenon, Germanium, and Scintillator, each with unique properties.
-   **Beautiful Dashboard**: A modern glassmorphic UI with a dark theme, designed for clarity and aesthetic appeal.
-   **Data Export**: Download the raw simulation event data in JSON format for external analysis.

## 🛠️ Technology Stack

-   **Frontend**: React, TypeScript
-   **Styling**: Tailwind CSS
-   **Charting**: Recharts
-   **State Management**: React Hooks (`useState`, `useCallback`, etc.)

*Note: This version is a frontend-only simulation. The physics engine is a client-side mock designed to produce visually representative results. It can be extended to connect to a full REST API backend (e.g., Python/Flask) for more complex calculations.*

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have [Node.js](https://nodejs.org/) (which includes npm) installed on your computer to use common development tools.

-   Node.js (v16 or later recommended)
-   npm (v8 or later) or yarn

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/XIVIX-Official/dark-matter-simulation.git
    cd dark-matter-simulation
    ```

2.  **Install dependencies:**
    This project uses an `importmap` for dependencies like React and Recharts, so there are no external packages to install with npm for the core functionality. The development setup assumes you have a local server to serve the static files.

3.  **Run the application:**

    **Option A: Using `live-server`**
    If you don't have `live-server`, install it globally:
    ```sh
    npm install -g live-server
    ```
    Then, run it from the project's root directory:
    ```sh
    live-server
    ```
    This will automatically open the application in your default web browser.

    **Option B: Using Python's HTTP Server**
    If you have Python installed, navigate to the project's root directory and run:
    ```sh
    # For Python 3
    python -m http.server

    # For Python 2
    python -m SimpleHTTPServer
    ```
    Then, open your browser and navigate to `http://localhost:8000`.

## 🖥️ How to Use

1.  **Open the application** in your web browser.
2.  Use the **Simulation Controls** panel on the left to configure the simulation.
    -   **Detector Type**: Select the material for the detector. This affects the energy distribution of detected events.
    -   **WIMP Mass**: Adjust the hypothetical mass of the dark matter particles. Heavier WIMPs will result in slightly higher energy events.
    -   **Cross-Section**: Modify the interaction probability. A higher cross-section leads to a higher rate of detected events.
3.  Click the **Start** button to begin the simulation.
4.  Observe the **Detector Chamber** for visual representations of particle hits and watch the **Energy Spectrum** chart update in real-time.
5.  Click **Stop** to pause the simulation. You can then change parameters and resume.
6.  Use the **Reset** button to clear all data and revert the parameters to their default values.
7.  Click **Export** to download a JSON file containing all the events generated during the session.

## 📄 License

This project is licensed under the MIT License.

---

*This simulation is for educational and demonstrative purposes only and does not represent a physically accurate model.*

---

**Powered by XIVIX**
