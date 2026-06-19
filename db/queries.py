from db.main_db import get_connection

def get_all_items():
    """Получить все товары из БД"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, is_bought FROM items")
    items = cursor.fetchall()
    conn.close()
    return items

def add_item(name: str):
    """Добавить новый товар и вернуть его ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, is_bought) VALUES (?, 0)", (name,))
    item_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return item_id

def toggle_item(item_id: int, is_bought: bool):
    """Обновить статус покупки (куплено/нет)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET is_bought = ? WHERE id = ?", (int(is_bought), item_id))
    conn.commit()
    conn.close()

def delete_item(item_id: int):
    """Удалить товар по ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()