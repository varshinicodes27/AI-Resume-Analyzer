import React, { useState } from "react";

function JobMatch({ onNavigate }) {
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const getToken = () => {
    return (
      localStorage.getItem("token") ||
      localStorage.getItem("access_token")
    );
  };

  const handleJobMatch = async () => {
    setError("");
    setResult(null);

    if (!jobDescription.trim()) {
      setError("Please enter a job description.");
      return;
    }

    const token = getToken();

    if (!token) {
      setError("Please login again to use Job Matcher.");
      return;
    }

    try {
      setLoading(true);

      const response = await fetch(
        "http://127.0.0.1:8000/api/resume/job_match",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },

          body: JSON.stringify({
            job_description: jobDescription,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.detail ||
            data?.message ||
            "Unable to analyze the job description."
        );
      }

      setResult(data);

    } catch (err) {
      console.error("Job Match Error:", err);

      setError(
        err.message ||
          "Something went wrong while matching your resume."
      );

    } finally {
      setLoading(false);
    }
  };


  const score =
    result?.match_percentage ??
    result?.match_score ??
    result?.score ??
    0;

  const matchedSkills =
    result?.matched_skills ||
    result?.matchedSkills ||
    [];

  const missingSkills =
    result?.missing_skills ||
    result?.missingSkills ||
    [];


  return (
    <main className="results-page">

      {/* ================= HEADER ================= */}

      <section className="job-matcher-section">

        <div className="job-matcher-header">

          <div className="section-label">
            AI JOB MATCHER
          </div>

          <h2>
            Find your{" "}
            <span>job match</span>
          </h2>

          <p>
            Paste a job description below and ResumeIQ will
            compare it with your uploaded resume to identify
            matching skills and areas you need to improve.
          </p>

        </div>


        {/* ================= INPUT CARD ================= */}

        <div className="job-matcher-card">

          <textarea
            className="job-description-input"
            placeholder="Paste the complete job description here...

Example:
We are looking for a Java Backend Developer with experience in Spring Boot, REST APIs, MySQL, Git and Docker..."
            value={jobDescription}
            onChange={(e) =>
              setJobDescription(e.target.value)
            }
          />


          {error && (
            <div className="job-match-error">
              ⚠ {error}
            </div>
          )}


          <button
            className="job-match-button"
            onClick={handleJobMatch}
            disabled={loading}
          >

            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing Job Match...
              </>
            ) : (
              <>
                ✦ Analyze Job Match
              </>
            )}

          </button>

        </div>


        {/* ================= RESULT ================= */}

        {result && (
          <div className="job-match-result">

            <div className="score-card-label">
              JOB MATCH SCORE
            </div>

            <div className="match-score">
              {score}%
            </div>


            {/* SCORE BAR */}

            <div className="score-progress">
              <div
                className="score-progress-fill"
                style={{
                  width: `${Math.min(
                    Math.max(score, 0),
                    100
                  )}%`,
                }}
              ></div>
            </div>


            {/* ================= MATCHED ================= */}

            <div style={{ marginTop: "35px" }}>

              <div className="score-card-label">
                MATCHED SKILLS
              </div>

              {matchedSkills.length > 0 ? (

                <div className="match-skills">

                  {matchedSkills.map(
                    (skill, index) => (
                      <span
                        className="match-skill"
                        key={`${skill}-${index}`}
                      >
                        ✓ {skill}
                      </span>
                    )
                  )}

                </div>

              ) : (
                <p
                  style={{
                    color: "var(--muted)",
                    fontSize: "13px",
                  }}
                >
                  No matching skills detected.
                </p>
              )}

            </div>


            {/* ================= MISSING ================= */}

            <div style={{ marginTop: "30px" }}>

              <div className="score-card-label">
                SKILLS TO IMPROVE
              </div>

              {missingSkills.length > 0 ? (

                <div className="match-skills">

                  {missingSkills.map(
                    (skill, index) => (
                      <span
                        className="match-skill"
                        key={`${skill}-${index}`}
                        style={{
                          background:
                            "rgba(251, 191, 36, 0.08)",
                          borderColor:
                            "rgba(251, 191, 36, 0.2)",
                          color: "#fcd34d",
                        }}
                      >
                        + {skill}
                      </span>
                    )
                  )}

                </div>

              ) : (
                <p
                  style={{
                    color: "var(--muted)",
                    fontSize: "13px",
                  }}
                >
                  Great! No major missing skills detected.
                </p>
              )}

            </div>

          </div>
        )}

      </section>


      {/* ================= BACK BUTTON ================= */}

      <div style={{ marginTop: "35px" }}>

        <button
          className="secondary-button"
          onClick={() =>
            onNavigate
              ? onNavigate("dashboard")
              : window.history.back()
          }
        >
          ← Back to Dashboard
        </button>

      </div>

    </main>
  );
}

export default JobMatch;