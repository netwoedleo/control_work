import flet as ft
from db.main_db import init_db
from db.queries import get_all_items, add_item, toggle_item, delete_item

def main(page: ft.Page):
    page.title = "Список покупок"
    page.window_width = 400
    page.window_height = 600

    init_db()

    new_item = ft.TextField(hint_text="Что купить?", expand=True)
    items_list = ft.Column()

    filter_radio = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="Все", label="Все"),
            ft.Radio(value="Купленные", label="Купленные"),
            ft.Radio(value="Некупленные", label="Некупленные"),
        ]),
        value="Все",
        on_change=lambda e: load_data()
    )

    def load_data():
        items_list.controls.clear() 
        status = filter_radio.value
        
        for item_id, name, is_bought in get_all_items():
            if status == "Купленные" and not is_bought:
                continue
            if status == "Некупленные" and is_bought:
                continue
                
            checkbox = ft.Checkbox(label=name, value=bool(is_bought), data=item_id, on_change=toggle)
            
            del_btn = ft.GestureDetector(
                content=ft.Text("[X]", color="red", size=16),
                data=item_id,
                on_tap=delete
            )
            
            items_list.controls.append(ft.Row([checkbox, del_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
            
        page.update()

    def toggle(e):
        toggle_item(e.control.data, e.control.value)
        load_data()

    def delete(e):
        delete_item(e.control.data)
        load_data()

    def add_click(e):
        if new_item.value:
            add_item(new_item.value)
            new_item.value = ""
            load_data()

    page.add(
        ft.Row([new_item, ft.FilledButton("ADD", on_click=add_click)]),
        filter_radio,
        items_list
    )

    load_data()

if __name__ == "__main__":
    ft.run(main)