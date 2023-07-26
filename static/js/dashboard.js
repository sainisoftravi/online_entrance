const Pie_Chart = document.getElementById('Pie-Chart-correct-vs-incorrect');
const Stacked_Bar_Chart = document.getElementById('Stacked-Bar-Chart-Results');
const Pie_Chart_Each_Programme = document.getElementById('Pie-Chart-each-programme');


new Chart(Pie_Chart, {
        type: 'doughnut',

        data: {
            labels: data['Pie-Chart-correct-vs-incorrect']['labels'],
            datasets: [
                {
                    data: data['Pie-Chart-correct-vs-incorrect']['data'],
                    backgroundColor: ["green", "red"],
                }
            ]
        },

        options: {
            plugins: {
                legend: {
                  position: 'top',
                  align: 'middle',
                },

                title: {
                    display: true,
                    position:'top',
                    align:'center',
                    fullSize: false,
                    text: data['Pie-Chart-correct-vs-incorrect']['title'],

                    font: {
                        size: 20,
                    }
                }
            },

            scales: {
                x: {
                    display: false,
                },

                y: {
                    display: false,
                }
            }
        }
    }
);


new Chart(Pie_Chart_Each_Programme, {
    type: 'pie',

    data: {
        labels: data['Pie-Chart-each-programme']['labels'],
        datasets: [
            {
                data: data['Pie-Chart-each-programme']['data'],
            }
        ]
    },

    options: {
        plugins: {
            legend: {
              position: 'top',
              align: 'middle',
            },

            title: {
                display: true,
                position:'top',
                align:'center',
                fullSize: false,
                text: data['Pie-Chart-each-programme']['title'],

                font: {
                    size: 20,
                }
            }
        },

        scales: {
            x: {
                display: false,
            },

            y: {
                display: false,
            }
        }
    }
}
);


new Chart(Stacked_Bar_Chart, {
        type: 'bar',

        data: {
            labels: data['Stacked-Bar-Chart-Results']['x-axis-labels'],
            datasets: [
                    {
                        label: 'Correct Answer',
                        backgroundColor: 'green',
                        data: data['Stacked-Bar-Chart-Results']['correct'],
                        borderWidth: 1,
                    },
                    {
                        backgroundColor: 'red',
                        label: 'Incorrect Answer',
                        data: data['Stacked-Bar-Chart-Results']['incorrect'],
                        borderWidth: 1,
                    }
                ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                position: 'top',
                align: 'middle',
                },

                title: {
                    display: true,
                    position:'top',
                    align:'center',
                    fullSize: false,
                    text: data['Stacked-Bar-Chart-Results']['title'],

                    font: {
                        size: 20,
                    }
                }
            },

            scales: {
                x: {
                    stacked: true,
                },

                y: {
                    stacked: true,
                }
            }
        }
    }
);
