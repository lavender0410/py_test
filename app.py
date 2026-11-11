import json

from pkg.book_tools import (read_books, show_books, add_book, input_not_empty,
                            search_books, toggle_borrowed, show_stats,
                            write_books)


def main() -> None:
    """主程式，讀入書籍資料後顯示主選單。"""
    # 先讀檔，讀不到就直接結束
    try:
        books = read_books("books.json")
    except FileNotFoundError:
        print("找不到 books.json，程式結束。")
        return
    except json.JSONDecodeError:
        print("books.json 的 JSON 格式錯誤，程式結束。")
        return
    except OSError as error:
        print(f"無法讀取 books.json：{error}")
        return

    while True:
        print("\n--- 簡易書籍管理系統 ---")
        print("1. 顯示全部書籍")
        print("2. 新增書籍")
        print("3. 查詢書籍")
        print("4. 變更借閱狀態")
        print("5. 顯示最後 3 筆書籍與統計")
        print("6. 匯出書籍資料")
        print("7. 離開系統")
        print("------------------------")

        choice = input("請選擇功能：").strip()

        if choice == "1":
            print("\n--- 全部書籍 ---")
            show_books(books)

        elif choice == "2":
            add_book(books)

        elif choice == "3":
            keyword = input_not_empty("請輸入書名關鍵字：")
            result = search_books(books, keyword)

            print("\n--- 查詢結果 ---")
            if len(result) == 0:
                print("查無符合的書籍")
            else:
                show_books(result)

        elif choice == "4":
            book_id = input("請輸入書籍編號：").strip()
            toggle_borrowed(books, book_id)

        elif choice == "5":
            show_stats(books)

        elif choice == "6":
            # 寫入失敗會跳到 except，不會印出匯出成功
            try:
                write_books(books, "output.json")
                print(f"已匯出 {len(books)} 筆書籍資料至 output.json。")
            except OSError as error:
                print(f"無法匯出資料：{error}")

        elif choice == "7":
            print("系統已退出。")
            break

        else:
            print("輸入錯誤，請輸入 1～7 的數字。")


main()
