import React, { useRef, useState } from "react";

function Home({ onNavigate }) {
  const fileInputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) return;

    setError("");

    if (selectedFile.type !== "application/pdf") {
      setError("Please upload a PDF resume.");
      return;
    }

    setFile(selectedFile);
  };

  const handleDrop = (event) => {
    event.preventDefault();

    const droppedFile = event.dataTransfer.files?.[0];

    if (!droppedFile) return;

    setError("");

    if (droppedFile.type !== "application/pdf") {
      setError("Please upload a PDF resume.");
      return;
    }

    setFile(droppedFile);
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please upload your resume first.");
      return;
    }

    const token =
      localStorage.getItem("token") ||
      localStorage.getItem("access_token");

    if (!token) {
      setError("Please login again to analyze your resume.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        "http://127.0.0.1:8000/api/resume/upload",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.detail ||
            data?.message ||
            "Resume analysis failed."
        );
      }

      /*
       * Store analysis result so Results page can use it.
       */
      localStorage.setItem(
        "resumeAnalysis",
        JSON.stringify(data)
      );

      if (onNavigate) {
        onNavigate("results");
      }

    } catch (err) {
      console.error("Resume Analysis Error:", err);

      setError(
        err.message ||
          "Something went wrong while analyzing your resume."
      );

    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="resumeiq-app">

      {/* ================= HERO ================= */}

      <section className="hero" id="home">

        <div className="hero-badge">
          <span>✦</span>
          AI-POWERED RESUME INTELLIGENCE
        </div>

        <h1>
          Build a resume that{" "}
          <span>gets noticed.</span>
        </h1>

        <p className="hero-description">
          ResumeIQ analyzes your resume with AI, evaluates
          ATS compatibility, identifies your strongest skills,
          and helps you understand exactly where you can improve.
        </p>

        <div className="hero-actions">

          <button
            className="primary-button"
            onClick={() =>
              document
                .getElementById("upload")
                ?.scrollIntoView({
                  behavior: "smooth",
                })
            }
          >
            Analyze My Resume
            <span>→</span>
          </button>

          <button
            className="secondary-button"
            onClick={() =>
              onNavigate
                ? onNavigate("dashboard")
                : null
            }
          >
            View Dashboard
          </button>

        </div>

        <div className="trust-row">
          <span>✓ AI-powered analysis</span>
          <span>✓ ATS compatibility</span>
          <span>✓ Skill insights</span>
        </div>

      </section>


      {/* ================= UPLOAD ================= */}

      <section
        className="upload-section"
        id="upload"
      >

        <div className="section-heading">

          <div className="section-label">
            START ANALYSIS
          </div>

          <h2>
            Upload your{" "}
            <span>resume.</span>
          </h2>

          <p>
            Upload your PDF resume and let ResumeIQ analyze
            your skills, education, experience, projects,
            and ATS readiness.
          </p>

        </div>


        <div className="upload-card">

          {!file ? (

            <div
              className="upload-dropzone"
              onClick={() =>
                fileInputRef.current?.click()
              }
              onDragOver={(event) =>
                event.preventDefault()
              }
              onDrop={handleDrop}
            >

              <div className="upload-icon">
                ↑
              </div>

              <h3>
                Drop your resume here
              </h3>

              <p>
                or click to browse your files
              </p>

              <span className="file-hint">
                PDF files only • Maximum recommended size: 10MB
              </span>

            </div>

          ) : (

            <div className="selected-file">

              <div className="file-icon">
                PDF
              </div>

              <div className="file-information">

                <strong>
                  {file.name}
                </strong>

                <span>
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </span>

              </div>

              <button
                className="change-file"
                onClick={() =>
                  fileInputRef.current?.click()
                }
              >
                Change
              </button>

            </div>

          )}


          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,application/pdf"
            onChange={handleFileChange}
            style={{ display: "none" }}
          />


          {error && (
            <div className="error-message">
              ⚠ {error}
            </div>
          )}


          <button
            className="analyze-button"
            disabled={!file || loading}
            onClick={handleAnalyze}
          >

            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing Resume...
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


      {/* ================= FEATURES ================= */}

      <section className="features-section">

        <div className="section-heading">

          <div className="section-label">
            WHAT RESUMEIQ ANALYZES
          </div>

          <h2>
            More than just an{" "}
            <span>ATS score.</span>
          </h2>

          <p>
            Understand your resume from multiple
            perspectives and get actionable insights.
          </p>

        </div>


        <div className="feature-grid">

          <div className="feature-card">

            <div className="feature-number">
              01
            </div>

            <div className="feature-icon">
              ◈
            </div>

            <h3>
              ATS Score
            </h3>

            <p>
              See how well your resume is structured
              for Applicant Tracking Systems.
            </p>

          </div>


          <div className="feature-card">

            <div className="feature-number">
              02
            </div>

            <div className="feature-icon">
              ✦
            </div>

            <h3>
              Skill Detection
            </h3>

            <p>
              Automatically identify technical skills,
              frameworks, tools, and technologies.
            </p>

          </div>


          <div className="feature-card">

            <div className="feature-number">
              03
            </div>

            <div className="feature-icon">
              ◎
            </div>

            <h3>
              AI Insights
            </h3>

            <p>
              Discover your resume strengths and the
              areas that need improvement.
            </p>

          </div>


          <div className="feature-card">

            <div className="feature-number">
              04
            </div>

            <div className="feature-icon">
              ↗
            </div>

            <h3>
              Job Matching
            </h3>

            <p>
              Compare your resume against real job
              descriptions and find skill gaps.
            </p>

          </div>

        </div>

      </section>


      {/* ================= HOW IT WORKS ================= */}

      <section className="steps-section">

        <div className="section-heading">

          <div className="section-label">
            HOW IT WORKS
          </div>

          <h2>
            From resume to{" "}
            <span>insights.</span>
          </h2>

        </div>


        <div className="steps-grid">

          <div className="step-card">

            <span>01</span>

            <h3>
              Upload
            </h3>

            <p>
              Upload your PDF resume securely through
              the ResumeIQ analyzer.
            </p>

          </div>


          <div className="step-card">

            <span>02</span>

            <h3>
              Analyze
            </h3>

            <p>
              Our backend extracts your resume content
              and evaluates important career signals.
            </p>

          </div>


          <div className="step-card">

            <span>03</span>

            <h3>
              Improve
            </h3>

            <p>
              Get your ATS score, detected skills,
              strengths, improvements, and job match insights.
            </p>

          </div>

        </div>

      </section>


      {/* ================= CTA ================= */}

      <section className="cta-section">

        <div className="cta-content">

          <h2>
            Your next opportunity
            <br />
            starts with a{" "}
            <span>better resume.</span>
          </h2>

          <button
            className="primary-button"
            onClick={() =>
              document
                .getElementById("upload")
                ?.scrollIntoView({
                  behavior: "smooth",
                })
            }
          >
            Analyze My Resume
            <span>→</span>
          </button>

        </div>

      </section>


      {/* ================= FOOTER ================= */}

      <footer className="footer">

        <div>
          <strong>
            ResumeIQ
          </strong>

          <span>
            AI-powered resume intelligence
          </span>
        </div>

        <span>
          © {new Date().getFullYear()} ResumeIQ
        </span>

      </footer>

    </main>
  );
}

export default Home;