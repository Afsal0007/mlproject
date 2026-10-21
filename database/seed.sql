-- =============================================================
-- PlacementAI — bootstrap admin and demo data
-- Run after schema.sql. Safe to re-run; demo rows are upserted and
-- one demo skill assessment per student is maintained by source tag.
-- =============================================================

-- FIRST SUPER_ADMIN TEMPLATE
-- 1. Create the first user in Supabase Dashboard > Authentication > Users.
-- 2. Replace the UUID and placeholder details below, then uncomment and run.
-- INSERT INTO public.admin_profiles (user_id, full_name, email, role, is_active)
-- VALUES ('PASTE-AUTH-USER-UUID-HERE'::uuid, 'Admin Name', 'admin@example.edu', 'super_admin', true)
-- ON CONFLICT (user_id) DO UPDATE
-- SET role = 'super_admin', is_active = true, full_name = EXCLUDED.full_name,
--     email = EXCLUDED.email;

-- Synthetic demonstration records; use real, consented data for production.
INSERT INTO public.students (
    usn, full_name, email, department, batch_year, tenth_pct, twelfth_pct, cgpa,
    aptitude_score, technical_score, communication_score, internships, projects,
    certifications, backlogs, extracurricular, placement_training,
    placement_status, company, package_lpa
) VALUES
    ('1XX21CS001', 'Aarav Sharma', 'aarav.sharma@example.edu', 'CSE', 2025, 92.40, 89.20, 9.12, 88, 91, 82, 2, 4, 3, 0, true, true, 'placed', 'Infosys', 8.50),
    ('1XX21CS002', 'Ananya Iyer', 'ananya.iyer@example.edu', 'CSE', 2025, 88.00, 91.60, 8.74, 84, 87, 90, 1, 3, 2, 0, true, true, 'placed', 'Accenture', 7.20),
    ('1XX21CS003', 'Vihaan Reddy', 'vihaan.reddy@example.edu', 'CSE', 2025, 79.80, 82.40, 7.68, 72, 76, 70, 1, 3, 1, 0, false, true, 'in_process', NULL, NULL),
    ('1XX21CS004', 'Diya Nair', 'diya.nair@example.edu', 'CSE', 2025, 95.20, 93.00, 9.48, 93, 95, 88, 2, 5, 4, 0, true, true, 'placed', 'Microsoft', 24.00),
    ('1XX21CS005', 'Arjun Menon', 'arjun.menon@example.edu', 'CSE', 2025, 74.60, 77.20, 6.92, 61, 65, 72, 0, 2, 1, 1, true, false, 'not_placed', NULL, NULL),
    ('1XX21CS006', 'Meera Kulkarni', 'meera.kulkarni@example.edu', 'CSE', 2025, 86.40, 88.80, 8.36, 81, 84, 86, 1, 4, 2, 0, true, true, 'placed', 'TCS', 6.80),
    ('1XX21CS007', 'Ishaan Patel', 'ishaan.patel@example.edu', 'CSE', 2025, 81.20, 80.60, 7.42, 68, 73, 66, 0, 2, 1, 0, false, true, 'in_process', NULL, NULL),
    ('1XX21CS008', 'Saanvi Rao', 'saanvi.rao@example.edu', 'CSE', 2025, 90.80, 92.20, 8.96, 89, 86, 92, 2, 4, 3, 0, true, true, 'placed', 'Wipro', 9.00),
    ('1XX21CS009', 'Kabir Desai', 'kabir.desai@example.edu', 'CSE', 2025, 68.40, 72.80, 6.48, 57, 60, 64, 0, 1, 0, 2, false, false, 'not_placed', NULL, NULL),
    ('1XX21CS010', 'Anika Bose', 'anika.bose@example.edu', 'CSE', 2025, 84.60, 86.40, 8.08, 78, 80, 83, 1, 3, 2, 0, true, true, 'opted_out', NULL, NULL),

    ('1XX21IT001', 'Aditya Verma', 'aditya.verma@example.edu', 'IT', 2025, 87.20, 85.60, 8.52, 83, 85, 78, 2, 4, 3, 0, true, true, 'placed', 'Capgemini', 7.50),
    ('1XX21IT002', 'Prisha Shah', 'prisha.shah@example.edu', 'IT', 2025, 91.60, 94.00, 9.24, 91, 90, 94, 1, 5, 4, 0, true, true, 'placed', 'Amazon', 18.00),
    ('1XX21IT003', 'Reyansh Gupta', 'reyansh.gupta@example.edu', 'IT', 2025, 77.80, 79.20, 7.18, 67, 71, 68, 0, 2, 1, 0, false, true, 'in_process', NULL, NULL),
    ('1XX21IT004', 'Aadhya Krishnan', 'aadhya.krishnan@example.edu', 'IT', 2025, 89.40, 87.60, 8.68, 86, 88, 91, 2, 4, 3, 0, true, true, 'placed', 'IBM', 10.20),
    ('1XX21IT005', 'Rohan Chatterjee', 'rohan.chatterjee@example.edu', 'IT', 2025, 72.20, 75.80, 6.74, 59, 63, 67, 0, 2, 0, 1, true, false, 'not_placed', NULL, NULL),
    ('1XX21IT006', 'Tara Srinivasan', 'tara.srinivasan@example.edu', 'IT', 2025, 93.80, 90.40, 9.02, 87, 92, 89, 2, 5, 4, 0, true, true, 'placed', 'Zoho', 12.00),
    ('1XX21IT007', 'Dhruv Joshi', 'dhruv.joshi@example.edu', 'IT', 2025, 82.60, 83.20, 7.86, 75, 78, 73, 1, 3, 2, 0, false, true, 'in_process', NULL, NULL),
    ('1XX21IT008', 'Myra Fernandes', 'myra.fernandes@example.edu', 'IT', 2025, 85.40, 89.80, 8.32, 80, 82, 88, 1, 3, 3, 0, true, true, 'placed', 'Deloitte', 9.50),
    ('1XX21IT009', 'Karthik Shetty', 'karthik.shetty@example.edu', 'IT', 2025, 66.80, 70.40, 6.32, 55, 58, 61, 0, 1, 1, 2, false, false, 'not_placed', NULL, NULL),
    ('1XX21IT010', 'Ira Mukherjee', 'ira.mukherjee@example.edu', 'IT', 2025, 88.60, 91.20, 8.88, 85, 89, 93, 1, 4, 3, 0, true, true, 'opted_out', NULL, NULL),

    ('1XX21AD001', 'Sai Kiran Reddy', 'sai.kiran.reddy@example.edu', 'AIDS', 2025, 90.20, 88.40, 8.82, 89, 87, 81, 2, 4, 3, 0, true, true, 'placed', 'Fractal Analytics', 11.00),
    ('1XX21AD002', 'Ishita Banerjee', 'ishita.banerjee@example.edu', 'AIDS', 2025, 94.40, 96.20, 9.56, 96, 94, 92, 2, 5, 5, 0, true, true, 'placed', 'Google', 28.00),
    ('1XX21AD003', 'Nikhil Pawar', 'nikhil.pawar@example.edu', 'AIDS', 2025, 78.40, 81.60, 7.52, 73, 74, 69, 1, 3, 2, 0, false, true, 'in_process', NULL, NULL),
    ('1XX21AD004', 'Kavya Hegde', 'kavya.hegde@example.edu', 'AIDS', 2025, 86.80, 90.00, 8.46, 84, 83, 90, 1, 4, 3, 0, true, true, 'placed', 'Mu Sigma', 8.00),
    ('1XX21AD005', 'Manav Sethi', 'manav.sethi@example.edu', 'AIDS', 2025, 70.60, 74.20, 6.58, 60, 62, 65, 0, 2, 1, 1, false, false, 'not_placed', NULL, NULL),
    ('1XX21AD006', 'Riya Pillai', 'riya.pillai@example.edu', 'AIDS', 2025, 92.80, 91.40, 9.08, 90, 93, 87, 2, 5, 4, 0, true, true, 'placed', 'IBM', 13.50),
    ('1XX21AD007', 'Yash Thakur', 'yash.thakur@example.edu', 'AIDS', 2025, 83.40, 84.60, 7.94, 77, 79, 75, 1, 3, 2, 0, true, true, 'in_process', NULL, NULL),
    ('1XX21AD008', 'Aditi Narayanan', 'aditi.narayanan@example.edu', 'AIDS', 2025, 88.20, 87.80, 8.62, 82, 86, 91, 1, 4, 3, 0, true, true, 'placed', 'Accenture', 7.80),
    ('1XX21AD009', 'Pranav Bhat', 'pranav.bhat@example.edu', 'AIDS', 2025, 65.20, 69.80, 6.18, 52, 56, 60, 0, 1, 0, 2, false, false, 'not_placed', NULL, NULL),
    ('1XX21AD010', 'Nisha Thomas', 'nisha.thomas@example.edu', 'AIDS', 2025, 87.60, 89.40, 8.38, 81, 84, 88, 1, 3, 3, 0, true, true, 'opted_out', NULL, NULL),

    ('1XX21EC001', 'Vikram Singh', 'vikram.singh@example.edu', 'ECE', 2025, 85.80, 83.60, 8.14, 78, 81, 76, 1, 3, 2, 0, true, true, 'placed', 'Tata Elxsi', 7.00),
    ('1XX21EC002', 'Sneha Das', 'sneha.das@example.edu', 'ECE', 2025, 91.40, 93.60, 9.18, 90, 92, 94, 2, 4, 4, 0, true, true, 'placed', 'Qualcomm', 16.00),
    ('1XX21EC003', 'Rahul Yadav', 'rahul.yadav@example.edu', 'ECE', 2025, 76.40, 78.60, 7.26, 69, 72, 70, 0, 2, 1, 0, false, true, 'in_process', NULL, NULL),
    ('1XX21EC004', 'Pooja Nambiar', 'pooja.nambiar@example.edu', 'ECE', 2025, 88.80, 86.20, 8.58, 84, 88, 90, 1, 4, 3, 0, true, true, 'placed', 'Bosch', 9.20),
    ('1XX21EC005', 'Siddharth Jain', 'siddharth.jain@example.edu', 'ECE', 2025, 69.40, 73.60, 6.62, 58, 61, 66, 0, 2, 0, 1, false, false, 'not_placed', NULL, NULL),
    ('1XX21EC006', 'Lavanya Gopal', 'lavanya.gopal@example.edu', 'ECE', 2025, 93.20, 90.80, 9.32, 92, 95, 89, 2, 5, 4, 0, true, true, 'placed', 'Texas Instruments', 17.50),
    ('1XX21EC007', 'Amanpreet Kaur', 'amanpreet.kaur@example.edu', 'ECE', 2025, 81.80, 82.20, 7.72, 74, 76, 82, 1, 3, 2, 0, true, true, 'in_process', NULL, NULL),
    ('1XX21EC008', 'Gautham Krish', 'gautham.krish@example.edu', 'ECE', 2025, 84.20, 88.60, 8.28, 79, 85, 80, 1, 3, 2, 0, false, true, 'placed', 'L&T Technology Services', 8.40),
    ('1XX21EC009', 'Shreya Dutta', 'shreya.dutta@example.edu', 'ECE', 2025, 63.80, 68.20, 6.04, 51, 55, 62, 0, 1, 0, 2, true, false, 'not_placed', NULL, NULL),
    ('1XX21EC010', 'Neil Mathew', 'neil.mathew@example.edu', 'ECE', 2025, 89.20, 90.60, 8.72, 86, 89, 91, 2, 4, 3, 0, true, true, 'opted_out', NULL, NULL)
