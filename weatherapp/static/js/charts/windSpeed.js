// Wind Speed Chart with Wind Gusts
// Wind Speeds formatted as a line chart
// Wind Gust formatted as a bar chart

const fetch = require('node-fetch')

var ctx = document.getElementById('windSpeed-chart');
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    datasets: [{
      label: "Rainfall",
      lineTension: 0.3,
      backgroundColor: "rgba(78, 115, 223, 0.05)",
      borderColor: "rgb(26,85,227)",
      pointRadius: 3,
      pointBackgroundColor: "rgba(78, 115, 223, 1)",
      pointBorderColor: "rgba(78, 115, 223, 1)",
      pointHoverRadius: 3,
      pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
      pointHoverBorderColor: "rgba(78, 115, 223, 1)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
      data: [0, 10000, 5000, 15000, 10000, 20000, 15000, 25000, 20000, 30000, 25000, 40000],
    }],
  },
  options: {
      maintainAspectRatio: false,
      layout: {
          padding: {
              left: 10,
              right: 25,
              top: 25,
              bottom: 0
          }
      },
      scales: {
          xAxes: [{
              time: {
                  unit: 'date'
              },
              gridLines: {
                  display: false,
                  drawBorder: false
              },
              ticks: {
                  maxTicksLimit: 7
              }
          }],
          yAxes: [{
              ticks: {
                  maxTicksLimit: 5,
                  padding: 10,
              },
              gridLines: {
                  color: "rgb(234, 236, 244)",
                  zeroLineColor: "rgb(234, 236, 244)",
                  drawBorder: false,
                  borderDash: [2],
                  zeroLineBorderDash: [2]
              }
          }],
      },
      legend: {
          display: false
      },
      tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          titleMarginBottom: 10,
          titleFontColor: '#6e707e',
          titleFontSize: 14,
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: false,
          intersect: false,
          mode: 'index',
          caretPadding: 10,
      }
  }
});
