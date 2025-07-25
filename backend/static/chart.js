// Chart.js script for graphs
// chart.js — draw progress over time
function renderSprintChart(ctxId, labels, totalTimes, t1List, t2List, t3List) {
  const ctx = document.getElementById(ctxId).getContext('2d');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Total Time',
          data: totalTimes,
          borderColor: 'blue',
          fill: false,
          tension: 0.1
        },
        {
          label: 'T1',
          data: t1List,
          borderColor: 'green',
          fill: false,
          tension: 0.1
        },
        {
          label: 'T2',
          data: t2List,
          borderColor: 'orange',
          fill: false,
          tension: 0.1
        },
        {
          label: 'T3',
          data: t3List,
          borderColor: 'red',
          fill: false,
          tension: 0.1
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top'
        },
        title: {
          display: true,
          text: 'Sprint Time Progress'
        }
      }
    }
  });
}
