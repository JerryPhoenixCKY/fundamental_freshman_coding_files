import { ref } from "vue";
import { sendAuthCode, verifyAuthCode } from "../api";
const emit = defineEmits();
const email = ref("");
const code = ref("");
const codeSent = ref(false);
const loading = ref(false);
const error = ref("");
async function request() {
    if (!email.value)
        return;
    loading.value = true;
    error.value = "";
    try {
        await sendAuthCode(email.value);
        codeSent.value = true;
    }
    catch (err) {
        error.value = err instanceof Error ? err.message : "Failed to send code";
    }
    finally {
        loading.value = false;
    }
}
async function verify() {
    if (!email.value || !code.value)
        return;
    loading.value = true;
    error.value = "";
    try {
        const res = await verifyAuthCode(email.value, code.value);
        if (res?.accessToken) {
            emit("login", res.accessToken);
        }
    }
    catch (err) {
        error.value = err instanceof Error ? err.message : "Failed to verify code";
    }
    finally {
        loading.value = false;
    }
}
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "auth-panel p-4 rounded bg-gray-50 border" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h2, __VLS_intrinsicElements.h2)({
    ...{ class: "text-lg font-bold mb-4" },
});
if (__VLS_ctx.error) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "error-banner mb-2 text-red-500" },
    });
    (__VLS_ctx.error);
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.form, __VLS_intrinsicElements.form)({
    ...{ onSubmit: (...[$event]) => {
            __VLS_ctx.codeSent ? __VLS_ctx.verify() : __VLS_ctx.request();
        } },
    ...{ class: "flex flex-col gap-2" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    type: "email",
    placeholder: "Enter your email",
    required: true,
    ...{ class: "p-2 border rounded w-full" },
    disabled: (__VLS_ctx.codeSent || __VLS_ctx.loading),
});
(__VLS_ctx.email);
if (__VLS_ctx.codeSent) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
        value: (__VLS_ctx.code),
        type: "text",
        placeholder: "Enter 6-digit code",
        required: true,
        ...{ class: "p-2 border rounded w-full" },
        disabled: (__VLS_ctx.loading),
    });
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    type: "submit",
    ...{ class: "bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:opacity-50" },
    disabled: (__VLS_ctx.loading),
});
(__VLS_ctx.loading ? "Processing..." : (__VLS_ctx.codeSent ? "Verify" : "Send Code"));
/** @type {__VLS_StyleScopedClasses['auth-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['p-4']} */ ;
/** @type {__VLS_StyleScopedClasses['rounded']} */ ;
/** @type {__VLS_StyleScopedClasses['bg-gray-50']} */ ;
/** @type {__VLS_StyleScopedClasses['border']} */ ;
/** @type {__VLS_StyleScopedClasses['text-lg']} */ ;
/** @type {__VLS_StyleScopedClasses['font-bold']} */ ;
/** @type {__VLS_StyleScopedClasses['mb-4']} */ ;
/** @type {__VLS_StyleScopedClasses['error-banner']} */ ;
/** @type {__VLS_StyleScopedClasses['mb-2']} */ ;
/** @type {__VLS_StyleScopedClasses['text-red-500']} */ ;
/** @type {__VLS_StyleScopedClasses['flex']} */ ;
/** @type {__VLS_StyleScopedClasses['flex-col']} */ ;
/** @type {__VLS_StyleScopedClasses['gap-2']} */ ;
/** @type {__VLS_StyleScopedClasses['p-2']} */ ;
/** @type {__VLS_StyleScopedClasses['border']} */ ;
/** @type {__VLS_StyleScopedClasses['rounded']} */ ;
/** @type {__VLS_StyleScopedClasses['w-full']} */ ;
/** @type {__VLS_StyleScopedClasses['p-2']} */ ;
/** @type {__VLS_StyleScopedClasses['border']} */ ;
/** @type {__VLS_StyleScopedClasses['rounded']} */ ;
/** @type {__VLS_StyleScopedClasses['w-full']} */ ;
/** @type {__VLS_StyleScopedClasses['bg-blue-600']} */ ;
/** @type {__VLS_StyleScopedClasses['text-white']} */ ;
/** @type {__VLS_StyleScopedClasses['p-2']} */ ;
/** @type {__VLS_StyleScopedClasses['rounded']} */ ;
/** @type {__VLS_StyleScopedClasses['hover:bg-blue-700']} */ ;
/** @type {__VLS_StyleScopedClasses['disabled:opacity-50']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            email: email,
            code: code,
            codeSent: codeSent,
            loading: loading,
            error: error,
            request: request,
            verify: verify,
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
