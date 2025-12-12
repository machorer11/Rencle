import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import re

PRICE_PER_KM = 20

class KessaiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("決済方法を選択（デモ）")
        self.geometry("480x640")
        self.method_var = tk.StringVar(value="card")
        self.distance_var = tk.StringVar(value="10")
        self.loading = False

        # Card fields
        self.card_number = tk.StringVar()
        self.card_exp = tk.StringVar()
        self.card_cvc = tk.StringVar()

        # PayPal
        self.paypal_email = tk.StringVar()

        # PayPay
        self.paypay_phone = tk.StringVar()
        self.paypay_userid = tk.StringVar()

        # Bank
        self.bank_name = tk.StringVar()
        self.bank_account = tk.StringVar()

        self._build_ui()
        self._update_calculated()

    def _build_ui(self):
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="支払い方法", font=("", 14)).pack(anchor="w", pady=(0,8))

        methods = [
            ("クレジット/デビットカード", "card"),
            ("PayPal", "paypal"),
            ("PayPay", "paypay"),
            ("銀行振込（デモ）", "bank"),
        ]
        for text, val in methods:
            ttk.Radiobutton(frame, text=text, variable=self.method_var, value=val, command=self._on_method_change).pack(anchor="w")

        ttk.Separator(frame).pack(fill="x", pady=10)

        # method-specific container
        self.method_container = ttk.Frame(frame)
        self.method_container.pack(fill="x")

        # Card frame
        self.card_frame = ttk.Frame(self.method_container)
        ttk.Label(self.card_frame, text="カード番号").pack(anchor="w")
        ttk.Entry(self.card_frame, textvariable=self.card_number).pack(fill="x", pady=4)
        row = ttk.Frame(self.card_frame)
        row.pack(fill="x")
        ttk.Label(row, text="有効期限").grid(row=0, column=0, sticky="w")
        ttk.Entry(row, textvariable=self.card_exp).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Label(row, text="CVC").grid(row=0, column=2, sticky="w")
        ttk.Entry(row, textvariable=self.card_cvc, width=10).grid(row=0, column=3, sticky="w", padx=4)
        row.columnconfigure(1, weight=1)

        # PayPal frame
        self.paypal_frame = ttk.Frame(self.method_container)
        ttk.Label(self.paypal_frame, text="PayPalメールアドレス").pack(anchor="w")
        ttk.Entry(self.paypal_frame, textvariable=self.paypal_email).pack(fill="x", pady=4)

        # PayPay frame
        self.paypay_frame = ttk.Frame(self.method_container)
        ttk.Label(self.paypay_frame, text="電話番号（PayPayアカウント）").pack(anchor="w")
        ttk.Entry(self.paypay_frame, textvariable=self.paypay_phone).pack(fill="x", pady=4)
        ttk.Label(self.paypay_frame, text="PayPayユーザーID（任意）").pack(anchor="w", pady=(8,0))
        ttk.Entry(self.paypay_frame, textvariable=self.paypay_userid).pack(fill="x", pady=4)
        ttk.Label(self.paypay_frame, text="※ PayPay の処理はデモです。実装してください。", foreground="gray").pack(anchor="w", pady=4)

        # Bank frame
        self.bank_frame = ttk.Frame(self.method_container)
        ttk.Label(self.bank_frame, text="銀行名").pack(anchor="w")
        ttk.Entry(self.bank_frame, textvariable=self.bank_name).pack(fill="x", pady=4)
        ttk.Label(self.bank_frame, text="口座番号").pack(anchor="w", pady=(8,0))
        ttk.Entry(self.bank_frame, textvariable=self.bank_account).pack(fill="x", pady=4)
        ttk.Label(self.bank_frame, text="※ 銀行振込はデモです。実際の振込受付は行われません。", foreground="gray").pack(anchor="w", pady=4)

        # Distance & amount
        ttk.Separator(frame).pack(fill="x", pady=10)
        ttk.Label(frame, text="走行距離 (km)").pack(anchor="w")
        dist_entry = ttk.Entry(frame, textvariable=self.distance_var)
        dist_entry.pack(fill="x", pady=4)
        dist_entry.bind("<KeyRelease>", lambda e: self._on_distance_change())
        self.amount_label = ttk.Label(frame, text="")
        self.amount_label.pack(anchor="w", pady=(8,0))

        # Submit button
        ttk.Button(frame, text="支払う", command=self._on_submit).pack(fill="x", pady=16)

        self._on_method_change()

    def _on_method_change(self):
        for child in self.method_container.winfo_children():
            child.pack_forget()
        method = self.method_var.get()
        if method == "card":
            self.card_frame.pack(fill="x")
        elif method == "paypal":
            self.paypal_frame.pack(fill="x")
        elif method == "paypay":
            self.paypay_frame.pack(fill="x")
        elif method == "bank":
            self.bank_frame.pack(fill="x")
        self._update_calculated()

    def _on_distance_change(self):
        self._update_calculated()

    def _update_calculated(self):
        try:
            d = int(self.distance_var.get().strip())
            if d < 0:
                d = 0
        except Exception:
            d = 0
        amount = d * PRICE_PER_KM
        self.amount_label.config(text=f"単価: ¥{PRICE_PER_KM} /km   支払金額: ¥{amount}")

    def _validate(self):
        # distance
        dstr = self.distance_var.get().strip()
        if dstr == "":
            messagebox.showwarning("入力エラー", "走行距離は必須です")
            return False
        try:
            d = int(dstr)
            if d < 0:
                messagebox.showwarning("入力エラー", "走行距離は正の数で入力してください")
                return False
        except:
            messagebox.showwarning("入力エラー", "走行距離は数値で入力してください")
            return False

        method = self.method_var.get()
        if method == "card":
            num = self.card_number.get().strip()
            exp = self.card_exp.get().strip()
            cvc = self.card_cvc.get().strip()
            if not num or not exp or not cvc:
                messagebox.showwarning("入力エラー", "カード情報は全て必須です")
                return False
            if len(re.sub(r"\D", "", num)) < 12:
                messagebox.showwarning("入力エラー", "カード番号が短すぎます")
                return False
            if len(re.sub(r"\D", "", cvc)) < 3:
                messagebox.showwarning("入力エラー", "CVC を確認してください")
                return False
        elif method == "paypal":
            email = self.paypal_email.get().strip()
            if not email:
                messagebox.showwarning("入力エラー", "PayPalメールアドレスは必須です")
                return False
            if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
                messagebox.showwarning("入力エラー", "有効なメールアドレスを入力してください")
                return False
        elif method == "paypay":
            phone = self.paypay_phone.get().strip()
            if not phone:
                messagebox.showwarning("入力エラー", "電話番号は必須です")
                return False
            if not phone.isdigit() or len(phone) < 9:
                messagebox.showwarning("入力エラー", "有効な電話番号を入力してください")
                return False
        elif method == "bank":
            name = self.bank_name.get().strip()
            account = self.bank_account.get().strip()
            if not name or not account:
                messagebox.showwarning("入力エラー", "銀行名と口座番号は必須です")
                return False
        return True

    def _on_submit(self):
        if not self._validate():
            return
        if self.loading:
            return
        self.loading = True
        # disable window during processing by changing cursor
        self.config(cursor="watch")
        threading.Thread(target=self._simulate_payment, daemon=True).start()

    def _simulate_payment(self):
        time.sleep(2)  # デモの待機
        amount = (int(self.distance_var.get().strip()) if self.distance_var.get().strip().isdigit() else 0) * PRICE_PER_KM
        method_label = {
            "card": "カード",
            "paypal": "PayPal",
            "paypay": "PayPay",
            "bank": "銀行振込"
        }.get(self.method_var.get(), "不明")
        # back to main thread to show dialog
        self.after(0, lambda: self._on_payment_done(method_label, amount))

    def _on_payment_done(self, method_label, amount):
        self.loading = False
        self.config(cursor="")
        messagebox.showinfo("支払い完了（デモ）", f"支払い方法: {method_label}\n走行距離: {self.distance_var.get().strip()} km\n金額: ¥{amount}")

if __name__ == "__main__":
    app = KessaiApp()
    app.mainloop()