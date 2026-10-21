-- =============================================================
-- Placement AI — Database Schema (Stub — Phase 0)
-- Full DDL will be written in Phase 1
-- =============================================================

-- Enable UUID extension (PostgreSQL)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================
-- USERS
-- =============================================================
CREATE TABLE IF NOT EXISTS users (
    id          SERIAL PRIMARY KEY,
    email       VARCHAR(255) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    role        VARCHAR(20) NOT NULL DEFAULT 'student',  -- student | recruiter | admin
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================
-- STUDENT PROFILES
-- =============================================================
CREATE TABLE IF NOT EXISTS student_profiles (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    full_name       VARCHAR(255),
    cgpa            NUMERIC(4, 2),
    backlogs        INTEGER DEFAULT 0,
    tenth_pct       NUMERIC(5, 2),
    twelfth_pct     NUMERIC(5, 2),
    stream          VARCHAR(100),
    skills          TEXT[],          -- array of skill names
    internships     INTEGER DEFAULT 0,
    projects        INTEGER DEFAULT 0,
    certifications  TEXT[],
    resume_url      TEXT,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================
-- COMPANIES
-- =============================================================
CREATE TABLE IF NOT EXISTS companies (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    industry    VARCHAR(100),
    website     TEXT,
    logo_url    TEXT,
    description TEXT,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================
-- JOB POSTINGS
-- =============================================================
CREATE TABLE IF NOT EXISTS job_postings (
    id              SERIAL PRIMARY KEY,
    company_id      INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    required_skills TEXT[],
    min_cgpa        NUMERIC(4, 2) DEFAULT 0.0,
    ctc_lpa         NUMERIC(6, 2),
    deadline        DATE,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================
-- APPLICATIONS
-- =============================================================
CREATE TABLE IF NOT EXISTS applications (
    id              SERIAL PRIMARY KEY,
    student_id      INTEGER NOT NULL REFERENCES student_profiles(id),
    job_posting_id  INTEGER NOT NULL REFERENCES job_postings(id),
    status          VARCHAR(30) DEFAULT 'applied',  -- applied | shortlisted | rejected | offered
    applied_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE (student_id, job_posting_id)
);

-- =============================================================
-- ML PREDICTIONS
-- =============================================================
CREATE TABLE IF NOT EXISTS predictions (
    id                  SERIAL PRIMARY KEY,
    student_id          INTEGER NOT NULL REFERENCES student_profiles(id),
    placement_prob      NUMERIC(5, 4),   -- 0.0000 – 1.0000
    predicted_ctc_lpa   NUMERIC(6, 2),
    model_version       VARCHAR(50),
    predicted_at        TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================
-- SKILL GAPS
-- =============================================================
CREATE TABLE IF NOT EXISTS skill_gaps (
    id              SERIAL PRIMARY KEY,
    student_id      INTEGER NOT NULL REFERENCES student_profiles(id),
    job_posting_id  INTEGER REFERENCES job_postings(id),
    missing_skills  TEXT[],
    gap_score       NUMERIC(5, 4),   -- 0 = no gap, 1 = full gap
    computed_at     TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
