import pandas as pd
import re
import pprint

pp = pprint.PrettyPrinter(indent=4)

df = pd.read_excel('sales.xlsx', sheet_name='Product report', header=1)
pol = pd.read_excel('sales.xlsx', sheet_name='Paid order list')

print(pol.head())

class Retriever:
    def __init__(self, category_flag, product_flag, paid_order_flag):
        self.category_flag = category_flag
        self.product_flag = product_flag
        self.paid_order_flag = paid_order_flag
        self.current = None
        self.has_variant = False
        
    def populate_categories(self, row):
        if row.iloc[0] == 'Total':
            self.category_flag = False

        if self.category_flag:
            category_items.append({
                "name": row.iloc[0],
                "qty": row.iloc[1],
                "grossSales": row.iloc[2],
                "discComsRewards": row.iloc[3],
                "netSale": row.iloc[4],
                "taxAmount": row.iloc[5],
                "totalSales": row.iloc[6],
                "refund": row.iloc[7]
        })
            
    def populate_products(self, row):
        if self.product_flag:
            if row.iloc[0] == 'Total':
                self.product_flag = False

            if pd.isna(row.iloc[0]):
                self.has_variant = True
                product_items.append({
                    "name": f"{self.current[0]} ({row.iloc[1]})"
                })
            else:
                if self.current is not None and not self.has_variant:
                    product_items.append({
                        "name": self.current[0],
                        "qty": self.current[1],
                        "grossSales": self.current[2]
                    })

                self.current = row
                self.has_variant = False
        
        if row.iloc[0] == 'Product':
            self.product_flag = True

    def populate_paid_order_list(self, row):
        if 'Explanation' in row.iloc[0]:
            self.paid_order_flag = False

        if self.paid_order_flag:
            products = re.split(r',|(?<!\S)x(?!\S)', row.iloc[6])
            product_list = []
            i = 0

            while i < len(products):
                if not products[i].strip():
                    i += 1
                    continue
                name = products[i].strip()
                qty = 0 
                if i + 1 < len(products):
                    next_item = products[i + 1].strip()
                    if next_item.isdigit():
                        qty = int(next_item)
                        i += 1 
                product_list.append({"productName": name, "qty": qty})
                i += 1

            paid_order_items.append({
                "orderId": row.iloc[0],
                "type": row.iloc[1],
                "status": row.iloc[2],
                "table": row.iloc[3],
                "takeUpNumber": row.iloc[4],
                "totalPaid": row.iloc[5],
                "products": product_list,
                "refund": row.iloc[7]
        })

category_items = [];
product_items = [];
paid_order_items = [];

rt = Retriever(True, False, True)

for index, row in pol.iterrows():
    rt.populate_paid_order_list(row);

for index, row, in df.iterrows():
    row_array = row.tolist()
    # rt.populate_categories(row)
    # rt.populate_products(row)

    

pp.pprint(paid_order_items)