
from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button

Window.clearcolor = (0.035, 0.025, 0.055, 1)

PURPLE = (0.48, 0.20, 0.82, 1)
DARK = (0.09, 0.06, 0.13, 1)
WHITE = (0.96, 0.93, 1, 1)
MUTED = (0.68, 0.62, 0.76, 1)

CATALOG = {
    "SKINS": [
        "AK-47 | Neon Rider",
        "AK-47 | Redline",
        "AWP | Dragon Lore",
        "AWP | Asiimov",
        "M4A4 | Howl",
        "M4A1-S | Printstream",
        "USP-S | Kill Confirmed",
        "Desert Eagle | Blaze",
        "Glock-18 | Fade"
    ],
    "KNIVES": [
        "Karambit | Doppler",
        "Karambit | Fade",
        "M9 Bayonet | Lore",
        "M9 Bayonet | Autotronic",
        "Butterfly Knife | Fade",
        "Bayonet | Marble Fade",
        "Talon Knife | Crimson Web"
    ],
    "GLOVES": [
        "Sport Gloves | Pandora",
        "Sport Gloves | Vice",
        "Driver Gloves | King Snake",
        "Specialist Gloves | Fade",
        "Moto Gloves | Spearmint",
        "Hand Wraps | Cobalt Skulls"
    ]
}


class CFMenu(App):

    def build(self):
        self.title = "CF MOD MENU 3.0"

        self.weapon = CATALOG["SKINS"][0]
        self.knife = CATALOG["KNIVES"][0]
        self.gloves = CATALOG["GLOVES"][0]

        self.wh = False
        self.aim = False
        self.page = "HOME"

        root = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(7)
        )

        header = BoxLayout(
            size_hint_y=None,
            height=dp(58),
            spacing=dp(10)
        )

        header.add_widget(Label(
            text="CF",
            color=PURPLE,
            bold=True,
            font_size="28sp",
            size_hint_x=None,
            width=dp(50)
        ))

        header.add_widget(Label(
            text="CF MOD MENU 3.0\n"
                 "[size=10sp]ANDROID EDITION[/size]",
            markup=True,
            color=WHITE,
            font_size="16sp",
            halign="left"
        ))

        root.add_widget(header)

        nav = GridLayout(
            cols=3,
            spacing=dp(5),
            size_hint_y=None,
            height=dp(100)
        )

        for page in [
            "HOME", "SKINS", "KNIVES",
            "GLOVES", "VISUALS", "ABOUT"
        ]:
            btn = self.button(page, PURPLE)
            btn.bind(
                on_release=lambda obj, p=page:
                self.show_page(p)
            )
            nav.add_widget(btn)

        root.add_widget(nav)

        self.status = Label(
            text="● READY",
            color=(0.35, 0.85, 0.6, 1),
            size_hint_y=None,
            height=dp(24),
            font_size="11sp"
        )
        root.add_widget(self.status)

        scroll = ScrollView(do_scroll_x=False)

        self.content = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=[0, dp(5), 0, dp(12)],
            size_hint_y=None
        )

        self.content.bind(
            minimum_height=self.content.setter("height")
        )

        scroll.add_widget(self.content)
        root.add_widget(scroll)

        self.show_page("HOME")
        return root

    def button(self, text, color=DARK):
        return Button(
            text=text,
            size_hint_y=None,
            height=dp(46),
            background_normal="",
            background_down="",
            background_color=color,
            color=WHITE,
            font_size="12sp",
            bold=True
        )

    def label(self, text, height=38, color=WHITE, size=14):
        item = Label(
            text=text,
            color=color,
            font_size=f"{size}sp",
            size_hint_y=None,
            height=dp(height),
            halign="left",
            valign="middle"
        )

        item.bind(
            size=lambda obj, val:
            setattr(obj, "text_size", (val[0], None))
        )

        self.content.add_widget(item)

    def add_button(self, text, callback, color=PURPLE):
        btn = self.button(text, color)
        btn.bind(on_release=callback)
        self.content.add_widget(btn)

    def show_page(self, page):
        self.page = page
        self.content.clear_widgets()

        if page == "HOME":
            self.home()
        elif page in CATALOG:
            self.catalog(page)
        elif page == "VISUALS":
            self.visuals()
        else:
            self.about()

    def home(self):
        self.label("YOUR LOADOUT", 42, PURPLE, 19)

        self.label("WEAPON", 25, MUTED, 11)
        self.label(self.weapon, 36, WHITE, 14)
        self.add_button(
            "CHANGE WEAPON",
            lambda *_: self.show_page("SKINS")
        )

        self.label("KNIFE", 25, MUTED, 11)
        self.label(self.knife, 36, WHITE, 14)
        self.add_button(
            "CHANGE KNIFE",
            lambda *_: self.show_page("KNIVES")
        )

        self.label("GLOVES", 25, MUTED, 11)
        self.label(self.gloves, 36, WHITE, 14)
        self.add_button(
            "CHANGE GLOVES",
            lambda *_: self.show_page("GLOVES")
        )

        self.label("QUICK MENU", 35, PURPLE, 15)
        self.add_button(
            "VISUALS & SETTINGS",
            lambda *_: self.show_page("VISUALS")
        )

    def catalog(self, category):
        self.label(category + " CATALOG", 42, PURPLE, 19)

        field = {
            "SKINS": "weapon",
            "KNIVES": "knife",
            "GLOVES": "gloves"
        }[category]

        current = getattr(self, field)

        self.label("Selected: " + current, 44, MUTED, 12)

        for item in CATALOG[category]:
            selected = item == current

            btn = self.button(
                ("✓  " if selected else "") + item,
                PURPLE if selected else DARK
            )

            btn.bind(
                on_release=lambda obj, value=item, f=field:
                self.select_item(f, value)
            )

            self.content.add_widget(btn)

    def select_item(self, field, value):
        setattr(self, field, value)
        self.status.text = "● SELECTED"
        self.show_page(self.page)

    def visuals(self):
        self.label("VISUAL SETTINGS", 42, PURPLE, 19)

        self.add_button(
            "WH DEMO: " + ("ON" if self.wh else "OFF"),
            self.toggle_wh
        )

        self.add_button(
            "AIM DEMO: " + ("ON" if self.aim else "OFF"),
            self.toggle_aim
        )

        self.label(
            "These switches are demonstrations only.",
            50, MUTED, 11
        )

    def toggle_wh(self, *_):
        self.wh = not self.wh
        self.status.text = "● WH DEMO UPDATED"
        self.show_page("VISUALS")

    def toggle_aim(self, *_):
        self.aim = not self.aim
        self.status.text = "● AIM DEMO UPDATED"
        self.show_page("VISUALS")

    def about(self):
        self.label("ABOUT CF MENU", 42, PURPLE, 19)
        self.label(
            "Version 3.0\n\n"
            "Android / Pydroid 3\n"
            "Black + Purple UI\n\n"
            "Local visual configurator.\n"
            "No CFG files or JSON storage.\n\n"
            "Selections reset when the app restarts.",
            180, WHITE, 13
        )


if __name__ == "__main__":
    CFMenu().run()
