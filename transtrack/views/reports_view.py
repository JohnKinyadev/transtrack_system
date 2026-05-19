import tkinter as tk
from tkinter import ttk
from datetime import datetime

from bson import ObjectId

from transtrack.db.connection import get_db
from transtrack.utils.numbers import to_float
from transtrack.views import styles
from transtrack.views.lookups import display_value, label_for
from transtrack.views.widgets import configure_ttk_styles, format_id, make_table, metric_card


class ReportsView(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=styles.WHITE)
        self.db = get_db()
        self.build()

    def build(self):
        header = tk.Frame(self, bg=styles.WHITE)
        header.pack(fill="x", pady=(0, 12))
        tk.Label(
            header,
            text="System-wide detailed reports",
            bg=styles.WHITE,
            fg=styles.TEXT,
            font=styles.FONT_HEADING,
        ).pack(side="left", anchor="w")
        tk.Button(
            header,
            text="Refresh",
            command=self.refresh,
            bg=styles.PRIMARY,
            fg=styles.WHITE,
            activebackground=styles.PRIMARY_HOVER,
            activeforeground=styles.WHITE,
            relief="flat",
            padx=14,
            pady=7,
            cursor="hand2",
        ).pack(side="right")

        configure_ttk_styles()
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.overview_tab = self.scrollable_tab("Overview")
        self.operations_tab = self.scrollable_tab("Operations")
        self.financials_tab = self.scrollable_tab("Financials")
        self.assets_tab = self.scrollable_tab("People & Assets")
        self.audit_tab = self.scrollable_tab("Users & Audit")

        self.load_reports()

    def refresh(self):
        for frame in (
            self.overview_tab,
            self.operations_tab,
            self.financials_tab,
            self.assets_tab,
            self.audit_tab,
        ):
            for child in frame.winfo_children():
                child.destroy()
        self.load_reports()

    def scrollable_tab(self, title):
        tab = tk.Frame(self.notebook, bg=styles.WHITE)
        self.notebook.add(tab, text=title)

        canvas = tk.Canvas(tab, bg=styles.WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=styles.WHITE)
        window = canvas.create_window((0, 0), window=content, anchor="nw")

        def sync_scroll_region(_event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def sync_width(event):
            canvas.itemconfigure(window, width=event.width)

        def scroll_with_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

        content.bind("<Configure>", sync_scroll_region)
        canvas.bind("<Configure>", sync_width)
        canvas.bind("<MouseWheel>", scroll_with_wheel)
        canvas.bind("<Button-4>", lambda _event: canvas.yview_scroll(-1, "units"))
        canvas.bind("<Button-5>", lambda _event: canvas.yview_scroll(1, "units"))
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        return content

    def load_reports(self):
        self.load_overview()
        self.load_operations()
        self.load_financials()
        self.load_assets()
        self.load_users_and_audit()

    def load_overview(self):
        collections = {
            "Owners": "owners",
            "Vehicles": "vehicles",
            "Drivers": "drivers",
            "Conductors": "conductors",
            "Stage Managers": "stage_managers",
            "Routes": "routes",
            "Trips": "trips",
            "Collections": "collections",
            "Expenses": "expenses",
            "Deductions": "deductions",
            "Payouts": "payouts",
            "Users": "users",
        }
        total_collections = self.sum_collection("collections", "amount_collected")
        total_expenses = self.sum_collection("expenses", "amount")
        total_deductions = self.sum_collection("deductions", "amount")
        total_payouts = self.sum_collection("payouts", "net_payout")
        net_estimate = total_collections - total_expenses - total_deductions - total_payouts

        cards = tk.Frame(self.overview_tab, bg=styles.WHITE)
        cards.pack(fill="x", anchor="nw")
        overview_cards = [
            ("Total Collections", self.money(total_collections)),
            ("Total Expenses", self.money(total_expenses)),
            ("Total Deductions", self.money(total_deductions)),
            ("Total Payouts", self.money(total_payouts)),
            ("Net After Payouts", self.money(net_estimate)),
            ("Active Trips", self.db.trips.count_documents({"status": {"$ne": "Completed"}})),
            ("Active Vehicles", self.db.vehicles.count_documents({"status": "Active"})),
            ("Active Users", self.db.users.count_documents({"status": "Active"})),
        ]
        for index, (label, value) in enumerate(overview_cards):
            metric_card(cards, label, value).grid(row=index // 4, column=index % 4, sticky="ew", padx=6, pady=6)
        for column in range(4):
            cards.columnconfigure(column, weight=1)

        counts = [
            {"module": label, "records": self.db[collection].count_documents({})}
            for label, collection in collections.items()
        ]
        self.add_section(self.overview_tab, "Record coverage", counts, ("module", "records"), height=8)

        trip_status = self.group_counts("trips", "status")
        vehicle_status = self.group_counts("vehicles", "status")
        user_roles = self.group_counts("users", "role")
        self.add_section(self.overview_tab, "Trip status breakdown", trip_status, ("status", "records"), height=5)
        self.add_section(self.overview_tab, "Vehicle status breakdown", vehicle_status, ("status", "records"), height=5)
        self.add_section(self.overview_tab, "User role breakdown", user_roles, ("role", "records"), height=5)

    def load_operations(self):
        self.add_collection_section(
            self.operations_tab,
            "Trips",
            "trips",
            ("id", "date", "status", "vehicle_id", "driver_id", "conductor_id", "route_id", "departure_time", "arrival_time"),
            sort=[("date", -1), ("created_at", -1)],
        )
        self.add_collection_section(
            self.operations_tab,
            "Collections",
            "collections",
            ("id", "date", "trip_id", "vehicle_id", "conductor_id", "amount_collected"),
            sort=[("date", -1), ("created_at", -1)],
        )
        self.add_collection_section(
            self.operations_tab,
            "Routes",
            "routes",
            ("id", "name", "origin", "destination", "stages", "fare_structure", "expected_revenue"),
            sort=[("name", 1)],
        )
        self.add_collection_section(
            self.operations_tab,
            "Stage Managers",
            "stage_managers",
            ("id", "full_name", "contact", "stage_name"),
            sort=[("full_name", 1)],
        )

    def load_financials(self):
        finance_summary = [
            {"category": "Collections", "records": self.db.collections.count_documents({}), "amount": self.money(self.sum_collection("collections", "amount_collected"))},
            {"category": "Expenses", "records": self.db.expenses.count_documents({}), "amount": self.money(self.sum_collection("expenses", "amount"))},
            {"category": "Deductions", "records": self.db.deductions.count_documents({}), "amount": self.money(self.sum_collection("deductions", "amount"))},
            {"category": "Gross Payout Earnings", "records": self.db.payouts.count_documents({}), "amount": self.money(self.sum_collection("payouts", "gross_earnings"))},
            {"category": "Net Payouts", "records": self.db.payouts.count_documents({}), "amount": self.money(self.sum_collection("payouts", "net_payout"))},
        ]
        self.add_section(self.financials_tab, "Financial summary", finance_summary, ("category", "records", "amount"), height=6)
        self.add_section(
            self.financials_tab,
            "Expenses by type",
            self.amount_breakdown("expenses", "type", "amount"),
            ("type", "records", "amount"),
            height=8,
        )
        self.add_section(
            self.financials_tab,
            "Deductions by type",
            self.amount_breakdown("deductions", "type", "amount"),
            ("type", "records", "amount"),
            height=8,
        )
        self.add_collection_section(
            self.financials_tab,
            "Expenses",
            "expenses",
            ("id", "date", "type", "trip_id", "vehicle_id", "logged_by", "amount"),
            sort=[("date", -1), ("created_at", -1)],
        )
        self.add_collection_section(
            self.financials_tab,
            "Deductions",
            "deductions",
            ("id", "date", "owner_id", "type", "amount", "reason"),
            sort=[("date", -1), ("created_at", -1)],
        )
        self.add_collection_section(
            self.financials_tab,
            "Payouts",
            "payouts",
            ("id", "date", "period", "owner_id", "gross_earnings", "total_deductions", "net_payout"),
            sort=[("date", -1), ("created_at", -1)],
        )

    def load_assets(self):
        self.add_collection_section(
            self.assets_tab,
            "Owners",
            "owners",
            ("id", "full_name", "contact", "email", "national_id", "shares", "status", "join_date"),
            sort=[("full_name", 1)],
        )
        self.add_collection_section(
            self.assets_tab,
            "Vehicles",
            "vehicles",
            ("id", "plate", "make", "model", "capacity", "owner_id", "route_id", "status", "insurance_expiry", "inspection_expiry"),
            sort=[("plate", 1)],
        )
        self.add_collection_section(
            self.assets_tab,
            "Drivers",
            "drivers",
            ("id", "full_name", "contact", "license_no", "license_expiry", "assigned_vehicle"),
            sort=[("full_name", 1)],
        )
        self.add_collection_section(
            self.assets_tab,
            "Conductors",
            "conductors",
            ("id", "full_name", "contact", "assigned_vehicle"),
            sort=[("full_name", 1)],
        )

    def load_users_and_audit(self):
        self.add_collection_section(
            self.audit_tab,
            "Users",
            "users",
            ("id", "full_name", "username", "role", "linked_id", "status", "permissions"),
            sort=[("role", 1), ("full_name", 1)],
        )
        self.add_collection_section(
            self.audit_tab,
            "Audit Logs",
            "audit_logs",
            ("id", "timestamp", "username", "action", "module", "details"),
            sort=[("timestamp", -1)],
        )

    def add_collection_section(self, parent, title, collection_name, columns, sort=None):
        rows = list(self.db[collection_name].find({}).sort(sort or [("created_at", -1)]))
        self.add_section(parent, f"{title} ({len(rows)} records)", rows, columns)

    def add_section(self, parent, title, rows, columns, height=None):
        section = tk.Frame(parent, bg=styles.WHITE)
        section.pack(fill="x", anchor="nw", pady=(0, 18))
        tk.Label(section, text=title, bg=styles.WHITE, fg=styles.TEXT, font=styles.FONT_HEADING).pack(anchor="w", pady=(0, 8))
        table_frame = tk.Frame(section, bg=styles.WHITE, highlightthickness=1, highlightbackground=styles.BORDER)
        table_frame.pack(fill="x", expand=False)
        table = make_table(table_frame, columns)
        table.configure(height=height or min(max(len(rows), 3), 10))

        if not rows:
            table.insert("", "end", values=["No records found"] + ["" for _column in columns[1:]], tags=("odd",))
            return

        for index, row in enumerate(rows):
            values = [self.value_for(row, column) for column in columns]
            table.insert("", "end", values=values, tags=("even" if index % 2 else "odd",))

    def value_for(self, row, column):
        if column == "id":
            return format_id(row)
        value = row.get(column, "")
        if column == "logged_by":
            return self.user_label(value)
        if column == "linked_id":
            return self.linked_label(value)
        if column in {"details", "permissions", "stages", "fare_structure"}:
            return self.compact(value)
        if column == "timestamp":
            return self.format_date(value, include_time=True)
        if column in {"created_at", "updated_at"}:
            return self.format_date(value, include_time=True)
        if column.endswith("date") or column.endswith("_expiry") or column == "date":
            return self.format_date(value)
        if column in {
            "amount",
            "amount_collected",
            "gross_earnings",
            "total_deductions",
            "net_payout",
            "expected_revenue",
        }:
            return self.money(value)
        return display_value(column, value)

    def sum_collection(self, collection_name, field):
        return sum(to_float(row.get(field, 0)) for row in self.db[collection_name].find({}))

    def group_counts(self, collection_name, field):
        counts = {}
        for row in self.db[collection_name].find({}):
            key = row.get(field) or "Not specified"
            counts[key] = counts.get(key, 0) + 1
        return [{field: key, "records": value} for key, value in sorted(counts.items())]

    def amount_breakdown(self, collection_name, group_field, amount_field):
        groups = {}
        for row in self.db[collection_name].find({}):
            key = row.get(group_field) or "Not specified"
            current = groups.setdefault(key, {"records": 0, "amount": 0})
            current["records"] += 1
            current["amount"] += to_float(row.get(amount_field, 0))
        return [
            {group_field: key, "records": value["records"], "amount": self.money(value["amount"])}
            for key, value in sorted(groups.items())
        ]

    def user_label(self, user_id):
        if not user_id:
            return ""
        text_id = str(user_id)
        query = [{"public_id": text_id}]
        if ObjectId.is_valid(text_id):
            query.append({"_id": ObjectId(text_id)})
        user = self.db.users.find_one({"$or": query})
        if user:
            return f"{user.get('public_id') or text_id} - {user.get('full_name') or user.get('username')}"
        return text_id

    def linked_label(self, linked_id):
        if not linked_id:
            return ""
        prefix = str(linked_id).strip().upper()[:1]
        collection_name = {
            "O": "owners",
            "D": "drivers",
            "C": "conductors",
            "S": "stage_managers",
        }.get(prefix)
        if not collection_name:
            return linked_id
        return label_for(collection_name, linked_id)

    def compact(self, value):
        if isinstance(value, dict):
            return ", ".join(f"{key}: {self.compact(item)}" for key, item in value.items())
        if isinstance(value, (list, tuple, set)):
            return ", ".join(str(item) for item in value)
        return "" if value is None else str(value)

    def format_date(self, value, include_time=False):
        if not value:
            return ""
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M" if include_time else "%Y-%m-%d")
        return str(value)

    def money(self, value):
        return f"{to_float(value):,.2f}"
