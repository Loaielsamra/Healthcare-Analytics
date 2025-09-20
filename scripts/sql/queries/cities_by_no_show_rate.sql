SELECT 
    p.neighborhood,
    ROUND(
        SUM(CASE WHEN a.attended = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS no_show_rate,
    RANK() OVER (
        ORDER BY SUM(CASE WHEN a.attended = 0 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) DESC
    ) AS rank_no_show
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY p.neighborhood
ORDER BY no_show_rate DESC;