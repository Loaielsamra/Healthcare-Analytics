SELECT *
FROM (
    SELECT 
        d.doctor_id,
        d.name,
        ROUND(
            SUM(CASE WHEN a.attended = TRUE THEN 1 ELSE 0 END)::numeric / COUNT(*) * 100,
            2
        ) AS attendance_rate,
        ROW_NUMBER() OVER (
            ORDER BY SUM(CASE WHEN a.attended = TRUE THEN 1 ELSE 0 END)::numeric / COUNT(*) DESC
        ) AS rank
    FROM appointments a
    JOIN doctors d ON a.doctor_id = d.doctor_id
    GROUP BY d.doctor_id, d.name
) ranked
WHERE rank <= 3;
