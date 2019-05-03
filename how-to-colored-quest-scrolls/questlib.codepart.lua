
function send_letter_ex(name, icon_type, icon_name) make_quest_button_ex(name, icon_type, icon_name) set_skin(NOWINDOW) q.set_title(name) q.set_icon(icon_name) q.start() end
function resend_letter_ex(name, icon_type, icon_name) make_quest_button_ex(name, icon_type, icon_name) q.set_title(name) q.set_icon(icon_name) q.start() end
function resend_letter(title) makequestbutton(title) q.set_title(title) q.start() end
