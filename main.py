from multiprocessing.dummy import Process
        
@staticmethod
def start_service():
    from jnius import autoclass
    service = autoclass("org.mindset.codered.ServiceCodered")
    mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
    service.start(mActivity, "")
    return service

def main():
    start_service()
