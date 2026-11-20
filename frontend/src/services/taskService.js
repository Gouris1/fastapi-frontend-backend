
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

// Get Task Summary
export const getTaskSummary = async () => {
    const token = localStorage.getItem("token");

    const response = await axios.get(
        `${API_URL}/tasks/summary`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    return response.data;
};

// Create New Task
export const createTask = async (taskData) => {
    const token = localStorage.getItem("token");

    const response = await axios.post(
        `${API_URL}/tasks/`,
        taskData,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    return response.data;
};

// Get All Tasks
export const getAllTasks = async () => {
    const token = localStorage.getItem("token");

    const response = await axios.get(
        `${API_URL}/tasks/?page=1&limit=100`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    return response.data;
};
