#define WIN32_LEAN_AND_MEAN
#define NOMINMAX

#include <windows.h>
#include <commctrl.h>
#include <mmsystem.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <wctype.h>
#include <algorithm>
#include <string>

static const int kCaseCount = 4;
static const int kSliderCount = 5;
static const int kTrailCap = 240;
static const int kSliderResolution = 1000;
static const double kFixedDt = 1.0 / 240.0;
static const double kPi = 3.14159265358979323846;
static const int kControlPanelWidth = 456;
static const int kHeaderHeight = 72;
static const int kRenderSupersampleScale = 2;

enum {
	IDC_BTN_TOGGLE = 1001,
	IDC_BTN_RESET = 1002,
	IDC_BTN_APPLY = 1003,
	IDC_SLIDER_B0 = 1100,
	IDC_SLIDER_B1 = 1101,
	IDC_SLIDER_B2 = 1102,
	IDC_SLIDER_B3 = 1103,
	IDC_SLIDER_THETA = 1104,
	IDC_EDIT_B0 = 1200,
	IDC_EDIT_B1 = 1201,
	IDC_EDIT_B2 = 1202,
	IDC_EDIT_B3 = 1203,
	IDC_EDIT_THETA = 1204
};

enum {
	IDX_B0 = 0,
	IDX_B1 = 1,
	IDX_B2 = 2,
	IDX_B3 = 3,
	IDX_THETA = 4
};

typedef struct {
	double theta;
	double omega;
} PendulumState;

typedef struct {
	double x[kTrailCap];
	double y[kTrailCap];
	int head;
	int size;
} TrailBuffer;

typedef struct {
	const char* name;
	COLORREF color;
	double b;
	PendulumState state;
	TrailBuffer trail;
} DampingState;

typedef struct {
	int id;
	int edit_id;
	const wchar_t* title;
	double min_value;
	double max_value;
	HWND label;
	HWND track;
	HWND value;
	HWND input;
} SliderUI;

typedef struct {
	HDC dc;
	HBITMAP bitmap;
	HBITMAP old_bitmap;
	int width;
	int height;
} BackBuffer;

typedef struct {
	HWND window;
	HWND button_toggle;
	HWND button_reset;
	HWND button_apply;
	HWND hint_text;
	HFONT ui_font;
	SliderUI sliders[kSliderCount];
	bool slider_update_guard;
	bool ui_refresh_guard;
	bool dragging_theta;
	bool resume_after_drag;

	bool running;
	bool quit_requested;
	double sim_time;
	double accumulator;

	LARGE_INTEGER perf_freq;
	LARGE_INTEGER last_tick;

	double m;
	double L;
	double g;
	double bc;
	double theta0;

	DampingState states[kCaseCount];
	BackBuffer back;
} AppState;

static AppState g_app = {};

static void reset_simulation(AppState* app);

static void derivatives(const PendulumState* s, double gamma, double omega0_sq, PendulumState* d) {
	d->theta = s->omega;
	d->omega = -gamma * s->omega - omega0_sq * s->theta;
}

static void rk4_step(PendulumState* s, double dt, double gamma, double omega0_sq) {
	PendulumState k1, k2, k3, k4, temp;

	derivatives(s, gamma, omega0_sq, &k1);

	temp.theta = s->theta + 0.5 * dt * k1.theta;
	temp.omega = s->omega + 0.5 * dt * k1.omega;
	derivatives(&temp, gamma, omega0_sq, &k2);

	temp.theta = s->theta + 0.5 * dt * k2.theta;
	temp.omega = s->omega + 0.5 * dt * k2.omega;
	derivatives(&temp, gamma, omega0_sq, &k3);

	temp.theta = s->theta + dt * k3.theta;
	temp.omega = s->omega + dt * k3.omega;
	derivatives(&temp, gamma, omega0_sq, &k4);

	s->theta += (dt / 6.0) * (k1.theta + 2.0 * k2.theta + 2.0 * k3.theta + k4.theta);
	s->omega += (dt / 6.0) * (k1.omega + 2.0 * k2.omega + 2.0 * k3.omega + k4.omega);
}

static void trail_reset(TrailBuffer* trail) {
	trail->head = 0;
	trail->size = 0;
}

static void trail_push(TrailBuffer* trail, double x, double y) {
	if (trail->size == kTrailCap) {
		trail->head = (trail->head + 1) % kTrailCap;
		trail->size = kTrailCap - 1;
	}
	int idx = (trail->head + trail->size) % kTrailCap;
	trail->x[idx] = x;
	trail->y[idx] = y;
	trail->size += 1;
}

static void world_to_bob(const AppState* app, double theta, double* x, double* y) {
	*x = app->L * sin(theta);
	*y = app->L * cos(theta);
}

static void set_control_font(HWND control, HFONT font) {
	if (control && font) {
		SendMessageA(control, WM_SETFONT, (WPARAM)font, TRUE);
	}
}

static SliderUI* slider_by_id(AppState* app, int id) {
	for (int i = 0; i < kSliderCount; ++i) {
		if (app->sliders[i].id == id) {
			return &app->sliders[i];
		}
	}
	return NULL;
}

static SliderUI* slider_by_track(AppState* app, HWND track) {
	for (int i = 0; i < kSliderCount; ++i) {
		if (app->sliders[i].track == track) {
			return &app->sliders[i];
		}
	}
	return NULL;
}

static SliderUI* slider_by_edit(AppState* app, HWND edit) {
	for (int i = 0; i < kSliderCount; ++i) {
		if (app->sliders[i].input == edit) {
			return &app->sliders[i];
		}
	}
	return NULL;
}

static double slider_get_value(const SliderUI* slider) {
	if (!slider || !slider->track) {
		return 0.0;
	}
	int pos = (int)SendMessageA(slider->track, TBM_GETPOS, 0, 0);
	double t = (double)pos / (double)kSliderResolution;
	return slider->min_value + (slider->max_value - slider->min_value) * t;
}

static void slider_set_value(const SliderUI* slider, double value) {
	if (!slider || !slider->track) {
		return;
	}
	double clamped = std::max(slider->min_value, std::min(value, slider->max_value));
	double t = (clamped - slider->min_value) / (slider->max_value - slider->min_value);
	int pos = (int)lround(t * (double)kSliderResolution);
	SendMessageA(slider->track, TBM_SETPOS, TRUE, pos);
}

