import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyBboxPatch
from matplotlib.widgets import Button, Slider, TextBox


def theta_response(t, theta0, m, L, g, b):
    """小角度近似下阻尼单摆解析解，默认初始角速度为 0。"""
    omega0 = np.sqrt(g / L)
    gamma = b / (2 * m)
    eps = 1e-10

    if b <= eps:
        return theta0 * np.cos(omega0 * t)

    if gamma < omega0 - eps:
        omega_d = np.sqrt(max(omega0 ** 2 - gamma ** 2, 0.0))
        if omega_d <= eps:
            return theta0 * (1 + omega0 * t) * np.exp(-omega0 * t)
        return theta0 * np.exp(-gamma * t) * (
            np.cos(omega_d * t) + (gamma / omega_d) * np.sin(omega_d * t)
        )

    if np.isclose(gamma, omega0, rtol=1e-5, atol=1e-9):
        return theta0 * (1 + omega0 * t) * np.exp(-omega0 * t)

    beta = np.sqrt(max(gamma ** 2 - omega0 ** 2, 0.0))
    if beta <= eps:
        return theta0 * (1 + omega0 * t) * np.exp(-omega0 * t)

    c1 = theta0 * (gamma + beta) / (2 * beta)
    c2 = theta0 * (beta - gamma) / (2 * beta)
    return c1 * np.exp((-gamma + beta) * t) + c2 * np.exp((-gamma - beta) * t)


