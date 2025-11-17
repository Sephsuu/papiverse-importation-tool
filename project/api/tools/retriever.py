import pandas as pd
import re
import math

def to_float(value):
    if pd.isna(value) or str(value).strip() in ["", "-", "–"]:
        return 0.0
    value = str(value)
    value = re.sub(r'[^\d.\-]', '', value)  # removes everything except digits, dot, minus
    return float(value) if value else 0.0

class Retriever:
    def __init__(self):
        self.category_flag = True
        self.product_flag = False
        self.paid_order_flag = True
        self.current = None
        self.has_variant = False
        self.category_items = []
        self.product_items = []
        self.paid_order_items = []
        
    def populate_categories(self, row):
        if row.iloc[0] == 'Total':
            self.category_flag = False

        if self.category_flag:
            self.category_items.append({
                "name": row.iloc[0],
                "qty": float(row.iloc[1].replace(",", "")),
                "grossSales": float(row.iloc[2].replace(",", "")),
                "discCompsRewards": float(row.iloc[3].replace(",", "")),
                "netSale": float(row.iloc[4].replace(",", "")),
                "taxAmount": float(row.iloc[5].replace(",", "")),
                "totalSales": float(row.iloc[6].replace(",", "")),
                "refund": float(row.iloc[7].replace(",", ""))
        })
            
    def populate_products(self, row):
        if self.product_flag:
            if row.iloc[0] == 'Total':
                self.product_flag = False

            if pd.isna(row.iloc[0]):
                self.has_variant = True
                self.product_items.append({
                    "name": f"{self.current[0]} ({row.iloc[1]})"
                })
            else:
                if self.current is not None and not self.has_variant:
                    self.product_items.append({
                        "name": self.current[0],
                        "specification": self.current[1],
                        "qty": float(row.iloc[2].replace(",", "")),
                        "grossSales": float(self.current[3].replace(",", "")),
                        "discCompsRewards": float(self.current[4].replace(",", "")),
                        "netSale": float(self.current[5].replace(",", "")),
                        "taxAmount": float(self.current[6].replace(",", "")),
                        "totalSales": float(self.current[7].replace(",", "")),
                        "refund": float(self.current[8].replace(",", ""))
                    })

                self.current = row
                self.has_variant = False
        
        if row.iloc[0] == 'Product':
            self.product_flag = True

    def populate_paid_order_list(self, row):
        if pd.notna(row.iloc[0]) and "Explanation" in str(row.iloc[0]):
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
                matches = re.findall(r'\(Default/([^)]+)\)', name)
                
                modifiers = []
                for m in matches:
                    modifiers.extend(m.split('/'))

                cleaned = re.sub(r'\(Default[^)]*\)', '', name).strip()

                product_list.append({
                    "productName": cleaned, 
                    "quantity": qty,
                    "modifiers": modifiers
                })

                i += 1

            self.paid_order_items.append({
                "orderId": row.iloc[0],
                "orderType": row.iloc[1],
                "orderStatus": row.iloc[2],
                # "table": row.iloc[3],
                # "takeUpNumber": row.iloc[4],
                "totalPaid": to_float(row.iloc[5]),
                "items": product_list,
                # "abnormalQuantity": int(row.iloc[7]),
                "productQty": int(row.iloc[8]),
                "productAmount": to_float(row.iloc[9]),
                # "productNeeding": row.iloc[10],
                # "serviceCharge": row.iloc[11],
                # "additionalCharge": row.iloc[12],
                # "temporaryCharge": row.iloc[13],
                # "packingCharge": row.iloc[14],
                # "dishesDiscount": row.iloc[15],
                # "orderDiscount": row.iloc[16],
                # "discountVoucher": row.iloc[17],
                # "deliveryCharge": row.iloc[18],
                "cash": to_float(row.iloc[21]),
                "gcash": to_float(row.iloc[22]),
                # "transactionFee": row.iloc[23],
                "receivedAmount": to_float(row.iloc[24]),
                # "source": row.iloc[27],
                "cashier": row.iloc[28],
                "paymentTime": row.iloc[29],

        })

        return self.paid_order_items

    def clean_data(self, data):
        if isinstance(data, list):
            return [self.clean_data(item) for item in data]
        elif isinstance(data, dict):
            return {k: self.clean_data(v) for k, v in data.items()}
        elif isinstance(data, float) and math.isnan(data):
            return None
        return data



