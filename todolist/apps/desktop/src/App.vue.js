import { onMounted, ref } from "vue";
import ClockPanel from "./components/ClockPanel.vue";
import QuickAdd from "./components/QuickAdd.vue";
import TodoList from "./components/TodoList.vue";
import { useReminderEngine } from "./composables/useReminderEngine";
import { createTask, fetchTasks, removeTask, toggleTask } from "./api";
const tasks = ref([]);
const loading = ref(false);
const error = ref("");
const { notices, dismissNotice } = useReminderEngine(tasks);
async function loadTasks() {
    loading.value = true;
    error.value = "";
    try {
        tasks.value = await fetchTasks();
    }
    catch (err) {
        error.value = err instanceof Error ? err.message : "Failed to load tasks";
    }
    finally {
        loading.value = false;
    }
}
async function handleCreate(input) {
    error.value = "";
    try {
        const task = await createTask(input);
        tasks.value = [task, ...tasks.value];
    }
    catch (err) {
        error.value = err instanceof Error ? err.message : "Failed to create task";
    }
}
async function handleToggle(id) {
    error.value = "";
    try {
        const updated = await toggleTask(id);
        tasks.value = tasks.value.map((task) => (task.id === id ? updated : task));
    }
    catch (err) {
        error.value = err instanceof Error ? err.message : "Failed to update task";
    }
}
async function handleRemove(id) {
    error.value = "";
    try {
        await removeTask(id);
        tasks.value = tasks.value.filter((task) => task.id !== id);
    }
    catch (err) {
        error.value = err instanceof Error ? err.message : "Failed to delete task";
    }
}
onMounted(() => {
    void loadTasks();
});
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.main, __VLS_intrinsicElements.main)({
    ...{ class: "app-shell" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "left-column" },
});
/** @type {[typeof ClockPanel, ]} */ ;
// @ts-ignore
const __VLS_0 = __VLS_asFunctionalComponent(ClockPanel, new ClockPanel({}));
const __VLS_1 = __VLS_0({}, ...__VLS_functionalComponentArgsRest(__VLS_0));
/** @type {[typeof QuickAdd, ]} */ ;
// @ts-ignore
const __VLS_3 = __VLS_asFunctionalComponent(QuickAdd, new QuickAdd({
    ...{ 'onSubmit': {} },
}));
const __VLS_4 = __VLS_3({
    ...{ 'onSubmit': {} },
}, ...__VLS_functionalComponentArgsRest(__VLS_3));
let __VLS_6;
let __VLS_7;
let __VLS_8;
const __VLS_9 = {
    onSubmit: (__VLS_ctx.handleCreate)
};
var __VLS_5;
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "right-column" },
});
if (__VLS_ctx.notices.length) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
        ...{ class: "reminder-stack" },
    });
    for (const [notice] of __VLS_getVForSourceType((__VLS_ctx.notices))) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
            key: (notice.id),
            ...{ class: "reminder-item" },
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
        __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
            ...{ class: "reminder-title" },
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
            ...{ class: "reminder-task" },
        });
        (notice.title);
        __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
            ...{ class: "reminder-time" },
        });
        (notice.remindAt ? new Date(notice.remindAt).toLocaleString() : "Now");
        __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
            ...{ onClick: (...[$event]) => {
                    if (!(__VLS_ctx.notices.length))
                        return;
                    __VLS_ctx.dismissNotice(notice.id);
                } },
            ...{ class: "ghost-btn" },
        });
    }
}
if (__VLS_ctx.error) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "error-banner" },
    });
    (__VLS_ctx.error);
}
/** @type {[typeof TodoList, ]} */ ;
// @ts-ignore
const __VLS_10 = __VLS_asFunctionalComponent(TodoList, new TodoList({
    ...{ 'onToggle': {} },
    ...{ 'onRemove': {} },
    loading: (__VLS_ctx.loading),
    tasks: (__VLS_ctx.tasks),
}));
const __VLS_11 = __VLS_10({
    ...{ 'onToggle': {} },
    ...{ 'onRemove': {} },
    loading: (__VLS_ctx.loading),
    tasks: (__VLS_ctx.tasks),
}, ...__VLS_functionalComponentArgsRest(__VLS_10));
let __VLS_13;
let __VLS_14;
let __VLS_15;
const __VLS_16 = {
    onToggle: (__VLS_ctx.handleToggle)
};
const __VLS_17 = {
    onRemove: (__VLS_ctx.handleRemove)
};
var __VLS_12;
/** @type {__VLS_StyleScopedClasses['app-shell']} */ ;
/** @type {__VLS_StyleScopedClasses['left-column']} */ ;
/** @type {__VLS_StyleScopedClasses['right-column']} */ ;
/** @type {__VLS_StyleScopedClasses['reminder-stack']} */ ;
/** @type {__VLS_StyleScopedClasses['reminder-item']} */ ;
/** @type {__VLS_StyleScopedClasses['reminder-title']} */ ;
/** @type {__VLS_StyleScopedClasses['reminder-task']} */ ;
/** @type {__VLS_StyleScopedClasses['reminder-time']} */ ;
/** @type {__VLS_StyleScopedClasses['ghost-btn']} */ ;
/** @type {__VLS_StyleScopedClasses['error-banner']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            ClockPanel: ClockPanel,
            QuickAdd: QuickAdd,
            TodoList: TodoList,
            tasks: tasks,
            loading: loading,
            error: error,
            notices: notices,
            dismissNotice: dismissNotice,
            handleCreate: handleCreate,
            handleToggle: handleToggle,
            handleRemove: handleRemove,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
