import { reactive } from "vue";
const emit = defineEmits();
const form = reactive({
    title: "",
    notes: "",
    dueAt: "",
    remindAt: "",
    priority: "medium"
});
function submit() {
    if (!form.title.trim()) {
        return;
    }
    emit("submit", {
        title: form.title.trim(),
        notes: form.notes?.trim() || undefined,
        dueAt: form.dueAt || undefined,
        remindAt: form.remindAt || undefined,
        priority: form.priority
    });
    form.title = "";
    form.notes = "";
    form.dueAt = "";
    form.remindAt = "";
    form.priority = "medium";
}
const priorities = ["low", "medium", "high"];
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.form, __VLS_intrinsicElements.form)({
    ...{ onSubmit: (__VLS_ctx.submit) },
    ...{ class: "quick-add" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    ...{ class: "field" },
    placeholder: "Add a task title",
    required: true,
});
(__VLS_ctx.form.title);
__VLS_asFunctionalElement(__VLS_intrinsicElements.textarea)({
    value: (__VLS_ctx.form.notes),
    ...{ class: "field field-notes" },
    placeholder: "Notes (optional)",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "row two-col" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    ...{ class: "field" },
    type: "datetime-local",
});
(__VLS_ctx.form.dueAt);
__VLS_asFunctionalElement(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    ...{ class: "field" },
    type: "datetime-local",
});
(__VLS_ctx.form.remindAt);
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "row action-row" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.select, __VLS_intrinsicElements.select)({
    value: (__VLS_ctx.form.priority),
    ...{ class: "field" },
});
for (const [p] of __VLS_getVForSourceType((__VLS_ctx.priorities))) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
        key: (p),
        value: (p),
    });
    (p);
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ class: "primary-btn" },
    type: "submit",
});
/** @type {__VLS_StyleScopedClasses['quick-add']} */ ;
/** @type {__VLS_StyleScopedClasses['field']} */ ;
/** @type {__VLS_StyleScopedClasses['field']} */ ;
/** @type {__VLS_StyleScopedClasses['field-notes']} */ ;
/** @type {__VLS_StyleScopedClasses['row']} */ ;
/** @type {__VLS_StyleScopedClasses['two-col']} */ ;
/** @type {__VLS_StyleScopedClasses['field']} */ ;
/** @type {__VLS_StyleScopedClasses['field']} */ ;
/** @type {__VLS_StyleScopedClasses['row']} */ ;
/** @type {__VLS_StyleScopedClasses['action-row']} */ ;
/** @type {__VLS_StyleScopedClasses['field']} */ ;
/** @type {__VLS_StyleScopedClasses['primary-btn']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            form: form,
            submit: submit,
            priorities: priorities,
        };
    },
    __typeEmits: {},
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
    __typeEmits: {},
});
; /* PartiallyEnd: #4569/main.vue */
