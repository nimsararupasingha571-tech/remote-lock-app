from jnius import autoclass, cast
from android.broadcast import BroadcastReceiver

# දුරකථනය Lock කරන function එක
def lock_phone():
    Context = autoclass('android.content.Context')
    DevicePolicyManager = autoclass('android.app.admin.DevicePolicyManager')
    activity = autoclass('org.kivy.android.PythonActivity').mActivity
    policy_manager = activity.getSystemService(Context.DEVICE_POLICY_SERVICE)
    policy_manager.lockNow()

# SMS එකක් ලැබෙනවද කියලා බලන කොටස
class SMSReceiver(BroadcastReceiver):
    def on_receive(self, context, intent):
        # ලැබුණු SMS එකේ විස්තර ලබා ගැනීම
        bundle = intent.getExtras()
        if bundle:
            pdus = bundle.get("pdus")
            for pdu in pdus:
                msg = autoclass('android.telephony.SmsMessage').createFromPdu(pdu)
                message_body = msg.getMessageBody()
                
                # මෙතන තමයි වැදගත්ම දේ: SMS එකේ #LOCK කියලා තිබුණොත් ලොක් කරනවා
                if "#LOCK" in message_body:
                    lock_phone()

# Receiver එක පණ ගැන්වීම
receiver = SMSReceiver(lambda x, y: None, actions=['android.provider.Telephony.SMS_RECEIVED'])
receiver.start()