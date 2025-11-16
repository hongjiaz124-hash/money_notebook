import tkinter as tk
from tkinter import messagebox
from tkinter import ttk # 用來顯示下拉選單和表格

class ExpenseTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("💰 簡易金錢追蹤器 (V2)")
        master.geometry("650x500")

        # 初始化資料
        self.balance = 0.0
        self.transactions = []
        
        # 定義預設的類別選項
        self.categories = ["飲食", "交通", "娛樂", "購物", "薪資", "投資", "其他"]
        
        # --- 建立使用者介面 (UI) ---
        
        # 1. 餘額顯示區域
        self.balance_frame = tk.Frame(master, padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
        self.balance_frame.pack(pady=10, fill='x')

        tk.Label(self.balance_frame, text="目前總餘額:", font=('Arial', 14)).pack(side=tk.LEFT, padx=10)
        
        self.balance_var = tk.StringVar(value=f"{self.balance:.2f} 元")
        self.balance_label = tk.Label(self.balance_frame, textvariable=self.balance_var, font=('Arial', 18, 'bold'), fg="green")
        self.balance_label.pack(side=tk.RIGHT, padx=10)

        # 2. 新增記錄輸入區域 (使用 LabelFrame 分組)
        self.input_group = tk.LabelFrame(master, text="新增交易", padx=10, pady=10)
        self.input_group.pack(pady=5, padx=10, fill='x')
        
        # Row 0: 交易類型下拉選單
        tk.Label(self.input_group, text="交易類型:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.type_var = tk.StringVar(value="支出") # 預設為支出
        self.type_combo = ttk.Combobox(self.input_group, textvariable=self.type_var, values=["支出", "收入"], state="readonly", width=12)
        self.type_combo.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # Row 0: 金額輸入
        tk.Label(self.input_group, text="金額 (絕對值):").grid(row=0, column=2, padx=10, pady=5, sticky='w')
        self.amount_entry = tk.Entry(self.input_group, width=15)
        self.amount_entry.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        # Row 1: 類別下拉選單
        tk.Label(self.input_group, text="類別:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.category_var = tk.StringVar(value=self.categories[0]) # 預設為第一個選項
        self.category_combo = ttk.Combobox(self.input_group, textvariable=self.category_var, values=self.categories, state="readonly", width=12)
        self.category_combo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        # Row 1: 描述/備註輸入
        tk.Label(self.input_group, text="備註 (選填):").grid(row=1, column=2, padx=10, pady=5, sticky='w')
        self.description_entry = tk.Entry(self.input_group, width=20)
        self.description_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # 3. 合併的新增按鈕
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=5)

        tk.Button(self.button_frame, text="✅ 新增記錄", command=self.add_transaction, font=('Arial', 12, 'bold'), bg='lightblue', width=20).pack(padx=10)
        
        # 4. 交易記錄表格 (Treeview)
        self.tree = ttk.Treeview(master, columns=("Type", "Amount", "Category", "Desc", "Balance"), show='headings', height=10)
        self.tree.heading("Type", text="類型")
        self.tree.heading("Amount", text="金額")
        self.tree.heading("Category", text="類別")
        self.tree.heading("Desc", text="備註")
        self.tree.heading("Balance", text="餘額")
        
        # 設定欄位寬度
        self.tree.column("Type", width=60, anchor='center')
        self.tree.column("Amount", width=80, anchor='e')
        self.tree.column("Category", width=80, anchor='w')
        self.tree.column("Desc", width=150, anchor='w')
        self.tree.column("Balance", width=100, anchor='e')
        
        self.tree.pack(padx=10, pady=10, fill='x')

        # 初始化表格顏色標籤
        self.tree.tag_configure('income_tag', background='#e0ffe0') # 淺綠色
        self.tree.tag_configure('expense_tag', background='#ffe0e0') # 淺紅色

    def update_balance_display(self):
        """更新餘額顯示標籤的文字和顏色"""
        self.balance_var.set(f"{self.balance:.2f} 元")
        
        # 根據餘額正負改變顏色
        if self.balance >= 0:
            self.balance_label.config(fg="green")
        else:
            self.balance_label.config(fg="red")

    def update_transaction_list(self):
        """清空並重新載入交易記錄表格"""
        # 清空所有舊紀錄
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
            # 1. 取得並驗證輸入
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
            # 支出時，將正數金額轉為負數來扣除
            transaction_amount = -amount if transaction_type == "支出" else amount
            
            self.balance += transaction_amount

            # 3. 建立記錄並儲存
            record = {
                "type": transaction_type,
                "amount": amount, # 儲存正數的絕對金額
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