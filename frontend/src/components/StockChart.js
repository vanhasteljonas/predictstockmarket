import React, { useEffect, useRef } from 'react';
import { Chart as ChartJS, registerables } from 'chart.js';
import 'chartjs-adapter-date-fns';
import zoomPlugin from 'chartjs-plugin-zoom';

ChartJS.register(...registerables, zoomPlugin);

const StockChart = ({ data, showRsi }) => {
  const chartRef = useRef(null);
  let myChartInstance = useRef(null);

  useEffect(() => {
    if (!Array.isArray(data)) {
      console.error('Data is not an array');
      return;
    }

    if (myChartInstance.current) {
      myChartInstance.current.destroy();
    }

    const ctx = chartRef.current.getContext('2d');
    const today = new Date();
    const historicalData = data.filter(d => new Date(d.Date) <= today);
    const predictionData = data.filter(d => new Date(d.Date) > today);

    const datasets = [
      {
        label: 'Historical Data',
        data: historicalData.map(d => ({ x: new Date(d.Date), y: d.Open })),
        borderColor: 'blue',
        fill: false,
      },
      {
        label: 'Prediction',
        data: predictionData.map(d => ({ x: new Date(d.Date), y: d.Open })),
        borderColor: 'red',
        fill: false,
      },
    ];

    if (showRsi) {
      datasets.push({
        label: 'RSI',
        data: data.map(d => ({ x: new Date(d.Date), y: d.Rsi14 })),
        borderColor: 'green',
        fill: false,
        yAxisID: 'y-rsi',
      });
    }

    myChartInstance.current = new ChartJS(ctx, {
      type: 'line',
      data: { datasets },
      options: {
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'day',
            },
            title: {
              display: true,
              text: 'Date',
            },
          },
          y: {
            beginAtZero: false,
            title: {
              display: true,
              text: 'Price',
            },
          },
          'y-rsi': {
            display: showRsi,
            beginAtZero: false,
            position: 'right',
            title: {
              display: true,
              text: 'RSI',
            },
            grid: {
              drawOnChartArea: false,
            },
          },
        },
        plugins: {
          zoom: {
            zoom: {
              wheel: { enabled: true },
              pinch: { enabled: true },
              mode: 'xy',
            },
            pan: {
              enabled: true,
              mode: 'xy',
            },
          },
        },
      },
    });

    return () => {
      if (myChartInstance.current) {
        myChartInstance.current.destroy();
      }
    };
  }, [data, showRsi]);

  return <canvas ref={chartRef} />;
};

export default StockChart;
