import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [filter, setFilter] = useState("all");
  const [editingTask, setEditingTask] = useState(null);
  const [editTitle, setEditTitle] = useState("");
  const [editDescription, setEditDescription] = useState("");
  const [editStatus, setEditStatus] = useState("pending");
  const [loading, setLoading] = useState(false);

  const loadTasks = async () => {
    setLoading(true);

/* React communicate with FastAPI */ 
    try {
      const response = await fetch(`${API_URL}/tasks`, {
        method: "GET",
        cache: "no-store",
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      setTasks(data);

    } catch (error) {
      console.error("LOAD TASK ERROR:", error);

      alert(
        "Unable to load tasks. Make sure FastAPI is running on port 8000."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    await loadTasks();
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const addTask = async () => {
    if (!title.trim()) {
      alert("Please enter a task title.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/tasks`, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        /* actual what data we are sending to API */
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim() || null,
          status: "pending",
          due_date: null,
        }),
      });

      const data = await response.json().catch(() => null);

      if (!response.ok) {
        alert( data?.detail ? JSON.stringify(data.detail) : "Failed to add task." );
        return;
      }

      /* clear the screen after task is added */
      setTitle("");
      setDescription("");
      await loadTasks();
      setFilter("all");
    } catch (error) {
      console.error("ADD ERROR:", error);
      alert("Could not connect to FastAPI.");
    }
  };

/* delete the task */
const deleteTask = async (id) => {
  if (!window.confirm("Are you sure you want to delete this task?")) return;

  try {
    const response = await fetch(`${API_URL}/tasks/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      alert("Failed to delete task.");
      return;
    }

    await loadTasks();
  } catch {
    alert("Could not connect to FastAPI.");
  }
};

const completeTask = async (id) => {
  try {
    const response = await fetch(`${API_URL}/tasks/${id}/complete`, {
      method: "POST",
    });

    if (!response.ok) {
      alert("Failed to complete task.");
      return;
    }

    await loadTasks();
  } catch {
    alert("Could not connect to FastAPI.");
  }
};

const openEdit = (task) => {
  setEditingTask(task);
  setEditTitle(task.title);
  setEditDescription(task.description || "");
  setEditStatus(task.status || "pending");
};

/* save the changes */
  const saveEdit = async () => {
    if (!editingTask) {
      return;
    }

    if (!editTitle.trim()) {
      alert("Task title cannot be empty.");
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/tasks/${editingTask.id}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            title: editTitle.trim(),
            description: editDescription.trim() || null,
            status: editStatus,
          }),
        }
      );

      const data = await response.json().catch(() => null);
      if (!response.ok) {
        console.error("EDIT ERROR:", data);
        alert( data?.detail ? JSON.stringify(data.detail) : "Failed to update task." );
        return;
      }

      setEditingTask(null);
      setEditTitle("");
      setEditDescription("");
      setEditStatus("pending");

      await loadTasks();
    } catch (error) {
      console.error("EDIT ERROR:", error);
      alert("Could not connect to FastAPI.");
    }
  };

  const filteredTasks = filter === "all" ? tasks : tasks.filter((task) => task.status === filter);

  /* display count of tasks */  
  const total = tasks.length;
  const pending = tasks.filter((task) => task.status === "pending").length;
  const inProgress = tasks.filter((task) => task.status === "in_progress").length;
  const completed = tasks.filter((task) => task.status === "completed").length;


  const formatStatus = (status) => {
    if (status === "in_progress") {
      return "In Progress";
    }
    if (status === "pending") {
      return "Pending";
    }
    if (status === "completed") {
      return "Completed";
    }
    return status;
  };

  const getFilterTitle = () => {
    if (filter === "pending") {
      return " Pending Tasks";
    }
    if (filter === "in_progress") {
      return " In Progress Tasks";
    }
    if (filter === "completed") {
      return " Completed Tasks";
    }
    return " All Tasks";
  };

  /* to display selected status tasks only */ 
  const selectFilter = (value) => {
    setFilter(value);

    setTimeout(() => {
      const taskSection = document.getElementById("task-list-section");

      if (taskSection) {
        taskSection.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    }, 50);
  };

  return (
    <div className="container">
      <header className="header">
        <div>
          <h1>Student Task Manager</h1>
          <p> Organize, track and complete your tasks </p>
        </div>

        <button
          type="button"
          className="refresh-button"
          onClick={handleRefresh}
          disabled={loading}
        >
          {loading ? "↻ Refreshing..." : "↻ Refresh"}
        </button>
      </header>


      <div className="stats">
        <div
          className={`stat-card total-card ${ filter === "all" ? "selected" : "" }`}
          onClick={() => selectFilter("all")}
        >
          <span>📋 Total Tasks</span>
          <strong>{total}</strong>
          <small>Click to view all</small>
        </div>

        <div
          className={`stat-card pending-card ${ filter === "pending" ? "selected" : "" }`}
          onClick={() => selectFilter("pending")}
        >
          <span> Pending</span>
          <strong>{pending}</strong>
          <small>Click to view pending</small>
        </div>


        <div
          className={`stat-card progress-card ${ filter === "in_progress" ? "selected" : "" }`}
          onClick={() => selectFilter("in_progress")}
        >
          <span> In Progress</span>
          <strong>{inProgress}</strong>
          <small>Click to view active</small>
        </div>

      
         <div
          className={`stat-card completed-card ${filter === "completed" ? "selected" : " " }`}
          onClick={() => selectFilter("completed")}
        >
          <span>  Completed </span>
          <strong> {completed} </strong>
          <small> Click to view completed </small>
        </div>
      </div>

      <section className="add-task">
        <h2>Add New Task</h2>
        <div className="form-group">
          <label>Task Title</label>
          <input
            type="text"
            value={title}
            maxLength={120}
            placeholder="Enter task title"
            onChange={(e) =>
              setTitle(e.target.value)
            }
          />

        </div>


        <div className="form-group">
          <label>Description</label>
          <textarea
            value={description}
            maxLength={500}
            placeholder="Enter task description"
            onChange={(e) =>
              setDescription(e.target.value)
            }
          />
        </div>


        <button
          type="button"
          className="primary-button"
          onClick={addTask}
        >
          + Add Task
        </button>
      </section>


      <section
        className="tasks-section"
        id="task-list-section"
      >
        <div className="section-header">
          <div>
            <h2>
              {getFilterTitle()}
            </h2>
            <p>Showing {filteredTasks.length}{" "}
              {filteredTasks.length === 1 ? "task" : "tasks"}  </p>
          </div>


          {filter !== "all" && (
            <button
              type="button"
              className="refresh-button"
              onClick={() => selectFilter("all")}
            >
              View All
            </button>
          )}

        </div>


        <div id="tasks">
          {loading ? (
            <div className="loading">
              Loading tasks...
            </div>

          ) : filteredTasks.length === 0 ? (
            <div className="empty">
              <div className="empty-icon">
                📭
              </div>

              <h3>  No tasks found </h3>
              <p> There are no tasks in this category. </p>
                
            </div>

          ) : (

            filteredTasks.map((task) => (

              <div
                className="task-card"
                key={task.id}
              >
                <div className="task-info">
                  <div className="task-title-row">
                    <span className="task-id">  {task.id} </span>
                    <h3> {task.title} </h3>
            
                  </div>
                  <p> {task.description || "No description"} </p>
                  <p>
                    <strong> Status: </strong>{" "}
                    <span className={`status ${task.status}`} > {formatStatus(task.status)} </span>
                  </p>
                </div>

                <div className="task-buttons">
                  <button type="button" onClick={() => openEdit(task)} > ✏️ Edit </button>

                  {task.status !== "completed" && (
                    <button
                      type="button"
                      onClick={() =>
                        completeTask(task.id)
                      }
                    >
                      ✓ Complete
                    </button>
                  )}


                  <button type="button" onClick={() => deleteTask(task.id)} > 🗑️ Delete </button>
                </div>
              </div>
            ))
          )}

        </div>
      </section>


      {editingTask && (
        <div className="modal" onClick={(e) => {
            if (e.target === e.currentTarget ) {
              setEditingTask(null);
            }
          }}
        >

          <div className="modal-content">
            <div className="modal-header">
              <h2> ✏️ Edit Task </h2>
              <button
                type="button"
                className="close-button"
                onClick={() =>
                  setEditingTask(null)
                }
              >
                ×
              </button>
            </div>

 {/* taking input title from user to add new task  */}
            <div className="form-group">
              <label> Task Title </label>
              <input
                type="text"
                value={editTitle}
                maxLength={120}
                onChange={(e) =>
                  setEditTitle( e.target.value )
                }
              />
            </div>

 {/* taking input from user to add new task */}
            <div className="form-group">
              <label>  Description </label>
              <textarea
                value={editDescription}
                maxLength={500}
                onChange={(e) =>
                  setEditDescription( e.target.value )
                }
              />

            </div>


            <div className="form-group">
              <label>  Status </label>
              <select
                value={editStatus}
                onChange={(e) =>
                  setEditStatus(e.target.value)
                }
              >
                <option value="pending"> Pending </option>
                <option value="in_progress"> In Progress </option>
                <option value="completed"> Completed </option>
              </select>
            </div>

 {/* button to edit or delete the task */}
            <div className="modal-buttons">
              <button
                type="button"
                className="primary-button"
                onClick={saveEdit}
              >
                ✓ Save Changes
              </button>


              <button
                type="button"
                className="cancel-button"
                onClick={() =>
                  setEditingTask(null)
                }
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;