class DampedPendulumAnimator:
    def __init__(self, m=1.0, L=1.0, g=9.8, theta0=0.5):
        self.m = float(m)
        self.L = float(L)
        self.g = float(g)
        self.theta0 = float(theta0)

        self.omega0 = np.sqrt(self.g / self.L)
        self.bc = 2 * self.m * self.omega0

        self.dt = 0.02
        self.time_window = 10.0
        self.max_points = 1200
        self.trail_points = 220

        self.t = 0.0
        self.time_history = [0.0]
        self.running = False
        self._updating_controls = False

        # Google Material 风格配色（亮色主题）
        self.theme = {
            "bg": "#f8f9fa",
            "surface": "#ffffff",
            "surface_muted": "#f1f3f4",
            "outline": "#dadce0",
            "grid": "#e8eaed",
            "text_primary": "#202124",
            "text_secondary": "#5f6368",
            "google_blue": "#1a73e8",
            "google_green": "#34a853",
            "google_red": "#ea4335",
            "google_yellow": "#fbbc04",
        }

        self.states = [
            {"name": "无阻尼", "color": self.theme["google_green"], "b": 0.00 * self.bc},
            {"name": "欠阻尼", "color": self.theme["google_blue"], "b": 0.15 * self.bc},
            {"name": "临界阻尼", "color": self.theme["google_red"], "b": 1.00 * self.bc},
            {"name": "过阻尼", "color": self.theme["google_yellow"], "b": 3.00 * self.bc},
        ]

        self._build_figure()
        self._bind_events()
        self._reset_simulation()

    def _build_figure(self):
        plt.rcParams["font.sans-serif"] = [
            "Microsoft YaHei",
            "Noto Sans CJK SC",
            "Segoe UI",
            "Arial Unicode MS",
        ]
        plt.rcParams["axes.unicode_minus"] = False

        self.fig = plt.figure(figsize=(14, 9), dpi=120)
        self.fig.patch.set_facecolor(self.theme["bg"])

        # 卡片背景：主动画区、曲线区、参数区、说明区
        self._add_card((0.035, 0.295, 0.565, 0.665))
        self._add_card((0.605, 0.295, 0.365, 0.665))
        self._add_card((0.035, 0.030, 0.470, 0.245))
        self._add_card((0.605, 0.030, 0.365, 0.245))

        self.ax_pendulum = self.fig.add_axes((0.06, 0.33, 0.52, 0.62))
        self.ax_theta = self.fig.add_axes((0.62, 0.33, 0.35, 0.62))

        self.fig.text(
            0.04,
            0.975,
            "Damped Pendulum Playground",
            fontsize=18,
            color=self.theme["text_primary"],
            fontweight="bold",
            va="top",
        )
        self.fig.text(
            0.04,
            0.952,
            "四种阻尼状态的并行动画与参数探索",
            fontsize=11,
            color=self.theme["text_secondary"],
            va="top",
        )

        self._style_axes(self.ax_pendulum)
        self._style_axes(self.ax_theta)

        self.ax_pendulum.set_title(
            "四状态单摆叠加动画（同一支点）",
            fontsize=14,
            fontweight="bold",
            color=self.theme["text_primary"],
            pad=10,
        )
        self.ax_pendulum.set_xlim(-1.22 * self.L, 1.22 * self.L)
        self.ax_pendulum.set_ylim(-1.30 * self.L, 0.18 * self.L)
        self.ax_pendulum.set_aspect("equal", adjustable="box")
        self.ax_pendulum.set_xlabel("水平位移 x", color=self.theme["text_secondary"])
        self.ax_pendulum.set_ylabel("竖直位移 y", color=self.theme["text_secondary"])
        self.ax_pendulum.grid(True, linestyle="-", linewidth=0.8, color=self.theme["grid"], alpha=0.95)
        self.ax_pendulum.plot([0], [0], marker="o", color=self.theme["text_primary"], markersize=5)

        self.ax_theta.set_title(
            "角位移-时间 实时对比",
            fontsize=13,
            fontweight="bold",
            color=self.theme["text_primary"],
            pad=10,
        )
        self.ax_theta.set_xlabel("时间 t (s)", color=self.theme["text_secondary"])
        self.ax_theta.set_ylabel("摆角 θ (rad)", color=self.theme["text_secondary"])
        self.ax_theta.grid(True, linestyle="-", linewidth=0.8, color=self.theme["grid"], alpha=0.95)
        self.ax_theta.axhline(0, color=self.theme["text_secondary"], linewidth=1, linestyle="--")

        self.time_text = self.ax_pendulum.text(
            0.02,
            0.96,
            "t = 0.00 s",
            transform=self.ax_pendulum.transAxes,
            fontsize=11,
            color=self.theme["text_primary"],
            verticalalignment="top",
            bbox=dict(
                boxstyle="round,pad=0.35,rounding_size=0.12",
                fc=self.theme["surface_muted"],
                ec=self.theme["outline"],
                alpha=0.97,
            ),
        )

        self.param_text = self.ax_theta.text(
            0.02,
            0.98,
            "",
            transform=self.ax_theta.transAxes,
            fontsize=10,
            color=self.theme["text_primary"],
            verticalalignment="top",
            bbox=dict(
                boxstyle="round,pad=0.4,rounding_size=0.15",
                fc=self.theme["surface_muted"],
                ec=self.theme["outline"],
                alpha=0.97,
            ),
        )

        for state in self.states:
            rod, = self.ax_pendulum.plot([], [], color=state["color"], linewidth=2.6, label=state["name"])
            bob, = self.ax_pendulum.plot(
                [],
                [],
                marker="o",
                color=state["color"],
                markeredgecolor=self.theme["surface"],
                markeredgewidth=1.2,
                markersize=9,
            )
            trace, = self.ax_pendulum.plot([], [], color=state["color"], linewidth=1.2, alpha=0.24)
            curve, = self.ax_theta.plot([], [], color=state["color"], linewidth=2.4, label=state["name"])

            state["rod"] = rod
            state["bob"] = bob
            state["trace"] = trace
            state["curve"] = curve
            state["x_history"] = []
            state["y_history"] = []
            state["theta_history"] = []

        legend_p = self.ax_pendulum.legend(loc="upper right", fontsize=10, frameon=True)
        legend_t = self.ax_theta.legend(loc="upper right", fontsize=10, frameon=True)
        legend_p.get_frame().set_facecolor(self.theme["surface"])
        legend_p.get_frame().set_edgecolor(self.theme["outline"])
        legend_t.get_frame().set_facecolor(self.theme["surface"])
        legend_t.get_frame().set_edgecolor(self.theme["outline"])

        ax_btn_start = self.fig.add_axes((0.06, 0.25, 0.12, 0.055))
        ax_btn_reset = self.fig.add_axes((0.20, 0.25, 0.12, 0.055))
        self.btn_start = Button(ax_btn_start, "开始", color=self.theme["google_blue"], hovercolor="#1667d8")
        self.btn_reset = Button(ax_btn_reset, "重置", color=self.theme["surface"], hovercolor="#eef2f7")
        self.btn_start.label.set_color("white")
        self.btn_start.label.set_fontweight("bold")
        self.btn_reset.label.set_color(self.theme["text_primary"])
        self.btn_reset.label.set_fontweight("bold")
        for btn_ax in [ax_btn_start, ax_btn_reset]:
            for spine in btn_ax.spines.values():
                spine.set_color(self.theme["outline"])
                spine.set_linewidth(1.0)

        ax_s0 = self.fig.add_axes((0.06, 0.19, 0.30, 0.03), facecolor=self.theme["surface_muted"])
        ax_s1 = self.fig.add_axes((0.06, 0.145, 0.30, 0.03), facecolor=self.theme["surface_muted"])
        ax_s2 = self.fig.add_axes((0.06, 0.10, 0.30, 0.03), facecolor=self.theme["surface_muted"])
        ax_s3 = self.fig.add_axes((0.06, 0.055, 0.30, 0.03), facecolor=self.theme["surface_muted"])
        ax_theta0 = self.fig.add_axes((0.62, 0.18, 0.25, 0.03), facecolor=self.theme["surface_muted"])

        ax_tb0 = self.fig.add_axes((0.38, 0.19, 0.10, 0.03), facecolor=self.theme["surface"])
        ax_tb1 = self.fig.add_axes((0.38, 0.145, 0.10, 0.03), facecolor=self.theme["surface"])
        ax_tb2 = self.fig.add_axes((0.38, 0.10, 0.10, 0.03), facecolor=self.theme["surface"])
        ax_tb3 = self.fig.add_axes((0.38, 0.055, 0.10, 0.03), facecolor=self.theme["surface"])
        ax_ttheta = self.fig.add_axes((0.89, 0.18, 0.08, 0.03), facecolor=self.theme["surface"])

        self.s_b0 = Slider(
            ax_s0,
            "无阻尼 b0 (kg/s)",
            0.00 * self.bc,
            0.20 * self.bc,
            valinit=self.states[0]["b"],
            color=self.states[0]["color"],
        )
        self.s_b1 = Slider(
            ax_s1,
            "欠阻尼 b1 (kg/s)",
            0.01 * self.bc,
            0.99 * self.bc,
            valinit=self.states[1]["b"],
            color=self.states[1]["color"],
        )
        self.s_b2 = Slider(
            ax_s2,
            "临界附近 b2 (kg/s)",
            0.80 * self.bc,
            1.20 * self.bc,
            valinit=self.states[2]["b"],
            color=self.states[2]["color"],
        )
        self.s_b3 = Slider(
            ax_s3,
            "过阻尼 b3 (kg/s)",
            1.01 * self.bc,
            4.00 * self.bc,
            valinit=self.states[3]["b"],
            color=self.states[3]["color"],
        )
        self.s_theta0 = Slider(ax_theta0, "初始角度 θ0 (rad)", 0.05, 1.00, valinit=self.theta0, color=self.theme["google_blue"])

        self.tb_b0 = TextBox(ax_tb0, "输入", initial=f"{self.s_b0.val:.3f}")
        self.tb_b1 = TextBox(ax_tb1, "输入", initial=f"{self.s_b1.val:.3f}")
        self.tb_b2 = TextBox(ax_tb2, "输入", initial=f"{self.s_b2.val:.3f}")
        self.tb_b3 = TextBox(ax_tb3, "输入", initial=f"{self.s_b3.val:.3f}")
        self.tb_theta0 = TextBox(ax_ttheta, "输入", initial=f"{self.s_theta0.val:.3f}")

        self._style_sliders([self.s_b0, self.s_b1, self.s_b2, self.s_b3, self.s_theta0])
        self._style_textboxes([self.tb_b0, self.tb_b1, self.tb_b2, self.tb_b3, self.tb_theta0])

        self.control_map = {
            "b0": (self.s_b0, self.tb_b0, 0.00 * self.bc, 0.20 * self.bc),
            "b1": (self.s_b1, self.tb_b1, 0.01 * self.bc, 0.99 * self.bc),
            "b2": (self.s_b2, self.tb_b2, 0.80 * self.bc, 1.20 * self.bc),
            "b3": (self.s_b3, self.tb_b3, 1.01 * self.bc, 4.00 * self.bc),
            "theta0": (self.s_theta0, self.tb_theta0, 0.05, 1.00),
        }

        self.fig.text(
            0.62,
            0.12,
            "操作提示：可拖动滑块，或在“输入”框填精确值后按回车；参数改变会从 t=0 重新演示。",
            fontsize=10,
            color=self.theme["text_secondary"],
        )

    def _add_card(self, rect):
        x, y, w, h = rect
        card = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.008,rounding_size=0.015",
            transform=self.fig.transFigure,
            linewidth=1.0,
            edgecolor=self.theme["outline"],
            facecolor=self.theme["surface"],
            zorder=-10,
        )
        self.fig.patches.append(card)

    def _style_axes(self, ax):
        ax.set_facecolor(self.theme["surface"])
        for spine in ax.spines.values():
            spine.set_color(self.theme["outline"])
            spine.set_linewidth(1.0)
        ax.tick_params(colors=self.theme["text_secondary"], labelsize=10)

    def _style_sliders(self, sliders):
        for slider in sliders:
            slider.label.set_color(self.theme["text_secondary"])
            slider.label.set_fontsize(9.5)
            slider.valtext.set_color(self.theme["text_primary"])
            slider.valtext.set_fontsize(9.5)
            if hasattr(slider, "track"):
                slider.track.set_color(self.theme["grid"])
            if hasattr(slider, "vline"):
                slider.vline.set_color(self.theme["text_secondary"])
                slider.vline.set_linewidth(1.2)

    def _style_textboxes(self, textboxes):
        for textbox in textboxes:
            textbox.label.set_color(self.theme["text_secondary"])
            textbox.label.set_fontsize(9.3)
            textbox.text_disp.set_color(self.theme["text_primary"])
            textbox.text_disp.set_fontsize(10)
            for spine in textbox.ax.spines.values():
                spine.set_color(self.theme["outline"])
                spine.set_linewidth(1.0)

    def _bind_events(self):
        self.btn_start.on_clicked(self._on_toggle_start)
        self.btn_reset.on_clicked(self._on_reset)

        self.s_b0.on_changed(self._on_slider_change)
        self.s_b1.on_changed(self._on_slider_change)
        self.s_b2.on_changed(self._on_slider_change)
        self.s_b3.on_changed(self._on_slider_change)
        self.s_theta0.on_changed(self._on_slider_change)

        self.tb_b0.on_submit(lambda text: self._on_text_submit("b0", text))
        self.tb_b1.on_submit(lambda text: self._on_text_submit("b1", text))
        self.tb_b2.on_submit(lambda text: self._on_text_submit("b2", text))
        self.tb_b3.on_submit(lambda text: self._on_text_submit("b3", text))
        self.tb_theta0.on_submit(lambda text: self._on_text_submit("theta0", text))

    def _refresh_param_text(self):
        lines = [
            "当前参数",
            f"bc = {self.bc:.3f} kg/s",
            f"b0 = {self.states[0]['b']:.3f} kg/s ({self.states[0]['b'] / self.bc:.3f} bc)",
            f"b1 = {self.states[1]['b']:.3f} kg/s ({self.states[1]['b'] / self.bc:.3f} bc)",
            f"b2 = {self.states[2]['b']:.3f} kg/s ({self.states[2]['b'] / self.bc:.3f} bc)",
            f"b3 = {self.states[3]['b']:.3f} kg/s ({self.states[3]['b'] / self.bc:.3f} bc)",
            f"θ0 = {self.theta0:.3f} rad",
        ]
        self.param_text.set_text("\n".join(lines))

    def _reset_simulation(self):
        self.t = 0.0
        self.time_history = [0.0]

        y_amp = max(0.18, self.theta0 * 1.2)
        self.ax_theta.set_ylim(-y_amp, y_amp)
        self.ax_theta.set_xlim(0, self.time_window)

        for state in self.states:
            theta = theta_response(0.0, self.theta0, self.m, self.L, self.g, state["b"])
            x = self.L * np.sin(theta)
            y = -self.L * np.cos(theta)

            state["x_history"] = [x]
            state["y_history"] = [y]
            state["theta_history"] = [theta]

            state["rod"].set_data([0.0, x], [0.0, y])
            state["bob"].set_data([x], [y])
            state["trace"].set_data(state["x_history"], state["y_history"])
            state["curve"].set_data(self.time_history, state["theta_history"])

        self.time_text.set_text("t = 0.00 s")
        self._refresh_param_text()

    def _on_toggle_start(self, _event):
        if self.running:
            self.running = False
            self.btn_start.label.set_text("开始")
            self.anim.event_source.stop()
        else:
            self.running = True
            self.btn_start.label.set_text("暂停")
            self.anim.event_source.start()

    def _on_reset(self, _event):
        self._reset_simulation()
        self.fig.canvas.draw_idle()

    def _on_slider_change(self, _value):
        if self._updating_controls:
            return

        self._sync_textboxes_from_sliders()

        self.states[0]["b"] = self.s_b0.val
        self.states[1]["b"] = self.s_b1.val
        self.states[2]["b"] = self.s_b2.val
        self.states[3]["b"] = self.s_b3.val
        self.theta0 = float(self.s_theta0.val)

        self._reset_simulation()
        self.fig.canvas.draw_idle()

    def _sync_textboxes_from_sliders(self):
        self._updating_controls = True
        self.tb_b0.set_val(f"{self.s_b0.val:.3f}")
        self.tb_b1.set_val(f"{self.s_b1.val:.3f}")
        self.tb_b2.set_val(f"{self.s_b2.val:.3f}")
        self.tb_b3.set_val(f"{self.s_b3.val:.3f}")
        self.tb_theta0.set_val(f"{self.s_theta0.val:.3f}")
        self._updating_controls = False

    def _on_text_submit(self, key, text):
        if self._updating_controls:
            return

        slider, textbox, min_val, max_val = self.control_map[key]
        try:
            value = float(text)
        except ValueError:
            self._sync_textboxes_from_sliders()
            self.fig.canvas.draw_idle()
            return

        value = float(np.clip(value, min_val, max_val))

        self._updating_controls = True
        slider.set_val(value)
        textbox.set_val(f"{value:.3f}")
        self._updating_controls = False

        self.states[0]["b"] = self.s_b0.val
        self.states[1]["b"] = self.s_b1.val
        self.states[2]["b"] = self.s_b2.val
        self.states[3]["b"] = self.s_b3.val
        self.theta0 = float(self.s_theta0.val)

        self._reset_simulation()
        self.fig.canvas.draw_idle()

    def _update(self, _frame):
        self.t += self.dt
        self.time_history.append(self.t)
        if len(self.time_history) > self.max_points:
            self.time_history = self.time_history[-self.max_points:]

        for state in self.states:
            theta = theta_response(self.t, self.theta0, self.m, self.L, self.g, state["b"])
            x = self.L * np.sin(theta)
            y = -self.L * np.cos(theta)

            state["x_history"].append(x)
            state["y_history"].append(y)
            state["theta_history"].append(theta)

            if len(state["x_history"]) > self.trail_points:
                state["x_history"] = state["x_history"][-self.trail_points:]
                state["y_history"] = state["y_history"][-self.trail_points:]

            if len(state["theta_history"]) > self.max_points:
                state["theta_history"] = state["theta_history"][-self.max_points:]

            state["rod"].set_data([0.0, x], [0.0, y])
            state["bob"].set_data([x], [y])
            state["trace"].set_data(state["x_history"], state["y_history"])
            state["curve"].set_data(self.time_history, state["theta_history"])

        left = max(0.0, self.t - self.time_window)
        self.ax_theta.set_xlim(left, left + self.time_window)
        self.time_text.set_text(f"t = {self.t:.2f} s")

        return []

    def show(self):
        self.anim = FuncAnimation(
            self.fig,
            self._update,
            interval=int(self.dt * 1000),
            blit=False,
            cache_frame_data=False,
        )
        self.anim.event_source.stop()
        plt.show()


def main():
    print("单摆阻尼振动四状态叠加动画")
    print("支持开始/暂停、重置、阻尼系数滑块和初始角度滑块。")
    animator = DampedPendulumAnimator(m=1.0, L=1.0, g=9.8, theta0=0.5)
    animator.show()


if __name__ == "__main__":
    main()
