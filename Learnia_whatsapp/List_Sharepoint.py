from .Autenticacion_sharepoint import auth_sharepoint
import json

context = auth_sharepoint()


def upload_list_sharepoint(tel, name, message, respuesta):
    sp_list = context.web.lists.get_by_title(
        "Development_Colibrí"
    )  # CONECTAMOS A LA LISTA
    # Define la nueva interacción
    new_interaction = [
        {"from": {"role": 1}, "text": message},
        {"from": {"role": 0}, "text": respuesta},
    ]

    # Busca en la lista un elemento con el mismo User_ID
    items = sp_list.get_items()
    context.load(items)
    context.execute_query()

    for item in items:
        if item.properties["User_ID"] == tel:
            # Si el elemento existe, obtén el contenido actual
            current_content = json.loads(item.properties["Content"], strict=False)

            # Agrega la nueva interacción a las actividades actuales
            current_content["activities"].extend(new_interaction)

            # Actualiza el campo Content con las nuevas actividades
            item.set_property(
                "Content", json.dumps(current_content, ensure_ascii=False)
            )
            item.update()
            context.execute_query()
            return

    # Si el elemento no existe, crea uno nuevo
    conv = {
        "User_Name": name,
        "User_ID": tel,
        "Content": json.dumps({"activities": new_interaction}),
    }

    # Agrega un elemento a la lista
    sp_list.add_item(conv)
    sp_list.execute_query()