static std::wstring utf8_to_wide(const char* text) {
	if (!text) {
		return L"";
	}

	int len = MultiByteToWideChar(CP_UTF8, 0, text, -1, NULL, 0);
	if (len <= 0) {
		return L"";
	}

	std::wstring out((size_t)len, L'\0');
	MultiByteToWideChar(CP_UTF8, 0, text, -1, &out[0], len);
	if (!out.empty() && out.back() == L'\0') {
		out.pop_back();
	}
	return out;
}

static COLORREF lighten(COLORREF c, int amount) {
	int r = std::min(255, (int)GetRValue(c) + amount);
	int g = std::min(255, (int)GetGValue(c) + amount);
	int b = std::min(255, (int)GetBValue(c) + amount);
	return RGB(r, g, b);
}

static void fill_rect(HDC dc, const RECT* rc, COLORREF color) {
	HBRUSH brush = CreateSolidBrush(color);
	FillRect(dc, rc, brush);
	DeleteObject(brush);
}

static void draw_line(HDC dc, int x1, int y1, int x2, int y2, COLORREF color, int width) {
	HPEN pen = CreatePen(PS_SOLID, width, color);
	HPEN old_pen = (HPEN)SelectObject(dc, pen);
	MoveToEx(dc, x1, y1, NULL);
	LineTo(dc, x2, y2);
	SelectObject(dc, old_pen);
	DeleteObject(pen);
}

static void draw_text(HDC dc, int x, int y, COLORREF color, const char* text) {
	SetTextColor(dc, color);
	std::wstring w = utf8_to_wide(text);
	TextOutW(dc, x, y, w.c_str(), (int)w.size());
}

static void draw_round_card(HDC dc, const RECT* rc, COLORREF fill, COLORREF border) {
	HBRUSH brush = CreateSolidBrush(fill);
	HPEN pen = CreatePen(PS_SOLID, 1, border);
	HBRUSH old_brush = (HBRUSH)SelectObject(dc, brush);
	HPEN old_pen = (HPEN)SelectObject(dc, pen);
	RoundRect(dc, rc->left, rc->top, rc->right, rc->bottom, 18, 18);
	SelectObject(dc, old_pen);
	SelectObject(dc, old_brush);
	DeleteObject(pen);
	DeleteObject(brush);
}

static void draw_button_ownerdraw(const AppState* app, const DRAWITEMSTRUCT* dis, COLORREF fill, COLORREF border, COLORREF text_color) {
	if (!dis) {
		return;
	}

	RECT rc = dis->rcItem;
	bool pressed = (dis->itemState & ODS_SELECTED) != 0;
	bool disabled = (dis->itemState & ODS_DISABLED) != 0;

	COLORREF final_fill = fill;
	COLORREF final_border = border;
	COLORREF final_text = text_color;

	if (pressed) {
		final_fill = lighten(fill, -26);
		final_border = lighten(border, -18);
	}
	if (disabled) {
		final_fill = RGB(232, 234, 237);
		final_border = RGB(218, 220, 224);
		final_text = RGB(154, 160, 166);
	}

	HBRUSH brush = CreateSolidBrush(final_fill);
	HPEN pen = CreatePen(PS_SOLID, 1, final_border);
	HBRUSH old_brush = (HBRUSH)SelectObject(dis->hDC, brush);
	HPEN old_pen = (HPEN)SelectObject(dis->hDC, pen);
	RoundRect(dis->hDC, rc.left, rc.top, rc.right, rc.bottom, 14, 14);
	SelectObject(dis->hDC, old_pen);
	SelectObject(dis->hDC, old_brush);
	DeleteObject(pen);
	DeleteObject(brush);

	wchar_t text[64];
	GetWindowTextW(dis->hwndItem, text, (int)(sizeof(text) / sizeof(text[0])));
	SetBkMode(dis->hDC, TRANSPARENT);
	SetTextColor(dis->hDC, final_text);
	if (app->ui_font) {
		SelectObject(dis->hDC, app->ui_font);
	}
	DrawTextW(dis->hDC, text, -1, &rc, DT_CENTER | DT_VCENTER | DT_SINGLELINE);

	if ((dis->itemState & ODS_FOCUS) != 0) {
		RECT focus = rc;
		InflateRect(&focus, -4, -4);
		DrawFocusRect(dis->hDC, &focus);
	}
}

static bool parse_double_strict(const wchar_t* raw, double* out) {
	if (!raw || !out) {
		return false;
	}

	wchar_t buf[96];
	size_t n = wcsnlen(raw, (sizeof(buf) / sizeof(buf[0])) - 1);
	wmemcpy(buf, raw, n);
	buf[n] = L'\0';

	wchar_t* begin = buf;
	while (*begin && iswspace(*begin)) {
		++begin;
	}
	if (*begin == L'\0') {
		return false;
	}

	wchar_t* end_ptr = NULL;
	double v = wcstod(begin, &end_ptr);
	if (end_ptr == begin) {
		return false;
	}
	while (*end_ptr && iswspace(*end_ptr)) {
		++end_ptr;
	}
	if (*end_ptr != L'\0') {
		return false;
	}

	*out = v;
	return true;
}

static bool slider_is_theta(const SliderUI* slider) {
	return slider && slider->id == IDC_SLIDER_THETA;
}

static void update_slider_label(AppState* app, SliderUI* slider) {
	if (!slider || !slider->value) {
		return;
	}

	double v = slider_get_value(slider);
	if (slider_is_theta(slider)) {
		double deg = v * 180.0 / kPi;
		wchar_t wtext[160];
		swprintf(wtext, sizeof(wtext) / sizeof(wtext[0]), L"%.4f rad (%.2f deg)", v, deg);
		SetWindowTextW(slider->value, wtext);
		return;
	} else {
		wchar_t wtext[160];
		swprintf(wtext, sizeof(wtext) / sizeof(wtext[0]), L"%.4f kg/s (%.4f bc)", v, v / app->bc);
		SetWindowTextW(slider->value, wtext);
		return;
	}
}

static void update_slider_edit(const SliderUI* slider) {
	if (!slider || !slider->input) {
		return;
	}

	wchar_t text[64];
	double v = slider_get_value(slider);
	swprintf(text, sizeof(text) / sizeof(text[0]), L"%.4f", v);
	SetWindowTextW(slider->input, text);
}

static void refresh_slider_ui(AppState* app, SliderUI* slider, bool refresh_edit_text) {
	if (!slider) {
		return;
	}
	update_slider_label(app, slider);
	if (refresh_edit_text) {
		update_slider_edit(slider);
	}
}

