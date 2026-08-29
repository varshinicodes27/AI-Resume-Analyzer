import React from "react";

function Dashboard({ onNavigate }) {
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  const userName =
    user?.name ||
    user?.username ||
    user?.email?.split("@")[0] ||
    "User";

  const goTo = (page) => {
    if (onNavigate) {
      onNavigate(page);
    }
  };

  return (
    <main className="dashboard-page">

      {/* ================= HEADER ================= */}
      <section className="dashboard-header">

        <div className="dashboard-header-content">
          <div className="section-label">
            RESUMEIQ DASHBOARD
          </div>

          <h1>
            Welcome back,{" "}
            <span>{userName}</span>
          </h1>

          <p>
            Manage your resume analysis, improve your ATS score,
            and match your resume with the right job opportunities.
          </p>
        </div>

        <div className="dashboard-welcome">
          ✦ AI-powered resume intelligence
        </div>

      </section>


      {/* ================= PROFILE ================= */}
      <section className="dashboard-card">

        <div className="dashboard-profile">

          <div className="dashboard-profile-avatar">
            {userName.charAt(0).toUpperCase()}
          </div>

          <div className="dashboard-profile-info">
            <strong>{userName}</strong>
            <span>
              {user?.email || "ResumeIQ User"}
            </span>
          </div>

        </div>

      </section>


      {/* ================= STATISTICS ================= */}
      <section className="dashboard-stat-grid">

        <div className="dashboard-stat-card">
          <div className="dashboard-stat-label">
            Resume Analyses
          </div>

          <div className="dashboard-stat-value purple">
            0
          </div>

          <div className="dashboard-stat-description">
            Total resumes analyzed
          </div>
        </div>


        <div className="dashboard-stat-card">
          <div className="dashboard-stat-label">
            Average ATS
          </div>

          <div className="dashboard-stat-value green">
            —
          </div>

          <div className="dashboard-stat-description">
            Your average resume score
          </div>
        </div>


        <div className="dashboard-stat-card">
          <div className="dashboard-stat-label">
            Job Matches
          </div>

          <div className="dashboard-stat-value yellow">
            0
          </div>

          <div className="dashboard-stat-description">
            Jobs analyzed
          </div>
        </div>


        <div className="dashboard-stat-card">
          <div className="dashboard-stat-label">
            Skills Found
          </div>

          <div className="dashboard-stat-value pink">
            —
          </div>

          <div className="dashboard-stat-description">
            Skills detected from resume
          </div>
        </div>

      </section>


      {/* ================= MAIN DASHBOARD ================= */}
      <section className="dashboard-main-grid">

        {/* QUICK ANALYSIS */}
        <div className="dashboard-card dashboard-large-card quick-analysis-card">

          <div className="quick-analysis-content">

            <div className="quick-analysis-icon">
              ✦
            </div>

            <h3>
              Analyze Your Resume
            </h3>

            <p>
              Upload your resume and let ResumeIQ analyze
              your skills, education, projects, experience,
              and ATS compatibility.
            </p>

          </div>

          <button
            className="quick-analysis-button"
            onClick={() => goTo("home")}
          >
            Upload & Analyze Resume →
          </button>

        </div>


        {/* JOB MATCH */}
        <div className="dashboard-card dashboard-large-card quick-analysis-card">

          <div className="quick-analysis-content">

            <div className="quick-analysis-icon">
              ◎
            </div>

            <h3>
              Job Matcher
            </h3>

            <p>
              Compare your resume against a job description
              and discover matched and missing skills.
            </p>

          </div>

          <button
            className="quick-analysis-button"
            onClick={() => goTo("jobmatch")}
          >
            Match With a Job →
          </button>

        </div>

      </section>


      {/* ================= RECENT ANALYSES ================= */}
      <section className="dashboard-card" style={{ marginTop: "16px" }}>

        <div className="dashboard-card-header">

          <div>
            <h2>
              Recent Analyses
            </h2>

            <p>
              Your latest resume activity
            </p>
          </div>

        </div>


        <div className="dashboard-empty">

          <div className="dashboard-empty-icon">
            ◫
          </div>

          <h3>
            No analyses yet
          </h3>

          <p>
            Upload your first resume to see your analysis
            history here.
          </p>

        </div>

      </section>


      {/* ================= BOTTOM CTA ================= */}
      <section
        className="results-final-cta"
        style={{ marginTop: "30px" }}
      >

        <div>
          <h2>
            Ready to make your resume{" "}
            <span>job-ready?</span>
          </h2>

          <p>
            Get an AI-powered analysis and discover exactly
            how you can improve your resume.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={() => goTo("home")}
        >
          Analyze Resume
          <span>→</span>
        </button>

      </section>

    </main>
  );
}

export default Dashboard;