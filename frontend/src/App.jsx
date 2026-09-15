import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:5000";

const apiFetch = async (url, options = {}) => {
  const token = localStorage.getItem("token");

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  return fetch(`${API_URL}${url}`, {
    ...options,
    headers,
  });
};

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);

  const [dashboard, setDashboard] = useState({
    total_machines: 0,
    high_risk_machines: 0,
    total_tickets: 0,
  });

  const [machines, setMachines] = useState([]);
  const [tickets, setTickets] = useState([]);

  const [selectedMachine, setSelectedMachine] = useState("");
  const [temperature, setTemperature] = useState("");
  const [vibration, setVibration] = useState("");
  const [pressure, setPressure] = useState("");
  const [prediction, setPrediction] = useState(null);

  // Login
  const handleLogin = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("token", data.token);

        setMessage("");
        setLoggedIn(true);
      } else {
        setMessage(data.message || "Login failed");
      }
    } catch (error) {
      setMessage("Unable to connect to server");
    }
  };

  // Machine health prediction
  const handlePrediction = async (event) => {
    event.preventDefault();

    try {
      const response = await apiFetch("/predict", {
        method: "POST",
        body: JSON.stringify({
          machine_id: Number(selectedMachine),
          temperature: Number(temperature),
          vibration: Number(vibration),
          pressure: Number(pressure),
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setPrediction(data);
        setMessage("");

        // Refresh dashboard
        const dashboardResponse = await apiFetch("/dashboard");
        const dashboardData = await dashboardResponse.json();

        if (dashboardResponse.ok) {
          setDashboard(dashboardData);
        }

        // Refresh tickets
        const ticketsResponse = await apiFetch("/tickets");
        const ticketsData = await ticketsResponse.json();

        if (ticketsResponse.ok) {
          setTickets(ticketsData);
        }
      } else {
        setMessage(data.message || "Prediction failed");
      }
    } catch (error) {
      setMessage("Unable to connect to prediction server");
    }
  };

  // Load dashboard data after login
  useEffect(() => {
    if (loggedIn) {
      // Load dashboard
      apiFetch("/dashboard")
        .then((response) => response.json())
        .then((data) => {
          if (data.message) {
            setMessage(data.message);
            return;
          }

          setDashboard(data);
        })
        .catch(() => {
          setMessage("Unable to load dashboard");
        });

      // Load machines
      apiFetch("/machines")
        .then((response) => response.json())
        .then((data) => {
          if (data.message) {
            setMessage(data.message);
            return;
          }

          setMachines(data);
        })
        .catch(() => {
          setMessage("Unable to load machines");
        });

      // Load tickets
      apiFetch("/tickets")
        .then((response) => response.json())
        .then((data) => {
          if (data.message) {
            setMessage(data.message);
            return;
          }

          setTickets(data);
        })
        .catch(() => {
          setMessage("Unable to load tickets");
        });
    }
  }, [loggedIn]);

  // Dashboard screen
  if (loggedIn) {
    return (
      <div className="dashboard-page">
        <header className="dashboard-header">
          <div>
            <h1>Maintena</h1>
            <p>Predictive Maintenance Platform</p>
          </div>

          <button
            className="logout-button"
            onClick={() => {
              localStorage.removeItem("token");
              setLoggedIn(false);
              setPrediction(null);
              setMachines([]);
              setTickets([]);
            }}
          >
            Logout
          </button>
        </header>

        <main className="dashboard-container">
          <section className="welcome-section">
            <h2>Predictive Maintenance Dashboard</h2>

            <p>Monitor machine health and identify potential failures early.</p>
          </section>

          {/* Dashboard overview */}
          <section className="overview-grid">
            <div className="overview-card">
              <p>Total Machines</p>

              <h3>{dashboard.total_machines}</h3>

              <span>Machines monitored</span>
            </div>

            <div className="overview-card risk-card">
              <p>High Risk Machines</p>

              <h3>{dashboard.high_risk_machines}</h3>

              <span>Require attention</span>
            </div>

            <div className="overview-card ticket-card">
              <p>Maintenance Tickets</p>

              <h3>{dashboard.total_tickets}</h3>

              <span>Open maintenance requests</span>
            </div>
          </section>

          {/* Prediction section */}
          <section className="prediction-section">
            <div className="section-heading">
              <h2>Machine Health Prediction</h2>

              <p>
                Enter current sensor values to predict machine failure risk.
              </p>
            </div>

            <form className="prediction-form" onSubmit={handlePrediction}>
              <div className="form-group">
                <label>Select Machine</label>

                <select
                  value={selectedMachine}
                  onChange={(event) => setSelectedMachine(event.target.value)}
                  required
                >
                  <option value="">Select a machine</option>

                  {machines.map((machine) => (
                    <option key={machine.id} value={machine.id}>
                      {machine.name} - ID {machine.id}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Temperature</label>

                <input
                  type="number"
                  step="0.1"
                  value={temperature}
                  onChange={(event) => setTemperature(event.target.value)}
                  placeholder="e.g. 85.5"
                  required
                />
              </div>

              <div className="form-group">
                <label>Vibration</label>

                <input
                  type="number"
                  step="0.1"
                  value={vibration}
                  onChange={(event) => setVibration(event.target.value)}
                  placeholder="e.g. 7.2"
                  required
                />
              </div>

              <div className="form-group">
                <label>Pressure</label>

                <input
                  type="number"
                  step="0.1"
                  value={pressure}
                  onChange={(event) => setPressure(event.target.value)}
                  placeholder="e.g. 95"
                  required
                />
              </div>

              <button className="predict-button" type="submit">
                Predict Failure Risk
              </button>
            </form>
          </section>

          {/* Prediction result */}
          {prediction && (
            <section className="prediction-result">
              <div className="section-heading">
                <h2>Prediction Result</h2>

                <p>Latest machine health prediction</p>
              </div>

              <div className="result-grid">
                <div className="result-item">
                  <span>Failure Probability</span>

                  <strong>{prediction.failure_probability}%</strong>
                </div>

                <div className="result-item">
                  <span>Risk Level</span>

                  <strong
                    className={
                      prediction.risk_level === "High"
                        ? "high-risk"
                        : prediction.risk_level === "Medium"
                          ? "medium-risk"
                          : "low-risk"
                    }
                  >
                    {prediction.risk_level}
                  </strong>
                </div>

                <div className="result-item">
                  <span>Ticket ID</span>

                  <strong>{prediction.ticket_id || "Not created"}</strong>
                </div>

                <div className="result-item">
                  <span>Technician</span>

                  <strong>{prediction.technician || "Not assigned"}</strong>
                </div>
              </div>
            </section>
          )}

          {/* Tickets */}
          <section className="content-section">
            <div className="section-heading">
              <h2>Maintenance Tickets</h2>

              <p>Recent maintenance requests generated by the system.</p>
            </div>

            <div className="ticket-grid">
              {tickets.length === 0 ? (
                <p className="empty-message">No maintenance tickets found.</p>
              ) : (
                tickets.map((ticket) => (
                  <div className="ticket-card" key={ticket.id}>
                    <div className="ticket-header">
                      <h3>{ticket.title}</h3>

                      <span className="priority-badge">{ticket.priority}</span>
                    </div>

                    <p>
                      <strong>Machine:</strong> {ticket.machine_name}
                    </p>

                    <p>
                      <strong>Status:</strong> {ticket.status}
                    </p>

                    <p>
                      <strong>Technician:</strong>{" "}
                      {ticket.technician || "Not assigned"}
                    </p>

                    <p>
                      <strong>Description:</strong> {ticket.description}
                    </p>
                  </div>
                ))
              )}
            </div>
          </section>

          {/* Machines */}
          <section className="content-section">
            <div className="section-heading">
              <h2>Machines</h2>

              <p>Current machines registered in the system.</p>
            </div>

            <div className="machine-grid">
              {machines.map((machine) => (
                <div className="machine-card" key={machine.id}>
                  <div className="machine-header">
                    <h3>{machine.name}</h3>

                    <span className="status-badge">{machine.status}</span>
                  </div>

                  <p>
                    <strong>Machine ID:</strong> {machine.id}
                  </p>

                  <p>
                    <strong>Location:</strong> {machine.location}
                  </p>
                </div>
              ))}
            </div>
          </section>
        </main>
      </div>
    );
  }

  // Login screen
  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-logo">M</div>

        <h1>Maintena</h1>

        <p className="login-subtitle">Predictive Maintenance Platform</p>

        <h2>Welcome Back</h2>

        <p className="login-description">
          Login to monitor machine health and maintenance activity.
        </p>

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label>Email</label>

            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label>Password</label>

            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
          </div>

          <button className="login-button" type="submit">
            Login
          </button>
        </form>

        {message && <p className="error-message">{message}</p>}
      </div>
    </div>
  );
}

export default App;