static void refresh_all_slider_ui(AppState* app, bool refresh_edit_text) {
	for (int i = 0; i < kSliderCount; ++i) {
		refresh_slider_ui(app, &app->sliders[i], refresh_edit_text);
	}
}

static void sync_model_from_controls(AppState* app) {
	app->states[0].b = slider_get_value(slider_by_id(app, IDC_SLIDER_B0));
	app->states[1].b = slider_get_value(slider_by_id(app, IDC_SLIDER_B1));
	app->states[2].b = slider_get_value(slider_by_id(app, IDC_SLIDER_B2));
	app->states[3].b = slider_get_value(slider_by_id(app, IDC_SLIDER_B3));
	app->theta0 = slider_get_value(slider_by_id(app, IDC_SLIDER_THETA));
	refresh_all_slider_ui(app, true);
}

static bool try_apply_slider_input(AppState* app, SliderUI* slider) {
	if (!slider || !slider->input) {
		return false;
	}

	wchar_t text[128];
	GetWindowTextW(slider->input, text, (int)(sizeof(text) / sizeof(text[0])));

	double v = 0.0;
	if (!parse_double_strict(text, &v)) {
		refresh_slider_ui(app, slider, true);
		return false;
	}

	v = std::max(slider->min_value, std::min(v, slider->max_value));
	app->slider_update_guard = true;
	slider_set_value(slider, v);
	app->slider_update_guard = false;

	refresh_slider_ui(app, slider, true);
	return true;
}

static bool apply_all_text_inputs(AppState* app) {
	bool changed_any = false;
	for (int i = 0; i < kSliderCount; ++i) {
		if (try_apply_slider_input(app, &app->sliders[i])) {
			changed_any = true;
		}
	}

	sync_model_from_controls(app);
	reset_simulation(app);
	return changed_any;
}

static void reset_simulation(AppState* app) {
	app->sim_time = 0.0;
	app->accumulator = 0.0;

	for (int i = 0; i < kCaseCount; ++i) {
		app->states[i].state.theta = app->theta0;
		app->states[i].state.omega = 0.0;
		trail_reset(&app->states[i].trail);

		double x = 0.0;
		double y = 0.0;
		world_to_bob(app, app->states[i].state.theta, &x, &y);
		trail_push(&app->states[i].trail, x, y);
	}
}

static void destroy_backbuffer(BackBuffer* back) {
	if (back->dc) {
		SelectObject(back->dc, back->old_bitmap);
		DeleteObject(back->bitmap);
		DeleteDC(back->dc);
	}
	back->dc = NULL;
	back->bitmap = NULL;
	back->old_bitmap = NULL;
	back->width = 0;
	back->height = 0;
}

static void ensure_backbuffer(AppState* app, HDC target, int width, int height) {
	BackBuffer* back = &app->back;

	if (width <= 0 || height <= 0) {
		return;
	}

	int buffer_w = width * kRenderSupersampleScale;
	int buffer_h = height * kRenderSupersampleScale;

	if (back->dc && back->width == buffer_w && back->height == buffer_h) {
		return;
	}

	destroy_backbuffer(back);

	back->dc = CreateCompatibleDC(target);
	if (!back->dc) {
		return;
	}

	back->bitmap = CreateCompatibleBitmap(target, buffer_w, buffer_h);
	if (!back->bitmap) {
		buffer_w = width;
		buffer_h = height;
		back->bitmap = CreateCompatibleBitmap(target, buffer_w, buffer_h);
	}

	if (!back->bitmap) {
		DeleteDC(back->dc);
		back->dc = NULL;
		return;
	}

	back->old_bitmap = (HBITMAP)SelectObject(back->dc, back->bitmap);
	back->width = buffer_w;
	back->height = buffer_h;
}

static void compute_scene_layout(
	const AppState* app,
	int width,
	int height,
	RECT* sim_area,
	RECT* ctrl_area,
	int* pivot_x,
	int* pivot_y,
	double* scale
) {
	int outer = 12;
	int panel_w = kControlPanelWidth;
	int top = outer + kHeaderHeight;
	int sim_right = std::max(outer + 280, width - panel_w - outer - 10);
	int ctrl_left = sim_right + 10;

	RECT sim = { outer, top, sim_right, height - outer };
	RECT ctrl = { ctrl_left, top, width - outer, height - outer };

	if (sim_area) {
		*sim_area = sim;
	}
	if (ctrl_area) {
		*ctrl_area = ctrl;
	}

	if (pivot_x) {
		*pivot_x = (sim.left + sim.right) / 2;
	}
	if (pivot_y) {
		*pivot_y = sim.top + 170;
	}
	if (scale) {
		double usable_w = (double)(sim.right - sim.left);
		double usable_h = (double)(sim.bottom - sim.top);
		double pend_px = std::min(usable_w * 0.34, usable_h * 0.56);
		*scale = pend_px / app->L;
	}
}

static bool point_in_rect_int(const RECT* rc, int x, int y) {
	if (!rc) {
		return false;
	}
	return x >= rc->left && x < rc->right && y >= rc->top && y < rc->bottom;
}

static void set_theta_from_direct(AppState* app, double theta) {
	SliderUI* theta_slider = slider_by_id(app, IDC_SLIDER_THETA);
	if (!theta_slider) {
		return;
	}

	double clamped = std::max(theta_slider->min_value, std::min(theta, theta_slider->max_value));
	app->slider_update_guard = true;
	slider_set_value(theta_slider, clamped);
	app->slider_update_guard = false;

	sync_model_from_controls(app);
	reset_simulation(app);
}

static bool hit_direct_drag_target(AppState* app, int mouse_x, int mouse_y) {
	RECT client;
	GetClientRect(app->window, &client);

	RECT sim_area;
	int pivot_x = 0;
	int pivot_y = 0;
	double scale = 1.0;
	compute_scene_layout(app, client.right, client.bottom, &sim_area, NULL, &pivot_x, &pivot_y, &scale);

	if (!point_in_rect_int(&sim_area, mouse_x, mouse_y)) {
		return false;
	}

	for (int i = 0; i < kCaseCount; ++i) {
		double x = 0.0;
		double y = 0.0;
		world_to_bob(app, app->states[i].state.theta, &x, &y);
		int bx = pivot_x + (int)lround(x * scale);
		int by = pivot_y + (int)lround(y * scale);
		int dx = mouse_x - bx;
		int dy = mouse_y - by;
		if (dx * dx + dy * dy <= 22 * 22) {
			return true;
		}
	}

	int dx = mouse_x - pivot_x;
	int dy = mouse_y - pivot_y;
	double dist = sqrt((double)dx * (double)dx + (double)dy * (double)dy);
	double radius = app->L * scale;
	if (dy >= -8 && fabs(dist - radius) <= 20.0) {
		return true;
	}

	return false;
}

