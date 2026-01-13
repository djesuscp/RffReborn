import tkinter
from tkinter import ttk
import threading
import queue

import controllers.fileManager as fm
from controllers.scanEngine import scan_duplicates


class oneDirectory(tkinter.Frame):

    def __init__(self, parent, showScreen):
        super().__init__(parent, bg="#000000")

        self.showScreen = showScreen

        # -------------------------------
        # Estado threading
        # -------------------------------
        self.scan_thread = None
        self.scan_queue = queue.Queue()
        self.cancel_event = threading.Event()

        # -------------------------------
        # UI
        # -------------------------------

        title = tkinter.Label(
            self,
            text="Examine One Directory",
            fg="white",
            bg="#000000",
            font=("Arial", 18)
        )
        title.pack(pady=20)

        # Directory selector
        dir_frame = tkinter.Frame(self, bg="#000000")
        dir_frame.pack(pady=10)

        self.directoryField = tkinter.Entry(dir_frame, width=80)
        self.directoryField.pack(side="left", padx=5)

        browse_btn = ttk.Button(
            dir_frame,
            text="Browse",
            command=lambda: fm.browseDirectory(self.directoryField)
        )
        browse_btn.pack(side="left", padx=5)

        # Buttons
        btn_frame = tkinter.Frame(self, bg="#000000")
        btn_frame.pack(pady=10)

        self.start_btn = ttk.Button(
            btn_frame,
            text="Start Scan",
            command=self.start_scan
        )
        self.start_btn.pack(side="left", padx=5)

        self.cancel_btn = ttk.Button(
            btn_frame,
            text="Cancel",
            command=self.cancel_scan,
            state=tkinter.DISABLED
        )
        self.cancel_btn.pack(side="left", padx=5)

        back_btn = ttk.Button(
            btn_frame,
            text="Back",
            command=lambda: self.showScreen("menu")
        )
        back_btn.pack(side="left", padx=5)

        # Progress
        self.progress_bar = ttk.Progressbar(
            self,
            mode="determinate"
        )
        self.progress_bar.pack(fill="x", padx=30, pady=10)

        self.status_label = tkinter.Label(
            self,
            text="Idle",
            fg="white",
            bg="#000000"
        )
        self.status_label.pack(pady=5)

        # Console
        self.console = tkinter.Text(
            self,
            height=25,
            bg="#111111",
            fg="white"
        )
        self.console.pack(fill="both", expand=True, padx=20, pady=10)

    # ==========================================================
    # Scan control
    # ==========================================================

    def start_scan(self):
        root_dir = self.directoryField.get().strip()
        if not root_dir:
            return

        self.console.delete("1.0", "end")
        self.status_label.config(text="Starting scan...")
        self.progress_bar.start()

        self.start_btn.config(state=tkinter.DISABLED)
        self.cancel_btn.config(state=tkinter.NORMAL)

        self.cancel_event.clear()
        self.scan_queue = queue.Queue()

        self.scan_thread = threading.Thread(
            target=self._scan_worker,
            args=(root_dir,),
            daemon=True
        )
        self.scan_thread.start()

        self.after(100, self.process_queue)

    def cancel_scan(self):
        if self.scan_thread and self.scan_thread.is_alive():
            self.cancel_event.set()
            self.status_label.config(text="Cancelling...")

    # ==========================================================
    # Worker (NO UI)
    # ==========================================================

    def _scan_worker(self, root_dir):
        try:
            results = scan_duplicates(
                root_dir,
                progress_cb=lambda data: self.scan_queue.put(data),
                cancel_event=self.cancel_event
            )
            self.scan_queue.put({
                "type": "done",
                "results": results
            })
        except Exception as e:
            self.scan_queue.put({
                "type": "error",
                "error": str(e)
            })

    # ==========================================================
    # UI Queue processing
    # ==========================================================

    def process_queue(self):
        try:
            while True:
                msg = self.scan_queue.get_nowait()

                # Progreso

                # Inicialización del total
                if msg.get("phase") == "count":
                    total = msg.get("total_files", 0)
                    self.progress_bar["maximum"] = total
                    self.progress_bar["value"] = 0
                    self.status_label.config(
                        text=f"Found {total} files. Starting scan..."
                    )
                
                if msg.get("processed") is not None:
                    self.progress_bar["value"] = msg["processed"]

                    percent = int(
                        (msg["processed"] / self.progress_bar["maximum"]) * 100
                    )
                    self.status_label.config(
                        text=f"{percent}% - {msg.get('current', '')}"
                    )

                if msg.get("phase"):
                    phase = msg["phase"]
                    current = msg.get("current", "")

                    if phase == "scan":
                        self.status_label.config(
                            text=f"Scanning: {current}"
                        )
                    elif phase == "partial-hash":
                        self.status_label.config(
                            text=f"Quick hash: {current}"
                        )
                    elif phase == "full-hash":
                        self.status_label.config(
                            text=f"Full hash: {current}"
                        )

                # Fin
                if msg.get("type") == "done":
                    self.progress_bar["value"] = self.progress_bar["maximum"]
                    self.status_label.config(text="100% - Scan finished")
                    # self.progress_bar.stop()
                    # self.status_label.config(text="Scan finished")
                    self.start_btn.config(state=tkinter.NORMAL)
                    self.cancel_btn.config(state=tkinter.DISABLED)
                    self.display_results(msg["results"])
                    return

                # Error
                if msg.get("type") == "error":
                    self.progress_bar.stop()
                    self.status_label.config(text="Error during scan")
                    self.console.insert("end", msg.get("error", "Unknown error"))
                    self.start_btn.config(state=tkinter.NORMAL)
                    self.cancel_btn.config(state=tkinter.DISABLED)
                    return

        except queue.Empty:
            pass

        if self.scan_thread and self.scan_thread.is_alive():
            self.after(100, self.process_queue)

    # ==========================================================
    # Results
    # ==========================================================

    def display_results(self, results):
        self.console.delete("1.0", "end")

        if not results:
            self.console.insert("end", "No duplicate files found.")
            return

        total_groups = len(results)
        self.console.insert(
            "end",
            f"Duplicate groups found: {total_groups}\n"
        )

        for idx, group in enumerate(results, start=1):
            self.console.insert(
                "end",
                f"\n[{idx}] Size: {group['size']} bytes | Files: {len(group['files'])}\n"
            )
            for f in group["files"]:
                self.console.insert("end", f"  {f}\n")
