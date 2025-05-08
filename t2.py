from send_text import WhatsApp

no = "917975201973"
wa = WhatsApp(no)
wa.login()
wa.send_text(no, "Hello from Python!")
