import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
function parsePort(value, fallback) {
    var parsed = Number(value);
    return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}
export default defineConfig(function (_a) {
    var mode = _a.mode;
    var env = loadEnv(mode, process.cwd(), "");
    return {
        plugins: [vue()],
        server: {
            port: parsePort(env.VITE_PORT, 5174),
            strictPort: true
        }
    };
});
