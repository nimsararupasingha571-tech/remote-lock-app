from kivy.app import App
from kivy.uix.label import Label
from jnius import autoclass

# Android වල ප්‍රධාන කොටස්
DevicePolicyManager = autoclass('android.app.admin.DevicePolicyManager')
Context = autoclass('android.content.Context')
ComponentName = autoclass('android.content.ComponentName')

class RemoteLockApp(App):
    def build(self):
        return Label(text="Remote Lock App is Running...")

    def on_start(self):
        # App එක පටන් ගත්තම Admin බලය තියෙනවද බලනවා
        self.check_admin()

    def check_admin(self):
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        policy_manager = activity.getSystemService(Context.DEVICE_POLICY_SERVICE)
        # මෙතනින් තමයි App එකේ නම පද්ධතියට හඳුන්වා දෙන්නේ
        app_admin = ComponentName(activity.getPackageName(), "org.kivy.android.PythonActivity")
        
        if not policy_manager.isAdminActive(app_admin):
            print("කරුණාකර Settings වලට ගොස් Admin Permission දෙන්න.")

if __name__ == '__main__':
    RemoteLockApp().run()