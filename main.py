from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView


class TelegramDemo(App):

    def build(self):
        self.running = False
        self.progress_value = 0

        layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        title = Label(
            text="TELEGRAM DEMO",
            font_size=25,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(title)

        subtitle = Label(
            text="CONTROL PANEL",
            size_hint_y=None,
            height=30
        )
        layout.add_widget(subtitle)

        self.channel = TextInput(
            hint_text="Channel Username",
            multiline=False,
            size_hint_y=None,
            height=45
        )
        layout.add_widget(self.channel)

        self.posts = TextInput(
            hint_text="Post Numbers",
            multiline=False,
            size_hint_y=None,
            height=45
        )
        layout.add_widget(self.posts)

        self.proxy = TextInput(
            hint_text="Proxy / Test Configuration",
            multiline=False,
            size_hint_y=None,
            height=45
        )
        layout.add_widget(self.proxy)

        self.progress = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=20
        )
        layout.add_widget(self.progress)

        self.percent = Label(
            text="0%",
            font_size=18,
            size_hint_y=None,
            height=35
        )
        layout.add_widget(self.percent)

        buttons = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=10
        )

        self.start_button = Button(
            text="START"
        )
        self.start_button.bind(
            on_press=self.start_demo
        )

        self.stop_button = Button(
            text="STOP"
        )
        self.stop_button.bind(
            on_press=self.stop_demo
        )

        buttons.add_widget(self.start_button)
        buttons.add_widget(self.stop_button)

        layout.add_widget(buttons)

        self.save_button = Button(
            text="SAVE LOG",
            size_hint_y=None,
            height=50
        )
        self.save_button.bind(
            on_press=self.save_log
        )

        layout.add_widget(self.save_button)

        layout.add_widget(
            Label(
                text="REAL-TIME LOG",
                size_hint_y=None,
                height=30
            )
        )

        self.log = Label(
            text="Ready...",
            size_hint_y=None,
            halign="left",
            valign="top"
        )

        self.log.bind(
            texture_size=self.update_log_height
        )

        scroll = ScrollView()

        scroll.add_widget(self.log)

        layout.add_widget(scroll)

        return layout

    def update_log_height(self, instance, value):
        instance.height = value[1]

    def add_log(self, message):
        self.log.text += "\n" + message

    def start_demo(self, instance):
        if self.running:
            return

        self.running = True
        self.progress_value = 0
        self.progress.value = 0
        self.percent.text = "0%"

        self.log.text = "Demo Started"

        self.add_log(
            "Channel: " +
            (self.channel.text or "Not entered")
        )

        self.add_log(
            "Posts: " +
            (self.posts.text or "Not entered")
        )

        Clock.schedule_interval(
            self.update_progress,
            0.04
        )

    def update_progress(self, dt):
        if not self.running:
            return False

        self.progress_value += 1

        self.progress.value = self.progress_value

        self.percent.text = (
            str(self.progress_value) + "%"
        )

        if self.progress_value % 10 == 0:
            self.add_log(
                "Progress: " +
                str(self.progress_value) + "%"
            )

        if self.progress_value >= 100:
            self.running = False
            self.add_log(
                "Demo completed successfully."
            )
            return False

        return True

    def stop_demo(self, instance):
        self.running = False
        self.add_log("Process stopped.")

    def save_log(self, instance):
        try:
            path = (
                "/storage/emulated/0/"
                "Download/telegram_demo_log.txt"
            )

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as file:
                file.write(self.log.text)

            self.add_log(
                "Log saved to Download folder."
            )

        except Exception as error:
            self.add_log(
                "Save error: " + str(error)
            )


TelegramDemo().run()
