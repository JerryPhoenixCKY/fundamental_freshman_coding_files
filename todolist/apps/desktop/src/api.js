const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:3000/api";
async function request(path, init) {
    const token = localStorage.getItem("token");
    const headers = {
        "Content-Type": "application/json",
        ...(init?.headers ?? {})
    };
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }
    const response = await fetch(`${API_BASE}${path}`, {
        ...init,
        headers,
    });
    if (!response.ok) {
        const text = await response.text();
        throw new Error(text || `Request failed: ${response.status}`);
    }
    return response.json();
}
export async function fetchTasks() {
    return request("/tasks");
}
export async function createTask(input) {
    return request("/tasks", {
        method: "POST",
        body: JSON.stringify(input)
    });
}
export async function toggleTask(id) {
    return request(`/tasks/${id}/toggle`, {
        method: "PATCH"
    });
}
export async function removeTask(id) {
    return request(`/tasks/${id}`, {
        method: "DELETE"
    });
}
export async function fetchDueReminders(limit = 20) {
    const query = new URLSearchParams({ limit: String(limit) });
    return request(`/tasks/reminders/due?${query.toString()}`);
}
export async function acknowledgeReminder(taskId) {
    return request(`/tasks/${taskId}/reminders/ack`, {
        method: "POST"
    });
}
export async function sendAuthCode(email) {
    return request("/auth/send-code", {
        method: "POST",
        body: JSON.stringify({ email })
    });
}
export async function verifyAuthCode(email, code) {
    return request("/auth/verify-code", {
        method: "POST",
        body: JSON.stringify({ email, code })
    });
}
