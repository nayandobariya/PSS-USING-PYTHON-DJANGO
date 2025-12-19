// Dashboard Interactivity Script

document.addEventListener('DOMContentLoaded', function () {
  // Fade in animation for cards
  const cards = document.querySelectorAll('.card');
  cards.forEach((card, index) => {
    card.style.opacity = 0;
    setTimeout(() => {
      card.style.transition = 'opacity 0.6s ease-in-out';
      card.style.opacity = 1;
    }, index * 150);
  });

  // Hover effects for cards
  cards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'scale(1.05)';
      card.style.boxShadow = '0 15px 35px rgba(0, 0, 0, 0.3)';
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'scale(1)';
      card.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
    });
  });

  // Tooltip initialization
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'));
  tooltipTriggerList.forEach(function (tooltipTriggerEl) {
    new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Chart.js integration for admin and teacher dashboards
  if (typeof Chart !== 'undefined') {
    // User Distribution Pie Chart
    const userChartCanvas = document.getElementById('userDistributionChart');
    if (userChartCanvas) {
      const userChart = new Chart(userChartCanvas, {
        type: 'pie',
        data: {
          labels: ['Approved Students', 'Approved Teachers', 'Pending Students', 'Pending Teachers'],
          datasets: [{
            data: [
              parseInt(userChartCanvas.dataset.approved_students),
              parseInt(userChartCanvas.dataset.approved_teachers),
              parseInt(userChartCanvas.dataset.pending_students),
              parseInt(userChartCanvas.dataset.pending_teachers)
            ],
            backgroundColor: [
              '#4C51BF',
              '#3186ca',
              '#FF6384',
              '#FF9F40'
            ],
            borderWidth: 2,
            borderColor: '#fff'
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                padding: 20,
                usePointStyle: true
              }
            },
            tooltip: {
              enabled: true,
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const value = context.parsed;
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = ((value / total) * 100).toFixed(1);
                  return `${label}: ${value} (${percentage}%)`;
                }
              }
            }
          },
          animation: {
            animateScale: true,
            animateRotate: true
          }
        }
      });
    }

    // System Metrics Doughnut Chart
    const systemChartCanvas = document.getElementById('systemMetricsChart');
    if (systemChartCanvas) {
      const systemChart = new Chart(systemChartCanvas, {
        type: 'doughnut',
        data: {
          labels: ['Courses', 'Questions', 'Pending Papers', 'Paper Requests'],
          datasets: [{
            data: [
              parseInt(systemChartCanvas.dataset.courses),
              parseInt(systemChartCanvas.dataset.questions),
              parseInt(systemChartCanvas.dataset.pending_papers),
              parseInt(systemChartCanvas.dataset.paper_requests)
            ],
            backgroundColor: [
              '#104f66',
              '#53616e',
              '#FF6384',
              '#4C51BF'
            ],
            borderWidth: 2,
            borderColor: '#fff'
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                padding: 20,
                usePointStyle: true
              }
            },
            tooltip: {
              enabled: true,
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const value = context.parsed;
                  return `${label}: ${value}`;
                }
              }
            }
          },
          animation: {
            animateScale: true,
            animateRotate: true
          }
        }
      });
    }

    // Paper Request Status Bar Chart
    const paperChartCanvas = document.getElementById('paperRequestChart');
    if (paperChartCanvas) {
      const paperChart = new Chart(paperChartCanvas, {
        type: 'bar',
        data: {
          labels: ['Approved Requests', 'Pending Requests'],
          datasets: [{
            label: 'Paper Requests',
            data: [
              parseInt(paperChartCanvas.dataset.approved_requests),
              parseInt(paperChartCanvas.dataset.pending_requests)
            ],
            backgroundColor: [
              '#28a745',
              '#ffc107'
            ],
            borderColor: [
              '#1e7e34',
              '#e0a800'
            ],
            borderWidth: 2,
            borderRadius: 4,
            borderSkipped: false
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              enabled: true,
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const value = context.parsed.y;
                  return `${label}: ${value}`;
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0, 0, 0, 0.1)'
              },
              ticks: {
                precision: 0
              }
            },
            x: {
              grid: {
                display: false
              }
            }
          },
          animation: {
            duration: 2000,
            easing: 'easeInOutQuart'
          }
        }
      });
    }

    // Teacher Dashboard Chart
    const teacherChartCanvas = document.getElementById('teacherStatsChart');
    if (teacherChartCanvas) {
      const teacherChart = new Chart(teacherChartCanvas, {
        type: 'doughnut',
        data: {
          labels: ['Registered Students', 'Courses', 'Questions'],
          datasets: [{
            data: [
              parseInt(teacherChartCanvas.dataset.students),
              parseInt(teacherChartCanvas.dataset.courses),
              parseInt(teacherChartCanvas.dataset.questions)
            ],
            backgroundColor: [
              '#303a3c',
              '#4C51BF',
              '#104f66'
            ]
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'bottom',
            },
            tooltip: {
              enabled: true
            }
          }
        }
      });
    }
  }
});
