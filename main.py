import pandas as pd
from segno import helpers
import smtplib
import imghdr
from email.message import EmailMessage

df_email = pd.read_csv("responses4.csv")
print("Total Record Count: " + str(df_email.count()))
df_email = df_email[df_email['Payment'].str.lower() == "ok"]
print("--------------------------------------------------")
print("Total OK Record Count: " + str(df_email.count()))

# Your Credentials here
Sender_Email = "user@gmail.com"
Password = "password"

email_list = df_email["Email Address"].tolist()
name_list_first_name = df_email["First Name"].tolist()
name_list_last_name = df_email["Last Name"].tolist()
number_list = df_email["Number"].tolist()
contact_list = df_email["Contact Number"].tolist()
Reference_list = df_email["Reference Number (Transaction ID)"].tolist()

print("--------------------------------------------------")
print("---Starting QR and Email Service---")
for x in range(len(email_list)):
    qrcode = helpers.make_mecard(
        # url=str(x + 1) +"_PAYMENT_CONFIRMED",
        url=str(number_list[x]) + "_PAYMENT_CONFIRMED",
        name=name_list_first_name[x].strip()
             + ' '
             + name_list_last_name[x].strip(),
        email=str(email_list[x]),
        phone=str(contact_list[x]))

    # imageName = './QR_IMAGES/'+ str(x + 1)+ '_'+ name_list_first_name[x].strip()+ '.png'
    imageName = './QR_IMAGES/' + str(number_list[x]) + '_' + name_list_first_name[x].strip() + '.png'

    qrcode.save(imageName, scale=5)
    Reciever_Email = email_list[x]

    newMessage = EmailMessage()
    newMessage['Subject'] = "Ticket Purchase Confirmation For DS අවාරේ Event"
    newMessage['From'] = Sender_Email
    newMessage['To'] = Reciever_Email
    newMessage.set_content('Please show the Attached QR for the bouncer for entry. Enjoy and have a blast!!!')

    with open(imageName, 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name

    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Sender_Email, Password)
        print("Sending Email to: " + str(Reciever_Email) + " " + imageName)
        smtp.send_message(newMessage)

print("Program Successfully Completed...")
