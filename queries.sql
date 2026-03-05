-- 1. What is the overall attrition rate?
SELECT 
    (SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as Attrition_Rate
FROM attrition_data;

-- 2. Which Department has the highest turnover?
SELECT Department, COUNT(*) as Leavers
FROM attrition_data
WHERE Attrition = 'Yes'
GROUP BY Department
ORDER BY Leavers DESC;

-- 3. Is there a correlation between OverTime and Attrition?
SELECT OverTime, Attrition, COUNT(*) as Count
FROM attrition_data
GROUP BY OverTime, Attrition;