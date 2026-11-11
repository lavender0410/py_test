import json


def read_books(file_name: str) -> list:
    """讀取 JSON 檔案，回傳書籍資料的 list。
    file_name 是要讀取的檔名。
    """
    with open(file_name, "r", encoding="utf-8") as file:
        books = json.load(file)
    return books


def write_books(books: list, file_name: str) -> None:
    """把書籍資料寫入 JSON 檔案。
    books 是書籍資料，file_name 是要寫入的檔名。
    """
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(books, file, ensure_ascii=False, indent=4)


def search_books(books: list, keyword: str) -> list:
    """用書名關鍵字查詢書籍。
    books 是書籍資料，keyword 是關鍵字，回傳符合的書籍 list。
    """
    # 都轉小寫再比對，這樣 python 也能找到 Python
    keyword = keyword.lower()
    result = [book for book in books if keyword in book["title"].lower()]
    return result


def show_books(books: list) -> None:
    """顯示書籍資料。
    books 是要顯示的書籍 list。
    """
    if len(books) == 0:
        print("目前沒有書籍資料")
        return

    print("編號  書籍編號  書名                  作者          價格  狀態")

    for number, book in enumerate(books, 1):
        status = "已借出" if book["borrowed"] else "可借閱"
        print(
            f"{number:>4}  {book['id']:<8}  "
            f"{book['title']:<20}  {book['author']:<8}  "
            f"{book['price']:>10,}  {status}"
        )


def input_not_empty(prompt: str) -> str:
    """輸入不能空白的文字，空白就重新輸入。
    prompt 是提示文字，回傳輸入的字串。
    """
    while True:
        text = input(prompt).strip()

        if text != "":
            return text

        print("欄位不可空白，請重新輸入。")


def input_price(prompt: str) -> int:
    """輸入價格，不是大於 0 的整數就重新輸入。
    prompt 是提示文字，回傳價格 (int)。
    """
    while True:
        try:
            price = int(input(prompt).strip())
        except ValueError:
            print("價格須為大於 0 的整數，請重新輸入。")
            continue

        if price > 0:
            return price

        print("價格須為大於 0 的整數，請重新輸入。")


def find_book_index(books: list, book_id: str) -> int:
    """用書籍編號找書。
    books 是書籍資料，book_id 是書籍編號，回傳位置，找不到回傳 -1。
    """
    for index, book in enumerate(books):
        if book["id"] == book_id:
            return index

    return -1


def add_book(books: list) -> None:
    """新增一本書。
    books 是書籍資料，新書會加在最後面。
    """
    # 編號重複就一直重新輸入
    while True:
        book_id = input_not_empty("請輸入書籍編號：")

        if find_book_index(books, book_id) == -1:
            break

        print("書籍編號已存在，請重新輸入。")

    title = input_not_empty("請輸入書名：")
    author = input_not_empty("請輸入作者：")
    price = input_price("請輸入價格：")

    new_book = {
        "id": book_id,
        "title": title,
        "author": author,
        "price": price,
        "borrowed": False
    }

    books.append(new_book)
    print("新增成功。")


def toggle_borrowed(books: list, book_id: str) -> None:
    """變更書籍的借閱狀態。
    books 是書籍資料，book_id 是要變更的書籍編號。
    """
    index = find_book_index(books, book_id)

    if index == -1:
        print("查無此書籍編號")
        return

    # 切換借閱狀態
    book = books[index]
    book["borrowed"] = not book["borrowed"]

    status = "已借出" if book["borrowed"] else "可借閱"
    print(f"「{book['title']}」的狀態已變更為：{status}")


def show_stats(books: list) -> None:
    """顯示最後 3 筆書籍和統計資料。
    books 是書籍資料。
    """
    if len(books) == 0:
        print("目前沒有書籍資料")
        return

    # 用切片取最後 3 筆，不足 3 筆會全部顯示
    print("\n--- 最後 3 筆書籍 ---")
    show_books(books[-3:])

    total = len(books)
    borrowed_count = 0
    price_sum = 0

    # 計算已借出數量和總價
    for book in books:
        if book["borrowed"]:
            borrowed_count += 1

        price_sum += book["price"]

    available_count = total - borrowed_count
    average_price = price_sum / total

    print("\n--- 書籍統計 ---")
    print(f"書籍總數：{total}")
    print(f"可借閱：{available_count}")
    print(f"已借出：{borrowed_count}")
    print(f"價格合計：{price_sum:,} 元")
    print(f"平均價格：{average_price:,.2f} 元")
