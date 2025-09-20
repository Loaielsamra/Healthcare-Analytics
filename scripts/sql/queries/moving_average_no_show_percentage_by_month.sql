WITH monthly_rates AS (
    SELECT 
        CAST(FORMAT(a.appointment_day, 'yyyy-MM-01') AS DATE) AS month,
        ROUND(
            SUM(CASE WHEN a.attended = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
            2
        ) AS no_show_rate
    FROM appointments a
    GROUP BY CAST(FORMAT(a.appointment_day, 'yyyy-MM-01') AS DATE)
)
SELECT
    month,
    no_show_rate,
    ROUND(
        AVG(no_show_rate) OVER (
            ORDER BY month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 2
    ) AS moving_avg_no_show
FROM monthly_rates
ORDER BY month;
