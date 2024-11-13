import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Tasks = () => {
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState(null);
  const [users, setUsers] = useState([]);
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    deadline: '',
    assigned_to: null,
  });
  const token = localStorage.getItem('token');

  const getTasks = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/tasks/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTasks(response.data);
    } catch (error) {
      setError('Failed to fetch tasks');
    }
  };

  const getUsers = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/users/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUsers(response.data);
    } catch (error) {
      setError('Failed to fetch users');
    }
  };

  const updateTask = async (taskId, data) => {
    try {
      await axios.put(`http://127.0.0.1:8000/api/tasks/${taskId}/`, data, {
        headers: { Authorization: `Bearer ${token}` },
      });
      getTasks();
    } catch (error) {
      setError('Failed to update task');
    }
  };

  const deleteTask = async (taskId) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/tasks/${taskId}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      getTasks();
    } catch (error) {
      setError('Failed to delete task');
    }
  };

  const createTask = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/tasks/', newTask, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTasks([response.data, ...tasks]);
      setNewTask({
        title: '',
        description: '',
        deadline: '',
        assigned_to: null,
      });
    } catch (error) {
      setError('Failed to create task');
    }
  };

  useEffect(() => {
    getTasks();
    getUsers();
  }, []);

  const handleChange = (e) => {
    setNewTask({ ...newTask, [e.target.name]: e.target.value });
  };

  const handleUserChange = (e) => {
    setNewTask({ ...newTask, assigned_to: e.target.value });
  };

  return (
    <div>
      <h1>Tasks</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <h2>Create New Task</h2>
      <form onSubmit={(e) => {
        e.preventDefault();
        createTask();
      }}>
        <label>
          Title:
          <input type="text" name="title" value={newTask.title} onChange={handleChange} />
        </label>
        <br />
        <label>
          Description:
          <input type="text" name="description" value={newTask.description} onChange={handleChange} />
        </label>
        <br />
        <label>
          Deadline (hours):
          <input type="number" name="deadline" value={newTask.deadline} onChange={handleChange} />
        </label>
        <br />
        <label>
          Assign to:
          <select name="assigned_to" value={newTask.assigned_to} onChange={handleUserChange}>
            <option value="">Select User</option>
            {users.map((user) => (
              <option key={user.id} value={user.id}>{user.username}</option>
            ))}
          </select>
        </label>
        <br />
        <button type="submit">Create Task</button>
      </form>

      <ul>
        {tasks.map((task) => (
            <li key={task.id}>
              <h2>{task.title}</h2>
              <p>{task.description}</p>
              <p>Deadline: {task.deadline}</p>
              <p>Created By: {task.created_by}</p>
              <h3>Statuses:</h3>
              <ul>
                {task.statuses.map((status) => (
                    <li key={status.date}>
                      {status.status} by {status.responsible} on {status.date}
                    </li>
                ))}
              </ul>
              <select value={task.assigned_to} onChange={(e) => updateTask(task.id, {assigned_to: e.target.value})}>
                <option value="">Select Assign To</option>
                {users.map((user) => (
                    <option key={user.id} value={user.id}>{user.username}</option>
                ))}
              </select>
              <select value={task.assigned_to} onChange={(e) => updateTask(task.id, {completed_by: e.target.value})}>
                <option value="">Select Completed By</option>
                {users.map((user) => (
                    <option key={user.id} value={user.id}>{user.username}</option>
                ))}
              </select>
              <select value={task.assigned_to} onChange={(e) => updateTask(task.id, {checked_by: e.target.value})}>
                <option value="">Select Checked By</option>
                {users.map((user) => (
                    <option key={user.id} value={user.id}>{user.username}</option>
                ))}
              </select>
              <button onClick={() => deleteTask(task.id)}>Delete</button>
            </li>
        ))}
      </ul>
    </div>
  );
};

export default Tasks;