static void update_theta_from_mouse(AppState* app, int mouse_x, int mouse_y) {
	RECT client;
	GetClientRect(app->window, &client);

	int pivot_x = 0;
	int pivot_y = 0;
	compute_scene_layout(app, client.right, client.bottom, NULL, NULL, &pivot_x, &pivot_y, NULL);

	double dx = (double)mouse_x - (double)pivot_x;
	double dy = (double)mouse_y - (double)pivot_y;
	if (fabs(dx) < 0.5 && fabs(dy) < 0.5) {
		return;
	}

	double theta = atan2(dx, dy);
	set_theta_from_direct(app, theta);
}

static void layout_controls(AppState* app, int width, int height) {
	int outer = 12;
	int panel_w = kControlPanelWidth;
	int panel_x = std::max(0, width - panel_w);
	int panel_top = outer + kHeaderHeight;

	int x = panel_x + 20;
	int y = panel_top + 68;

	int button_w = (panel_w - 40 - 16) / 3;
	int button_h = 34;
	MoveWindow(app->button_toggle, x, y, button_w, button_h, TRUE);
	MoveWindow(app->button_reset, x + button_w + 8, y, button_w, button_h, TRUE);
	MoveWindow(app->button_apply, x + (button_w + 8) * 2, y, button_w, button_h, TRUE);
	y += button_h + 12;

	MoveWindow(app->hint_text, x, y, panel_w - 40, 54, TRUE);
	y += 64;

	int value_w = 176;
	int input_w = 96;
	int track_w = panel_w - 40 - value_w - input_w - 18;
	track_w = std::max(track_w, 90);

	for (int i = 0; i < kSliderCount; ++i) {
		SliderUI* s = &app->sliders[i];
		MoveWindow(s->label, x, y, panel_w - 40, 20, TRUE);
		y += 24;
		MoveWindow(s->track, x, y, track_w, 30, TRUE);
		MoveWindow(s->value, x + track_w + 8, y + 5, value_w, 20, TRUE);
		MoveWindow(s->input, x + track_w + 8 + value_w + 10, y + 3, input_w, 24, TRUE);
		y += 46;
	}

	(void)height;
}

static void raise_control(HWND hwnd) {
	if (!hwnd) {
		return;
	}
	SetWindowPos(hwnd, HWND_TOP, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE);
}

static void bring_controls_to_front(AppState* app) {
	raise_control(app->button_toggle);
	raise_control(app->button_reset);
	raise_control(app->button_apply);
	raise_control(app->hint_text);

	for (int i = 0; i < kSliderCount; ++i) {
		raise_control(app->sliders[i].label);
		raise_control(app->sliders[i].track);
		raise_control(app->sliders[i].value);
		raise_control(app->sliders[i].input);
	}
}

static void exclude_control_rect(HWND parent, HDC dc, HWND child) {
	if (!child || !IsWindowVisible(child)) {
		return;
	}

	RECT rc;
	if (!GetWindowRect(child, &rc)) {
		return;
	}
	MapWindowPoints(NULL, parent, (LPPOINT)&rc, 2);
	ExcludeClipRect(dc, rc.left, rc.top, rc.right, rc.bottom);
}

static void exclude_controls_from_dc(AppState* app, HDC dc) {
	exclude_control_rect(app->window, dc, app->button_toggle);
	exclude_control_rect(app->window, dc, app->button_reset);
	exclude_control_rect(app->window, dc, app->button_apply);
	exclude_control_rect(app->window, dc, app->hint_text);

	for (int i = 0; i < kSliderCount; ++i) {
		exclude_control_rect(app->window, dc, app->sliders[i].label);
		exclude_control_rect(app->window, dc, app->sliders[i].track);
		exclude_control_rect(app->window, dc, app->sliders[i].value);
		exclude_control_rect(app->window, dc, app->sliders[i].input);
	}
}

