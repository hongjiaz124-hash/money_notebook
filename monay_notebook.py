import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 

# --- 設定帳號密碼 (簡單示範，實際應用應使用更安全的儲存方式) ---
VALID_USERNAME = "user"
VALID_PASSWORD = "123"

class LoginWindow:
    """
    登入視窗類別，負責處理身份驗證
    """
    def __init__(self, master, on_success_callback):
        self.master = master
        self.on_success_callback = on_success_callback
        
        # 隱藏主視窗，直到登入成功
        self.master.withdraw() 
        
        self.login_window = tk.Toplevel(master)
        self.login_window.title("🔐 請登入")
        self.login_window.geometry("350x200")
        self.login_window.configure(bg='#F0F8FF')
        self.login_window.resizable(False, False)
        
        # 設定登入視窗關閉時的行為 (防止直接關閉)
        self.login_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 設定風格
        style = ttk.Style()
        style.configure('TLabel', font=('Microsoft YaHei', 10), background='#F0F8FF')
        style.configure('TEntry', font=('Microsoft YaHei', 10))
        
        # 設定登入按鈕風格
        style.configure('Login.TButton', 
                        font=('Microsoft YaHei', 10, 'bold'), 
                        padding=5,
                        foreground='white', 
                        background='#000093')
        style.map('Login.TButton', background=[('active', '#0080FF')])

        # 登入框架
        login_frame = tk.Frame(self.login_window, bg='#F0F8FF', padx=20, pady=20)
        login_frame.pack(expand=True)
        
        # --- 帳號輸入 ---
        ttk.Label(login_frame, text="帳號:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.username_entry = ttk.Entry(login_frame, width=25)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # --- 密碼輸入 ---
        ttk.Label(login_frame, text="密碼:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.password_entry = ttk.Entry(login_frame, show="*", width=25)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # --- 登入按鈕 ---
        ttk.Button(login_frame, text="🔑 登入", command=self.attempt_login, style='Login.TButton').grid(row=2, column=0, columnspan=2, pady=15, sticky='we')

        # 綁定 Enter 鍵
        self.login_window.bind('<Return>', lambda event: self.attempt_login())
        
        # 設置焦點
        self.username_entry.focus_set()

    def attempt_login(self):
        """嘗試登入並驗證帳號密碼"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            self.login_window.destroy()  # 關閉登入視窗
            self.master.deiconify()      # 顯示主視窗
            self.on_success_callback()   # 呼叫成功回撥函數來建立主應用程式
        else:
            messagebox.showerror("登入失敗", "帳號或密碼錯誤，請重新輸入。", parent=self.login_window)
            self.password_entry.delete(0, tk.END) # 清空密碼欄位

    def on_closing(self):
        """處理登入視窗關閉事件，強制關閉整個應用程式"""
        if messagebox.askyesno("離開應用程式", "確定要關閉程式嗎？", parent=self.login_window):
            self.master.destroy()

class ExpenseTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("💰 金錢追蹤器")
        master.geometry("1000x600") 
        master.configure(bg='#00E3E3') 
        
        # --- 設定風格與配色 ---
        style = ttk.Style()
        PRIMARY_COLOR = '#000093' # 深藍色
        SECONDARY_COLOR = '#0080FF' # 淺藍色
        
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
                        background='#FF3333', # 紅色
                        font=('Microsoft YaHei', 12, 'bold'),
                        padding=8, 
                        borderwidth=0)
        style.map('Delete.TButton', background=[('active', '#FF6666')])
        
        # 設定表格(Treeview)樣式
        style.configure("Treeview.Heading", font=('Microsoft YaHei', 11, 'bold'), background=SECONDARY_COLOR, foreground='white')
        style.configure("Treeview", rowheight=28)

        # 初始化資料
        self.balance = 0.0
        self.transactions = []
        self.categories = ["飲食", "交通", "娛樂", "購物", "薪資", "投資", "其他"]
        
        # --- 介面佈局：主框架分為左右兩欄 ---
        self.main_paned_window = ttk.PanedWindow(master, orient=tk.HORIZONTAL)
        self.main_paned_window.pack(fill='both', expand=True, padx=10, pady=10)

        # ----------------------------------------------------
        # 區塊 A: 左側 - 餘額和新增交易 (Input/Control)
        # ----------------------------------------------------
        self.left_frame = tk.Frame(self.main_paned_window, bg='#F0F8FF', padx=10, pady=10)
        self.main_paned_window.add(self.left_frame, weight=30) 

        # 1. 餘額顯示區域 (已調整大小)
        self.balance_frame = tk.Frame(self.left_frame, bg='white', padx=10, pady=5, relief=tk.RAISED, borderwidth=1) 
        self.balance_frame.pack(pady=8, fill='x') 

        # 縮小標題字體：從 14 調整為 12
        tk.Label(self.balance_frame, text="💵 當前總餘額:", font=('Microsoft YaHei', 12), bg='white').pack(side=tk.LEFT, padx=5) 
        
        self.balance_var = tk.StringVar(value=f"{self.balance:.2f} 元")
        # 縮小金額字體：從 20 調整為 16
        self.balance_label = tk.Label(self.balance_frame, textvariable=self.balance_var, font=('Microsoft YaHei', 16, 'bold'), bg='white', fg=PRIMARY_COLOR)
        self.balance_label.pack(side=tk.RIGHT, padx=5)

        # 2. 新增記錄輸入區域
        self.input_group = tk.LabelFrame(self.left_frame, text="➕ 新增交易", font=('Microsoft YaHei', 12, 'bold'), bg='#F0F8FF', fg=PRIMARY_COLOR, padx=10, pady=10)
        self.input_group.pack(pady=10, fill='x')
        
        # 交易類型
        tk.Label(self.input_group, text="類型:", bg='#F0F8FF').grid(row=0, column=0, padx=5, pady=8, sticky='w')
        self.type_var = tk.StringVar(value="支出")
        self.type_combo = ttk.Combobox(self.input_group, textvariable=self.type_var, values=["支出", "收入"], state="readonly", width=15)
        self.type_combo.grid(row=0, column=1, padx=5, pady=8, sticky='we')
        
        # 金額
        tk.Label(self.input_group, text="金額:", bg='#F0F8FF').grid(row=1, column=0, padx=5, pady=8, sticky='w')
        self.amount_entry = ttk.Entry(self.input_group, width=20)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=8, sticky='we')

        # 類別
        tk.Label(self.input_group, text="類別:", bg='#F0F8FF').grid(row=2, column=0, padx=5, pady=8, sticky='w')
        self.category_var = tk.StringVar(value=self.categories[0])
        self.category_combo = ttk.Combobox(self.input_group, textvariable=self.category_var, values=self.categories, state="readonly", width=15)
        self.category_combo.grid(row=2, column=1, padx=5, pady=8, sticky='we')
        
        # 備註
        tk.Label(self.input_group, text="備註:", bg='#F0F8FF').grid(row=3, column=0, padx=5, pady=8, sticky='w')
        self.description_entry = ttk.Entry(self.input_group, width=20)
        self.description_entry.grid(row=3, column=1, padx=5, pady=8, sticky='we')

        self.input_group.grid_columnconfigure(1, weight=1) 

        # 3. 新增記錄按鈕 (含 Icon)
        self.button_frame = tk.Frame(self.left_frame, bg='#F0F8FF')
        self.button_frame.pack(pady=15, fill='x')

        ttk.Button(self.button_frame, text="💾 儲存並新增記錄", command=self.add_transaction, style='TButton').pack(fill='x', padx=10)


        # ----------------------------------------------------
        # 區塊 B: 右側 - 交易記錄表格 (Record Table)
        # ----------------------------------------------------
        self.right_frame = tk.Frame(self.main_paned_window, bg='#F0F8FF')
        self.main_paned_window.add(self.right_frame, weight=70) 

        tk.Label(self.right_frame, text="📜 所有交易記錄", font=('Microsoft YaHei', 14, 'bold'), bg='#F0F8FF', fg=PRIMARY_COLOR).pack(pady=10)

        self.tree_frame = tk.Frame(self.right_frame, bg='#F0F8FF')
        self.tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Type", "Amount", "Category", "Desc", "Balance"), show='headings', height=10)
        self.tree.heading("Type", text="類型")
        self.tree.heading("Amount", text="金額")
        self.tree.heading("Category", text="類別")
        self.tree.heading("Desc", text="備註")
        self.tree.heading("Balance", text="餘額")
        
        # 設定欄位寬度
        self.tree.column("Type", width=70, anchor='center')
        self.tree.column("Amount", width=100, anchor='e')
        self.tree.column("Category", width=100, anchor='w')
        self.tree.column("Desc", width=180, anchor='w')
        self.tree.column("Balance", width=120, anchor='e')
        
        self.tree.pack(side='left', fill='both', expand=True)
        
        # 加入滾動條
        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)

        # 設定行顏色標籤 (與配色主題呼應)
        self.tree.tag_configure('income_tag', background='#CCEEFF') 
        self.tree.tag_configure('expense_tag', background='#FFFFFF') 
        
        # --- 新增刪除按鈕框架 ---
        self.delete_frame = tk.Frame(self.right_frame, bg='#F0F8FF')
        self.delete_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(self.delete_frame, 
                   text="🗑️ 刪除選定記錄", 
                   command=self.delete_transaction, 
                   style='Delete.TButton').pack(fill='x')


        # 初始化餘額顯示
        self.update_balance_display()


    def update_balance_display(self):
        """更新餘額顯示標籤的文字和顏色"""
        PRIMARY_COLOR = '#000093' 
        
        self.balance_var.set(f"{self.balance:.2f} 元")
        
        if self.balance >= 0:
            self.balance_label.config(fg=PRIMARY_COLOR)
        else:
            self.balance_label.config(fg="red")

    def update_transaction_list(self):
        """清空並重新載入交易記錄表格，並將內部資料與表格ID綁定"""
        
        # 1. 取得現有的 Treeview 項目 ID
        current_ids = self.tree.get_children()
        
        # 2. 刪除所有舊項目
        for item in current_ids:
            self.tree.delete(item)
            
        # 3. 插入新紀錄 (由最新到最舊顯示)
        # 注意：我們使用 reversed() 來確保最新紀錄在最上方
        # 由於每次更新列表都會重新計算 new_balance，所以我們不用擔心刪除造成的餘額變動
        
        # 這裡需要一個映射來知道 Treeview 的 ID 對應到 self.transactions 列表中的哪個索引
        # 但由於 Treeview ID 是不穩定的，我們將依靠 self.transactions 列表的索引
        # 我們將列表中的交易按原順序賦予一個 ID，但插入時仍是倒序
        
        # 插入新紀錄 (由最新到最舊顯示)
        for index, record in enumerate(reversed(self.transactions)):
            amount_display = f"{record['amount']:.2f}"
            balance_display = f"{record['new_balance']:.2f}"
            tag = 'income_tag' if record['type'] == '收入' else 'expense_tag'
            
            # 使用列表中的索引作為 item ID (在 delete_transaction 時需要用到)
            # 由於是倒序顯示，我們需要計算其在正序列表中的真實索引
            original_index = len(self.transactions) - 1 - index
            
            # 插入項目，將其內部數據ID (Original Index) 作為 iid
            self.tree.insert("", tk.END, iid=original_index, values=(
                record['type'], 
                amount_display, 
                record['category'],
                record['description'],
                balance_display
            ), tags=(tag,))
            
    def recalculate_balance(self):
        """重新計算總餘額並更新所有交易記錄中的 new_balance 欄位"""
        self.balance = 0.0
        for record in self.transactions:
            transaction_amount = record['amount']
            if record['type'] == '支出':
                transaction_amount = -transaction_amount
            
            self.balance += transaction_amount
            record['new_balance'] = self.balance # 更新每筆交易後的餘額
            
        self.update_balance_display()
        self.update_transaction_list()
            
    def delete_transaction(self):
        """刪除選中的交易記錄"""
        selected_item_id = self.tree.focus() # 獲取當前選中項目的 iid (這是我們在 update_transaction_list 中設置的索引)
        
        if not selected_item_id:
            messagebox.showwarning("刪除警告", "請先在表格中選中一條記錄。", parent=self.master)
            return

        try:
            # 獲取 Treeview item ID (即交易在 self.transactions 中的索引)
            # 由於 iid 儲存的是字串，需要轉換為整數
            transaction_index_to_delete = int(selected_item_id) 

            # 彈出確認視窗
            if not messagebox.askyesno("確認刪除", "確定要刪除這筆交易記錄嗎？", parent=self.master):
                return
            
            # 1. 從內部列表中刪除記錄
            # 刪除指定索引的記錄
            del self.transactions[transaction_index_to_delete]
            
            # 2. 重新計算餘額並更新介面
            self.recalculate_balance()
            
            messagebox.showinfo("成功", "交易記錄已刪除。", parent=self.master)

        except IndexError:
            messagebox.showerror("錯誤", "無法找到該交易記錄。", parent=self.master)
        except ValueError:
            messagebox.showerror("錯誤", "選中的項目格式錯誤。", parent=self.master)


    def add_transaction(self):
        """處理新增交易的邏輯"""
        try:
            transaction_type = self.type_var.get()
            category = self.category_var.get()
            amount_str = self.amount_entry.get()
            description = self.description_entry.get().strip()

            if not amount_str or not category:
                messagebox.showerror("輸入錯誤", "金額與類別欄位不能為空！")
                return

            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("輸入錯誤", "金額必須是正數。")
                return

            # 1. 計算新的餘額 (在新增時只需要計算一次)
            transaction_amount_value = -amount if transaction_type == "支出" else amount
            self.balance += transaction_amount_value
            new_balance_after_add = self.balance # 記錄當前的新餘額

            # 2. 建立記錄並儲存
            record = {
                "type": transaction_type,
                "amount": amount,
                "category": category,
                "description": description,
                "new_balance": new_balance_after_add # 儲存交易後的餘額
            }
            self.transactions.append(record)
            
            # 3. 更新介面 (在新增時，需要重新計算所有項目的 new_balance，以確保餘額是正確累積的)
            self.recalculate_balance()

            # 4. 清空輸入欄位
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("輸入錯誤", "金額必須是有效的數字！")
        except Exception as e:
            messagebox.showerror("錯誤", f"發生了一個錯誤: {e}")

# --- 啟動應用程式 ---
def start_app(root):
    """登入成功後的回撥函數，用於建立主應用程式"""
    ExpenseTrackerApp(root)

if __name__ == "__main__":
    root = tk.Tk()
    
    # 在主視窗顯示前，先啟動登入視窗
    login = LoginWindow(root, lambda: start_app(root)) 
    
    root.mainloop()