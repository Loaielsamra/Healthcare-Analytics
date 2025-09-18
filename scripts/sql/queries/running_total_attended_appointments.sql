SELECT
    appointment_day::date AS day,
    SUM(CASE WHEN attended = TRUE THEN 1 ELSE 0 END) AS attended_on_day,
    SUM(SUM(CASE WHEN attended = TRUE THEN 1 ELSE 0 END))
        OVER (ORDER BY appointment_day::date) AS running_total_attended
FROM appointments
GROUP BY appointment_day::date
ORDER BY day;
