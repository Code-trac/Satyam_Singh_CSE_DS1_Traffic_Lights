const API_URL = '/api/traffic_data';
const UPDATE_INTERVAL = 1000;

const densitySpans = [
    document.getElementById('density-0'),
    document.getElementById('density-1'),
    document.getElementById('density-2'),
    document.getElementById('density-3'),
];
const statusSpans = [
    document.getElementById('status-0'),
    document.getElementById('status-1'),
    document.getElementById('status-2'),
    document.getElementById('status-3'),
];
const timerSpans = [
    document.getElementById('timer-0'),
    document.getElementById('timer-1'),
    document.getElementById('timer-2'),
    document.getElementById('timer-3'),
];
const laneCards = [
    document.getElementById('lane-0'),
    document.getElementById('lane-1'),
    document.getElementById('lane-2'),
    document.getElementById('lane-3'),
];
const lastUpdateSpan = document.getElementById('last-update');

async function fetchTrafficData() {
    try {

        const response = await fetch(API_URL);


        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }


        const data = await response.json();


        updateDashboard(data);

    } catch (error) {

        console.error("Error fetching traffic data:", error);

        if (lastUpdateSpan) lastUpdateSpan.textContent = `Error fetching data: ${error.message}`;
    }
}


function updateDashboard(data) {

    if (!data || !Array.isArray(data.lane_densities) || data.current_green_lane === undefined || data.signal_timer === undefined) {
        console.error("Invalid or incomplete data received:", data);
        return;
    }

    const greenLaneIndex = data.current_green_lane;
    const timer = data.signal_timer;


    data.lane_densities.forEach((density, index) => {

        if (densitySpans[index]) {
            densitySpans[index].textContent = `${density.toFixed(1)}%`;
        }
        const isGreen = (index === greenLaneIndex);
        const statusText = isGreen ? 'GREEN' : 'RED';
        const timerText = isGreen ? `${timer.toFixed(1)}s` : '--s';

        if (statusSpans[index]) {
            statusSpans[index].textContent = statusText;
            statusSpans[index].className = isGreen ? 'font-bold text-green-600' : 'font-bold text-red-600';
        }

         if (timerSpans[index]) {
            timerSpans[index].textContent = timerText;
        }

        if (laneCards[index]) {
            laneCards[index].classList.remove('lane-green', 'lane-red', 'border-green-500', 'border-red-500', 'border-gray-400');

            if (isGreen) {
                laneCards[index].classList.add('lane-green', 'border-green-500');
            } else {
                laneCards[index].classList.add('lane-red', 'border-red-500');
            }
        }
    });

    if (lastUpdateSpan && data.timestamp) {
        const updateTime = new Date(data.timestamp * 1000);
        lastUpdateSpan.textContent = updateTime.toLocaleTimeString();
    }
}

fetchTrafficData();

setInterval(fetchTrafficData, UPDATE_INTERVAL);

console.log(`Traffic dashboard script loaded. Fetching data from ${API_URL} every ${UPDATE_INTERVAL / 1000} seconds.`);
