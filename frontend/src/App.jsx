import { useRef, useState } from "react";
import "./App.css";
import Auth from "./Auth.jsx";
import { API_ENDPOINTS } from "./services/api.js";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!localStorage.getItem("access_token")
  );

  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);
  const [error, setError] = useState("");

  // ================= JOB MATCHER =================

  const [jobDescription, setJobDescription] = useState("");
  const [jobMatchData, setJobMatchData] = useState(null);
  const [isMatching, setIsMatching] = useState(false);
  const [jobMatchError, setJobMatchError] = useState("");

  // ================= AUTH =================

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("full_name");

    setIsAuthenticated(false);
    setAnalysisData(null);
    setSelectedFile(null);
    setJobDescription("");
    setJobMatchData(null);
    setError("");
    setJobMatchError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  // ================= TOKEN HANDLER =================

  const handleUnauthorized = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("full_name");

    setIsAuthenticated(false);
    setAnalysisData(null);
    setSelectedFile(null);
    setJobMatchData(null);

    setError("Your session has expired. Please login again.");
  };

  // ================= FILE HANDLING =================

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    if (!file) return;

    if (file.type !== "application/pdf") {
      setError("Please upload a PDF resume.");
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
    setError("");
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  // ================= RESUME ANALYSIS =================

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError("Please upload your resume first.");
      return;
    }

    const token = localStorage.getItem("access_token");

    if (!token) {
      handleUnauthorized();
      return;
    }

    setIsAnalyzing(true);
    setError("");
    setAnalysisData(null);
    setJobMatchData(null);
    setJobMatchError("");

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(
        API_ENDPOINTS.UPLOAD_RESUME,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      if (response.status === 401) {
        handleUnauthorized();
        return;
      }

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.detail ||
            data?.message ||
            "Resume analysis failed."
        );
      }

      console.log("ResumeIQ Analysis:", data);

      setAnalysisData(data);
    } catch (err) {
      console.error("Analysis error:", err);

      setError(
        err.message ||
          "Something went wrong while analyzing the resume."
      );
    } finally {
      setIsAnalyzing(false);
    }
  };

  // ================= JOB MATCHING =================

  const handleJobMatch = async () => {
    const trimmedJd = jobDescription.trim();

    if (!trimmedJd) {
      setJobMatchError(
        "Please paste a job description first."
      );
      return;
    }

    if (trimmedJd.length < 20) {
      setJobMatchError(
        "Job description is too short. Please provide at least 20 characters."
      );
      return;
    }

    if (!analysisData) {
      setJobMatchError(
        "Please upload and analyze your resume first."
      );
      return;
    }

    const token = localStorage.getItem("access_token");

    if (!token) {
      handleUnauthorized();
      return;
    }

    setIsMatching(true);
    setJobMatchError("");
    setJobMatchData(null);

    try {
      const response = await fetch(
        API_ENDPOINTS.JOB_MATCH,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            job_description: trimmedJd,
          }),
        }
      );

      if (response.status === 401) {
        handleUnauthorized();
        return;
      }

      const data = await response.json();

      if (!response.ok) {
        if (response.status === 500) {
          throw new Error(
            "Unable to analyze the job description right now. Please try again."
          );
        }

        throw new Error(
          data?.detail ||
            data?.message ||
            "Job matching failed. Please check the job description."
        );
      }

      console.log("ResumeIQ Job Match:", data);

      setJobMatchData(data);
    } catch (err) {
      console.error("Job match error:", err);

      setJobMatchError(
        err.message ||
          "Unable to analyze the job description right now. Please try again."
      );
    } finally {
      setIsMatching(false);
    }
  };

  // ================= NAVIGATION =================

  const scrollToUpload = () => {
    document
      .getElementById("upload")
      ?.scrollIntoView({
        behavior: "smooth",
      });
  };

  const scrollToSection = (id) => {
    document
      .getElementById(id)
      ?.scrollIntoView({
        behavior: "smooth",
      });
  };

  // ================= RESET =================

  const resetAnalysis = () => {
    setAnalysisData(null);
    setSelectedFile(null);
    setError("");

    setJobDescription("");
    setJobMatchData(null);
    setJobMatchError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  // ================= SAFE DATA =================

  const candidate = analysisData?.candidate || {};

  const education = Array.isArray(
    analysisData?.education
  )
    ? analysisData.education
    : [];

  const skills = Array.isArray(
    analysisData?.skills
  )
    ? analysisData.skills
    : [];

  const projects = Array.isArray(
    analysisData?.projects
  )
    ? analysisData.projects
    : [];

  const experience = Array.isArray(
    analysisData?.experience
  )
    ? analysisData.experience
    : [];

  const certifications = Array.isArray(
    analysisData?.certifications
  )
    ? analysisData.certifications
    : [];

  const atsReport =
    analysisData?.ats_report || {};

  const sectionScores =
    atsReport.section_scores || {};

  const score = Number(
    atsReport.overall_score ?? 0
  );

  // ================= SCORE HELPERS =================

  const getScoreClass = (value) => {
    const numericValue = Number(value) || 0;

    if (numericValue >= 80) {
      return "score-good";
    }

    if (numericValue >= 60) {
      return "score-medium";
    }

    return "score-low";
  };

  const getInitials = (name) => {
    if (!name) return "R";

    return name
      .split(" ")
      .filter(Boolean)
      .slice(0, 2)
      .map((word) => word[0])
      .join("")
      .toUpperCase();
  };

  // ================= JOB MATCH DATA =================

  const matchPercentage = Number(
    jobMatchData?.match_percentage ??
      jobMatchData?.percentage ??
      0
  );

  const matchStrength =
    jobMatchData?.match_strength ||
    (matchPercentage >= 85
      ? "Excellent Match"
      : matchPercentage >= 70
      ? "Strong Match"
      : matchPercentage >= 50
      ? "Moderate Match"
      : "Low Match");

  const matchedSkills = Array.isArray(
    jobMatchData?.matched_skills
  )
    ? jobMatchData.matched_skills
    : [];

  const missingSkills = Array.isArray(
    jobMatchData?.missing_skills
  )
    ? jobMatchData.missing_skills
    : [];

  const jobDescriptionSkills = Array.isArray(
    jobMatchData?.job_description_skills
  )
    ? jobMatchData.job_description_skills
    : [];

  const resumeSuggestions = Array.isArray(
    jobMatchData?.resume_suggestions
  )
    ? jobMatchData.resume_suggestions
    : [];

  const matchRecommendation =
    jobMatchData?.recommendation || "";

  // =========================================================
  // AUTH SCREEN
  // =========================================================

  if (!isAuthenticated) {
    return <Auth onLogin={handleLogin} />;
  }

  // =========================================================
  // RETURN
  // =========================================================

  return (
    <div className="resumeiq-app">

      {/* =====================================================
          NAVBAR
      ===================================================== */}

      <header className="navbar">

        <div
          className="brand"
          onClick={() =>
            window.scrollTo({
              top: 0,
              behavior: "smooth",
            })
          }
        >
          <div className="brand-icon">✦</div>

          <div>
            <div className="brand-name">
              ResumeIQ
            </div>

            <div className="brand-tagline">
              AI-Powered Resume Analyzer
            </div>
          </div>
        </div>

        <nav className="nav-links">

          <button
            onClick={() =>
              scrollToSection("features")
            }
          >
            Features
          </button>

          <button
            onClick={() =>
              scrollToSection("how-it-works")
            }
          >
            How It Works
          </button>

          <button
            onClick={scrollToUpload}
            className="nav-cta"
          >
            Analyze Resume
          </button>

          {/* LOGOUT */}

          <button
            onClick={handleLogout}
            className="logout-button"
          >
            Logout
          </button>

        </nav>

      </header>

      {/* =====================================================
          LANDING PAGE
      ===================================================== */}

      {!analysisData && (
        <>

          {/* HERO */}

          <main className="hero">

            <div className="hero-badge">
              <span>✦</span>
              AI-powered career intelligence
            </div>

            <h1>
              Make your resume
              <br />
              <span>impossible to ignore.</span>
            </h1>

            <p className="hero-description">
              Upload your resume and let ResumeIQ
              analyze it with AI. Discover your ATS
              score, strengths, missing opportunities,
              and ways to improve your chances of
              getting shortlisted.
            </p>

            <div className="hero-actions">

              <button
                className="primary-button"
                onClick={scrollToUpload}
              >
                Analyze My Resume
                <span>→</span>
              </button>

              <button
                className="secondary-button"
                onClick={() =>
                  scrollToSection("how-it-works")
                }
              >
                See how it works
              </button>

            </div>

            <div className="trust-row">
              <span>✓ AI-powered analysis</span>
              <span>✓ Instant results</span>
              <span>✓ ATS-focused insights</span>
            </div>

          </main>

          {/* UPLOAD */}

          <section
            id="upload"
            className="upload-section"
          >

            <div className="section-heading">

              <div className="section-label">
                01 — UPLOAD
              </div>

              <h2>
                Let's analyze your
                <span> resume.</span>
              </h2>

              <p>
                Drop your resume below and ResumeIQ
                will take care of the rest.
              </p>

            </div>

            <div className="upload-card">

              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,application/pdf"
                onChange={handleFileChange}
                hidden
              />

              {!selectedFile ? (

                <div
                  className="upload-dropzone"
                  onClick={handleUploadClick}
                >

                  <div className="upload-icon">
                    ↑
                  </div>

                  <h3>
                    Upload your resume
                  </h3>

                  <p>
                    Click to browse and select your
                    PDF resume
                  </p>

                  <span className="file-hint">
                    PDF files only
                  </span>

                </div>

              ) : (

                <div className="selected-file">

                  <div className="file-icon">
                    PDF
                  </div>

                  <div className="file-information">

                    <strong>
                      {selectedFile.name}
                    </strong>

                    <span>
                      {(
                        selectedFile.size /
                        1024 /
                        1024
                      ).toFixed(2)}{" "}
                      MB
                    </span>

                  </div>

                  <button
                    className="change-file"
                    onClick={handleUploadClick}
                  >
                    Change
                  </button>

                </div>

              )}

              {error && (
                <div className="error-message">
                  ⚠ {error}
                </div>
              )}

              <button
                className="analyze-button"
                onClick={handleAnalyze}
                disabled={
                  !selectedFile ||
                  isAnalyzing
                }
              >

                {isAnalyzing ? (
                  <>
                    <span className="spinner"></span>
                    AI is analyzing...
                  </>
                ) : (
                  <>
                    Analyze Resume
                    <span>→</span>
                  </>
                )}

              </button>

            </div>

          </section>

          {/* FEATURES */}

          <section
            id="features"
            className="features-section"
          >

            <div className="section-heading">

              <div className="section-label">
                02 — FEATURES
              </div>

              <h2>
                Everything you need to
                <span> level up.</span>
              </h2>

            </div>

            <div className="feature-grid">

              <div className="feature-card">
                <div className="feature-number">
                  01
                </div>

                <div className="feature-icon">
                  ◈
                </div>

                <h3>ATS Score</h3>

                <p>
                  Understand how well your resume
                  performs against Applicant Tracking
                  Systems.
                </p>
              </div>

              <div className="feature-card">
                <div className="feature-number">
                  02
                </div>

                <div className="feature-icon">
                  ✦
                </div>

                <h3>AI Insights</h3>

                <p>
                  Get intelligent feedback about
                  strengths, weaknesses, and
                  improvement opportunities.
                </p>
              </div>

              <div className="feature-card">
                <div className="feature-number">
                  03
                </div>

                <div className="feature-icon">
                  ◎
                </div>

                <h3>Skill Analysis</h3>

                <p>
                  Discover the technical skills
                  detected from your resume
                  automatically.
                </p>
              </div>

              <div className="feature-card">
                <div className="feature-number">
                  04
                </div>

                <div className="feature-icon">
                  ↗
                </div>

                <h3>Career Ready</h3>

                <p>
                  Turn your resume into a stronger,
                  more professional representation
                  of your skills.
                </p>
              </div>

            </div>

          </section>

          {/* HOW IT WORKS */}

          <section
            id="how-it-works"
            className="steps-section"
          >

            <div className="section-heading">

              <div className="section-label">
                03 — HOW IT WORKS
              </div>

              <h2>
                Three steps.
                <span> One better resume.</span>
              </h2>

            </div>

            <div className="steps-grid">

              <div className="step-card">
                <span>01</span>

                <h3>Upload</h3>

                <p>
                  Upload your PDF resume securely
                  through ResumeIQ.
                </p>
              </div>

              <div className="step-card">
                <span>02</span>

                <h3>Analyze</h3>

                <p>
                  Our AI extracts and analyzes your
                  resume content.
                </p>
              </div>

              <div className="step-card">
                <span>03</span>

                <h3>Improve</h3>

                <p>
                  Get actionable insights to make
                  your resume stronger.
                </p>
              </div>

            </div>

          </section>

          {/* CTA */}

          <section className="cta-section">

            <div className="cta-content">

              <div className="section-label">
                READY?
              </div>

              <h2>
                Your next opportunity
                <br />
                <span>
                  starts with your resume.
                </span>
              </h2>

              <button
                className="primary-button"
                onClick={scrollToUpload}
              >
                Analyze My Resume
                <span>→</span>
              </button>

            </div>

          </section>

          {/* FOOTER */}

          <footer className="footer">

            <div>
              <strong>ResumeIQ</strong>

              <span>
                AI-Powered Resume Analyzer
              </span>
            </div>

            <p>
              Built with AI • Designed for
              ambitious careers
            </p>

          </footer>

        </>
      )}

      {/* =====================================================
          RESULTS DASHBOARD
      ===================================================== */}

      {analysisData && (

        <main className="results-page">

          {/* RESULT HEADER */}

          <section className="results-header">

            <div>

              <div className="section-label">
                RESUME ANALYSIS
              </div>

              <h1>
                Your resume,
                <span> decoded.</span>
              </h1>

              <p>
                ResumeIQ analyzed your resume and
                generated personalized ATS insights.
              </p>

            </div>

            <div className="result-status">
              <span className="status-dot"></span>
              AI Analysis Complete
            </div>

          </section>

          {/* CANDIDATE */}

          <section className="candidate-card">

            <div className="candidate-avatar">
              {getInitials(candidate.name)}
            </div>

            <div className="candidate-info">

              <div className="candidate-name">
                {candidate.name ||
                  "Candidate"}
              </div>

              <div className="candidate-contact">

                {candidate.email && (
                  <span>
                    ✉ {candidate.email}
                  </span>
                )}

                {candidate.phone && (
                  <span>
                    ☎ {candidate.phone}
                  </span>
                )}

              </div>

              <div className="profile-links">

                {candidate.linkedin && (
                  <span>LinkedIn</span>
                )}

                {candidate.github && (
                  <span>GitHub</span>
                )}

                {candidate.portfolio && (
                  <span>Portfolio</span>
                )}

              </div>

            </div>

            <button
              className="new-analysis-button"
              onClick={resetAnalysis}
            >
              Analyze Another
              <span>↗</span>
            </button>

          </section>

          {/* ATS SCORE */}

          <section className="score-overview">

            <div className="ats-score-card">

              <div className="score-card-label">
                OVERALL ATS SCORE
              </div>

              <div
                className={
                  "ats-score " +
                  getScoreClass(score)
                }
              >
                {score}
                <small>/100</small>
              </div>

              <div className="score-progress">

                <div
                  className="score-progress-fill"
                  style={{
                    width:
                      Math.min(
                        Math.max(score, 0),
                        100
                      ) + "%",
                  }}
                ></div>

              </div>

              <p>
                {score >= 80
                  ? "Excellent ATS compatibility"
                  : score >= 60
                  ? "Good foundation with room for improvement"
                  : "Your resume needs optimization"}
              </p>

            </div>

            <div className="section-score-card">

              <div className="score-card-label">
                SECTION PERFORMANCE
              </div>

              <div className="section-score-list">

                {Object.entries(sectionScores).length >
                0 ? (

                  Object.entries(sectionScores).map(
                    ([key, value]) => {

                      const percentage = Number(
                        value?.percentage ?? 0
                      );

                      return (
                        <div
                          className="section-score-row"
                          key={key}
                        >

                          <div className="section-score-title">

                            <span>
                              {key
                                .replace(/_/g, " ")
                                .replace(
                                  /\b\w/g,
                                  (letter) =>
                                    letter.toUpperCase()
                                )}
                            </span>

                            <strong>
                              {percentage}%
                            </strong>

                          </div>

                          <div className="mini-progress">

                            <div
                              className={
                                "mini-progress-fill " +
                                getScoreClass(
                                  percentage
                                )
                              }
                              style={{
                                width:
                                  Math.min(
                                    Math.max(
                                      percentage,
                                      0
                                    ),
                                    100
                                  ) + "%",
                              }}
                            ></div>

                          </div>

                        </div>
                      );
                    }
                  )

                ) : (

                  <div className="empty-state">
                    Section scores are not
                    available.
                  </div>

                )}

              </div>

            </div>

          </section>

          {/* JOB MATCHER */}

          <section className="job-matcher-section">

            <div className="result-section-heading">

              <div>

                <div className="section-label">
                  JOB MATCHER
                </div>

                <h2>
                  Match your resume
                  <span> to a job.</span>
                </h2>

                <p>
                  Paste a job description below and
                  ResumeIQ will compare it with the
                  skills detected in your resume.
                </p>

              </div>

            </div>

            <div className="job-matcher-card">

              <textarea
                className="job-description-input"
                placeholder="Paste the complete job description here (minimum 20 characters, e.g. role overview, responsibilities, required technical skills)..."
                value={jobDescription}
                onChange={(event) =>
                  setJobDescription(
                    event.target.value
                  )
                }
                rows={7}
                disabled={isMatching}
              />

              <div className="job-input-footer">
                <div className="job-char-counter">
                  <span>{jobDescription.length} characters</span>
                  {jobDescription.trim().length > 0 && jobDescription.trim().length < 20 ? (
                    <span className="char-warning"> • Minimum 20 characters required</span>
                  ) : jobDescription.trim().length >= 20 ? (
                    <span className="char-ready"> • Ready to analyze</span>
                  ) : null}
                </div>

                {jobDescription && (
                  <button
                    type="button"
                    className="clear-jd-btn"
                    onClick={() => {
                      setJobDescription("");
                      setJobMatchError("");
                    }}
                    disabled={isMatching}
                  >
                    Clear
                  </button>
                )}
              </div>

              {jobMatchError && (
                <div className="job-match-error-alert">
                  <span className="alert-icon">⚠</span>
                  <span>{jobMatchError}</span>
                </div>
              )}

              <div className="job-matcher-actions">
                <button
                  className="primary-button job-match-submit-btn"
                  onClick={handleJobMatch}
                  disabled={isMatching || jobDescription.trim().length < 20}
                >
                  {isMatching ? (
                    <>
                      <span className="spinner"></span>
                      Analyzing Job Match...
                    </>
                  ) : (
                    <>
                      Analyze Job Match
                      <span>→</span>
                    </>
                  )}
                </button>
              </div>

            </div>

            {jobMatchData && (

              <div className="job-match-result">

                {/* OVERVIEW SCORE CARD */}
                <div className="job-match-overview-card">

                  <div className="job-match-score-pill-container">
                    <div className="score-card-label">
                      JOB MATCH SCORE
                    </div>

                    <div
                      className={
                        "ats-score " +
                        getScoreClass(
                          matchPercentage
                        )
                      }
                    >
                      {matchPercentage}
                      <small>/100</small>
                    </div>

                    <div className={`match-strength-badge ${getScoreClass(matchPercentage)}`}>
                      {matchStrength}
                    </div>
                  </div>

                  <div className="job-match-progress-container">
                    <div className="job-match-progress-header">
                      <span className="match-summary-text">
                        <strong>{matchedSkills.length}</strong> of{" "}
                        <strong>
                          {jobDescriptionSkills.length ||
                            matchedSkills.length + missingSkills.length}
                        </strong>{" "}
                        required skills matched
                      </span>
                      <span className="match-percentage-text">
                        {matchPercentage}% Match
                      </span>
                    </div>

                    <div className="score-progress">
                      <div
                        className={`score-progress-fill ${getScoreClass(matchPercentage)}`}
                        style={{
                          width:
                            Math.min(
                              Math.max(
                                matchPercentage,
                                0
                              ),
                              100
                            ) + "%",
                        }}
                      ></div>
                    </div>

                    {matchRecommendation && (
                      <div className="job-match-recommendation-box">
                        <span className="recommendation-icon">💡</span>
                        <p>{matchRecommendation}</p>
                      </div>
                    )}
                  </div>

                </div>

                {/* SKILL COMPARISON COLUMNS */}
                <div className="job-match-columns-grid">

                  {/* MATCHED SKILLS */}
                  <div className="match-column matched-column-card">

                    <div className="column-header">
                      <span className="column-dot matched-dot"></span>
                      <h3>Matched Skills</h3>
                      <span className="column-badge matched-badge">
                        {matchedSkills.length}
                      </span>
                    </div>

                    {matchedSkills.length > 0 ? (
                      <div className="skills-container matched-container">
                        {matchedSkills.map(
                          (skill, index) => (
                            <span
                              className="skill-pill matched-skill-pill"
                              key={
                                "matched-" +
                                index
                              }
                            >
                              <span className="pill-icon">✓</span> {skill}
                            </span>
                          )
                        )}
                      </div>
                    ) : (
                      <div className="empty-state">
                        No matching skills detected in the current resume.
                      </div>
                    )}

                  </div>

                  {/* MISSING SKILLS */}
                  <div className="match-column missing-column-card">

                    <div className="column-header">
                      <span className="column-dot missing-dot"></span>
                      <h3>Missing Skills</h3>
                      <span className="column-badge missing-badge">
                        {missingSkills.length}
                      </span>
                    </div>

                    {missingSkills.length > 0 ? (
                      <div className="skills-container missing-container">
                        {missingSkills.map(
                          (skill, index) => (
                            <span
                              className="skill-pill missing-skill-pill"
                              key={
                                "missing-" +
                                index
                              }
                            >
                              <span className="pill-icon">+</span> {skill}
                            </span>
                          )
                        )}
                      </div>
                    ) : (
                      <div className="empty-state">
                        No major skill gaps detected for this role!
                      </div>
                    )}

                  </div>

                  {/* DETECTED JOB REQUIREMENTS */}
                  {jobDescriptionSkills.length > 0 && (
                    <div className="match-column jd-column-card">

                      <div className="column-header">
                        <span className="column-dot jd-dot"></span>
                        <h3>Job Requirements</h3>
                        <span className="column-badge jd-badge">
                          {jobDescriptionSkills.length}
                        </span>
                      </div>

                      <div className="skills-container jd-container">
                        {jobDescriptionSkills.map(
                          (skill, index) => (
                            <span
                              className="skill-pill jd-skill-pill"
                              key={
                                "jd-" +
                                index
                              }
                            >
                              {skill}
                            </span>
                          )
                        )}
                      </div>

                    </div>
                  )}

                </div>

                {/* RESUME SUGGESTIONS */}
                {resumeSuggestions.length > 0 && (
                  <div className="job-match-suggestions-card">
                    <h4>📌 Recommendations to Improve Alignment</h4>
                    <ul>
                      {resumeSuggestions.map((suggestion, index) => (
                        <li key={"suggestion-" + index}>{suggestion}</li>
                      ))}
                    </ul>
                  </div>
                )}

              </div>

            )}

          </section>

          {/* SKILLS */}

          <section className="result-section">

            <div className="result-section-heading">

              <div>

                <div className="section-label">
                  SKILLS
                </div>

                <h2>
                  Technical{" "}
                  <span>toolkit.</span>
                </h2>

              </div>

              <div className="result-count">
                {skills.length} skills detected
              </div>

            </div>

            {skills.length > 0 ? (

              <div className="skills-container">

                {skills.map(
                  (skill, index) => (

                    <span
                      className="skill-pill"
                      key={
                        skill +
                        "-" +
                        index
                      }
                    >
                      {skill}
                    </span>

                  )
                )}

              </div>

            ) : (

              <div className="empty-state">
                No technical skills detected.
              </div>

            )}

          </section>

          {/* EDUCATION */}

          <section className="result-section">

            <div className="result-section-heading">

              <div>

                <div className="section-label">
                  EDUCATION
                </div>

                <h2>
                  Academic{" "}
                  <span>journey.</span>
                </h2>

              </div>

            </div>

            {education.length > 0 ? (

              <div className="timeline">

                {education.map(
                  (item, index) => (

                    <div
                      className="timeline-item"
                      key={index}
                    >

                      <div className="timeline-marker">
                        ●
                      </div>

                      <div className="timeline-content">

                        <div className="timeline-year">
                          {item.year ||
                            "Year not specified"}
                        </div>

                        <h3>
                          {item.degree ||
                            "Education"}
                        </h3>

                        <p>
                          {item.institution ||
                            "Institution not specified"}
                        </p>

                        {item.cgpa && (
                          <span className="timeline-meta">
                            CGPA: {item.cgpa}
                          </span>
                        )}

                      </div>

                    </div>

                  )
                )}

              </div>

            ) : (

              <div className="empty-state">
                No education details detected.
              </div>

            )}

          </section>

          {/* PROJECTS */}

          <section className="result-section">

            <div className="result-section-heading">

              <div>

                <div className="section-label">
                  PROJECTS
                </div>

                <h2>
                  Things you've{" "}
                  <span>built.</span>
                </h2>

              </div>

              <div className="result-count">
                {projects.length} projects
              </div>

            </div>

            {projects.length > 0 ? (

              <div className="project-grid">

                {projects.map(
                  (project, index) => (

                    <article
                      className="project-card"
                      key={index}
                    >

                      <div className="project-card-top">

                        <span className="project-index">
                          {String(
                            index + 1
                          ).padStart(2, "0")}
                        </span>

                        <span className="project-arrow">
                          ↗
                        </span>

                      </div>

                      <h3>
                        {project.name ||
                          "Untitled Project"}
                      </h3>

                      <p>
                        {project.description ||
                          "Project description not available."}
                      </p>

                    </article>

                  )
                )}

              </div>

            ) : (

              <div className="empty-state">
                No projects detected.
              </div>

            )}

          </section>

          {/* EXPERIENCE */}

          <section className="result-section">

            <div className="result-section-heading">

              <div>

                <div className="section-label">
                  EXPERIENCE
                </div>

                <h2>
                  Professional{" "}
                  <span>impact.</span>
                </h2>

              </div>

              <div className="result-count">
                {experience.length} experience
              </div>

            </div>

            <div className="experience-list">

              {experience.length > 0 ? (

                experience.map(
                  (item, index) => (

                    <article
                      className="experience-card"
                      key={index}
                    >

                      <div className="experience-marker">
                        {index + 1}
                      </div>

                      <div className="experience-main">

                        <div className="experience-top">

                          <div>

                            <h3>
                              {item.role ||
                                "Role not specified"}
                            </h3>

                            <p>
                              {item.company ||
                                "Company not specified"}
                            </p>

                          </div>

                          <span>
                            {item.dates ||
                              "Dates not specified"}
                          </span>

                        </div>

                        <p className="experience-description">
                          {item.description ||
                            "No description available."}
                        </p>

                      </div>

                    </article>

                  )
                )

              ) : (

                <div className="empty-state">
                  No professional experience
                  detected.
                </div>

              )}

            </div>

          </section>

          {/* CERTIFICATIONS */}

          <section className="result-section">

            <div className="result-section-heading">

              <div>

                <div className="section-label">
                  CERTIFICATIONS
                </div>

                <h2>
                  Proof of{" "}
                  <span>learning.</span>
                </h2>

              </div>

              <div className="result-count">
                {certifications.length}{" "}
                certifications
              </div>

            </div>

            {certifications.length > 0 ? (

              <div className="certification-grid">

                {certifications.map(
                  (certification, index) => (

                    <div
                      className="certification-card"
                      key={index}
                    >

                      <div className="certificate-icon">
                        ✦
                      </div>

                      <div>

                        <h3>
                          {certification.name ||
                            "Certification"}
                        </h3>

                        <p>
                          {certification.organization ||
                            "Organization not specified"}
                        </p>

                      </div>

                    </div>

                  )
                )}

              </div>

            ) : (

              <div className="empty-state">
                No certifications detected.
              </div>

            )}

          </section>

          {/* AI INSIGHTS */}

          <section className="insights-section">

            <div className="insights-heading">

              <div className="section-label">
                AI INSIGHTS
              </div>

              <h2>
                What ResumeIQ
                <span> noticed.</span>
              </h2>

            </div>

            <div className="insights-grid">

              <div className="insight-card strengths">

                <div className="insight-card-header">

                  <div className="insight-icon">
                    ✓
                  </div>

                  <h3>
                    Strengths
                  </h3>

                </div>

                <div className="insight-list">

                  {(atsReport.strengths || [])
                    .length > 0 ? (

                    atsReport.strengths.map(
                      (strength, index) => (

                        <div
                          className="insight-item"
                          key={index}
                        >

                          <span>✓</span>

                          <p>
                            {strength}
                          </p>

                        </div>

                      )
                    )

                  ) : (

                    <div className="insight-item">

                      <span>✓</span>

                      <p>
                        No specific strengths
                        were detected.
                      </p>

                    </div>

                  )}

                </div>

              </div>

              <div className="insight-card improvements">

                <div className="insight-card-header">

                  <div className="insight-icon">
                    ↑
                  </div>

                  <h3>
                    Improvements
                  </h3>

                </div>

                <div className="insight-list">

                  {(atsReport.improvements || [])
                    .length > 0 ? (

                    atsReport.improvements.map(
                      (
                        improvement,
                        index
                      ) => (

                        <div
                          className="insight-item"
                          key={index}
                        >

                          <span>→</span>

                          <p>
                            {improvement}
                          </p>

                        </div>

                      )
                    )

                  ) : (

                    <div className="insight-item">

                      <span>✓</span>

                      <p>
                        No major improvements
                        were identified.
                      </p>

                    </div>

                  )}

                </div>

              </div>

            </div>

          </section>

          {/* FINAL CTA */}

          <section className="results-final-cta">

            <div>

              <div className="section-label">
                NEXT STEP
              </div>

              <h2>
                Ready to make your resume
                <span> even stronger?</span>
              </h2>

              <p>
                Use these insights to improve
                your resume and increase your
                chances of getting shortlisted.
              </p>

            </div>

            <button
              className="primary-button"
              onClick={resetAnalysis}
            >
              Analyze Another Resume
              <span>→</span>
            </button>

          </section>

        </main>

      )}

    </div>
  );
}

export default App;