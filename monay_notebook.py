import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 

class ExpenseTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("💰 金錢追蹤器")
        master.geometry("1000x600") # 增加寬度以適應左右佈局
        master.configure(bg='#00E3E3') 
        
        # --- 設定風格與配色 ---
        style = ttk.Style()
        PRIMARY_COLOR = '#000093' # 深藍色
        SECONDARY_COLOR = '#0080FF' # 淺藍色
        
        style.configure('.', font=('Microsoft YaHei', 10))
        
        # 設定按鈕樣式
        style.configure('TButton', 
                        foreground='#0080FF', 
                        background=PRIMARY_COLOR, 
                        font=('Microsoft YaHei', 12, 'bold'),
                        padding=8, # 調整 padding
                        borderwidth=0)
        style.map('TButton', background=[('active', SECONDARY_COLOR)])
        
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
        self.main_paned_window.add(self.left_frame, weight=30) # 佔 30% 寬度

        # 1. 餘額顯示區域
        self.balance_frame = tk.Frame(self.left_frame, bg='white', padx=15, pady=10, relief=tk.RAISED, borderwidth=1)
        self.balance_frame.pack(pady=10, fill='x')

        tk.Label(self.balance_frame, text="💵 當前總餘額:", font=('Microsoft YaHei', 14), bg='white').pack(side=tk.LEFT, padx=5)
        
        self.balance_var = tk.StringVar(value=f"{self.balance:.2f} 元")
        self.balance_label = tk.Label(self.balance_frame, textvariable=self.balance_var, font=('Microsoft YaHei', 20, 'bold'), bg='white', fg=PRIMARY_COLOR)
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

        self.input_group.grid_columnconfigure(1, weight=1) # 讓輸入欄位可以擴展

        # 3. 新增記錄按鈕 (含 Icon)
        self.button_frame = tk.Frame(self.left_frame, bg='#F0F8FF')
        self.button_frame.pack(pady=15, fill='x')

        ttk.Button(self.button_frame, text="💾 儲存並新增記錄", command=self.add_transaction, style='TButton').pack(fill='x', padx=10)


        # ----------------------------------------------------
        # 區塊 B: 右側 - 交易記錄表格 (Record Table)
        # ----------------------------------------------------
        self.right_frame = tk.Frame(self.main_paned_window, bg='#F0F8FF')
        self.main_paned_window.add(self.right_frame, weight=70) # 佔 70% 寬度

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

        # 初始化餘額顯示
        self.update_balance_display()


    def update_balance_display(self):
        """更新餘額顯示標籤的文字和顏色"""
        PRIMARY_COLOR = '#0000E3'
        
        self.balance_var.set(f"{self.balance:.2f} 元")
        
        if self.balance >= 0:
            self.balance_label.config(fg=PRIMARY_COLOR)
        else:
            self.balance_label.config(fg="red")

    def update_transaction_list(self):
        """清空並重新載入交易記錄表格"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 插入新紀錄 (由最新到最舊顯示)
        for record in reversed(self.transactions):
            amount_display = f"{record['amount']:.2f}"
            balance_display = f"{record['new_balance']:.2f}"
            tag = 'income_tag' if record['type'] == '收入' else 'expense_tag'
            
            self.tree.insert("", tk.END, values=(
                record['type'], 
                amount_display, 
                record['category'],
                record['description'],
                balance_display
            ), tags=(tag,))

    def add_transaction(self):
        """處理新增交易的邏輯"""
        try:
            # ... (輸入驗證邏輯與之前相同，確保金額是數字且大於 0)
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

            # 2. 處理金額正負並更新餘額
            transaction_amount = -amount if transaction_type == "支出" else amount
            self.balance += transaction_amount

            # 3. 建立記錄並儲存
            record = {
                "type": transaction_type,
                "amount": amount,
                "category": category,
                "description": description,
                "new_balance": self.balance
            }
            self.transactions.append(record)
            
            # 4. 更新介面
            self.update_balance_display()
            self.update_transaction_list()

            # 5. 清空輸入欄位
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("輸入錯誤", "金額必須是有效的數字！")
        except Exception as e:
            messagebox.showerror("錯誤", f"發生了一個錯誤: {e}")

# --- 啟動應用程式 ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()