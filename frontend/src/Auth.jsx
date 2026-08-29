import { useState } from "react";
import "./App.css";
import { API_ENDPOINTS } from "./services/api.js";

function Auth({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setMessage("");
    setLoading(true);

    try {
      const endpoint = isLogin
        ? API_ENDPOINTS.LOGIN
        : API_ENDPOINTS.REGISTER;

      const body = isLogin
        ? {
            email,
            password,
          }
        : {
            full_name: fullName,
            email,
            password,
          };

      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.detail ||
            data?.message ||
            "Authentication failed."
        );
      }

      if (!isLogin) {
        setMessage(
          "Account created successfully. You can now login."
        );

        setIsLogin(true);
        setPassword("");
        return;
      }

      localStorage.setItem(
        "access_token",
        data.access_token
      );

      localStorage.setItem(
        "user_id",
        data.user_id
      );

      localStorage.setItem(
        "full_name",
        data.full_name
      );

      onLogin();

    } catch (err) {
      console.error("Authentication error:", err);

      setError(
        err.message ||
          "Something went wrong. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const switchMode = () => {
    setIsLogin(!isLogin);
    setError("");
    setMessage("");
    setPassword("");
  };

  return (
    <div className="auth-page">

      {/* Background decoration */}

      <div className="auth-glow auth-glow-one"></div>
      <div className="auth-glow auth-glow-two"></div>

      <div className="auth-wrapper">

        {/* =================================================
            LEFT BRAND PANEL
        ================================================= */}

        <div className="auth-intro">

          <div className="auth-logo">

            <div className="auth-logo-icon">
              ✦
            </div>

            <div>
              <div className="auth-logo-name">
                ResumeIQ
              </div>

              <div className="auth-logo-tagline">
                AI-Powered Resume Analyzer
              </div>
            </div>

          </div>

          <div className="auth-intro-content">

            <div className="auth-badge">
              <span>✦</span>
              AI-powered career intelligence
            </div>

            <h1>
              Build a resume
              <br />
              <span>that gets noticed.</span>
            </h1>

            <p>
              Analyze your resume, understand your
              ATS performance, discover skill gaps,
              and match your profile with real job
              opportunities.
            </p>

            <div className="auth-benefits">

              <div>
                <span>✓</span>
                AI-powered resume analysis
              </div>

              <div>
                <span>✓</span>
                ATS score & section insights
              </div>

              <div>
                <span>✓</span>
                Intelligent job matching
              </div>

            </div>

          </div>

          <div className="auth-footer-note">
            Your career. Your potential. Your ResumeIQ.
          </div>

        </div>

        {/* =================================================
            AUTH CARD
        ================================================= */}

        <div className="auth-panel">

          <div className="auth-card">

            <div className="auth-card-top">

              <div className="auth-mobile-logo">
                <div className="auth-logo-icon">
                  ✦
                </div>
                <span>ResumeIQ</span>
              </div>

              <div className="auth-heading">

                <div className="section-label">
                  {isLogin
                    ? "WELCOME BACK"
                    : "GET STARTED"}
                </div>

                <h2>
                  {isLogin
                    ? "Welcome back."
                    : "Create your account."}
                </h2>

                <p>
                  {isLogin
                    ? "Login to continue your resume journey."
                    : "Join ResumeIQ and build a stronger career profile."}
                </p>

              </div>

            </div>

            {/* FORM */}

            <form
              className="auth-form"
              onSubmit={handleSubmit}
            >

              {!isLogin && (
                <div className="auth-field">

                  <label>FULL NAME</label>

                  <div className="auth-input-wrapper">

                    <span className="auth-input-icon">
                      ◯
                    </span>

                    <input
                      type="text"
                      placeholder="Enter your full name"
                      value={fullName}
                      onChange={(event) =>
                        setFullName(
                          event.target.value
                        )
                      }
                      required
                    />

                  </div>

                </div>
              )}

              <div className="auth-field">

                <label>EMAIL ADDRESS</label>

                <div className="auth-input-wrapper">

                  <span className="auth-input-icon">
                    @
                  </span>

                  <input
                    type="email"
                    placeholder="you@example.com"
                    value={email}
                    onChange={(event) =>
                      setEmail(
                        event.target.value
                      )
                    }
                    required
                  />

                </div>

              </div>

              <div className="auth-field">

                <label>PASSWORD</label>

                <div className="auth-input-wrapper">

                  <span className="auth-input-icon">
                    •••
                  </span>

                  <input
                    type={
                      showPassword
                        ? "text"
                        : "password"
                    }
                    placeholder="Enter your password"
                    value={password}
                    onChange={(event) =>
                      setPassword(
                        event.target.value
                      )
                    }
                    required
                  />

                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() =>
                      setShowPassword(
                        !showPassword
                      )
                    }
                  >
                    {showPassword
                      ? "Hide"
                      : "Show"}
                  </button>

                </div>

              </div>

              {error && (
                <div className="auth-message auth-error">
                  <span>!</span>
                  {error}
                </div>
              )}

              {message && (
                <div className="auth-message auth-success">
                  <span>✓</span>
                  {message}
                </div>
              )}

              <button
                type="submit"
                className="auth-submit"
                disabled={loading}
              >

                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Please wait...
                  </>
                ) : (
                  <>
                    {isLogin
                      ? "Login to ResumeIQ"
                      : "Create ResumeIQ Account"}

                    <span>→</span>
                  </>
                )}

              </button>

            </form>

            {/* SWITCH */}

            <div className="auth-switch">

              <span>
                {isLogin
                  ? "Don't have an account?"
                  : "Already have an account?"}
              </span>

              <button
                type="button"
                onClick={switchMode}
              >
                {isLogin
                  ? "Create account"
                  : "Login instead"}
              </button>

            </div>

            <div className="auth-security">
              <span>✓</span>
              Secure authentication powered by ResumeIQ
            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

export default Auth;