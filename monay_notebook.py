import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os 
from typing import Dict, Any, List

# 引入 Matplotlib 相關模組
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# *** 變更點 1：引入 datetime 模組 ***
import datetime as dt

# --- 檔案設定 ---
USERS_FILE = "users.json"
TRANSACTIONS_FILE = "transactions.json"

# --- 用戶資料處理函數 ---

def load_users() -> Dict[str, str]:
    """從 JSON 檔案載入用戶帳號密碼。"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {"user": "123"} 

def save_users(users: Dict[str, str]):
    """將用戶帳號密碼儲存到 JSON 檔案。"""
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"ERROR: 無法儲存用戶檔案: {e}")


class LoginWindow:
    """ 登入/註冊視窗類別... (內容省略，與之前版本相同) """
    def __init__(self, master, on_success_callback):
        self.master = master
        self.on_success_callback = on_success_callback
        self.users = load_users()
        
        self.master.withdraw() 
        
        self.login_window = tk.Toplevel(master)
        self.login_window.title("🔐 請登入或註冊")
        self.login_window.geometry("350x230")
        self.login_window.configure(bg='#F0F8FF')
        self.login_window.resizable(False, False)
        self.login_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 設定風格
        style = ttk.Style()
        style.configure('TLabel', font=('Microsoft YaHei', 10), background='#F0F8FF')
        style.configure('TEntry', font=('Microsoft YaHei', 10))
        
        style.configure('Login.TButton', 
                        font=('Microsoft YaHei', 10, 'bold'), 
                        padding=5,
                        foreground='white', 
                        background='#000093')
        style.map('Login.TButton', background=[('active', '#0080FF')])

        # 登入框架
        login_frame = tk.Frame(self.login_window, bg='#F0F8FF', padx=20, pady=10)
        login_frame.pack(expand=True)
        
        # 帳號輸入
        ttk.Label(login_frame, text="帳號:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.username_entry = ttk.Entry(login_frame, width=25)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # 密碼輸入
        ttk.Label(login_frame, text="密碼:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.password_entry = ttk.Entry(login_frame, show="*", width=25)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # 按鈕框架 (登入/註冊)
        button_frame = tk.Frame(login_frame, bg='#F0F8FF')
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='we')
        
        ttk.Button(button_frame, text="🔑 登入", command=self.attempt_login, style='Login.TButton').pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 5))
        
        # 新增註冊按鈕
        ttk.Button(button_frame, text="📝 註冊", command=self.show_registration_window, style='Login.TButton').pack(side=tk.RIGHT, expand=True, fill='x', padx=(5, 0))

        self.login_window.bind('<Return>', lambda event: self.attempt_login())
        self.username_entry.focus_set()

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.users.get(username) == password:
            self.login_window.destroy()
            self.master.deiconify() 
            self.on_success_callback()
        else:
            messagebox.showerror("登入失敗", "帳號或密碼錯誤，請重新輸入。", parent=self.login_window)
            self.password_entry.delete(0, tk.END)

    def on_closing(self):
        if messagebox.askyesno("離開應用程式", "確定要關閉程式嗎？", parent=self.login_window):
            self.master.destroy()

    def show_registration_window(self):
        reg_window = tk.Toplevel(self.login_window)
        reg_window.title("📝 註冊新帳號")
        reg_window.geometry("350x250")
        reg_window.configure(bg='#F0F8FF')
        reg_window.resizable(False, False)
        
        reg_window.transient(self.login_window)
        reg_window.grab_set()

        reg_frame = tk.Frame(reg_window, bg='#F0F8FF', padx=20, pady=10)
        reg_frame.pack(expand=True)

        ttk.Label(reg_frame, text="新帳號:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.reg_username_entry = ttk.Entry(reg_frame, width=25)
        self.reg_username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(reg_frame, text="密碼:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.reg_password_entry = ttk.Entry(reg_frame, show="*", width=25)
        self.reg_password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(reg_frame, text="確認密碼:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.reg_confirm_entry = ttk.Entry(reg_frame, show="*", width=25)
        self.reg_confirm_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(reg_frame, text="✔ 確認註冊", 
                   command=lambda: self.attempt_register(reg_window), 
                   style='Login.TButton').grid(row=3, column=0, columnspan=2, pady=15, sticky='we')

        reg_window.bind('<Return>', lambda event: self.attempt_register(reg_window))
        self.reg_username_entry.focus_set()

        self.login_window.wait_window(reg_window)

    def attempt_register(self, reg_window: tk.Toplevel):
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("註冊失敗", "所有欄位都不能為空。", parent=reg_window)
            return

        if password != confirm_password:
            messagebox.showerror("註冊失敗", "兩次密碼輸入不一致。", parent=reg_window)
            self.reg_password_entry.delete(0, tk.END)
            self.reg_confirm_entry.delete(0, tk.END)
            return

        if username in self.users:
            messagebox.showerror("註冊失敗", f"帳號 '{username}' 已存在，請使用其他名稱。", parent=reg_window)
            return

        self.users[username] = password
        save_users(self.users) 
        
        messagebox.showinfo("註冊成功", f"帳號 '{username}' 註冊成功，請登入。", parent=reg_window)
        
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, username)
        self.password_entry.delete(0, tk.END)
        self.username_entry.focus_set()

        reg_window.destroy()


class ExpenseTrackerApp:
    
    # *** 變更點 2-1：設定日期格式 ***
    DATE_FORMAT = "%Y-%m-%d" # 固定的日期格式

    def __init__(self, master):
        self.master = master
        master.title("💰 金錢追蹤器")
        master.geometry("1000x600") 
        master.configure(bg='#00E3E3') 
        
        master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.balance = 0.0
        self.transactions: List[Dict[str, Any]] = []
        self.categories = ["飲食", "交通", "娛樂", "購物", "薪資", "投資", "其他"]
        
        self.load_transactions()
        
        # --- 設定風格與配色 ---
        style = ttk.Style()
        PRIMARY_COLOR = '#000093' 
        SECONDARY_COLOR = '#0080FF' 
        
        style.configure('.', font=('Microsoft YaHei', 10))
        
        # 設定按鈕樣式
        style.configure('TButton', 
                        foreground='white', 
                        background=PRIMARY_COLOR, 
                        font=('Microsoft YaHei', 12, 'bold'),
                        padding=8, 
                        borderwidth=0)
        style.map('TButton', background=[('active', SECONDARY_COLOR)])
        
        # 設定刪除按鈕樣式 (使用紅色強調)
        style.configure('Delete.TButton', 
                        foreground='white', 
                        background='#FF3333', 
                        font=('Microsoft YaHei', 12, 'bold'),
                        padding=8, 
                        borderwidth=0)
        style.map('Delete.TButton', background=[('active', '#FF6666')])
        
        style.configure("Treeview.Heading", font=('Microsoft YaHei', 11, 'bold'), background=SECONDARY_COLOR, foreground='white')
        style.configure("Treeview", rowheight=28)

        # --- 介面佈局：主框架分為左右兩欄 ---
        self.main_paned_window = ttk.PanedWindow(master, orient=tk.HORIZONTAL)
        self.main_paned_window.pack(fill='both', expand=True, padx=10, pady=10)

        # ----------------------------------------------------
        # 區塊 A: 左側 - 餘額和新增交易 (Input/Control)
        # ----------------------------------------------------
        self.left_frame = tk.Frame(self.main_paned_window, bg='#F0F8FF', padx=10, pady=10)
        self.main_paned_window.add(self.left_frame, weight=30) 

        # 1. 餘額顯示區域 
        self.balance_frame = tk.Frame(self.left_frame, bg='white', padx=10, pady=5, relief=tk.RAISED, borderwidth=1) 
        self.balance_frame.pack(pady=8, fill='x') 

        tk.Label(self.balance_frame, text="💵 當前總餘額:", font=('Microsoft YaHei', 12), bg='white').pack(side=tk.LEFT, padx=5) 
        
        self.balance_var = tk.StringVar(value=f"{self.balance:.2f} 元")
        self.balance_label = tk.Label(self.balance_frame, textvariable=self.balance_var, font=('Microsoft YaHei', 16, 'bold'), bg='white', fg=PRIMARY_COLOR)
        self.balance_label.pack(side=tk.RIGHT, padx=5)

        # 2. 新增記錄輸入區域
        self.input_group = tk.LabelFrame(self.left_frame, text="➕ 新增交易", font=('Microsoft YaHei', 12, 'bold'), bg='#F0F8FF', fg=PRIMARY_COLOR, padx=10, pady=10)
        self.input_group.pack(pady=10, fill='x')
        
        # *** 變更點 3-1：新增日期輸入欄位 (Row 0) ***
        tk.Label(self.input_group, text="日期:", bg='#F0F8FF').grid(row=0, column=0, padx=5, pady=8, sticky='w')
        # 設定預設值為今日日期
        self.date_var = tk.StringVar(value=dt.datetime.now().strftime(self.DATE_FORMAT))
        self.date_entry = ttk.Entry(self.input_group, textvariable=self.date_var, width=20)
        self.date_entry.grid(row=0, column=1, padx=5, pady=8, sticky='we')
        
        # 交易類型 (Row 1)
        tk.Label(self.input_group, text="類型:", bg='#F0F8FF').grid(row=1, column=0, padx=5, pady=8, sticky='w')
        self.type_var = tk.StringVar(value="支出")
        self.type_combo = ttk.Combobox(self.input_group, textvariable=self.type_var, values=["支出", "收入"], state="readonly", width=15)
        self.type_combo.grid(row=1, column=1, padx=5, pady=8, sticky='we')
        
        # 金額 (Row 2)
        tk.Label(self.input_group, text="金額:", bg='#F0F8FF').grid(row=2, column=0, padx=5, pady=8, sticky='w')
        self.amount_entry = ttk.Entry(self.input_group, width=20)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=8, sticky='we')

        # 類別 (Row 3)
        tk.Label(self.input_group, text="類別:", bg='#F0F8FF').grid(row=3, column=0, padx=5, pady=8, sticky='w')
        self.category_var = tk.StringVar(value=self.categories[0])
        self.category_combo = ttk.Combobox(self.input_group, textvariable=self.category_var, values=self.categories, state="readonly", width=15)
        self.category_combo.grid(row=3, column=1, padx=5, pady=8, sticky='we')
        
        # 備註 (Row 4)
        tk.Label(self.input_group, text="備註:", bg='#F0F8FF').grid(row=4, column=0, padx=5, pady=8, sticky='w')
        self.description_entry = ttk.Entry(self.input_group, width=20)
        self.description_entry.grid(row=4, column=1, padx=5, pady=8, sticky='we')
        # *** 變更點 3-1 結束 ***

        self.input_group.grid_columnconfigure(1, weight=1) 

        # 3. 按鈕區域 (新增記錄 + 分析圖表)
        self.button_frame = tk.Frame(self.left_frame, bg='#F0F8FF')
        self.button_frame.pack(pady=15, fill='x')

        ttk.Button(self.button_frame, text="💾 儲存並新增記錄", command=self.add_transaction, style='TButton').pack(fill='x', padx=10)
        
        ttk.Button(self.button_frame, 
                   text="📊 顯示花費分析圖", 
                   command=self.show_analysis_window, 
                   style='TButton').pack(fill='x', padx=10, pady=(10, 0))


        # ----------------------------------------------------
        # 區塊 B: 右側 - 交易記錄表格 (Record Table)
        # ----------------------------------------------------
        self.right_frame = tk.Frame(self.main_paned_window, bg='#F0F8FF')
        self.main_paned_window.add(self.right_frame, weight=70) 

        tk.Label(self.right_frame, text="📜 所有交易記錄", font=('Microsoft YaHei', 14, 'bold'), bg='#F0F8FF', fg=PRIMARY_COLOR).pack(pady=10)

        self.tree_frame = tk.Frame(self.right_frame, bg='#F0F8FF')
        self.tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # *** 變更點 4：調整 Treeview 欄位，新增 "Date" ***
        self.tree = ttk.Treeview(self.tree_frame, columns=("Date", "Type", "Amount", "Category", "Desc", "Balance"), show='headings', height=10)
        self.tree.heading("Date", text="日期")
        self.tree.heading("Type", text="類型")
        self.tree.heading("Amount", text="金額")
        self.tree.heading("Category", text="類別")
        self.tree.heading("Desc", text="備註")
        self.tree.heading("Balance", text="餘額")
        
        self.tree.column("Date", width=100, anchor='center') # 日期寬度
        self.tree.column("Type", width=70, anchor='center')
        self.tree.column("Amount", width=100, anchor='e')
        self.tree.column("Category", width=100, anchor='w')
        self.tree.column("Desc", width=180, anchor='w')
        self.tree.column("Balance", width=120, anchor='e')
        # *** 變更點 4 結束 ***
        
        self.tree.pack(side='left', fill='both', expand=True)
        
        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.tag_configure('income_tag', background='#E6FFE6', foreground='green') 
        self.tree.tag_configure('expense_tag', background='#FFE6E6', foreground='red')
        
        self.delete_frame = tk.Frame(self.right_frame, bg='#F0F8FF')
        self.delete_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(self.delete_frame, 
                   text="🗑️ 刪除選定記錄", 
                   command=self.delete_transaction, 
                   style='Delete.TButton').pack(fill='x')

        self.recalculate_balance()


    # --- 分析圖表方法 (create_pie_chart 函式已調整幣別為 NT$，在此保留) ---
    
    def create_pie_chart(self, frame):
        """計算支出並在指定框架內繪製圓餅圖"""
        
        CURRENCY_SYMBOL = "NT$" 

        expenses = [t for t in self.transactions if t['type'] == '支出']
        
        if not expenses:
            tk.Label(frame, text="目前沒有支出記錄，無法產生圓餅圖。", font=('Microsoft YaHei', 12), fg='red').pack(pady=50)
            return

        category_totals: Dict[str, float] = {}
        for t in expenses:
            category = t['category']
            amount = t['amount']
            category_totals[category] = category_totals.get(category, 0.0) + amount

        labels = list(category_totals.keys())
        sizes = list(category_totals.values())
        total_expense = sum(sizes)
        
        def make_autopct(values):
            def my_autopct(pct):
                absolute = round(pct/100. * total_expense, 2)
                return f'{pct:.1f}%\n({CURRENCY_SYMBOL}{absolute:.2f})'
            return my_autopct

        fig, ax = plt.subplots(figsize=(6, 5))
        
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False 
        
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            autopct=make_autopct(sizes), 
            startangle=90, 
            textprops={'fontsize': 10} 
        )
        
        ax.set_title("依類別劃分的總支出百分比", fontsize=14, fontweight='bold')
        ax.axis('equal')  
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()


    def show_analysis_window(self):
        """創建一個新的 Toplevel 視窗來顯示分析圖表"""
        
        analysis_window = tk.Toplevel(self.master)
        analysis_window.title("📊 支出分析圖表")
        analysis_window.geometry("700x550")
        analysis_window.resizable(False, False)
        analysis_window.configure(bg='#FFFFFF')
        
        analysis_window.transient(self.master)
        analysis_window.grab_set()

        chart_frame = tk.Frame(analysis_window, bg='white')
        chart_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.create_pie_chart(chart_frame)

        ttk.Button(analysis_window, 
                   text="關閉圖表", 
                   command=analysis_window.destroy, 
                   style='TButton').pack(pady=10)
        
        self.master.wait_window(analysis_window)


    # --- 數據處理方法 ---

    # *** 變更點 5：修改 load_transactions 函式，兼容舊數據並確保日期存在 ***
    def load_transactions(self):
        """從檔案載入交易，並處理舊數據兼容性 (若無日期則補上今日)"""
        if os.path.exists(TRANSACTIONS_FILE):
            try:
                with open(TRANSACTIONS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.transactions = data.get('transactions', [])
                    
                    today_str = dt.datetime.now().strftime(self.DATE_FORMAT)
                    
                    for record in self.transactions:
                        # 確保 'date' 欄位存在
                        if 'date' not in record:
                            record['date'] = today_str 
                        
                        # 確保數值型別正確
                        record['amount'] = float(record.get('amount', 0.0))
                        record['new_balance'] = float(record.get('new_balance', 0.0))

            except Exception as e:
                messagebox.showerror("載入錯誤", f"無法讀取檔案 {TRANSACTIONS_FILE}: {e}", parent=self.master)
                self.transactions = [] 
    # *** 變更點 5 結束 ***
    
    def save_transactions(self):
        data_to_save = {'transactions': self.transactions}
        try:
            with open(TRANSACTIONS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("存檔錯誤", f"無法儲存檔案 {TRANSACTIONS_FILE}: {e}", parent=self.master)

    def on_closing(self):
        if messagebox.askyesno("離開應用程式", "確定要關閉程式嗎？所有變動將自動儲存。", parent=self.master):
            self.save_transactions()
            self.master.destroy()

    def update_balance_display(self):
        PRIMARY_COLOR = '#000093' 
        self.balance_var.set(f"{self.balance:.2f} 元")
        if self.balance >= 0:
            self.balance_label.config(fg=PRIMARY_COLOR)
        else:
            self.balance_label.config(fg="red")

    # *** 變更點 6：修改 update_transaction_list 函式，新增日期欄位並依日期/時間排序 ***
    def update_transaction_list(self):
        """清空表格並重新載入、排序交易紀錄"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 1. 根據日期排序 (最新的在最前面)
        # 為了穩定性，同時考慮日期和在列表中的原始索引作為次要排序鍵
        sorted_transactions = sorted(
            enumerate(self.transactions), 
            key=lambda item: (item[1]['date'], item[0]), # 以日期為主，原始索引為輔
            reverse=True # 降冪排序，最新日期在前
        )
        
        for original_index, record in sorted_transactions:
            amount_display = f"{record['amount']:.2f}"
            balance_display = f"{record['new_balance']:.2f}"
            tag = 'income_tag' if record['type'] == '收入' else 'expense_tag'

            self.tree.insert("", tk.END, iid=original_index, values=(
                record['date'],              # <--- 新增日期
                record['type'], 
                amount_display, 
                record['category'],
                record['description'],
                balance_display
            ), tags=(tag,))
    # *** 變更點 6 結束 ***
            
    def recalculate_balance(self):
        self.balance = 0.0
        # 注意：重新計算餘額時，必須按照原始的交易順序，而不是日期順序
        for record in self.transactions:
            transaction_amount = record['amount']
            if record['type'] == '支出':
                transaction_amount = -transaction_amount
            self.balance += transaction_amount
            record['new_balance'] = self.balance
        self.update_balance_display()
        self.update_transaction_list()
            
    def delete_transaction(self):
        selected_item_id = self.tree.focus() 
        if not selected_item_id:
            messagebox.showwarning("刪除警告", "請先在表格中選中一條記錄。", parent=self.master)
            return

        try:
            # 這裡的 selected_item_id 是原始 index (iid)，不是 Treeview 中的行號
            transaction_index_to_delete = int(selected_item_id) 
            if not messagebox.askyesno("確認刪除", "確定要刪除這筆交易記錄嗎？", parent=self.master):
                return
            
            del self.transactions[transaction_index_to_delete]
            self.recalculate_balance()
            self.save_transactions() 
            messagebox.showinfo("成功", "交易記錄已刪除。", parent=self.master)

        except Exception:
            messagebox.showerror("錯誤", "無法刪除該交易記錄。", parent=self.master)

    # *** 變更點 7：修改 add_transaction 函式，加入日期驗證和儲存 ***
    def add_transaction(self):
        try:
            date_str = self.date_var.get().strip() # 獲取日期
            transaction_type = self.type_var.get()
            category = self.category_var.get()
            amount_str = self.amount_entry.get()
            description = self.description_entry.get().strip()

            if not amount_str or not category or not date_str:
                messagebox.showerror("輸入錯誤", "日期、金額與類別欄位不能為空！")
                return

            # 驗證日期格式
            try:
                dt.datetime.strptime(date_str, self.DATE_FORMAT)
            except ValueError:
                messagebox.showerror("輸入錯誤", f"日期格式不正確，請使用 {self.DATE_FORMAT} 格式 (例如: 2023-11-30)。")
                return

            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("輸入錯誤", "金額必須是正數。")
                return

            transaction_amount_value = -amount if transaction_type == "支出" else amount
            self.balance += transaction_amount_value
            new_balance_after_add = self.balance 

            record = {
                "date": date_str,  # <--- 新增日期欄位
                "type": transaction_type,
                "amount": amount,
                "category": category,
                "description": description,
                "new_balance": new_balance_after_add
            }
            self.transactions.append(record)
            
            self.update_balance_display()
            self.update_transaction_list()
            self.save_transactions()

            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            # 新增記錄後，將日期重設為今日日期，方便下次輸入
            self.date_var.set(dt.datetime.now().strftime(self.DATE_FORMAT))
            
        except ValueError:
            messagebox.showerror("輸入錯誤", "金額必須是有效的數字！")
        except Exception as e:
            messagebox.showerror("錯誤", f"發生了一個錯誤: {e}")
    # *** 變更點 7 結束 ***


# --- 啟動應用程式 ---
def start_app(root):
    """登入成功後的回撥函數，用於建立主應用程式"""
    ExpenseTrackerApp(root)

if __name__ == "__main__":
    root = tk.Tk()
    
    # 在主視窗顯示前，先啟動登入視窗
    login = LoginWindow(root, lambda: start_app(root)) 
    
    root.mainloop()