ON CONFLICT (usn) DO UPDATE SET
    full_name = EXCLUDED.full_name,
    email = EXCLUDED.email,
    department = EXCLUDED.department,
    batch_year = EXCLUDED.batch_year,
    tenth_pct = EXCLUDED.tenth_pct,
    twelfth_pct = EXCLUDED.twelfth_pct,
    cgpa = EXCLUDED.cgpa,
    aptitude_score = EXCLUDED.aptitude_score,
    technical_score = EXCLUDED.technical_score,
    communication_score = EXCLUDED.communication_score,
    internships = EXCLUDED.internships,
    projects = EXCLUDED.projects,
    certifications = EXCLUDED.certifications,
    backlogs = EXCLUDED.backlogs,
    extracurricular = EXCLUDED.extracurricular,
    placement_training = EXCLUDED.placement_training,
    placement_status = EXCLUDED.placement_status,
    company = EXCLUDED.company,
    package_lpa = EXCLUDED.package_lpa;

WITH demo_assessments (usn, dsa, system_design, core_cs, aptitude, communication) AS (
    VALUES
    ('1XX21CS001', 91, 78, 88, 88, 82), ('1XX21CS002', 86, 77, 84, 84, 90),
    ('1XX21CS003', 74, 61, 72, 72, 70), ('1XX21CS004', 96, 89, 94, 93, 88),
    ('1XX21CS005', 62, 48, 60, 61, 72), ('1XX21CS006', 83, 71, 82, 81, 86),
    ('1XX21CS007', 70, 56, 69, 68, 66), ('1XX21CS008', 88, 76, 85, 89, 92),
    ('1XX21CS009', 57, 42, 55, 57, 64), ('1XX21CS010', 79, 67, 77, 78, 83),
    ('1XX21IT001', 84, 72, 81, 83, 78), ('1XX21IT002', 92, 84, 90, 91, 94),
    ('1XX21IT003', 69, 57, 68, 67, 68), ('1XX21IT004', 87, 75, 85, 86, 91),
    ('1XX21IT005', 60, 46, 58, 59, 67), ('1XX21IT006', 91, 79, 89, 87, 89),
    ('1XX21IT007', 76, 64, 74, 75, 73), ('1XX21IT008', 81, 69, 79, 80, 88),
    ('1XX21IT009', 54, 40, 53, 55, 61), ('1XX21IT010', 85, 73, 83, 85, 93),
    ('1XX21AD001', 88, 81, 86, 89, 81), ('1XX21AD002', 95, 91, 93, 96, 92),
    ('1XX21AD003', 75, 67, 73, 73, 69), ('1XX21AD004', 82, 74, 81, 84, 90),
    ('1XX21AD005', 61, 50, 59, 60, 65), ('1XX21AD006', 93, 86, 92, 90, 87),
    ('1XX21AD007', 78, 68, 77, 77, 75), ('1XX21AD008', 85, 76, 84, 82, 91),
    ('1XX21AD009', 52, 39, 51, 52, 60), ('1XX21AD010', 80, 70, 79, 81, 88),
    ('1XX21EC001', 79, 68, 82, 78, 76), ('1XX21EC002', 91, 82, 93, 90, 94),
    ('1XX21EC003', 70, 60, 74, 69, 70), ('1XX21EC004', 86, 74, 88, 84, 90),
    ('1XX21EC005', 59, 47, 63, 58, 66), ('1XX21EC006', 94, 88, 95, 92, 89),
    ('1XX21EC007', 75, 65, 79, 74, 82), ('1XX21EC008', 83, 72, 86, 79, 80),
    ('1XX21EC009', 50, 38, 54, 51, 62), ('1XX21EC010', 87, 78, 89, 86, 91)
)
INSERT INTO public.skill_assessments (
    student_id, dsa, system_design, core_cs, aptitude, communication, source
)
SELECT s.id, a.dsa, a.system_design, a.core_cs, a.aptitude, a.communication, 'demo_seed_v1'
FROM demo_assessments AS a
JOIN public.students AS s ON s.usn = a.usn
WHERE NOT EXISTS (
    SELECT 1 FROM public.skill_assessments AS existing
    WHERE existing.student_id = s.id AND existing.source = 'demo_seed_v1'
);