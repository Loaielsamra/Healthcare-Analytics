SELECT
    CAST(a.appointment_day AS DATE) AS day,
    SUM(CASE WHEN a.attended = 1 THEN 1 ELSE 0 END) AS attended_on_day,
    SUM(SUM(CASE WHEN a.attended = 1 THEN 1 ELSE 0 END))
        OVER (ORDER BY CAST(a.appointment_day AS DATE)) AS running_total_attended
FROM appointments a
GROUP BY CAST(a.appointment_day AS DATE)
ORDER BY day;