static void create_controls(AppState* app) {
	app->ui_font = CreateFontA(
		-17,
		0,
		0,
		0,
		FW_NORMAL,
		FALSE,
		FALSE,
		FALSE,
		DEFAULT_CHARSET,
		OUT_DEFAULT_PRECIS,
		CLIP_DEFAULT_PRECIS,
		CLEARTYPE_QUALITY,
		DEFAULT_PITCH | FF_DONTCARE,
		"Segoe UI"
	);

	app->button_toggle = CreateWindowExW(
		0,
		L"BUTTON",
		L"开始",
		WS_CHILD | WS_VISIBLE | WS_TABSTOP | BS_OWNERDRAW,
		0,
		0,
		0,
		0,
		app->window,
		(HMENU)(INT_PTR)IDC_BTN_TOGGLE,
		GetModuleHandleW(NULL),
		NULL
	);

	app->button_reset = CreateWindowExW(
		0,
		L"BUTTON",
		L"重置",
		WS_CHILD | WS_VISIBLE | WS_TABSTOP | BS_OWNERDRAW,
		0,
		0,
		0,
		0,
		app->window,
		(HMENU)(INT_PTR)IDC_BTN_RESET,
		GetModuleHandleW(NULL),
		NULL
	);

	app->button_apply = CreateWindowExW(
		0,
		L"BUTTON",
		L"应用",
		WS_CHILD | WS_VISIBLE | WS_TABSTOP | BS_OWNERDRAW,
		0,
		0,
		0,
		0,
		app->window,
		(HMENU)(INT_PTR)IDC_BTN_APPLY,
		GetModuleHandleW(NULL),
		NULL
	);

	app->hint_text = CreateWindowExW(
		0,
		L"STATIC",
		L"直接操作：拖动摆球调角度；鼠标滚轮微调，Shift 可精调。",
		WS_CHILD | WS_VISIBLE,
		0,
		0,
		0,
		0,
		app->window,
		NULL,
		GetModuleHandleW(NULL),
		NULL
	);

	const int ids[kSliderCount] = {
		IDC_SLIDER_B0,
		IDC_SLIDER_B1,
		IDC_SLIDER_B2,
		IDC_SLIDER_B3,
		IDC_SLIDER_THETA
	};

	const int edit_ids[kSliderCount] = {
		IDC_EDIT_B0,
		IDC_EDIT_B1,
		IDC_EDIT_B2,
		IDC_EDIT_B3,
		IDC_EDIT_THETA
	};

	const wchar_t* titles[kSliderCount] = {
		L"无阻尼 b0 (kg/s)",
		L"欠阻尼 b1 (kg/s)",
		L"临界附近 b2 (kg/s)",
		L"过阻尼 b3 (kg/s)",
		L"初始角度 theta0 (rad)"
	};

	const double mins[kSliderCount] = {
		0.0,
		0.0,
		0.0,
		0.0,
		-0.80
	};

	const double maxs[kSliderCount] = {
		4.0 * app->bc,
		4.0 * app->bc,
		4.0 * app->bc,
		4.0 * app->bc,
		0.80
	};

	for (int i = 0; i < kSliderCount; ++i) {
		SliderUI* s = &app->sliders[i];
		s->id = ids[i];
		s->edit_id = edit_ids[i];
		s->title = titles[i];
		s->min_value = mins[i];
		s->max_value = maxs[i];

		s->label = CreateWindowExW(
			0,
			L"STATIC",
			s->title,
			WS_CHILD | WS_VISIBLE,
			0,
			0,
			0,
			0,
			app->window,
			NULL,
			GetModuleHandleW(NULL),
			NULL
		);

		s->track = CreateWindowExW(
			0,
			TRACKBAR_CLASSW,
			L"",
			WS_CHILD | WS_VISIBLE | TBS_HORZ,
			0,
			0,
			0,
			0,
			app->window,
			(HMENU)(INT_PTR)s->id,
			GetModuleHandleW(NULL),
			NULL
		);

		s->value = CreateWindowExW(
			0,
			L"STATIC",
			L"",
			WS_CHILD | WS_VISIBLE | SS_RIGHT,
			0,
			0,
			0,
			0,
			app->window,
			NULL,
			GetModuleHandleW(NULL),
			NULL
		);

		s->input = CreateWindowExW(
			WS_EX_CLIENTEDGE,
			L"EDIT",
			L"",
			WS_CHILD | WS_VISIBLE | ES_AUTOHSCROLL | ES_RIGHT,
			0,
			0,
			0,
			0,
			app->window,
			(HMENU)(INT_PTR)s->edit_id,
			GetModuleHandleW(NULL),
			NULL
		);

		SendMessageW(s->input, EM_LIMITTEXT, 24, 0);

		SendMessageA(s->track, TBM_SETRANGE, TRUE, MAKELONG(0, kSliderResolution));
		SendMessageA(s->track, TBM_SETPAGESIZE, 0, 70);
		SendMessageA(s->track, TBM_SETLINESIZE, 0, 12);
	}

	set_control_font(app->button_toggle, app->ui_font);
	set_control_font(app->button_reset, app->ui_font);
	set_control_font(app->button_apply, app->ui_font);
	set_control_font(app->hint_text, app->ui_font);
	for (int i = 0; i < kSliderCount; ++i) {
		set_control_font(app->sliders[i].label, app->ui_font);
		set_control_font(app->sliders[i].value, app->ui_font);
		set_control_font(app->sliders[i].input, app->ui_font);
	}

	app->slider_update_guard = true;
	slider_set_value(slider_by_id(app, IDC_SLIDER_B0), app->states[0].b);
	slider_set_value(slider_by_id(app, IDC_SLIDER_B1), app->states[1].b);
	slider_set_value(slider_by_id(app, IDC_SLIDER_B2), app->states[2].b);
	slider_set_value(slider_by_id(app, IDC_SLIDER_B3), app->states[3].b);
	slider_set_value(slider_by_id(app, IDC_SLIDER_THETA), app->theta0);
	app->slider_update_guard = false;

	sync_model_from_controls(app);
}

static void update_simulation(AppState* app, double frame_dt) {
	if (!app->running) {
		return;
	}

	if (frame_dt < 0.0) {
		frame_dt = 0.0;
	}
	if (frame_dt > 0.05) {
		frame_dt = 0.05;
	}

	app->accumulator += frame_dt;

	while (app->accumulator >= kFixedDt) {
		for (int i = 0; i < kCaseCount; ++i) {
			DampingState* st = &app->states[i];
			double gamma = st->b / app->m;
			rk4_step(&st->state, kFixedDt, gamma, app->g / app->L);

			double x = 0.0;
			double y = 0.0;
			world_to_bob(app, st->state.theta, &x, &y);
			trail_push(&st->trail, x, y);
		}

		app->sim_time += kFixedDt;
		app->accumulator -= kFixedDt;
	}
}

