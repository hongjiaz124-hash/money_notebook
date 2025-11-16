import tkinter as tk
from tkinter import messagebox
from tkinter import ttk # 用來顯示表格的 Treeview

class ExpenseTrackerApp:
    def __init__(self, master):
        # 設置主視窗
        self.master = master
        master.title("💰 簡易金錢追蹤器")
        master.geometry("600x500") # 設定視窗大小

        # 初始化資料
        self.balance = 0.0
        self.transactions = []

        # --- 建立使用者介面 (UI) ---

        # 1. 餘額顯示區域
        self.balance_frame = tk.Frame(master, padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
        self.balance_frame.pack(pady=10, fill='x')

        tk.Label(self.balance_frame, text="目前總餘額:", font=('Arial', 14)).pack(side=tk.LEFT, padx=10)
        
        self.balance_var = tk.StringVar(value=f"{self.balance:.2f} 元")
        self.balance_label = tk.Label(self.balance_frame, textvariable=self.balance_var, font=('Arial', 18, 'bold'), fg="green")
        self.balance_label.pack(side=tk.RIGHT, padx=10)

        # 2. 新增記錄輸入區域
        self.input_frame = tk.Frame(master, padx=10, pady=10)
        self.input_frame.pack(pady=5)
        
        # 金額輸入
        tk.Label(self.input_frame, text="金額 (絕對值):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.amount_entry = tk.Entry(self.input_frame, width=15)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        # 類別輸入
        tk.Label(self.input_frame, text="類別:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.category_entry = tk.Entry(self.input_frame, width=15)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # 描述/備註輸入
        tk.Label(self.input_frame, text="備註 (選填):").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.description_entry = tk.Entry(self.input_frame, width=15)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)

        # 3. 按鈕區域
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        # 新增收入按鈕
        tk.Button(self.button_frame, text="➕ 記為收入", command=lambda: self.add_transaction("收入"), bg='light green').pack(side=tk.LEFT, padx=10)
        
        # 新增支出按鈕
        tk.Button(self.button_frame, text="➖ 記為支出", command=lambda: self.add_transaction("支出"), bg='salmon').pack(side=tk.LEFT, padx=10)
        
        # 4. 交易記錄表格 (使用 Treeview)
        self.tree = ttk.Treeview(master, columns=("Type", "Amount", "Category", "Balance"), show='headings', height=8)
        self.tree.heading("Type", text="類型")
        self.tree.heading("Amount", text="金額")
        self.tree.heading("Category", text="類別")
        self.tree.heading("Balance", text="餘額")
        
        # 設定欄位寬度
        self.tree.column("Type", width=80, anchor='center')
        self.tree.column("Amount", width=100, anchor='e')
        self.tree.column("Category", width=120, anchor='w')
        self.tree.column("Balance", width=120, anchor='e')
        
        self.tree.pack(padx=10, pady=10, fill='x')

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
            # 格式化金額顯示
            amount_display = f"{record['amount']:.2f}"
            balance_display = f"{record['new_balance']:.2f}"
            
            # 決定顏色標籤 (tag)
            tag = 'income_tag' if record['type'] == '收入' else 'expense_tag'
            
            self.tree.insert("", tk.END, values=(
                record['type'], 
                amount_display, 
                record['category'], 
                balance_display
            ), tags=(tag,))

        # 設定表格顏色 (可選)
        self.tree.tag_configure('income_tag', background='#e0ffe0') # 淺綠色
        self.tree.tag_configure('expense_tag', background='#ffe0e0') # 淺紅色

    def add_transaction(self, transaction_type):
        """處理新增交易的邏輯"""
        try:
            # 1. 取得並驗證輸入
            amount_str = self.amount_entry.get()
            category = self.category_entry.get().strip()
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
            self.category_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("輸入錯誤", "金額必須是有效的數字！")
        except Exception as e:
            messagebox.showerror("錯誤", f"發生了一個錯誤: {e}")

# --- 啟動應用程式 ---
if __name__ == "__main__":
    # 建立主視窗物件
    root = tk.Tk()
    
    # 建立應用程式實例
    app = ExpenseTrackerApp(root)
    
    # 進入主循環，讓視窗保持開啟並等待使用者操作
    root.mainloop()