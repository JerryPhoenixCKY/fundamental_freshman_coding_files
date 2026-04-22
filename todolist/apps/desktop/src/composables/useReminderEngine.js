import { onMounted, onUnmounted, ref } from "vue";
import { acknowledgeReminder, fetchDueReminders } from "../api";
function parseNumber(value, fallback) {
    const parsed = Number(value);
    return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}
const POLL_MS = parseNumber(import.meta.env.VITE_REMINDER_POLL_MS, 15000);
const SOUND_ENABLED = String(import.meta.env.VITE_REMINDER_SOUND ?? "true").toLowerCase() !== "false";
function playReminderBeep() {
    if (!SOUND_ENABLED) {
        return;
    }
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) {
        return;
    }
    const context = new AudioContextClass();
    const oscillator = context.createOscillator();
    const gain = context.createGain();
    oscillator.type = "sine";
    oscillator.frequency.value = 880;
    gain.gain.setValueAtTime(0.0001, context.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.12, context.currentTime + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.0001, context.currentTime + 0.35);
    oscillator.connect(gain);
    gain.connect(context.destination);
    oscillator.start();
    oscillator.stop(context.currentTime + 0.36);
    window.setTimeout(() => {
        void context.close();
    }, 450);
}
function showBrowserNotification(task) {
    if (!("Notification" in window) || Notification.permission !== "granted") {
        return;
    }
    const body = task.remindAt
        ? `Scheduled at ${new Date(task.remindAt).toLocaleString()}`
        : "Task reminder";
    new Notification(`Reminder: ${task.title}`, {
        body,
        tag: `task-reminder-${task.id}`
    });
}
async function requestNotificationPermission() {
    if (!("Notification" in window) || Notification.permission !== "default") {
        return;
    }
    try {
        await Notification.requestPermission();
    }
    catch {
        // Ignore permission errors and keep in-app reminders only.
    }
}
export function useReminderEngine(tasks) {
    const notices = ref([]);
    let timerId;
    let polling = false;
    function dismissNotice(id) {
        notices.value = notices.value.filter((item) => item.id !== id);
    }
    function upsertTaskInStore(task) {
        const index = tasks.value.findIndex((candidate) => candidate.id === task.id);
        if (index === -1) {
            tasks.value = [task, ...tasks.value];
            return;
        }
        tasks.value[index] = task;
    }
    async function pollDueReminders() {
        if (polling) {
            return;
        }
        polling = true;
        try {
            const dueTasks = await fetchDueReminders(20);
            for (const task of dueTasks) {
                upsertTaskInStore(task);
                notices.value = [
                    {
                        id: `${task.id}-${Date.now()}`,
                        taskId: task.id,
                        title: task.title,
                        remindAt: task.remindAt,
                        createdAt: new Date().toISOString()
                    },
                    ...notices.value
                ].slice(0, 6);
                showBrowserNotification(task);
                playReminderBeep();
                await acknowledgeReminder(task.id);
            }
        }
        catch {
            // Keep reminder polling resilient without breaking the page.
        }
        finally {
            polling = false;
        }
    }
    onMounted(() => {
        void requestNotificationPermission();
        void pollDueReminders();
        timerId = window.setInterval(() => {
            void pollDueReminders();
        }, POLL_MS);
    });
    onUnmounted(() => {
        if (timerId !== undefined) {
            window.clearInterval(timerId);
        }
    });
    return {
        notices,
        dismissNotice,
        pollDueReminders
    };
}