static void render_scene(AppState* app, HDC dc, int width, int height) {
	RECT full = { 0, 0, width, height };
	fill_rect(dc, &full, RGB(248, 249, 250));

	RECT sim_area;
	RECT ctrl_area;
	int pivot_x = 0;
	int pivot_y = 0;
	double scale = 1.0;
	compute_scene_layout(app, width, height, &sim_area, &ctrl_area, &pivot_x, &pivot_y, &scale);

	SetBkMode(dc, TRANSPARENT);
	if (app->ui_font) {
		SelectObject(dc, app->ui_font);
	}
	draw_text(dc, 22, 18, RGB(32, 33, 36), "Damped Pendulum Playground");
	draw_text(dc, 22, 40, RGB(95, 99, 104), "四种阻尼状态并行动画与参数探索（C++ 交互版）");

	RECT sim_shadow = sim_area;
	RECT ctrl_shadow = ctrl_area;
	OffsetRect(&sim_shadow, 1, 1);
	OffsetRect(&ctrl_shadow, 1, 1);
	draw_round_card(dc, &sim_shadow, RGB(241, 243, 244), RGB(241, 243, 244));
	draw_round_card(dc, &ctrl_shadow, RGB(241, 243, 244), RGB(241, 243, 244));
	draw_round_card(dc, &sim_area, RGB(255, 255, 255), RGB(218, 220, 224));
	draw_round_card(dc, &ctrl_area, RGB(255, 255, 255), RGB(218, 220, 224));

	RECT ctrl_info = { ctrl_area.left + 12, ctrl_area.bottom - 152, ctrl_area.right - 12, ctrl_area.bottom - 12 };
	draw_round_card(dc, &ctrl_info, RGB(241, 243, 244), RGB(218, 220, 224));

	draw_line(dc, sim_area.left + 14, sim_area.top + 56, sim_area.right - 14, sim_area.top + 56, RGB(232, 234, 237), 1);
	draw_line(dc, ctrl_area.left + 14, ctrl_area.top + 56, ctrl_area.right - 14, ctrl_area.top + 56, RGB(232, 234, 237), 1);

	draw_text(dc, sim_area.left + 18, sim_area.top + 16, RGB(32, 33, 36), "四状态单摆叠加动画（同一支点）");
	draw_text(dc, sim_area.left + 18, sim_area.top + 36, RGB(95, 99, 104), "Fixed-step integration + 低延迟渲染");
	draw_text(dc, ctrl_area.left + 18, ctrl_area.top + 16, RGB(32, 33, 36), "参数控制面板");
	draw_text(dc, ctrl_area.left + 18, ctrl_area.top + 36, RGB(95, 99, 104), "拖拽、滚轮与精确输入可同时使用");

	char status[180];
	const char* state_text = app->running ? "运行中" : "已暂停";
	snprintf(
		status,
		sizeof(status),
		"time = %.2f s   state = %s   fixed dt = %.4f s",
		app->sim_time,
		state_text,
		kFixedDt
	);
	draw_text(dc, sim_area.left + 18, sim_area.top + 66, RGB(26, 115, 232), status);

	int grid_left = sim_area.left + 20;
	int grid_right = sim_area.right - 20;
	int grid_top = sim_area.top + 84;
	int grid_bottom = sim_area.bottom - 58;
	for (int i = 1; i <= 4; ++i) {
		int gx = grid_left + (grid_right - grid_left) * i / 5;
		draw_line(dc, gx, grid_top, gx, grid_bottom, RGB(232, 234, 237), 1);
	}
	for (int i = 1; i <= 3; ++i) {
		int gy = grid_top + (grid_bottom - grid_top) * i / 4;
		draw_line(dc, grid_left, gy, grid_right, gy, RGB(232, 234, 237), 1);
	}

	draw_line(dc, pivot_x - 80, pivot_y - 2, pivot_x + 80, pivot_y - 2, RGB(95, 99, 104), 4);
	draw_line(dc, pivot_x, pivot_y - 2, pivot_x, pivot_y + (int)lround(app->L * scale), RGB(226, 232, 240), 1);

	for (int i = 0; i < kCaseCount; ++i) {
		const DampingState* st = &app->states[i];
		if (st->trail.size > 1) {
			POINT pts[kTrailCap];
			for (int p = 0; p < st->trail.size; ++p) {
				int idx = (st->trail.head + p) % kTrailCap;
				pts[p].x = pivot_x + (int)lround(st->trail.x[idx] * scale);
				pts[p].y = pivot_y + (int)lround(st->trail.y[idx] * scale);
			}

			HPEN trace_pen = CreatePen(PS_SOLID, 1, lighten(st->color, 90));
			HPEN old_pen = (HPEN)SelectObject(dc, trace_pen);
			Polyline(dc, pts, st->trail.size);
			SelectObject(dc, old_pen);
			DeleteObject(trace_pen);
		}
	}

	for (int i = 0; i < kCaseCount; ++i) {
		const DampingState* st = &app->states[i];
		double x = 0.0;
		double y = 0.0;
		world_to_bob(app, st->state.theta, &x, &y);
		int bx = pivot_x + (int)lround(x * scale);
		int by = pivot_y + (int)lround(y * scale);

		draw_line(dc, pivot_x, pivot_y, bx, by, st->color, 2);

		HBRUSH brush = CreateSolidBrush(st->color);
		HBRUSH old_brush = (HBRUSH)SelectObject(dc, brush);
		HPEN pen = CreatePen(PS_SOLID, 1, RGB(255, 255, 255));
		HPEN old_pen = (HPEN)SelectObject(dc, pen);
		Ellipse(dc, bx - 8, by - 8, bx + 8, by + 8);
		SelectObject(dc, old_pen);
		SelectObject(dc, old_brush);
		DeleteObject(pen);
		DeleteObject(brush);
	}

	RECT legend_box = { sim_area.left + 18, sim_area.top + 92, sim_area.left + 482, sim_area.top + 206 };
	draw_round_card(dc, &legend_box, RGB(241, 243, 244), RGB(218, 220, 224));

	char line[200];
	for (int i = 0; i < kCaseCount; ++i) {
		int y = legend_box.top + 11 + i * 24;
		draw_line(dc, legend_box.left + 10, y + 7, legend_box.left + 30, y + 7, app->states[i].color, 3);
		snprintf(
			line,
			sizeof(line),
			"%s: b = %.4f kg/s (%.4f bc)",
			app->states[i].name,
			app->states[i].b,
			app->states[i].b / app->bc
		);
		draw_text(dc, legend_box.left + 38, y, RGB(60, 64, 67), line);
	}

	snprintf(line, sizeof(line), "bc = %.4f kg/s, theta0 = %.4f rad", app->bc, app->theta0);
	draw_text(dc, sim_area.left + 18, sim_area.bottom - 38, RGB(26, 115, 232), line);
	draw_text(dc, sim_area.left + 18, sim_area.bottom - 18, RGB(95, 99, 104), "提示：可直接拖拽摆球；滚轮微调 theta0，按住 Shift 进行精调。 ");

	draw_text(dc, ctrl_info.left + 14, ctrl_info.top + 12, RGB(32, 33, 36), "操作提示");
	draw_text(dc, ctrl_info.left + 14, ctrl_info.top + 36, RGB(95, 99, 104), "1) 点击“开始”播放，点击“重置”回到 t=0。 ");
	draw_text(dc, ctrl_info.left + 14, ctrl_info.top + 58, RGB(95, 99, 104), "2) 支持拖动滑块和输入框精确改值。 ");
	draw_text(dc, ctrl_info.left + 14, ctrl_info.top + 80, RGB(95, 99, 104), "3) 在左侧画布拖摆球可直接设初始角度。 ");
	draw_text(dc, ctrl_info.left + 14, ctrl_info.top + 102, RGB(95, 99, 104), "4) 鼠标滚轮调角度，Shift 为更细步长。 ");
}

