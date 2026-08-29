// ============================================================
// ResumeIQ API Configuration
// ============================================================

// VITE_API_URL is used when running locally or in production.
// If it is not provided, the deployed Render backend is used.
export const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  "https://ai-resume-analyzer-u3qk.onrender.com";

// ============================================================
// API ENDPOINTS
// ============================================================

export const API_ENDPOINTS = {
  // Authentication
  LOGIN: `${API_BASE_URL}/api/auth/login`,
  REGISTER: `${API_BASE_URL}/api/auth/register`,

  // Resume Analysis
  UPLOAD_RESUME: `${API_BASE_URL}/api/resume/upload`,

  // Job Matching
  JOB_MATCH: `${API_BASE_URL}/api/resume/job_match`,

  // Resume History
  RESUME_HISTORY: `${API_BASE_URL}/api/resume/history`,

  // Resume Details
  RESUME_DETAILS: (id) =>
    `${API_BASE_URL}/api/resume/${id}`,

  // Resume Analysis Details
  RESUME_ANALYSIS: (id) =>
    `${API_BASE_URL}/api/resume/${id}/analysis`,
};

// ============================================================
// DEFAULT EXPORT
// ============================================================

export default {
  API_BASE_URL,
  API_ENDPOINTS,
};