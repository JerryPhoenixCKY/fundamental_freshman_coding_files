import { onMounted, ref, watch } from "vue";
import ClockPanel from "./components/ClockPanel.vue";
import QuickAdd from "./components/QuickAdd.vue";
import TodoList from "./components/TodoList.vue";
import AuthPanel from "./components/AuthPanel.vue";
import { useReminderEngine } from "./composables/useReminderEngine";
import { createTask, fetchTasks, removeTask, toggleTask } from "./api";
const token = ref(localStorage.getItem("token") || "");
const tasks = ref([]);
const loading = ref(false);
const error = ref("");
const { notices, dismissNotice } = useReminderEngine(tasks);
watch(token, (newVal) => {
    if (newVal) {
        localStorage.setItem("token", newVal);
        void loadTasks();
    }
    else {
        localStorage.removeItem("token");
        tasks.value = [];
    }
});
async function loadTasks() {
    if (!token.value)
        return;
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
    if (token.value) {
        void loadTasks();
    }
});
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.main, __VLS_intrinsicElements.main)({
    ...{ class: "app-shell relative" },
});
if (!__VLS_ctx.token) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "fixed inset-0 z-50 flex items-center justify-center bg-black/50 overflow-hidden" },
    });
    /** @type {[typeof AuthPanel, ]} */ ;
    // @ts-ignore
    const __VLS_0 = __VLS_asFunctionalComponent(AuthPanel, new AuthPanel({
        ...{ 'onLogin': {} },
        ...{ class: "bg-white" },
    }));
    const __VLS_1 = __VLS_0({
        ...{ 'onLogin': {} },
        ...{ class: "bg-white" },
    }, ...__VLS_functionalComponentArgsRest(__VLS_0));
    let __VLS_3;
    let __VLS_4;
    let __VLS_5;
    const __VLS_6 = {
        onLogin: ((t) => __VLS_ctx.token = t)
    };
    var __VLS_2;
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "left-column opacity-30" },
    ...{ class: ({ '!opacity-100': __VLS_ctx.token }) },
});
/** @type {[typeof ClockPanel, ]} */ ;
// @ts-ignore
const __VLS_7 = __VLS_asFunctionalComponent(ClockPanel, new ClockPanel({}));
const __VLS_8 = __VLS_7({}, ...__VLS_functionalComponentArgsRest(__VLS_7));
/** @type {[typeof QuickAdd, ]} */ ;
// @ts-ignore
const __VLS_10 = __VLS_asFunctionalComponent(QuickAdd, new QuickAdd({
    ...{ 'onSubmit': {} },
}));
const __VLS_11 = __VLS_10({
    ...{ 'onSubmit': {} },
}, ...__VLS_functionalComponentArgsRest(__VLS_10));
let __VLS_13;
let __VLS_14;
let __VLS_15;
const __VLS_16 = {
    onSubmit: (__VLS_ctx.handleCreate)
};
var __VLS_12;
if (__VLS_ctx.token) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "absolute top-4 right-4 flex gap-2 items-center" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (...[$event]) => {
                if (!(__VLS_ctx.token))
                    return;
                __VLS_ctx.token = '';
            } },
        ...{ class: "px-2 py-1 text-xs border rounded bg-white text-gray-700 hover:bg-gray-100" },
    });
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "right-column opacity-30" },
    ...{ class: ({ '!opacity-100': __VLS_ctx.token }) },
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
const __VLS_17 = __VLS_asFunctionalComponent(TodoList, new TodoList({
    ...{ 'onToggle': {} },
    ...{ 'onRemove': {} },
    loading: (__VLS_ctx.loading),
    tasks: (__VLS_ctx.tasks),
}));
const __VLS_18 = __VLS_17({
    ...{ 'onToggle': {} },
    ...{ 'onRemove': {} },
    loading: (__VLS_ctx.loading),
    tasks: (__VLS_ctx.tasks),
}, ...__VLS_functionalComponentArgsRest(__VLS_17));
let __VLS_20;
let __VLS_21;
let __VLS_22;
const __VLS_23 = {
    onToggle: (__VLS_ctx.handleToggle)
};
const __VLS_24 = {
    onRemove: (__VLS_ctx.handleRemove)
};
var __VLS_19;
/** @type {__VLS_StyleScopedClasses['app-shell']} */ ;
/** @type {__VLS_StyleScopedClasses['relative']} */ ;
/** @type {__VLS_StyleScopedClasses['fixed']} */ ;
/** @type {__VLS_StyleScopedClasses['inset-0']} */ ;
/** @type {__VLS_StyleScopedClasses['z-50']} */ ;
/** @type {__VLS_StyleScopedClasses['flex']} */ ;
/** @type {__VLS_StyleScopedClasses['items-center']} */ ;
/** @type {__VLS_StyleScopedClasses['justify-center']} */ ;
/** @type {__VLS_StyleScopedClasses['bg-black/50']} */ ;
/** @type {__VLS_StyleScopedClasses['overflow-hidden']} */ ;
/** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
/** @type {__VLS_StyleScopedClasses['left-column']} */ ;
/** @type {__VLS_StyleScopedClasses['opacity-30']} */ ;
/** @type {__VLS_StyleScopedClasses['absolute']} */ ;
/** @type {__VLS_StyleScopedClasses['top-4']} */ ;
/** @type {__VLS_StyleScopedClasses['right-4']} */ ;
/** @type {__VLS_StyleScopedClasses['flex']} */ ;
/** @type {__VLS_StyleScopedClasses['gap-2']} */ ;
/** @type {__VLS_StyleScopedClasses['items-center']} */ ;
/** @type {__VLS_StyleScopedClasses['px-2']} */ ;
/** @type {__VLS_StyleScopedClasses['py-1']} */ ;
/** @type {__VLS_StyleScopedClasses['text-xs']} */ ;
/** @type {__VLS_StyleScopedClasses['border']} */ ;
/** @type {__VLS_StyleScopedClasses['rounded']} */ ;
/** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
/** @type {__VLS_StyleScopedClasses['text-gray-700']} */ ;
/** @type {__VLS_StyleScopedClasses['hover:bg-gray-100']} */ ;
/** @type {__VLS_StyleScopedClasses['right-column']} */ ;
/** @type {__VLS_StyleScopedClasses['opacity-30']} */ ;
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
            AuthPanel: AuthPanel,
            token: token,
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
