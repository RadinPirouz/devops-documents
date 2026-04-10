# آموزش نصب و تنظیم SMB در لینوکس
 یا Server Message Block پروتکلی جهت به اشتراک گذاری فایل ها، چاپگرها و پورتهای سریال است. از این پروتکل می توان بر روی پروتکل TCP/IP یا بر روی دیگر پروتکل های شبکه استفاده کرد.
 
 **این آموزش فقط روی Ubuntu 22.04 LTS آزمایش و تست شده است. اگر می خواهید روی Ubuntu Server از این آموزش استفاده کنید. به جای gedit از nano یا vim استفاده کنید**

## مرحله اول: نصب Samba
پروتکل SMB در لینوکس با Samba پیاده سازی می شود برای نصب Samba از دستور زیر استفاده کنید

	sudo apt update
	sudo apt install samba

**اختیاری:** با استفاده از دستور زیر از نصب بودن Samba اطمینان پیدا کنید

	whereis samba

## مرحله دوم: تنظیمات Samba
نخست یک پوشه با نام و مسیر دلخواه که می خواهید آن را به اشتراک بگذارید بسازید یا انتخاب کنید. من با دستور زیر پوشه ای برای این پروژه می سازم

	mkdir /home/mahdiyar/smbshare

**نکته: به جای Mahdiyar ُ نام کاربری خود را جایگزین کنید**
فایل تنظیمات **Samba** را با دستور زیر باز کنید

	sudo gedit /etc/samba/smb.conf

۵ خط کد زیر را به آخر فایل اضافه کنید

	[sambashare]
	comment = Mahdiyar XPS File Share
	path = /home/mahdiyar/smbshare
	read only = no
	browsable = yes
   
**نکته مهم:** به جای `/home/mahdiyar/smbshare` آدرس پوشه ای را که برای اشتراک گذاری انتخاب کردید قرار دهید

  **نکته مهم:** به جای `Mahdiyar XPS File Share` متنی دلخواه که پوشه شما را توصیف می کند قرار دهید
  
  با دستور زیر Smaba را Restart کرده و اطمینان پیدا کنید که به درستی کار می کند
  

	sudo service smbd restart
	sudo service smbd status


اگر از فایروال استفاده می کنید با دستور زیر Samba را به فایروال اضافه کنید

	sudo ufw allow samba


با دستور زیر رمز عبوری برای Samba مشخص کنید

	sudo smbpasswd -a username

**نکته مهم: username حتما باید نام کاربری شما در Ubuntu باشد**

## مرحله سوم: استفاده از SMB
حالا که سرور را آماده کردیم نوبت به استفاده از فولدری که به اشتراک گذاشتیم رسیده است

با دستور زیر در لینوکس IP سرور خود را مشخص می کنیم

	ifconfig

### استفاده در ویندوز


با وارد کردن `//linuxserverip/sambashare` در منوی جستجو ویندوز می توان به پوشه که به اشتراک گذاشتیم دسترسی پیدا کرد

### استفاده در سیستم عامل های دیگر

[استفاده از SMB در اندروید](https://www.techrepublic.com/article/how-to-connect-to-an-smb-share-from-your-android-device/) 

[استفاده از SMB در iPhone/iPad](https://osxdaily.com/2019/11/04/how-connect-smb-share-iphone-ipad-files-app/) 

[استفاده از SMB در لینوکس (گنوم)](https://www.zdnet.com/article/how-to-connect-to-a-network-share-from-the-gnome-desktop/#:~:text=At%20the%20bottom%20of%20the,the%20computer%20hosting%20the%20sare%29.)

