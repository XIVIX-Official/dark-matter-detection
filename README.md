# Dark Matter Detection

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

This is a React based application.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/XIVIX-Official/dark-matter-detection.git
    ```

2.  **Navigate to the directory:**
    ```bash
    cd dark-matter-detection
    ```

3.  **Install dependencies:**
    ```bash
    npm install
    ```

4.  **Start the development server:**
    ```bash
    npm run dev
    ```

5.  **Open the application:**
    - The development server will provide a local URL (typically `http://localhost:3000`)
    - Open this URL in your web browser
    
6.  **For production build:**
    ```bash
    npm run build
    npm run preview    # To preview the production build
    ```

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
