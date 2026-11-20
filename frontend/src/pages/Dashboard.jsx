
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { getTaskSummary } from "../services/taskService";
import AddTask from "./AddTask";
import "./Dashboard.css";

function Dashboard() {
  const navigate = useNavigate();

  const [summary, setSummary] = useState({
    total_tasks: 0,
    pending_tasks: 0,
    in_progress_tasks: 0,
    completed_tasks: 0
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showAddPopup, setShowAddPopup] = useState(false);
  const [showTasksPopup, setShowTasksPopup] = useState(false);
  const [refreshSummary, setRefreshSummary] = useState(0);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const data = await getTaskSummary();
        setSummary(data);
        setError("");

      } catch (error) {
        setError(
          error.response?.data?.detail ||
          "Failed to load task summary"
        );

      } finally {
        setLoading(false);
      }
    };

    fetchSummary();

  }, [refreshSummary]);

  // Logout
  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-main">
        <div className="dashboard-header">
          <div>
            <h1>Welcome to Dashboard!</h1>
            <p>Manage your tasks efficiently.</p>
          </div>
          <button
            className="logout-btn"
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>
        <div className="dashboard-cards">
          <div className="dashboard-card total-card">
            <h3>Total Tasks</h3>
            <h2>
              {loading ? "Loading..." : summary.total_tasks}
            </h2>
          </div>
          <div className="dashboard-card pending-card">
            <h3>Pending Tasks</h3>
            <h2>
              {loading ? "Loading..." : summary.pending_tasks}
            </h2>
          </div>
          <div className="dashboard-card progress-card">
            <h3>In Progress Tasks</h3>
            <h2>
              {loading ? "Loading..." : summary.in_progress_tasks}
            </h2>
          </div>
          <div className="dashboard-card completed-card">
            <h3>Completed Tasks</h3>
            <h2>
              {loading ? "Loading..." : summary.completed_tasks}
            </h2>
          </div>
        </div>
        {error && (
          <p className="error-message">{error}</p>
        )}
        <div className="recent-tasks">
          <h2>Recent Tasks</h2>
          <div className="task-actions">
            <button
              onClick={() => setShowAddPopup(true)}
            >
              + Add New Task
            </button>
            <button
              onClick={() => setShowTasksPopup(true)}
            >
              View All Tasks
            </button>
          </div>
          <p className="empty-message">
            Your task summary is updated from the database.
          </p>
        </div>
      </div>
      {showAddPopup && (
        <div className="popup-overlay">
          <div className="popup-content">
            <button
              className="popup-close"
              onClick={() => setShowAddPopup(false)}
            >
              ×
            </button>
            <h2>Add New Task</h2>
            <AddTask
              onSuccess={() => {
                setShowAddPopup(false);
                setRefreshSummary(prev => prev + 1);

              }}
              onCancel={() => setShowAddPopup(false)}
            />
          </div>
        </div>
      )}
      {showTasksPopup && (
        <div className="popup-overlay">
          <div className="popup-content">
            <button
              className="popup-close"
              onClick={() => setShowTasksPopup(false)}
            >
              ×
            </button>
            <h2>All Tasks</h2>
            <p>Task list will appear here.</p>
            <button
              className="popup-action-btn"
              onClick={() => {
                setShowTasksPopup(false);
                navigate("/tasks");
              }}
            >
              Open All Tasks
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
export default Dashboard;
