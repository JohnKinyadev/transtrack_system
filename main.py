from tkinter import messagebox

from transtrack.app import TransTrackApp
from transtrack.controllers.auth_controller import AuthController
from transtrack.db.connection import check_connection, create_indexes


def main():
    ok, message = check_connection()
    if not ok:
        messagebox.showerror(
            "MongoDB required",
            "TransTrack needs a working MongoDB connection before it can start.\n\n" + message,
        )
        return
    create_indexes()
    AuthController().ensure_seed_admin()
    app = TransTrackApp()
    app.mainloop()


if __name__ == "__main__":
    main()