static void render_frame(AppState* app, HDC target, int width, int height) {
	ensure_backbuffer(app, target, width, height);
	if (!app->back.dc) {
		return;
	}

	int back_saved = SaveDC(app->back.dc);
	SetMapMode(app->back.dc, MM_ANISOTROPIC);
	SetWindowExtEx(app->back.dc, width, height, NULL);
	SetViewportExtEx(app->back.dc, app->back.width, app->back.height, NULL);
	render_scene(app, app->back.dc, width, height);
	RestoreDC(app->back.dc, back_saved);

	int saved = SaveDC(target);
	exclude_controls_from_dc(app, target);

	if (app->back.width == width && app->back.height == height) {
		BitBlt(target, 0, 0, width, height, app->back.dc, 0, 0, SRCCOPY);
	} else {
		SetStretchBltMode(target, HALFTONE);
		SetBrushOrgEx(target, 0, 0, NULL);
		StretchBlt(target, 0, 0, width, height, app->back.dc, 0, 0, app->back.width, app->back.height, SRCCOPY);
	}

	RestoreDC(target, saved);
}

static LRESULT CALLBACK window_proc(HWND hwnd, UINT msg, WPARAM wparam, LPARAM lparam) {
	AppState* app = &g_app;

	switch (msg) {
	case WM_CREATE: {
		app->window = hwnd;
		create_controls(app);

		RECT rc;
		GetClientRect(hwnd, &rc);
		layout_controls(app, rc.right, rc.bottom);
		bring_controls_to_front(app);
		reset_simulation(app);
		return 0;
	}

	case WM_SIZE: {
		int width = LOWORD(lparam);
		int height = HIWORD(lparam);
		layout_controls(app, width, height);
		bring_controls_to_front(app);
		return 0;
	}

	case WM_GETMINMAXINFO: {
		MINMAXINFO* info = (MINMAXINFO*)lparam;
			   info->ptMinTrackSize.x = 1440; // 提高最小宽度
			   info->ptMinTrackSize.y = 900;  // 提高最小高度
		return 0;
	}

	case WM_COMMAND: {
		int id = LOWORD(wparam);
		int code = HIWORD(wparam);
		HWND source = (HWND)lparam;

		if (id == IDC_BTN_TOGGLE) {
			app->running = !app->running;
			SetWindowTextW(app->button_toggle, app->running ? L"暂停" : L"开始");
			return 0;
		}
		if (id == IDC_BTN_RESET) {
			apply_all_text_inputs(app);
			return 0;
		}
		if (id == IDC_BTN_APPLY) {
			apply_all_text_inputs(app);
			return 0;
		}

		SliderUI* edit_slider = slider_by_edit(app, source);
		if (!edit_slider) {
			break;
		}

		if (code == EN_KILLFOCUS) {
			try_apply_slider_input(app, edit_slider);
			sync_model_from_controls(app);
			reset_simulation(app);
			return 0;
		}

		if (code == EN_UPDATE) {
			update_slider_label(app, edit_slider);
			return 0;
		}

		if (code == EN_CHANGE) {
			return 0;
		}

		if (code == EN_SETFOCUS) {
			if (edit_slider->input) {
				SendMessageW(edit_slider->input, EM_SETSEL, 0, -1);
			}
			return 0;
		}
		break;
	}

	case WM_HSCROLL: {
		HWND track = (HWND)lparam;
		SliderUI* slider = slider_by_track(app, track);
		if (slider) {
			refresh_slider_ui(app, slider, true);
			if (!app->slider_update_guard) {
				sync_model_from_controls(app);
				reset_simulation(app);
			}
			return 0;
		}
		break;
	}

	case WM_LBUTTONDOWN: {
		int mouse_x = (int)(short)LOWORD(lparam);
		int mouse_y = (int)(short)HIWORD(lparam);
		if (hit_direct_drag_target(app, mouse_x, mouse_y)) {
			app->dragging_theta = true;
			app->resume_after_drag = false;
			if (app->running) {
				app->running = false;
				app->resume_after_drag = true;
				SetWindowTextW(app->button_toggle, L"开始");
			}
			SetFocus(hwnd);
			SetCapture(hwnd);
			update_theta_from_mouse(app, mouse_x, mouse_y);
			return 0;
		}
		break;
	}

	case WM_MOUSEMOVE: {
		if (app->dragging_theta) {
			int mouse_x = (int)(short)LOWORD(lparam);
			int mouse_y = (int)(short)HIWORD(lparam);
			update_theta_from_mouse(app, mouse_x, mouse_y);
			return 0;
		}
		break;
	}

	case WM_LBUTTONUP: {
		if (app->dragging_theta) {
			int mouse_x = (int)(short)LOWORD(lparam);
			int mouse_y = (int)(short)HIWORD(lparam);
			update_theta_from_mouse(app, mouse_x, mouse_y);
			app->dragging_theta = false;
			ReleaseCapture();
			if (app->resume_after_drag) {
				app->resume_after_drag = false;
				app->running = true;
				SetWindowTextW(app->button_toggle, L"暂停");
			}
			return 0;
		}
		break;
	}

	case WM_CAPTURECHANGED: {
		if (app->dragging_theta) {
			app->dragging_theta = false;
			if (app->resume_after_drag) {
				app->resume_after_drag = false;
				app->running = true;
				SetWindowTextW(app->button_toggle, L"暂停");
			}
		}
		break;
	}

	case WM_MOUSEWHEEL: {
		POINT pt;
		pt.x = (int)(short)LOWORD(lparam);
		pt.y = (int)(short)HIWORD(lparam);
		ScreenToClient(hwnd, &pt);

		RECT client;
		GetClientRect(hwnd, &client);
		RECT sim_area;
		compute_scene_layout(app, client.right, client.bottom, &sim_area, NULL, NULL, NULL, NULL);
		if (point_in_rect_int(&sim_area, pt.x, pt.y)) {
			double ticks = (double)GET_WHEEL_DELTA_WPARAM(wparam) / (double)WHEEL_DELTA;
			double step = (GET_KEYSTATE_WPARAM(wparam) & MK_SHIFT) ? 0.005 : 0.02;
			if (fabs(ticks) > 0.0) {
				set_theta_from_direct(app, app->theta0 + ticks * step);
			}
			return 0;
		}
		break;
	}

	case WM_DRAWITEM: {
		DRAWITEMSTRUCT* dis = (DRAWITEMSTRUCT*)lparam;
		if (!dis || dis->CtlType != ODT_BUTTON) {
			break;
		}

		switch (dis->CtlID) {
		case IDC_BTN_TOGGLE:
			if (app->running) {
				draw_button_ownerdraw(app, dis, RGB(234, 67, 53), RGB(217, 48, 37), RGB(255, 255, 255));
			} else {
				draw_button_ownerdraw(app, dis, RGB(26, 115, 232), RGB(25, 103, 210), RGB(255, 255, 255));
			}
			return TRUE;

		case IDC_BTN_APPLY:
			draw_button_ownerdraw(app, dis, RGB(52, 168, 83), RGB(44, 145, 72), RGB(255, 255, 255));
			return TRUE;

		case IDC_BTN_RESET:
			draw_button_ownerdraw(app, dis, RGB(255, 255, 255), RGB(218, 220, 224), RGB(60, 64, 67));
			return TRUE;

		default:
			break;
		}
		break;
	}

	case WM_CTLCOLORSTATIC: {
		static HBRUSH panel_brush = CreateSolidBrush(RGB(255, 255, 255));
		HDC hdc = (HDC)wparam;
		HWND ctrl = (HWND)lparam;
		SetBkMode(hdc, OPAQUE);
		SetBkColor(hdc, RGB(255, 255, 255));
		if (ctrl == app->hint_text) {
			SetTextColor(hdc, RGB(95, 99, 104));
		} else {
			SetTextColor(hdc, RGB(60, 64, 67));
		}
		return (LRESULT)panel_brush;
	}

	case WM_CTLCOLOREDIT: {
		static HBRUSH edit_brush = CreateSolidBrush(RGB(255, 255, 255));
		HDC hdc = (HDC)wparam;
		SetTextColor(hdc, RGB(32, 33, 36));
		SetBkColor(hdc, RGB(255, 255, 255));
		return (LRESULT)edit_brush;
	}

	case WM_ERASEBKGND:
		return 1;

	case WM_PAINT: {
		PAINTSTRUCT ps;
		HDC hdc = BeginPaint(hwnd, &ps);
		RECT rc;
		GetClientRect(hwnd, &rc);
		render_frame(app, hdc, rc.right, rc.bottom);
		EndPaint(hwnd, &ps);
		return 0;
	}

	case WM_DESTROY:
		destroy_backbuffer(&app->back);
		if (app->ui_font) {
			DeleteObject(app->ui_font);
			app->ui_font = NULL;
		}
		PostQuitMessage(0);
		return 0;
	}

	return DefWindowProcA(hwnd, msg, wparam, lparam);
}

