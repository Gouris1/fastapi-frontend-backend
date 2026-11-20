import { useState } from "react";
import { createTask } from "../services/taskService";

function AddTask({ onSuccess, onCancel }) {

  const [formData, setFormData] = useState({
    title: "",
    description: "",
    status: "pending",
    priority: "medium",
    due_date: ""
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const getLocalDateTime = () => {
    const date = new Date();

    date.setMinutes(
      date.getMinutes() - date.getTimezoneOffset()
    );

    return date.toISOString().slice(0, 16);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");

    if (formData.title.trim().length < 3) {
      setError("Title must contain at least 3 characters");
      return;
    }

    try {
      setLoading(true);

      const taskData = {
        title: formData.title.trim(),
        description: formData.description.trim() || null,
        status: formData.status,
        priority: formData.priority,
        due_date: formData.due_date || null
      };

      await createTask(taskData);

      setSuccess("Task created successfully!");

      setFormData({
        title: "",
        description: "",
        status: "pending",
        priority: "medium",
        due_date: ""
      });

      if (onSuccess) {
        onSuccess();
      }

    } catch (err) {
      setError(
        err.response?.data?.detail?.[0]?.msg ||
        err.response?.data?.detail ||
        "Failed to create task"
      );

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-task-form">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Task Title *</label>
          <input
            type="text"
            name="title"
            placeholder="Enter task title"
            value={formData.title}
            onChange={handleChange}
            minLength={3}
            maxLength={100}
            required
          />
        </div>
        <div className="form-group">
          <label>Description</label>
          <textarea
            name="description"
            placeholder="Enter task description"
            value={formData.description}
            onChange={handleChange}
            rows="3"
          />
        </div>
        <div className="form-group">
          <label>Status</label>
          <select
            name="status"
            value={formData.status}
            onChange={handleChange}
          >
            <option value="pending">
              Pending
            </option>
            <option value="in_progress">
              In Progress
            </option>
            <option value="completed">
              Completed
            </option>
          </select>
        </div>
        <div className="form-group">
          <label>Priority</label>
          <select
            name="priority"
            value={formData.priority}
            onChange={handleChange}
          >
            <option value="low">
              Low
            </option>
            <option value="medium">
              Medium
            </option>
            <option value="high">
              High
            </option>
          </select>
        </div>
        <div className="form-group">
          <label>Due Date</label>
          <input
            type="datetime-local"
            name="due_date"
            min={getLocalDateTime()}
            value={formData.due_date}
            onChange={handleChange}
          />
        </div>
        {error && (
          <p className="error-message">
            {error}
          </p>
        )}
        {success && (
          <p className="success-message">
            {success}
          </p>
        )}
        <div className="form-buttons">
          <button
            type="submit"
            disabled={loading}
            className="popup-action-btn"
          >
            {loading ? "Creating..." : "Create Task"}
          </button>
          <button
            type="button"
            className="cancel-btn"
            onClick={onCancel}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
export default AddTask;
