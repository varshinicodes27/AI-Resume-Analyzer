export const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8001";

export const API_ENDPOINTS = {
  LOGIN: `${API_BASE_URL}/api/auth/login`,
  REGISTER: `${API_BASE_URL}/api/auth/register`,
  UPLOAD_RESUME: `${API_BASE_URL}/api/resume/upload`,
  JOB_MATCH: `${API_BASE_URL}/api/resume/job_match`,
  RESUME_HISTORY: `${API_BASE_URL}/api/resume/history`,
  RESUME_DETAILS: (id) => `${API_BASE_URL}/api/resume/${id}`,
  RESUME_ANALYSIS: (id) => `${API_BASE_URL}/api/resume/${id}/analysis`,
};

export default {
  API_BASE_URL,
  API_ENDPOINTS,
};
