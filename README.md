Pembuatan API
a) Buat API dengan Flask dan Database MongoDB
b) Buat data penjualan:
i. Collection Customer
Field: - name type char
- handphone type char
ii. Collection Product
Field: - name type char
- unit_price type Float
- stock type Integer
iii. Collection Sales
Field: - customer_id relasi ke Customer
- product_id relasi ke Product
- unit_price relasi ke Product.unit_price
- qty type Integer
- total_price type Float
c) Buatkan API CRUD untuk masing-masing collection tersebu
