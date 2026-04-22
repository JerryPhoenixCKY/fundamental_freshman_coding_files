import { computed, onMounted, onUnmounted, ref } from "vue";
const now = ref(new Date());
let timer;
onMounted(() => {
    timer = window.setInterval(() => {
        now.value = new Date();
    }, 1000);
});
onUnmounted(() => {
    if (timer !== undefined) {
        window.clearInterval(timer);
    }
});
const displayTime = computed(() => now.value.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }));
const displayDate = computed(() => now.value.toLocaleDateString([], { weekday: "long", year: "numeric", month: "short", day: "numeric" }));
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "clock-panel" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "clock-label" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "clock-time" },
});
(__VLS_ctx.displayTime);
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "clock-date" },
});
(__VLS_ctx.displayDate);
/** @type {__VLS_StyleScopedClasses['clock-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['clock-label']} */ ;
/** @type {__VLS_StyleScopedClasses['clock-time']} */ ;
/** @type {__VLS_StyleScopedClasses['clock-date']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            displayTime: displayTime,
            displayDate: displayDate,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
