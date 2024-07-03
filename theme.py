from gradio.themes.soft import Soft
from gradio.themes.utils import fonts


class CustomTheme(Soft):

    def __init__(self):
        super().__init__(
            font=fonts.GoogleFont("Roboto")
        )

        white = "#FFFFFF"
        purple = "#2F1009D"
        red = "#FC5555"

        primary = white
        secondary = "#e6e6e6"
        panel_color = red
        accent = purple
        accent_soft = "#49637a28"
        
        primary_dark = "#121212"
        secondary_dark = "#242424"
        panel_color_dark = red
        accent_dark = purple
        accent_soft_dark = "#101727"
        text_color_dark = white

        super().set(
            # LIGHT MODE
            body_background_fill=primary,
            background_fill_secondary=primary,
            panel_background_fill=panel_color,
            border_color_primary=primary,
            block_background_fill=secondary,
            block_border_color=primary,
            block_label_background_fill=primary,
            input_background_fill="#DADFE6",
            input_border_color=secondary,
            button_secondary_background_fill=accent,
            button_secondary_text_color=white,
            color_accent_soft=accent_soft,
            border_color_accent_subdued=white,

            # DARK MODE
            body_background_fill_dark=primary_dark,
            background_fill_secondary_dark=secondary_dark,
            panel_background_fill_dark=secondary_dark,
            border_color_primary_dark=primary_dark,
            block_background_fill_dark=secondary_dark,
            block_border_color_dark=secondary_dark,
            block_label_background_fill_dark=primary_dark,
            block_label_text_color_dark=text_color_dark,
            input_background_fill_dark=panel_color_dark,
            input_border_color_dark=secondary_dark,
            button_primary_background_fill_dark=accent_dark,
            button_primary_text_color_dark=primary_dark,
            color_accent_soft_dark=accent_soft_dark,
            border_color_accent_subdued_dark=accent_soft_dark,

            #block_radius="15px",
        )
