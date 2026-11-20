import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAllTasks } from "../services/taskService";
import "./Tasks.css";

function Tasks() {
  const navigate = useNavigate();

  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const data = await getAllTasks();

        setTasks(
          Array.isArray(data) ? data : data.tasks || []
        );

      } catch (err) {
        setError(
          err.response?.data?.detail ||
          "Failed to load tasks"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, []);

  return (
    <div className="tasks-page">
      <div className="tasks-header">
        <div>
          <h1>All Users Tasks</h1>
          <p>View all tasks created by every user.</p>
        </div>
        <button onClick={() => navigate("/dashboard")}>
          Back to Dashboard
        </button>
      </div>
      {loading && <p>Loading tasks...</p>}
      {error && <p className="error-message">{error}</p>}
      {!loading && !error && (
        <>
          <h3>Total Tasks: {tasks.length}</h3>
          {tasks.length === 0 ? (
            <p>No tasks found.</p>
          ) : (
            <div className="tasks-table-container">
              <table className="tasks-table">
                <thead>
                  <tr>
                    <th>Task ID</th>
                    <th>Title</th>
                    <th>User ID</th>
                    <th>Status</th>
                    <th>Priority</th>
                  </tr>
                </thead>
                <tbody>
                  {tasks.map((task) => (
                    <tr key={task.id}>
                      <td>{task.id}</td>
                      <td>{task.title}</td>
                      <td>{task.user_id ?? "N/A"}</td>
                      <td>{task.status}</td>
                      <td>{task.priority}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  );
}
export default Tasks;
