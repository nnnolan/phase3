import tkinter as tk
from tkinter import ttk
import io
import sys
import os
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(__file__))
from airplane import search_available_flights, make_reservation_and_book_ticket, view_itinerary

# ── palette ──────────────────────────────────────────────
NAVY      = "#003580"
NAVY_DARK = "#002060"
BLUE      = "#0057b7"
BLUE_HOV  = "#003da5"
BG        = "#f0f4f8"
CARD      = "#ffffff"
BORDER    = "#dde3ec"
TEXT      = "#1e293b"
MUTED     = "#64748b"
TERM_BG   = "#0f172a"
TERM_FG   = "#e2e8f0"
GREEN     = "#4ade80"
RED       = "#f87171"


class AirlineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SkyBook — Airline Portal")
        self.geometry("700x590")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._current_tab = None

        self._build_header()
        self._build_tabbar()
        self._build_content()
        self._build_output()
        self._switch("search")

    # ── header ───────────────────────────────────────────

    def _build_header(self):
        bar = tk.Frame(self, bg=NAVY, height=76)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        inner = tk.Frame(bar, bg=NAVY)
        inner.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(inner, text="✈", bg=NAVY, fg="white",
                 font=("Helvetica Neue", 30)).pack(side="left", padx=(0, 12))

        txt = tk.Frame(inner, bg=NAVY)
        txt.pack(side="left")
        tk.Label(txt, text="SKYBOOK", bg=NAVY, fg="white",
                 font=("Helvetica Neue", 22, "bold")).pack(anchor="w")
        tk.Label(txt, text="Airline Reservation Portal", bg=NAVY, fg="#93c5fd",
                 font=("Helvetica Neue", 9)).pack(anchor="w")

    # ── tab bar ──────────────────────────────────────────

    def _build_tabbar(self):
        self._tabbar = tk.Frame(self, bg=NAVY_DARK, height=42)
        self._tabbar.pack(fill="x")
        self._tabbar.pack_propagate(False)

        self._tab_btns = {}
        tabs = [
            ("search",    "✈   Search Flights"),
            ("book",      "🎫   Book Ticket"),
            ("itinerary", "📋   View Itinerary"),
        ]
        for key, label in tabs:
            btn = tk.Button(
                self._tabbar, text=label, bd=0, padx=22, pady=0,
                font=("Helvetica Neue", 10), cursor="hand2",
                command=lambda k=key: self._switch(k),
            )
            btn.pack(side="left", fill="y")
            self._tab_btns[key] = btn

    def _switch(self, key):
        if self._current_tab == key:
            return
        self._current_tab = key

        for k, btn in self._tab_btns.items():
            if k == key:
                btn.config(bg=BLUE, fg="white", font=("Helvetica Neue", 10, "bold"),
                           activebackground=BLUE_HOV, activeforeground="white")
            else:
                btn.config(bg=NAVY_DARK, fg="#93c5fd", font=("Helvetica Neue", 10),
                           activebackground=NAVY, activeforeground="white")

        for k, panel in self._panels.items():
            if k == key:
                panel.pack(fill="x")
            else:
                panel.pack_forget()

    # ── content area ─────────────────────────────────────

    def _build_content(self):
        self._content = tk.Frame(self, bg=BG)
        self._content.pack(fill="x", padx=24, pady=18)

        self._panels = {
            "search":    self._panel_search(),
            "book":      self._panel_book(),
            "itinerary": self._panel_itinerary(),
        }

    def _card(self, title):
        """Returns a white card frame with a titled header. Use the body frame for fields."""
        outer = tk.Frame(self._content, bg=BG)

        shadow = tk.Frame(outer, bg=BORDER)
        shadow.pack(fill="x", padx=1, pady=1)

        card = tk.Frame(shadow, bg=CARD)
        card.pack(fill="x", padx=1, pady=1)

        tk.Label(card, text=title, bg=CARD, fg=TEXT,
                 font=("Helvetica Neue", 13, "bold")).pack(anchor="w", padx=20, pady=(16, 0))
        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(10, 0))

        body = tk.Frame(card, bg=CARD)
        body.pack(fill="x", padx=20, pady=16)

        return outer, body

    def _field(self, parent, label, row, col, factory=None):
        """Labelled input cell for a grid parent."""
        cell = tk.Frame(parent, bg=CARD)
        cell.grid(row=row, column=col, sticky="nsew", padx=(0, 14), pady=6)
        cell.columnconfigure(0, weight=1)

        tk.Label(cell, text=label.upper(), bg=CARD, fg=MUTED,
                 font=("Helvetica Neue", 8, "bold")).pack(anchor="w")

        w = factory(cell) if factory else ttk.Entry(cell, font=("Helvetica Neue", 11))
        w.pack(fill="x", ipady=5, pady=(3, 0))
        return w

    def _btn(self, parent, text, cmd):
        return tk.Button(
            parent, text=text, command=cmd,
            bg=BLUE, fg="white", activebackground=BLUE_HOV, activeforeground="white",
            font=("Helvetica Neue", 11, "bold"), bd=0, padx=26, pady=9,
            cursor="hand2", relief="flat",
        )

    # ── panels ───────────────────────────────────────────

    def _panel_search(self):
        outer, body = self._card("Search Available Flights")
        body.columnconfigure((0, 1), weight=1)

        self.s_dep  = self._field(body, "Departure (IATA code)", 0, 0)
        self.s_arr  = self._field(body, "Arrival (IATA code)",   0, 1)
        self.s_date = self._field(body, "Travel date (YYYY-MM-DD)", 1, 0)

        f = tk.Frame(body, bg=CARD)
        f.grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self._btn(f, "Search Flights  →", self._do_search).pack(side="left")
        return outer

    def _panel_book(self):
        outer, body = self._card("Book a Ticket")
        body.columnconfigure((0, 1), weight=1)

        self.b_passport = self._field(body, "Passport ID",    0, 0)
        self.b_flight   = self._field(body, "Flight ID",      0, 1)
        self.b_method   = self._field(body, "Payment method", 1, 0,
            factory=lambda p: ttk.Combobox(
                p, values=["Credit Card", "Debit Card", "Cash"],
                state="readonly", font=("Helvetica Neue", 11),
            ))
        self.b_method.set("Credit Card")

        f = tk.Frame(body, bg=CARD)
        f.grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self._btn(f, "Book Ticket  →", self._do_book).pack(side="left")
        return outer

    def _panel_itinerary(self):
        outer, body = self._card("View Itinerary")
        body.columnconfigure(0, weight=1)

        self.i_res = self._field(body, "Reservation ID", 0, 0)

        f = tk.Frame(body, bg=CARD)
        f.grid(row=1, column=0, sticky="w", pady=(10, 0))
        self._btn(f, "View Itinerary  →", self._do_itinerary).pack(side="left")
        return outer

    # ── output ───────────────────────────────────────────

    def _build_output(self):
        wrapper = tk.Frame(self, bg=BG)
        wrapper.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        # label row
        lrow = tk.Frame(wrapper, bg=BG)
        lrow.pack(fill="x", pady=(0, 6))
        tk.Label(lrow, text="OUTPUT", bg=BG, fg=MUTED,
                 font=("Helvetica Neue", 8, "bold")).pack(side="left")
        self._dot = tk.Label(lrow, text="●", bg=BG, fg=BORDER,
                             font=("Helvetica Neue", 11))
        self._dot.pack(side="right")

        # terminal box
        box = tk.Frame(wrapper, bg=TERM_BG)
        box.pack(fill="both", expand=True)

        self._out = tk.Text(
            box, state="disabled", wrap="word",
            bg=TERM_BG, fg=TERM_FG,
            font=("Menlo", 10), bd=0, padx=16, pady=14,
            selectbackground=BLUE, insertbackground=TERM_FG,
        )
        sb = ttk.Scrollbar(box, command=self._out.yview)
        self._out.configure(yscrollcommand=sb.set)
        self._out.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

    def _show(self, text, ok=True):
        self._out.config(state="normal")
        self._out.delete("1.0", tk.END)
        self._out.insert(tk.END, text.strip() or "(no output returned)")
        self._out.config(state="disabled")
        self._dot.config(fg=GREEN if ok else RED)

    # ── actions ──────────────────────────────────────────

    def _call(self, func, *args):
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                func(*args)
            self._show(buf.getvalue(), ok=True)
        except Exception as e:
            self._show(f"Error: {e}", ok=False)

    def _do_search(self):
        self._call(search_available_flights,
                   self.s_dep.get(), self.s_arr.get(), self.s_date.get())

    def _do_book(self):
        self._call(make_reservation_and_book_ticket,
                   self.b_passport.get(), self.b_flight.get(), self.b_method.get())

    def _do_itinerary(self):
        self._call(view_itinerary, self.i_res.get())


if __name__ == "__main__":
    AirlineApp().mainloop()
