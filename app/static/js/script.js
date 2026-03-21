
// Graphique mensuel
const ctxMonthly = document.getElementById('monthlyChart').getContext('2d');
const monthlyChart = new Chart(ctxMonthly, {
    type: 'bar',
    data: {
        labels: {{ months|tojson }},
        datasets: [
            {
                label: 'Revenus',
                data: {{ income_data|tojson }},
                backgroundColor: 'rgba(40, 167, 69, 0.5)',
                borderColor: 'rgba(40, 167, 69, 1)',
                borderWidth: 1
            },
            {
                label: 'Dépenses',
                data: {{ expense_data|tojson }},
                backgroundColor: 'rgba(220, 53, 69, 0.5)',
                borderColor: 'rgba(220, 53, 69, 1)',
                borderWidth: 1
            }
        ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Graphique des catégories
const ctxCategory = document.getElementById('categoryChart').getContext('2d');
const categoryChart = new Chart(ctxCategory, {
    type: 'pie',
    data: {
        labels: {{ cat_labels|tojson }},
        datasets: [{
            data: {{ cat_expenses|tojson }},
            backgroundColor: [
                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
            ],
        }]
    }
});
document.addEventListener('DOMContentLoaded', () => {
    // Animation des cartes
    gsap.utils.toArray('.card').forEach((card, i) => {
        gsap.from(card, {
            scrollTrigger: { trigger: card, start: 'top 80%' },
            y: 50,
            opacity: 0,
            duration: 0.6,
            delay: i * 0.1,
            ease: 'power2.out'
        });
    });
});