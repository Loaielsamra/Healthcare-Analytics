SELECT 
    neighborhood,
    ROUND(
        SUM(CASE WHEN attended = false THEN 1 ELSE 0 END)::numeric / COUNT(*) * 100,
        2
    ) AS no_show_rate,
    RANK() OVER (ORDER BY SUM(CASE WHEN attended = false THEN 1 ELSE 0 END)::numeric / COUNT(*) DESC) AS rank_no_show
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY neighborhood
ORDER BY no_show_rate DESC;
