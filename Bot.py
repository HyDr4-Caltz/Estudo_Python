import dearpygui.dearpygui as dpg
from dearpygui.dearpygui import set_global_font_scale
from Config_Bot import executar_bot, encerrar_bot

contato_alvo = ''
subir = 0


def comecar_callback(sender, app_data, user_data):
    """Inicia o bot ao clicar no botão 'Iniciar Bot'."""
    global contato_alvo, subir
    contato_alvo = dpg.get_value("input_contato")
    print(f'Contato alvo: {contato_alvo}')

    subir = dpg.get_value("subir")
    print(f'Páginas que irá subir: {subir}')

    executar_bot(contato_alvo, subir)


def sair_callback(sender, app_data, user_data):
    """Encerra o bot e fecha a interface."""
    encerrar_bot()
    dpg.destroy_context()


def main():
    dpg.create_context()
    set_global_font_scale(1.25)

    with dpg.window(label="Bot WhatsApp", width=400, height=300):
        dpg.add_text("Informe o nome do contato:")
        dpg.add_input_text(label="Nome Contato", tag="input_contato", width=300)
        dpg.add_text("Informe a quantidade de páginas que quer subir:")
        dpg.add_input_int(label="Páginas", tag="subir", width=300, min_value=1)
        dpg.add_button(label="Iniciar Bot", callback=comecar_callback)
        dpg.add_text("Resultado:", tag="resultado_text", wrap=400)
        dpg.add_button(label="Sair", callback=sair_callback)


    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 140, 23), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

        with dpg.theme_component(dpg.mvInputInt):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (140, 255, 23), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

        dpg.bind_theme(global_theme)

    dpg.create_viewport(title="WhatsApp Bot Interface", width=500, height=400)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()