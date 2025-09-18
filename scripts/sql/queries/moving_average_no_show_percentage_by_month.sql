WITH monthly_rates AS (
    SELECT 
        DATE_TRUNC('month', appointment_day) AS month,
        ROUND(
            SUM(CASE WHEN attended = FALSE THEN 1 ELSE 0 END)::numeric / COUNT(*) * 100,
            2
        ) AS no_show_rate
    FROM appointments
    GROUP BY DATE_TRUNC('month', appointment_day)
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