static void init_defaults(AppState* app) {
	app->m = 1.0;
	app->L = 1.0;
	app->g = 9.81;
	app->bc = 2.0 * app->m * sqrt(app->g / app->L);
	app->theta0 = 0.30;
	app->running = false;
	app->quit_requested = false;
	app->dragging_theta = false;
	app->resume_after_drag = false;
	app->sim_time = 0.0;
	app->accumulator = 0.0;

	app->states[0].name = "无阻尼";
	app->states[0].color = RGB(52, 168, 83);
	app->states[0].b = 0.0;

	app->states[1].name = "欠阻尼";
	app->states[1].color = RGB(26, 115, 232);
	app->states[1].b = 0.15 * app->bc;

	app->states[2].name = "临界阻尼";
	app->states[2].color = RGB(234, 67, 53);
	app->states[2].b = 1.00 * app->bc;

	app->states[3].name = "过阻尼";
	app->states[3].color = RGB(251, 188, 4);
	app->states[3].b = 3.00 * app->bc;

	for (int i = 0; i < kCaseCount; ++i) {
		app->states[i].state.theta = app->theta0;
		app->states[i].state.omega = 0.0;
		trail_reset(&app->states[i].trail);
	}
}

int WINAPI WinMain(HINSTANCE instance, HINSTANCE prev, LPSTR cmd, int show) {
	(void)prev;
	(void)cmd;

	INITCOMMONCONTROLSEX icc;
	icc.dwSize = sizeof(icc);
	icc.dwICC = ICC_BAR_CLASSES;
	InitCommonControlsEx(&icc);

	init_defaults(&g_app);

	WNDCLASSEXA wc;
	ZeroMemory(&wc, sizeof(wc));
	wc.cbSize = sizeof(wc);
	wc.lpfnWndProc = window_proc;
	wc.hInstance = instance;
	wc.lpszClassName = "DampedPendulumOverlayWindow";
	wc.hCursor = LoadCursor(NULL, IDC_ARROW);
	wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
	wc.style = CS_HREDRAW | CS_VREDRAW;

	if (!RegisterClassExA(&wc)) {
		MessageBoxA(NULL, "Failed to register window class.", "Error", MB_ICONERROR | MB_OK);
		return 1;
	}

	       HWND hwnd = CreateWindowExA(
		       0,
		       wc.lpszClassName,
		       "Damped Pendulum Playground (C++ Win32)",
		       WS_OVERLAPPEDWINDOW | WS_CLIPCHILDREN | WS_CLIPSIBLINGS,
		       CW_USEDEFAULT,
		       CW_USEDEFAULT,
		       1680, // 提高初始宽度
		       1080, // 提高初始高度
		       NULL,
		       NULL,
		       instance,
		       NULL
	       );

	if (!hwnd) {
		MessageBoxA(NULL, "Failed to create main window.", "Error", MB_ICONERROR | MB_OK);
		return 1;
	}

	ShowWindow(hwnd, show);
	UpdateWindow(hwnd);

	QueryPerformanceFrequency(&g_app.perf_freq);
	QueryPerformanceCounter(&g_app.last_tick);

	timeBeginPeriod(1);

	MSG msg;
	while (!g_app.quit_requested) {
		while (PeekMessageA(&msg, NULL, 0, 0, PM_REMOVE)) {
			if (msg.message == WM_QUIT) {
				g_app.quit_requested = true;
				break;
			}
			TranslateMessage(&msg);
			DispatchMessageA(&msg);
		}

		if (g_app.quit_requested) {
			break;
		}

		LARGE_INTEGER now;
		QueryPerformanceCounter(&now);

		double frame_dt = (double)(now.QuadPart - g_app.last_tick.QuadPart) / (double)g_app.perf_freq.QuadPart;
		g_app.last_tick = now;

		update_simulation(&g_app, frame_dt);

		if (!IsIconic(hwnd)) {
			RECT rc;
			GetClientRect(hwnd, &rc);
			if (rc.right > 0 && rc.bottom > 0) {
				HDC hdc = GetDC(hwnd);
				render_frame(&g_app, hdc, rc.right, rc.bottom);
				ReleaseDC(hwnd, hdc);
			}
		}

		Sleep(1);
	}

	timeEndPeriod(1);
	return 0;
}
